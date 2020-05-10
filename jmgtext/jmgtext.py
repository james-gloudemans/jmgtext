"""jmgtext.py: A text editor for fun."""
# standard library
import curses
import string

# third party libraries

# local modules
from rope import Rope


def main(stdscr):
    """Main text editor loop."""
    buffer = ""
    str_pos = 0
    while True:
        key = stdscr.getkey()
        cur_pos = stdscr.getyx()

        if len(key) == 1 and curses.unctrl(key) == b"^P":
            stdscr.addstr(10, 0, buffer)
        elif key in string.printable:
            buffer = buffer[:str_pos] + key + buffer[str_pos:]
            str_pos += 1
        elif key == "KEY_BACKSPACE":
            buffer = buffer[: str_pos - 1] + buffer[str_pos:]
            str_pos -= 1
            if cur_pos[1] == 0:
                if cur_pos[0] != 0:
                    x = len(buffer.splitlines()[-1])
                    stdscr.move(cur_pos[0] - 1, x)
            else:
                cur_pos = (cur_pos[0], cur_pos[1] - 1)
                stdscr.move(*cur_pos)
                stdscr.delch(*cur_pos)
        else:
            pass

        stdscr.addstr(0, 0, buffer)


if __name__ == "__main__":

    curses.wrapper(main)
