import curses
from cgitb import enable
# Get more detailed traceback reports
enable(format="text")  # https://pymotw.com/2/cgitb/


def color():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(9, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(11, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
    curses.init_pair(12, curses.COLOR_CYAN, curses.COLOR_WHITE)


def header(screen):
    msg = " GET YOUR FORTUNES HERE! "
    screen.addstr(msg, curses.color_pair(10) |
                  curses.A_BOLD | curses.A_REVERSE)
    screen.chgat(-1, curses.color_pair(10) | curses.A_BOLD | curses.A_REVERSE)


def footer(screen):
    msg = " Press (f) for a new fortune, (q) to quit."
    screen.addstr(curses.LINES - 1, 0, msg)
    screen.chgat(curses.LINES - 1, 7, 3, curses.A_BOLD | curses.color_pair(3))
    screen.chgat(curses.LINES - 1, 30, 3, curses.A_BOLD | curses.color_pair(3))


def body(screen):
    div = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    div.box()  # draw border around container window
    # use a sub-window so we don't clobber the the container window's border.
    txt = div.subwin(curses.LINES - 5, curses.COLS - 4, 2, 2)
    fortune(txt, '-a')
    # update internal window data structures
    screen.noutrefresh()
    div.noutrefresh()
    # redraw the screen
    curses.doupdate()
    return div, txt


def fortune(txt, arg):
    from subprocess import check_output
    try:
        txt.erase()
        msg = check_output(["fortune", arg])
        txt.addstr(msg)
    except TypeError:
        msg = "The soothsayer does not like being touched in that way."
        txt.addstr(msg, curses.color_pair(1) | curses.A_BOLD)
    except Exception:
        txt.erase()
        msg = "The soothsayer likes a larger terminal than this."
        txt.addstr(msg, curses.color_pair(1) | curses.A_BOLD)
    finally:
        txt.refresh()


def key(div):
    arg = None
    c = div.getch()
    if c == ord('f') or c == ord('F') or c == ord(' '):
        arg = "-a"
    elif c == ord('s') or c == ord('S'):
        arg = "-s"
    elif c == ord('l') or c == ord('L'):
        arg = "-l"
    elif c == ord('o') or c == ord('O'):
        arg = "-o"
    elif c == ord('q') or c == ord('Q') or c == 27:
        arg = "quit"
    elif c == curses.KEY_RESIZE:
        pass
    return arg


def eventloop(div, txt, screen):
    while True:
        arg = key(div)
        if arg == "quit":
            return
        fortune(txt, arg)
        # refresh the windows from the bottom up
        screen.noutrefresh()
        div.noutrefresh()
        txt.noutrefresh()
        curses.doupdate


def cfortune(screen):
    curses.curs_set(0)
    color()
    header(screen)
    footer(screen)
    div, txt = body(screen)
    eventloop(div, txt, screen)
