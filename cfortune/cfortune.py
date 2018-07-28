import curses


def get_fortune(arg):
    from subprocess import check_output
    try:
        fortune = check_output(["fortune", arg])
    except:
        fortune = "You have no future."
    return fortune


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


def body(screen):
    div = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    div.box()  # draw border around container window
    # use a sub-window so we don't clobber the the container window's border.
    txt = div.subwin(curses.LINES - 5, curses.COLS - 6, 2, 2)
    write_fortune(txt, '-a')
    # update internal window data structures
    screen.noutrefresh()
    div.noutrefresh()
    # redraw the screen
    curses.doupdate()
    return div, txt


def write_fortune(txt, arg):
    fortune = get_fortune(arg)
    txt.clear()
    txt.addstr(fortune)
    txt.refresh()


def eventloop(div, txt, screen):
    while True:
        c = div.getch()
        if c == ord('f') or c == ord('F') or c == ord(' '):
            arg = "-a"
        elif c == ord('q') or c == ord('Q') or c == 27:
            break
        else:
            arg = "-" + chr(c)
        try:
            write_fortune(txt, arg)
        except:
            pass
        # refresh the windows from the bottom up
        screen.noutrefresh()
        div.noutrefresh()
        txt.noutrefresh()
        curses.doupdate


def footer(screen):
    msg = " Press (f) for a new fortune, (q) to quit."
    screen.addstr(curses.LINES - 1, 0, msg)
    screen.chgat(curses.LINES - 1, 7, 3, curses.A_BOLD | curses.color_pair(3))
    screen.chgat(curses.LINES - 1, 30, 3, curses.A_BOLD | curses.color_pair(3))


def cfortune(screen):
    curses.curs_set(0)
    color()
    header(screen)
    footer(screen)
    div, txt = body(screen)
    eventloop(div, txt, screen)
