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
    msg = " Press (f) for a new fortune, (h) for help, or (q) to quit."
    screen.addstr(curses.LINES - 1, 0, msg)
    screen.chgat(curses.LINES - 1, 7, 3, curses.A_BOLD | curses.color_pair(3))
    screen.chgat(curses.LINES - 1, 30, 3, curses.A_BOLD | curses.color_pair(3))
    screen.chgat(curses.LINES - 1, 47, 3, curses.A_BOLD | curses.color_pair(3))


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


def fortune(txt, arg, save=False):
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
    return msg


def show(txt):
    from textwrap import dedent
    msg = '''
        KEYBINDINGS:

        f, F, SPC  :  Display any old fortune.
        s, S       :  Display a short fortune.
        l, L       :  Display a long fortune.
        o, O,      :  Display an offensive fortune.
        ?, h, H    :  Display this help page.
        q, Q, ESC  :  Quit and display all marked paths.

        Good luck & God speed!
        '''
    txt.erase()
    try:
        msg = dedent(msg).strip()
        txt.addstr(msg)
        txt.chgat(0, 0, curses.A_BOLD | curses.color_pair(3))
        txt.chgat(9, 0, curses.A_BOLD | curses.color_pair(3))
    except:
        msg = "The soothsayer is squished!"
        txt.addstr(msg, curses.color_pair(1) | curses.A_BOLD)
    txt.refresh()


def key(div, txt):
    from os import environ
    environ.setdefault('ESCDELAY', '12')  # otherwise it takes an age!
    ESC = 27
    c = div.getch()
    if c == ord('f') or c == ord('F') or c == ord(' '):
        fortune(txt, '-a')
    elif c == ord('S'):
        fortune(txt, '-a')
    elif c == ord('s'):
        fortune(txt, '-s')
    elif c == ord('l') or c == ord('L'):
        fortune(txt, '-l')
    elif c == ord('o') or c == ord('O'):
        fortune(txt, '-o')
    elif c == ord('h') or c == ord('H') or c == ord('?'):
        show(txt)
    elif c == ord('q') or c == ord('Q') or c == ESC:
        quit()


def eventloop(div, txt, screen):
    while True:
        key(div, txt)
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
