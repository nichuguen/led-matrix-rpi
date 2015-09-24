#!/usr/bin/python
import os
import time
import signal
import localconstants
import sys
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def createTextColor( text, color):
    '''returns a tuple containing the text and the color. the color attribute must be a tuple: (R, G, B)'''
    return (text, color)


def clearLEDMatrix():
    '''clears the LED matrix'''
    os.system(localconstants.clear)
    
def showRMNLEDMatrix():
	filename = localconstants.pathprog + "/RMN.ppm"
	return os.spawnl( os.P_NOWAIT, localconstants.ledmatrix, localconstants.ledmatrix, "1",filename)

def showOnLEDMatrix(textsTuple, endof_string_space = True):
    '''shows the texts on the LED matrix 
    the text must be a tuple of (text, color)
    returns the PID of the process displaying the text'''
    text = textsTuple
    font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
    #/fonts/truetype/droid/DroidSans.ttf
    #"/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf" size 14
    #NO ONE FUCKS WITH FUCKING EMPTY SPACE
    '''if text[0][0] is not None: #MAYBE SOMEONE FUCKS WITH THEM
        text[0][0] = " " + text[0][0]'''
    all_text = ''
    for text_color_pair in text:
        if text_color_pair is not None:
            t = text_color_pair[0]
            all_text = all_text + t

    print(all_text)
    width, ignore = font.getsize(all_text)
    print(width)

    offset = 0
    if endof_string_space:
        offset = 30

    im = Image.new("RGB", (width + offset, 16), "black")
    draw = ImageDraw.Draw(im)

    x = 0;
    for text_color_pair in text:
        if text_color_pair is not None:
            t = text_color_pair[0]
            if x == 0:
                t = "" + t
            c = text_color_pair[1]
            draw.text((x, 0), t, c, font=font)
            x = x + font.getsize(t)[0]
    filename = localconstants.pathprog + "/test.ppm"
    im.save(filename)
    return os.spawnl( os.P_NOWAIT, localconstants.ledmatrix, localconstants.ledmatrix, "1",filename)
    
def encodeAndPrint(args):
    usage = """
        <str> <r> <g> <b>: displays the <str> with RGB color <r><g><b>
        """
    try:
        textString = str(args[1])
        colR = int(args[2])
        colG = int(args[3])
        colB = int(args[4])
        text = (createTextColor(textString, (colR, colG, colB)), None)
        pid = showOnLEDMatrix(text)
        print "{ PID: %d }" % pid
        return pid
    except Exception as e:
        print e
        print usage
        return None
        
def killClearPid(pid):
    usage = """
        killclear <pid>: kills the process <pid> and clears the board
        """
    os.kill(pid, signal.SIGKILL)
    clearLEDMatrix()
    
def killClearArgs(args):
    usage = """
        killclear <pid>: kills the process <pid> and clears the board
        """
    if args[1] == 'killclear':
        pid = 0
        try:
            pid = int(args[2])
            killClearPid(pid)
        except:
            print(usage)
                
def default():
    text = (createTextColor("KOM TM LA BIT", (0, 255, 255)), None)
    pid = showOnLEDMatrix(text)
    raw_input("Press Enter to continue...")
    os.kill(pid, signal.SIGKILL)
    clearLEDMatrix()

if __name__ == "__main__":
    usage = ''' 
        clear: clears the board
        <str> <r> <g> <b>: displays the <str> with RGB color <r><g><b>
        killclear <pid>: kills the process <pid> and clears the board
        '''
    if len(sys.argv) == 5:
        encodeAndPrint(sys.argv)            
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'clear':
            clearLEDMatrix()
        else:
            print (usage)
    elif len(sys.argv) == 3:
        killClearArgs(sys.argv)
    else:
        default()
