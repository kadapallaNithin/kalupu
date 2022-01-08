from PIL import Image
import PIL.ImageOps

file_name = "drawing_Dr. NAGESH BHATTU SRISTY Sir_temp.jpg"
img = Image.open(file_name)
if img.mode == "RGBA":
    r,g,b,a = img.split()
    rgb_img = Image.merge("RGB",(r,g,b))
    inv = PIL.ImageOps.invert(rgb_img)
else:
    inv = PIL.ImageOps.invert(img)
inv.save("inverted_"+file_name)