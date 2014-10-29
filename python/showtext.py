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

def showOnLEDMatrix(textsTuple):
	'''shows the texts on the LED matrix 
	the text must be a tuple of (text, color)
	returns the PID of the process displaying the text'''
	text = textsTuple
	font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf", 14)
	#/fonts/truetype/droid/DroidSans.ttf
	#"/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf" size 14
	all_text = ""
	for text_color_pair in text:
		if text_color_pair is not None:
			t = text_color_pair[0]
			all_text = all_text + t

	print(all_text)
	width, ignore = font.getsize(all_text)
	print(width)


	im = Image.new("RGB", (width + 30, 16), "black")
	draw = ImageDraw.Draw(im)

	x = 0;
	for text_color_pair in text:
		if text_color_pair is not None:
			t = text_color_pair[0]
			c = text_color_pair[1]
			print("t=" + t + " " + str(c) + " " + str(x))
			draw.text((x, 0), t, c, font=font)
			x = x + font.getsize(t)[0]

	im.save("test.ppm")
	return os.spawnl( os.P_NOWAIT, localconstants.ledmatrix, localconstants.ledmatrix, "1","test.ppm")
    
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
    except:
        print usage
        
def killclearpid(pid):
    usage = """
        killclear <pid>: kills the process <pid> and clears the board
        """
    os.kill(pid, signal.SIGKILL)
    clearLEDMatrix()
    
def killclearargs(args):
    usage = """
        killclear <pid>: kills the process <pid> and clears the board
        """
    if args[1] == 'killclear':
        pid = 0
        try:
            pid = int(args[2])
            killclearpid(pid)
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
        killclearargs(sys.argv)
    else:
        default()
