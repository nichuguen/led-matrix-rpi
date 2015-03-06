import showtext, fcntl

'''
example:
import struct, fcntl, os

f = open(...)
rv = fcntl.fcntl(f, fcntl.F_SETFL, os.O_NDELAY)

lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, 0, 0, 0, 0, 0)
rv = fcntl.fcntl(f, fcntl.F_SETLKW, lockdata)

'''

path = "/home/pi/led-matrix-rpi/python/"
def getPid():
    global path
    f = open(path + "pid.log")
    fcntl.flock(f, fcntl.LOCK_EX)
    try:
        pid = f.readline()
        
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        return int(pid)
    except:
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        return None
def setPid(pid):
    global path
    f = open(path + "pid.log", 'w')
    fcntl.flock(f, fcntl.LOCK_EX)
    try:
        f.write("%d" %pid)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        return True
    except:
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        return False
    
def main(args):
    pid = getPid()
    if pid is not None and pid != 0:
        showtext.killClearPid(pid)
        setPid(0)
    if len(args) == 5:
        if args[1] != '':
            pid = showtext.encodeAndPrint(args)
        if pid is not None:
            setPid(pid)

if __name__ == "__main__":
    import sys
    log = open("log.log", "w")
    try:
        main(sys.argv)
    except Exception as e:
        log.write(str(e))