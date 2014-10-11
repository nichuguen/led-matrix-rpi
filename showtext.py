import os
import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

text = (("QWERTZUIOPASDFGHJKLYXCVBNM", (255, 0, 0)), ("qwertzuiopasdfghjklyxcvbnm", (0, 255, 0)), ("1234567890", (0, 0, 255)))

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

os.system("./led-matrix 1 test.ppm")

'''pid = os.spawnl( os.P_NOWAIT, "./led-matrix", "1","test.ppm")

time.sleep(10)
strcommand = "kill -9 %d" %pid
os.system(strcommand)'''