"""jmgtext.py: A text editor for fun."""
# standard library
import curses
import string

# third party libraries

# local modules
from rope import Rope


def main(screen):
    """Main text editor loop."""
    buffer = ""
    str_pos = 0
    while True:
        key = screen.getkey()
        cur_pos = screen.getyx()

        if len(key) == 1 and curses.unctrl(key) == b"^X":
            break
        elif len(key) == 1 and curses.unctrl(key) == b"^P":
            screen.addstr(10, 0, buffer)
        elif key == "KEY_BACKSPACE":
            buffer = buffer[: str_pos - 1] + buffer[str_pos:]
            if cur_pos[1] == 0:
                if cur_pos[0] != 0:
                    x = len(buffer.splitlines()[-1])
                    cur_pos = (cur_pos[0] - 1, x)
                    str_pos -= 1
            else:
                cur_pos = (cur_pos[0], cur_pos[1] - 1)
                screen.delch(*cur_pos)
                str_pos -= 1
        elif key == "KEY_LEFT":
            if cur_pos[1] == 0:
                if cur_pos[0] != 0:
                    x = len(buffer.splitlines()[-1])
                    cur_pos = (cur_pos[0] - 1, x)
                    str_pos -= 1
            else:
                cur_pos = (cur_pos[0], cur_pos[1] - 1)
                str_pos -= 1
        elif key in string.printable:
            buffer = buffer[:str_pos] + key + buffer[str_pos:]
            if key == "\n":
                cur_pos = (cur_pos[0] + 1, 0)
            else:
                cur_pos = (cur_pos[0], cur_pos[1] + 1)
            str_pos += 1
        else:
            pass

        screen.addstr(0, 0, buffer)
        screen.move(*cur_pos)


if __name__ == "__main__":

    curses.wrapper(main)
