import curses
from .cfortune import cfortune


def main():
    curses.wrapper(cfortune)
    print("\nGoodbye!\n")


if __name__ == '__main__':
    main()
