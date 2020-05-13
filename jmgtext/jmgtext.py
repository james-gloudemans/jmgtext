"""jmgtext.py: A text editor for fun."""
# standard library
import curses
import string

# third party libraries

# local modules
from rope import Rope


def insert(s: str, i: int, sub: str) -> str:
    """Shortcut to insert sub at position i in s."""
    return s[:i] + sub + s[i:]


def remove(s: str, i: int) -> str:
    """Shortcut to remove character i from s."""
    return s[: i - 1] + s[i:]


def main(screen):
    """Main text editor loop."""
    buffer = [""]
    while True:
        key = screen.getkey()
        y, x = screen.getyx()
        if len(key) == 1 and curses.unctrl(key) == b"^X":
            break
        elif len(key) == 1 and curses.unctrl(key) == b"^P":
            screen.addstr(10, 0, "\n".join(buffer))
        elif key == "KEY_BACKSPACE":
            if x == 0:
                if y != 0:
                    x = len(buffer[y - 1])
                    buffer[y - 1] += buffer[y]
                    buffer[y:] = buffer[y + 1 :]
                    buffer[-1] = ""
                    screen.clear()
                    y -= 1
            else:
                buffer[y] = remove(buffer[y], x)
                x -= 1
                screen.delch(y, x)
        elif key == "KEY_LEFT":
            if x == 0:
                if y != 0:
                    y -= 1
                    x = len(buffer[y])
            else:
                x -= 1

        elif key in string.printable:
            if key == "\n":
                buffer.insert(y + 1, buffer[y][x:])
                buffer[y] = buffer[y][:x]
                y += 1
                x = 0
            else:
                buffer[y] = insert(buffer[y], x, key)
                x += 1
        else:
            pass

        screen.addstr(0, 0, "\n".join(buffer))
        screen.move(y, x)


if __name__ == "__main__":

    curses.wrapper(main)
