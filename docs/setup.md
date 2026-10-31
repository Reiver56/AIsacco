# Setup

## 1. ViGEmBus (virtual gamepad driver)

1. Download the latest installer from the [ViGEmBus releases](https://github.com/nefarius/ViGEmBus/releases).
2. Install it and reboot if asked.

## 2. Python environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-windows.txt
```

## 3. Isaac options

- Run the game in windowed mode.
- In `options.ini` (folder `Documents/My Games/Binding of Isaac Repentance/`) set `PauseOnFocusLost=0`, so the game does not pause when you click elsewhere.
- Close Isaac before editing `options.ini`, otherwise the game overwrites your change.
- Use a dedicated save slot so the agent does not touch your real progress.

## 4. Gamepad test

1. Start Isaac and enter a run.
2. Run `python scripts/test_gamepad.py` and click on the game window within 5 seconds.
3. Expected: the character moves right, then left, then shoots upward.

If nothing happens, see the troubleshooting notes below (to be completed while testing).

## Troubleshooting

- `vgamepad` import error: ViGEmBus is not installed or needs a reboot.
- The game ignores the pad: check the controller in Isaac's options menu, and try unplugging other pads.
