##@Author:   Akai
##@Date:     2/2/2012

##A Simple time keeper program to help keep track of when and how much time
##you spend on task. Should be used by time-valued people. Run it in the command
##line. Each time you finish a task, press <space> or <enter> and record down
##what you have done for the period. The output file is csv-formatted and could
##be processed further using excel

from datetime import datetime
import sys

##Copied from: http://code.activestate.com/recipes/134892/

class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the
    screen. Works for both windows and ms
    """
    def __init__(self):
        try:            
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
      
getch = _Getch()


current = prev = datetime.now()
f = open(sys.argv[0]+'.'+datetime.now().strftime("%d%m%Y")+'.txt', 'w')
c = getch()
while c!=chr(27):    
  if c==' ' or c==chr(13):
    current = datetime.now()
    current_str = current.strftime("%a %d/%m/%Y %I:%M%p")
    difference = (current-prev).total_seconds()*1.0/60
    output_str = "%s, %4.2f, " % (current_str, difference)
    print output_str,
    reason = raw_input()
    f.write(output_str+reason+'\n')
    prev = current
  c = getch()
f.close()


