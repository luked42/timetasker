from time import monotonic

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Digits, Static


class CompleteCounter(Static):
    complete_count: reactive[int] = reactive(0)

    def __init__(self, id: str) -> None:
        super().__init__(id=id)

    def on_mount(self) -> None:
        self._update_count()

    def increment_count(self) -> None:
        self.complete_count += 1
        self._update_count()

    def _update_count(self) -> None:
        self.update(f"{self.complete_count}")


class FooterBar(Static):
    def __init__(self, id: str, complete_counter: CompleteCounter) -> None:
        super().__init__(id=id)
        self.complete_counter = complete_counter

    def compose(self) -> ComposeResult:
        yield self.complete_counter


class TimeDisplay(Digits):
    minutes: float = 0.05
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


class PomodoroTimer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "pomodoro_timer.tcss"

    BINDINGS = [
        ("b", "toggle_timer", "Toggle"),
        ("r", "reset_timer", "Reset"),
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


if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
