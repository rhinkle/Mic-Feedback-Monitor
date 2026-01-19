"""Audio engine module for mic-to-headset audio passthrough."""

import numpy as np
import sounddevice as sd
from numpy.typing import NDArray
from typing import Any


class AudioEngine:
    """Handles audio passthrough from mic to headset with volume and latency control."""

    def __init__(self) -> None:
        """Initialize the audio engine."""
        self._volume: int = 50  # Volume level 0-100
        self._latency_ms: int = 20  # Latency in milliseconds
        self._stream: sd.Stream | None = None
        self._is_running: bool = False

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
        # Apply volume gain (0-100 mapped to 0.0-1.0)
        gain = self._volume / 100.0
        outdata[:] = indata * gain

    def start(self) -> None:
        """Begin audio passthrough using system default input/output devices."""
        if self._is_running:
            return

        # Calculate blocksize from latency
        # Using 44100 Hz sample rate as a common default
        sample_rate = 44100
        blocksize = int(sample_rate * self._latency_ms / 1000)

        self._stream = sd.Stream(
            samplerate=sample_rate,
            blocksize=blocksize,
            channels=1,  # Mono for mic monitoring
            dtype=np.float32,
            callback=self._audio_callback,
        )
        self._stream.start()
        self._is_running = True

    def stop(self) -> None:
        """Stop audio passthrough cleanly."""
        if not self._is_running or self._stream is None:
            return

        self._stream.stop()
        self._stream.close()
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
