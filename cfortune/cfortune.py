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
    msg = fortune(txt, '-a')
    # update internal window data structures
    screen.noutrefresh()
    div.noutrefresh()
    # redraw the screen
    curses.doupdate()
    return div, txt, msg


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
    return msg


def show(txt):
    from textwrap import dedent
    msg = '''
        KEYBINDINGS:

        f, F, SPC : Display any old fortune.
        s         : Display a short fortune.
        l         : Display a long fortune.
        o         : Display an offensive fortune.
        ?, h      : Display this help page.
        S         : Save your fortune.
        q, ESC    : Quit and display all marked paths.

        Good luck & God speed!
        '''
    txt.erase()
    try:
        msg = dedent(msg).strip()
        txt.addstr(msg)
        txt.chgat(0, 0, curses.color_pair(3) |
                  curses.A_BOLD | curses.A_UNDERLINE)
        txt.chgat(9, 0, curses.color_pair(3) | curses.A_BOLD)
    except:
        msg = "The soothsayer is squished!"
        txt.addstr(msg, curses.color_pair(1) | curses.A_BOLD)
    txt.refresh()


def key(div, txt, msg):
    from os import environ
    environ.setdefault('ESCDELAY', '12')  # otherwise it takes an age!
    ESC = 27
    save = False
    c = div.getch()
    if c == ord('f') or c == ord('F') or c == ord(' '):
        msg = fortune(txt, '-a')
    elif c == ord('S'):
        save = True
    elif c == ord('s'):
        msg = fortune(txt, '-s')
    elif c == ord('l') or c == ord('L'):
        msg = fortune(txt, '-l')
    elif c == ord('o') or c == ord('O'):
        msg = fortune(txt, '-o')
    elif c == ord('h') or c == ord('H') or c == ord('?'):
        show(txt)
    elif c == ord('q') or c == ord('Q') or c == ESC:
        quit()
    return msg, save


def getfile(txt):
    from curses.textpad import Textbox
    curses.curs_set(1)
    txt.addstr(0, 0, "Enter a file name (Enter c or q to cancel):")
    txt.refresh()
    y, x = txt.getmaxyx()
    tb = txt.subwin(1, x - 1, 3, 2)
    box = Textbox(tb)
    txt.refresh
    box.edit()
    curses.curs_set(0)
    return box.gather()


def savemsg(txt, msg):
    from pathlib import Path
    err = None
    out = None
    s = str(msg.decode("ascii"))
    home = str(Path.home())
    name = getfile(txt)
    if name == "c" or name == "q":
        return
    path = home + "/" + name
    try:
        # removes need to use f.close
        with open(path, 'a+') as f:
            f.write("\n" + s + "\n")
    except FileNotFoundError:
        err = "Can't find " + path
    except IsADirectoryError:
        err = path + " is a directory."
    except Exception:
        err = "Something went wrong..."
    else:
        out = "Saved fortune to " + path
    finally:
        if err:
            txt.erase()
            txt.addstr(2, 0, err, curses.color_pair(1) | curses.A_BOLD)
            savemsg(txt, msg)
        elif out:
            txt.addstr(2, 0, out, curses.color_pair(3) | curses.A_BOLD)
        txt.refresh()


def eventloop(screen, div, txt, msg):
    while True:
        msg, save = key(div, txt, msg)
        if save:
            txt.erase()
            savemsg(txt, msg)
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
    div, txt, msg = body(screen)
    eventloop(screen, div, txt, msg)
