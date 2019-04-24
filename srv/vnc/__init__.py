from flask import Blueprint
from pyVNC.Client import Client
from PIL import Image,ImageFilter, ImageEnhance
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
bp = Blueprint('vnc', __name__)

vnc = Client(host='176.62.226.169',
             port=5900,
             password='c835',
             gui=True,array=True
             )
vnc.start()
time.sleep(3)
# vnc.send_key("a")  # Sends the key "a"
vnc.send_mouse("Left", (245, 40))  # Left Clicks at x=200, y=200
# vnc.send_mouse("Right", (50, 50))  # Right Clicks at x=200, y=200
time.sleep(2)
vnc.send_mouse("Left", (407, 247))  # Left Clicks at x=200, y=200
time.sleep(2)

ar = vnc.screen.get_array()  # Get a array representation of the screen shape: (?, ?, 3)
im = Image.fromarray(ar)
im.save("vnc.png")
im = im.convert('L')
print(pytesseract.image_to_string(im.crop((144,153,224,171)),lang="rus"))
im.crop((144,153,224,171)).save("vncCr.png")
print(pytesseract.image_to_string(im.crop((148,273,224,288)),lang="rus"))
im.crop((148,273,224,288)).save("vncCr1.png")
print(pytesseract.image_to_string(im.crop((597,499,700,526)),lang="rus"))
im.crop((597,499,700,526)).save("vncCr2.png")
vnc.send_mouse("Left", (49, 43))  # Left Clicks at x=200, y=200
time.sleep(2)
vnc.exit()

from srv.main import routes