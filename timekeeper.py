##@Author:   Akai
##@Date:     2/2/2012

##A Simple time keeper program to help keep track of when and how much time
##you spend on task. Should be used by time-valued people. Run it in the command
##line. Each time you finish a task, press <space> or <enter> and record down
##what you have done for the period. The output file is csv-formatted and could
##be processed further using excel

from datetime import datetime
import sys
import os

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

STRFMT_DATETIME = "%a %d/%m/%Y %I:%M%p"
STRFMT_FILENAME = "%d%m%Y"
STRFMT_OUTPUT = "%s, %4.2f, "

getch = _Getch()

def get_diff_msg(prev, current):
    '''return the msg of <current_time>, <time_taken>'''
    
    difference = (current-prev).total_seconds()*1.0/60
    current_str = current.strftime(STRFMT_DATETIME)
    output_str = STRFMT_OUTPUT % (current_str, difference)
    return output_str
      
current = prev = datetime.now()
filename = sys.argv[0]+'.'+datetime.now().strftime(STRFMT_FILENAME)+'.txt'

#if the file existed, open to append
file_existed = os.path.exists(filename)

if file_existed:    
    #get the last time stamp
    with open(filename, 'r') as f:
        lines = f.readlines()
        if len(lines)>0:        
            prev = datetime.strptime(lines[-1].split(',')[0], STRFMT_DATETIME)
    #Added msg '...program restarted' to the log file
    with open(filename, 'a') as f:
        current = datetime.now()
        f.write(get_diff_msg(prev, current)+' ...program interrupted\n')
        prev = current
            
f = open(filename, file_existed and 'a' or 'w')

c = getch()
while c!=chr(27):    
  if c==' ' or c==chr(13):
    current = datetime.now()
    output_str = get_diff_msg(prev, current)    
    print output_str,
    reason = raw_input()
    f.write(output_str+reason+'\n')
    prev = current
  c = getch()
f.close()


