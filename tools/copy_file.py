import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
       tty.setraw(fd)          # disable buffering
       while True:
          b = sys.stdin.read(1)  # read 1 char immediately
          if b is not None:
             yield b
    finally:
       termios.tcsetattr(fd, termios.TCSADRAIN, old)

path = sys.argv[1]
with open(path, "w") as fp:
      for c in getch():
       print(f"{c=}")
       if c == '\x03':
          break
       fp.write(c)


