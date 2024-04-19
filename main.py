from time import monotonic

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Digits


class TimeDisplay(Digits):
    start_time: reactive[float] = reactive(monotonic)
    total_countdown_seconds: reactive[float] = reactive(25.0 * 60)
    time_left_seconds: reactive[float] = reactive(25.0 * 60)

    def __init__(self, id: str) -> None:
        super().__init__(id=id)
        self.started = False

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time_left_seconds = self.total_countdown_seconds - (monotonic() - self.start_time)

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
        self.time_left_seconds = 25.0 * 60

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
        yield TimeDisplay(id="countdown_timer")
        yield Footer()

    def action_toggle_timer(self) -> None:
        countdown_timer: TimeDisplay = self.query_one(TimeDisplay)
        countdown_timer.toggle_timer()


    def action_reset_timer(self) -> None:
        countdown_timer: TimeDisplay = self.query_one(TimeDisplay)
        countdown_timer.reset()


if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
