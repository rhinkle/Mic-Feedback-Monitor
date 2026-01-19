# PRD: Mic Monitor for macOS

## Introduction

A lightweight macOS menu bar application that monitors microphone audio and feeds it back to the user's headset in real-time. This enables users to hear themselves during calls and meetings, improving communication quality and self-awareness of audio levels. Built with Python, the app provides simple controls for toggling monitoring on/off, adjusting feedback volume, and tuning latency.

## Goals

- Provide real-time mic-to-headset audio feedback with minimal latency
- Live entirely in the macOS menu bar for unobtrusive access
- Allow users to control feedback volume via a slider
- Include latency adjustment for optimal audio sync
- Persist user settings (volume, latency) between application sessions
- Use system default audio input and output devices automatically

## User Stories

### US-001: Menu Bar Presence
**Description:** As a user, I want the app to live in my menu bar so I can access it quickly without cluttering my dock or desktop.

**Acceptance Criteria:**
- [ ] App displays an icon in the macOS menu bar
- [ ] Clicking the icon reveals a dropdown with controls
- [ ] App does not appear in the Dock
- [ ] App does not open a main window on launch
- [ ] Typecheck/lint passes

### US-002: Toggle Mic Monitoring
**Description:** As a user, I want to toggle mic monitoring on and off so I can enable it only when needed during calls.

**Acceptance Criteria:**
- [ ] Dropdown includes a clearly labeled toggle switch or button
- [ ] Toggle state is visually indicated (on/off)
- [ ] Menu bar icon changes to reflect monitoring state (e.g., different icon or color indicator)
- [ ] Audio passthrough starts immediately when toggled on
- [ ] Audio passthrough stops immediately when toggled off
- [ ] Typecheck/lint passes

### US-003: Volume Control
**Description:** As a user, I want to adjust the feedback volume so I can set a comfortable listening level without it being too loud or too quiet.

**Acceptance Criteria:**
- [ ] Dropdown includes a volume slider
- [ ] Slider range is 0% to 100%
- [ ] Volume changes apply in real-time (no need to toggle off/on)
- [ ] Current volume level is displayed as a percentage
- [ ] Typecheck/lint passes

### US-004: Latency Adjustment
**Description:** As a user, I want to adjust the audio latency so I can minimize delay or tune it to my preference for call scenarios.

**Acceptance Criteria:**
- [ ] Dropdown includes a latency slider or control
- [ ] Latency range is appropriate for real-time audio (e.g., 5ms to 100ms)
- [ ] Current latency value is displayed in milliseconds
- [ ] Changes apply without requiring monitoring restart
- [ ] Typecheck/lint passes

### US-005: Persist Settings
**Description:** As a user, I want my volume and latency settings saved so I don't have to reconfigure them every time I open the app.

**Acceptance Criteria:**
- [ ] Volume level persists after quitting and reopening app
- [ ] Latency setting persists after quitting and reopening app
- [ ] Settings are stored in an appropriate location (e.g., user preferences/config file)
- [ ] App loads saved settings on startup
- [ ] Typecheck/lint passes

### US-006: Use System Default Devices
**Description:** As a user, I want the app to automatically use my system's default input and output devices so I don't have to configure audio devices manually.

**Acceptance Criteria:**
- [ ] App automatically detects and uses system default input device (mic)
- [ ] App automatically detects and uses system default output device (headset)
- [ ] If default devices change while app is running, app handles gracefully (either auto-switches or shows error)
- [ ] Typecheck/lint passes

### US-007: Quit Application
**Description:** As a user, I want a way to quit the application from the menu bar dropdown.

**Acceptance Criteria:**
- [ ] Dropdown includes a "Quit" option
- [ ] Clicking Quit stops any active audio monitoring
- [ ] App exits cleanly without errors
- [ ] Typecheck/lint passes

## Functional Requirements

- FR-1: App shall run as a macOS menu bar application (LSUIElement or equivalent)
- FR-2: App shall display an icon in the menu bar that opens a dropdown when clicked
- FR-3: Dropdown shall contain: toggle switch, volume slider, latency slider, and quit button
- FR-4: Toggle shall start/stop real-time audio passthrough from default mic to default output
- FR-5: Volume slider shall control the gain of the passthrough audio (0-100%)
- FR-6: Latency slider shall control the buffer size affecting audio delay (target range: 5-100ms)
- FR-7: Menu bar icon shall visually indicate whether monitoring is active or inactive
- FR-8: App shall save settings (volume, latency) to a config file on change
- FR-9: App shall load saved settings on startup and apply them
- FR-10: App shall use PyAudio, sounddevice, or equivalent library for audio I/O
- FR-11: App shall use rumps, PyObjC, or equivalent for menu bar integration

## Non-Goals

- No custom audio device selection (uses system defaults only)
- No audio effects or processing (EQ, noise cancellation, etc.)
- No keyboard shortcuts
- No recording or logging of audio
- No multi-channel or surround sound support
- No Windows or Linux support (macOS only)

## Technical Considerations

### Dependencies
- **Audio handling:** `sounddevice` or `pyaudio` for low-latency audio streaming
- **Menu bar UI:** `rumps` (Ridiculously Uncomplicated macOS Python Statusbar apps) for menu bar integration
- **Settings persistence:** JSON config file in `~/.config/mic-monitor/` or `~/Library/Application Support/MicMonitor/`

### Architecture
- Main thread handles menu bar UI via rumps
- Separate thread or callback-based stream for audio passthrough
- Audio stream uses a ring buffer with configurable size for latency control
- Settings manager class handles load/save of configuration

### Performance
- Target latency under 50ms for comfortable real-time monitoring
- Audio processing should use minimal CPU
- App should be lightweight in memory footprint

### Packaging
- Can be run directly as Python script during development
- Consider py2app or PyInstaller for distribution as standalone .app

## Success Metrics

- Audio passthrough works with latency under 50ms at default settings
- Toggle responds within 100ms (near-instant feedback)
- App uses less than 5% CPU during active monitoring
- Settings persist correctly across app restarts
- App runs stably without crashes during extended use (1+ hour sessions)

## Open Questions

- Should the app auto-start monitoring on launch, or always start in "off" state?
- Should there be an "About" menu item with version info?
- Should the app check for and handle audio device disconnection gracefully?
- What should the default volume level be (50%? 75%?)?
- Should latency show exact ms value or use descriptive labels (Low/Medium/High)?
