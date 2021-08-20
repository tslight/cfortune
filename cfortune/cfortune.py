# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import curses
import subprocess

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
    msg = " [SPC] for fortunes, [h] for help, [w] to save, [q] to quit."
    try:
        screen.addstr(curses.LINES - 1, 0, msg)
        screen.chgat(curses.LINES - 1, 1, 5,
                     curses.A_BOLD | curses.color_pair(3))
        screen.chgat(curses.LINES - 1, 21, 3,
                     curses.A_BOLD | curses.color_pair(3))
        screen.chgat(curses.LINES - 1, 35, 3,
                     curses.A_BOLD | curses.color_pair(3))
        screen.chgat(curses.LINES - 1, 48, 3,
                     curses.A_BOLD | curses.color_pair(3))
    except:
        pass


def body(screen):
    div = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    div.box()  # draw border around container window
    # use a sub-window so we don't clobber the the container window's border.
    txt = div.subwin(curses.LINES - 5, curses.COLS - 4, 2, 2)
    args = ['fortune', '-a']
    msg = fortune(txt, args)
    # update internal window data structures
    screen.noutrefresh()
    div.noutrefresh()
    # redraw the screen
    curses.doupdate()
    return div, txt, msg


def fortune(txt, args):
    err, out = (None,)*2
    try:
        out = subprocess.check_output(args)
        out = str(out.decode("ascii"))
        txt.addstr(out)
    except TypeError:
        err = "The soothsayer does not like being touched in that way."
    except subprocess.CalledProcessError:
        err = "That topic doesn't exist. Ya numpty."
    except Exception:
        err = "The soothsayer likes a larger terminal than this."
    finally:
        if err:
            txt.erase()
            txt.addstr(err, curses.color_pair(1) | curses.A_BOLD)
        txt.refresh()
    return out


def show(txt):
    from textwrap import dedent
    msg = '''
        KEYBINDINGS:

        RET, SPC    : Display any old fortune.
        f           | Enter a fortune topic.
        l           : Display a long fortune.
        o           : Display an offensive fortune.
        s           : Display a short fortune.
        ?, h        : Display this help page.
        w           : Save your fortune.
        q, ESC      : Quit and display all marked paths.

        Good luck & God speed!
        '''
    txt.erase()
    try:
        msg = dedent(msg).strip()
        txt.addstr(msg)
        txt.chgat(0, 0, curses.color_pair(3) | curses.A_BOLD)
        txt.chgat(11, 0, curses.color_pair(3) | curses.A_BOLD)
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
    if c == ord('\n') or c == ord(' '):
        args = ['fortune', '-a']
        msg = fortune(txt, args)
    elif c == ord('f') or c == ord('F'):
        prompt = "Enter a fortune topic:"
        args = ['fortune', txtbox(txt, prompt).strip()]
        msg = fortune(txt, args)
    elif c == ord('m') or c == ord('M'):
        prompt = "Enter a search string:"
        args = ['fortune', '-m', txtbox(txt, prompt).strip()]
        msg = fortune(txt, args)
    elif c == ord('w') or c == ord('W'):
        save = True
    elif c == ord('s') or c == ord('S'):
        args = ['fortune', '-s']
        msg = fortune(txt, args)
    elif c == ord('l') or c == ord('L'):
        args = ['fortune', '-l', '-n', '300']
        msg = fortune(txt, args)
    elif c == ord('o') or c == ord('O'):
        args = ['fortune', '-o']
        msg = fortune(txt, args)
    elif c == ord('h') or c == ord('H') or c == ord('?'):
        show(txt)
    elif c == ord('q') or c == ord('Q') or c == ESC:
        quit()
    return msg, save


def txtbox(txt, prompt):
    from curses.textpad import Textbox
    curses.curs_set(1)
    txt.addstr(0, 0, prompt)
    txt.refresh()
    y, x = txt.getmaxyx()
    tb = txt.subwin(1, x - 1, 4, 2)
    box = Textbox(tb)
    txt.refresh
    box.edit()
    curses.curs_set(0)
    return box.gather()


def savemsg(txt, msg):
    from pathlib import Path
    err, out = (None,)*2
    home = str(Path.home())
    prompt = "Enter a file name (or c to cancel):"
    name = txtbox(txt, prompt).strip()
    if not name == 'c ':
        path = home + "/" + name
    try:
        # removes need to use f.close
        with open(path, 'a+') as f:
            f.write("\n" + msg + "\n")
    except FileNotFoundError:
        err = "Can't find " + path
    except IsADirectoryError:
        err = path + " is a directory."
    except UnboundLocalError:  # bit of a hack but fuck it
        out = "Not saving fortune."
    except Exception:
        err = "Something went wrong..."
    else:
        out = "Saved fortune to " + path
    finally:
        txt.erase()
        if err:
            txt.addstr(4, 0, err, curses.color_pair(1) | curses.A_BOLD)
            savemsg(txt, msg)
        elif out:
            txt.addstr(0, 0, out, curses.color_pair(3) | curses.A_BOLD)
        txt.refresh()
    return msg


def eventloop(screen, div, txt, msg):
    while True:
        txt.erase()
        msg, save = key(div, txt, msg)
        if save:
            msg = savemsg(txt, msg)
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
