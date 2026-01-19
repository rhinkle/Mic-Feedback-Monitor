"""MicMonitor - macOS menu bar application for real-time mic-to-headset audio monitoring."""

import rumps

from audio_engine import AudioEngine
from settings import SettingsManager


class MicMonitorApp(rumps.App):
    """Menu bar application for mic-to-headset audio monitoring."""

    # Menu bar icons for different states
    ICON_INACTIVE = "🎤"
    ICON_ACTIVE = "🎤🔊"

    # Menu item text
    TEXT_START = "Start Monitoring"
    TEXT_STOP = "Stop Monitoring"

    def __init__(self) -> None:
        """Initialize the MicMonitor menu bar app."""
        super().__init__(
            name="MicMonitor",
            title=self.ICON_INACTIVE,
            quit_button="Quit",
        )
        self._audio_engine = AudioEngine()
        self._toggle_item = rumps.MenuItem(self.TEXT_START, callback=self._toggle_monitoring)
        self.menu = [self._toggle_item]

    def _toggle_monitoring(self, sender: rumps.MenuItem) -> None:
        """Toggle audio monitoring on/off.

        Args:
            sender: The menu item that was clicked.
        """
        if self._audio_engine.is_running:
            self._audio_engine.stop()
            self._toggle_item.title = self.TEXT_START
            self.title = self.ICON_INACTIVE
        else:
            self._audio_engine.start()
            self._toggle_item.title = self.TEXT_STOP
            self.title = self.ICON_ACTIVE


def main() -> None:
    """Main entry point for the MicMonitor application."""
    app = MicMonitorApp()
    app.run()


if __name__ == "__main__":
    main()
