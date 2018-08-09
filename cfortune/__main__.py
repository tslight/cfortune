# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import curses
from .cfortune import cfortune


def main():
    curses.wrapper(cfortune)
    print("\nGoodbye!\n")


if __name__ == '__main__':
    main()
