import curses
from .cfortune import cfortune


def main():
    curses.wrapper(cfortune)


if __name__ == '__main__':
    main()
