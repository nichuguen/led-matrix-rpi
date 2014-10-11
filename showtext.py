import os
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def createTextColor( text, color):
	'''returns a tuple containing the text and the color. the color attribute must be a tuple: (R, G, B)'''
	return (text, color)


def clearLEDMatrix():
	'''clears the LED matrix'''
	os.system("./test-clear")

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
		t = text_color_pair[0]
		all_text = all_text + t

	print(all_text)
	width, ignore = font.getsize(all_text)
	print(width)


	im = Image.new("RGB", (width + 30, 16), "black")
	draw = ImageDraw.Draw(im)

	x = 0;
	for text_color_pair in text:
		t = text_color_pair[0]
		c = text_color_pair[1]
		print("t=" + t + " " + str(c) + " " + str(x))
		draw.text((x, 0), t, c, font=font)
		x = x + font.getsize(t)[0]

	im.save("test.ppm")
	return os.spawnl( os.P_NOWAIT, "./led-matrix", "./led-matrix", "1","test.ppm")

if __name__ == "__main__":
	text = (createTextColor("QWERTZUIOPASDFGHJKLYXCVBNM", (255, 0, 0)), createTextColor("qwertzuiopasdfghjklyxcvbnm", (0, 255, 0)), createTextColor("1234567890", (0, 0, 255)))
	pid = showOnLEDMatrix(text)
	time.sleep(2)
	strcommand = "kill -9 %d" %pid
	os.system(strcommand)
	clearLEDMatrix()