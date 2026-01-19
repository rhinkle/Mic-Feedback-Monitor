"""MicMonitor - macOS menu bar application for real-time mic-to-headset audio monitoring."""

import rumps

from audio_engine import AudioEngine
from settings import SettingsManager


class MicMonitorApp(rumps.App):
    """Menu bar application for mic-to-headset audio monitoring."""

    def __init__(self) -> None:
        """Initialize the MicMonitor menu bar app."""
        super().__init__(
            name="MicMonitor",
            title="🎤",
            quit_button="Quit",
        )


def main() -> None:
    """Main entry point for the MicMonitor application."""
    app = MicMonitorApp()
    app.run()


if __name__ == "__main__":
    main()
