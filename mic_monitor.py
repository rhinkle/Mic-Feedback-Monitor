"""MicMonitor - macOS menu bar application for real-time mic-to-headset audio monitoring."""

import rumps

from audio_engine import AudioEngine


class MicMonitorApp(rumps.App):
    """Menu bar application for mic-to-headset audio monitoring."""

    # Menu bar icons for different states
    ICON_INACTIVE = "🎤"
    ICON_ACTIVE = "🎤🔊"

    # Menu item text
    TEXT_START = "Start Monitoring"
    TEXT_STOP = "Stop Monitoring"

    # Volume constants
    VOLUME_MIN = 0
    VOLUME_MAX = 100
    VOLUME_STEP = 10

    def __init__(self) -> None:
        """Initialize the MicMonitor menu bar app."""
        super().__init__(
            name="MicMonitor",
            title=self.ICON_INACTIVE,
            quit_button="Quit",
        )
        self._audio_engine = AudioEngine()
        self._volume: int = 50  # Default volume

        # Create menu items
        self._toggle_item = rumps.MenuItem(self.TEXT_START, callback=self._toggle_monitoring)
        self._volume_display = rumps.MenuItem(self._get_volume_text())
        self._volume_up = rumps.MenuItem("Volume Up (+10%)", callback=self._increase_volume)
        self._volume_down = rumps.MenuItem("Volume Down (-10%)", callback=self._decrease_volume)

        self.menu = [
            self._toggle_item,
            None,  # Separator
            self._volume_display,
            self._volume_up,
            self._volume_down,
        ]

    def _get_volume_text(self) -> str:
        """Get the volume display text."""
        return f"Volume: {self._volume}%"

    def _update_volume_display(self) -> None:
        """Update the volume display menu item."""
        self._volume_display.title = self._get_volume_text()

    def _increase_volume(self, sender: rumps.MenuItem) -> None:
        """Increase volume by step amount.

        Args:
            sender: The menu item that was clicked.
        """
        self._volume = min(self.VOLUME_MAX, self._volume + self.VOLUME_STEP)
        self._audio_engine.set_volume(self._volume)
        self._update_volume_display()

    def _decrease_volume(self, sender: rumps.MenuItem) -> None:
        """Decrease volume by step amount.

        Args:
            sender: The menu item that was clicked.
        """
        self._volume = max(self.VOLUME_MIN, self._volume - self.VOLUME_STEP)
        self._audio_engine.set_volume(self._volume)
        self._update_volume_display()

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
