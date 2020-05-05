"""jmgtext.py: A text editor for fun."""
# standard library
import curses
import string

# third party libraries

# local modules


def main(stdscr):
    """Main text editor loop."""
    buffer = ""
    while True:
        key = stdscr.getkey()
        pos = stdscr.getyx()

        if len(key) == 1 and curses.unctrl(key) == b"^P":
            stdscr.addstr(10, 0, buffer)
        elif key in string.printable:
            buffer += key
        elif key == "KEY_BACKSPACE":
            buffer = buffer[:-1]
            if pos[1] == 0:
                if pos[0] != 0:
                    x = len(buffer.splitlines()[-1])
                    stdscr.move(pos[0] - 1, x)
            else:
                pos = (pos[0], pos[1] - 1)
                stdscr.move(*pos)
                stdscr.delch(*pos)
        else:
            pass

        stdscr.addstr(0, 0, buffer)


if __name__ == "__main__":

    curses.wrapper(main)
