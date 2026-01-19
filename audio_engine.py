"""Audio engine module for mic-to-headset audio passthrough."""

import numpy as np
import sounddevice as sd
from numpy.typing import NDArray
from typing import Any, Callable


class AudioEngine:
    """Handles audio passthrough from mic to headset with volume and latency control."""

    def __init__(self) -> None:
        """Initialize the audio engine."""
        self._volume: int = 50  # Volume level 0-100
        self._latency_ms: int = 20  # Latency in milliseconds
        self._stream: sd.Stream | None = None
        self._is_running: bool = False
        self._error_callback: Callable[[str], None] | None = None
        self._last_error: str | None = None

    def set_error_callback(self, callback: Callable[[str], None] | None) -> None:
        """Set callback function to be called when an audio error occurs.

        Args:
            callback: Function that takes an error message string.
        """
        self._error_callback = callback

    @property
    def last_error(self) -> str | None:
        """Get the last error message, if any."""
        return self._last_error

    def clear_error(self) -> None:
        """Clear the last error."""
        self._last_error = None

    @property
    def is_running(self) -> bool:
        """Check if audio passthrough is currently running."""
        return self._is_running

    def _audio_callback(
        self,
        indata: NDArray[np.float32],
        outdata: NDArray[np.float32],
        frames: int,
        time: Any,
        status: sd.CallbackFlags,
    ) -> None:
        """Process audio from input to output with volume adjustment.

        Args:
            indata: Input audio data from microphone.
            outdata: Output buffer to fill with processed audio.
            frames: Number of frames to process.
            time: Timing information.
            status: Stream status flags.
        """
        # Check for stream errors
        if status:
            error_msg = f"Audio stream error: {status}"
            self._last_error = error_msg
            if self._error_callback:
                self._error_callback(error_msg)

        # Apply volume gain (0-100 mapped to 0.0-1.0)
        gain = self._volume / 100.0
        outdata[:] = indata * gain

    def start(self) -> bool:
        """Begin audio passthrough using system default input/output devices.

        Returns:
            True if stream started successfully, False if an error occurred.
        """
        if self._is_running:
            return True

        # Clear any previous error
        self._last_error = None

        # Calculate blocksize from latency
        # Using 44100 Hz sample rate as a common default
        sample_rate = 44100
        blocksize = int(sample_rate * self._latency_ms / 1000)

        try:
            self._stream = sd.Stream(
                samplerate=sample_rate,
                blocksize=blocksize,
                channels=1,  # Mono for mic monitoring
                dtype=np.float32,
                callback=self._audio_callback,
            )
            self._stream.start()
            self._is_running = True
            return True
        except sd.PortAudioError as e:
            error_msg = f"Failed to start audio: {e}"
            self._last_error = error_msg
            if self._error_callback:
                self._error_callback(error_msg)
            self._stream = None
            self._is_running = False
            return False
        except Exception as e:
            error_msg = f"Unexpected audio error: {e}"
            self._last_error = error_msg
            if self._error_callback:
                self._error_callback(error_msg)
            self._stream = None
            self._is_running = False
            return False

    def stop(self) -> None:
        """Stop audio passthrough cleanly."""
        if not self._is_running or self._stream is None:
            self._is_running = False
            return

        try:
            self._stream.stop()
            self._stream.close()
        except Exception:
            # Silently handle errors when stopping, as the stream may already be invalid
            pass
        finally:
            self._stream = None
            self._is_running = False

    def set_volume(self, volume: int) -> None:
        """Adjust gain in real-time.

        Args:
            volume: Volume level from 0 to 100.
        """
        self._volume = max(0, min(100, volume))

    def set_latency(self, ms: int) -> None:
        """Set audio latency via buffer size.

        Latency changes take effect on the next start() call.
        If the stream is currently running, it will be restarted
        to apply the new latency setting.

        Args:
            ms: Latency in milliseconds (5 to 100).
        """
        self._latency_ms = max(5, min(100, ms))

        # If stream is running, restart to apply new latency
        if self._is_running:
            self.stop()
            self.start()
