"""Step 1 - check that Python can drive Isaac through a virtual gamepad.

Before running: start Isaac, enter a run, and keep the game window in the foreground.
Run with:  python scripts/test_gamepad.py
"""

import time

import vgamepad as vg


def set_move(pad: vg.VX360Gamepad, x: float, y: float) -> None:
    """Left stick = movement. x: -1 left ... +1 right, y: -1 down ... +1 up."""
    pad.left_joystick_float(x_value_float=x, y_value_float=y)
    pad.update()


def set_shoot(pad: vg.VX360Gamepad, x: float, y: float) -> None:
    """Right stick = shooting direction, same convention as set_move."""
    pad.right_joystick_float(x_value_float=x, y_value_float=y)
    pad.update()


def release(pad: vg.VX360Gamepad) -> None:
    """Put both sticks back to the center."""
    pad.reset()
    pad.update()


def main() -> None:
    pad = vg.VX360Gamepad()  # creates a virtual Xbox 360 controller
    print("Virtual gamepad created. Starting in 5 seconds: focus the Isaac window.")
    time.sleep(5)

    try:
        print("Move right for 1.5 s")
        set_move(pad, 1.0, 0.0)
        time.sleep(1.5)

        print("Move left for 1.5 s")
        set_move(pad, -1.0, 0.0)
        time.sleep(1.5)

        print("Stand still and shoot up for 2 s")
        set_move(pad, 0.0, 0.0)
        set_shoot(pad, 0.0, 1.0)
        time.sleep(2.0)
    finally:
        # Always release the sticks, even if something goes wrong or you press Ctrl+C.
        release(pad)
        print("Done, sticks released.")


if __name__ == "__main__":
    main()
