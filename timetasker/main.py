from datetime import date, datetime
import os
import pickle
from time import monotonic

from textual.app import App, ComposeResult, events
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Digits, Static, Label
from textual.containers import Grid


class CompleteCounter(Static):
    complete_count: reactive[int] = reactive(0)

    def __init__(self, id: str) -> None:
        super().__init__(id=id)
        self.complete_count_pickle_path: str = os.path.expanduser("~/.config/timetasker.pickle")
        self.event_list: list[datetime] = self._load_event_list()

    def on_mount(self) -> None:
        self._count_events_today()
        self._update_count()

    def increment_count(self) -> None:
        self.event_list.append(datetime.now())
        self._count_events_today()
        self._update_count()
        self._save_event_list()

    def _update_count(self) -> None:
        self.update(f"{self.complete_count}")

    def _save_event_list(self) -> None:
        with open(self.complete_count_pickle_path, "wb") as pickle_file:
            pickle.dump(self.event_list, pickle_file)

    def _load_event_list(self) -> list[datetime]:
        event_list: list[datetime] = []
        try:
            with open(self.complete_count_pickle_path, "rb") as pickle_file:
                event_list = pickle.load(pickle_file)
        except FileNotFoundError:
            pass

        return event_list

    def _count_events_today(self) -> None:
        today: date = datetime.now().date()
        self.complete_count = len([x for x in self.event_list if x.date() == today])


class FooterBar(Static):
    def __init__(self, id: str, complete_counter: CompleteCounter) -> None:
        super().__init__(id=id)
        self.complete_counter = complete_counter

    def compose(self) -> ComposeResult:
        yield self.complete_counter


class TimeDisplay(Digits):
    minutes: float = 25.0
    start_time: reactive[float] = reactive(monotonic)
    total_countdown_seconds: reactive[float] = reactive(0)
    time_left_seconds: reactive[float] = reactive(0)

    def __init__(self, id: str, complete_counter: CompleteCounter) -> None:
        super().__init__(id=id)
        self.started = False
        self.finished = False
        self.complete_counter: CompleteCounter = complete_counter
        self.count_down: bool = True

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.update_time, pause=True)
        self.reset()

    def update_time(self) -> None:
        time_difference: float = monotonic() - self.start_time
        if not self.count_down:
            time_difference = -1.0 * time_difference
        self.time_left_seconds = max(0.0, self.total_countdown_seconds - time_difference)
        if self.time_left_seconds <= 0.0 and not self.finished:
            self.complete_counter.increment_count()
            self.finished = True
            self.count_down = False
            self.add_class("finished")
            self.start()

    def watch_time_left_seconds(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.total_countdown_seconds = self.time_left_seconds
        self.start_time = monotonic()
        self.update_timer.resume()
        self.started = True

    def stop(self):
        self.update_timer.pause()
        self.update_time()
        self.started = False

    def reset(self):
        self.stop()
        self.start_time = monotonic()
        self.time_left_seconds = self.minutes * 60
        self.finished = False
        self.count_down = True
        self.remove_class("finished")

    def toggle_timer(self):
        if self.started:
            self.stop()
        else:
            self.start()


class HelpScreen(ModalScreen):
    HELP_TEXT = """
    Controls:

    - 'b' : toggle timer
    - 'r' : reset interval
    - 'q' : quit
    - '?' : show help

    (press any key to exit)
    """

    def compose(self) -> ComposeResult:
        yield Grid(Label(self.HELP_TEXT))

    def on_key(self, _: events.Key):
        self.dismiss()


class Timetasker(App):
    CSS_PATH = "timetasker.tcss"

    BINDINGS = [
        ("b", "toggle_timer", "Toggle"),
        ("r", "reset_timer", "Reset"),
        ("q", "quit", "Quit"),
        ("?", "show_help", "Show Help"),
    ]

    def compose(self) -> ComposeResult:
        complete_counter: CompleteCounter = CompleteCounter(id="complete_counter")
        yield TimeDisplay(id="countdown_timer", complete_counter=complete_counter)
        yield FooterBar(id="footer_bar", complete_counter=complete_counter)

    def action_toggle_timer(self) -> None:
        countdown_timer: TimeDisplay = self.query_one(TimeDisplay)
        countdown_timer.toggle_timer()

    def action_reset_timer(self) -> None:
        countdown_timer: TimeDisplay = self.query_one(TimeDisplay)
        countdown_timer.reset()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())


def main_func() -> None:
    app = Timetasker()
    app.run()


if __name__ == "__main__":
    app = Timetasker()
    app.run()
