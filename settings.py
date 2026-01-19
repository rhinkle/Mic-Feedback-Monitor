"""Settings manager module for persisting user configuration."""

import json
from pathlib import Path
from typing import Any


class SettingsManager:
    """Manages loading and saving user settings."""

    DEFAULT_VOLUME: int = 50
    DEFAULT_LATENCY_MS: int = 20
    DEFAULT_MONITORING_ENABLED: bool = False

    def __init__(self) -> None:
        """Initialize settings manager with config path."""
        app_support = Path.home() / "Library" / "Application Support" / "MicMonitor"
        self._config_path = app_support / "config.json"
        self._volume: int = self.DEFAULT_VOLUME
        self._latency_ms: int = self.DEFAULT_LATENCY_MS
        self._monitoring_enabled: bool = self.DEFAULT_MONITORING_ENABLED

    @property
    def volume(self) -> int:
        """Get current volume setting (0-100)."""
        return self._volume

    @volume.setter
    def volume(self, value: int) -> None:
        """Set volume (0-100)."""
        self._volume = max(0, min(100, value))

    @property
    def latency_ms(self) -> int:
        """Get current latency setting in milliseconds."""
        return self._latency_ms

    @latency_ms.setter
    def latency_ms(self, value: int) -> None:
        """Set latency in milliseconds (5-100)."""
        self._latency_ms = max(5, min(100, value))

    @property
    def monitoring_enabled(self) -> bool:
        """Get monitoring enabled state."""
        return self._monitoring_enabled

    @monitoring_enabled.setter
    def monitoring_enabled(self, value: bool) -> None:
        """Set monitoring enabled state."""
        self._monitoring_enabled = value

    def load(self) -> dict[str, Any]:
        """Load settings from config file or return defaults if file missing.

        Returns:
            Dictionary with volume, latency_ms, and monitoring_enabled keys.
        """
        if self._config_path.exists():
            try:
                with open(self._config_path, "r") as f:
                    data = json.load(f)
                self._volume = data.get("volume", self.DEFAULT_VOLUME)
                self._latency_ms = data.get("latency_ms", self.DEFAULT_LATENCY_MS)
                self._monitoring_enabled = data.get(
                    "monitoring_enabled", self.DEFAULT_MONITORING_ENABLED
                )
            except (json.JSONDecodeError, OSError):
                self._reset_to_defaults()
        else:
            self._reset_to_defaults()

        return {
            "volume": self._volume,
            "latency_ms": self._latency_ms,
            "monitoring_enabled": self._monitoring_enabled,
        }

    def save(self) -> None:
        """Write current settings to config file."""
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "volume": self._volume,
            "latency_ms": self._latency_ms,
            "monitoring_enabled": self._monitoring_enabled,
        }
        with open(self._config_path, "w") as f:
            json.dump(data, f, indent=2)

    def _reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self._volume = self.DEFAULT_VOLUME
        self._latency_ms = self.DEFAULT_LATENCY_MS
        self._monitoring_enabled = self.DEFAULT_MONITORING_ENABLED
