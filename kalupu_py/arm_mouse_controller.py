import cv2
import numpy as np
import requests
import os
import sys

WIDTH = 500
HEIGHT = 500
scale = (1,1)
def getIncreasingFileName(dir,extension=''):
    if not os.path.exists(dir):
        os.mkdir(dir)
    file_number = 0
    file_name = "0"+extension
    while os.path.exists(os.path.join(dir,file_name)):
        file_number += 1
        file_name = str(file_number)+extension
    return os.path.join(dir,file_name)

class MouseController:
    x = 0
    y = 0
    window_name = "window_name"
    draw = False
    # request = 2
    # responded = True
    # coords = list()
    contours = bytes(0)
    dir_path = "" #None # None if don't want to store '' otherwise
    contour_index = 0
    img = np.zeros((HEIGHT,WIDTH,3),np.uint8)
    url = "http://192.168.43.80/"
    def __init__(self):
        cv2.namedWindow(MouseController.window_name)
        cv2.setMouseCallback(MouseController.window_name,MouseController.draw_event)
        if MouseController.dir_path != None:
            MouseController.dir_path = getIncreasingFileName("drawing_bytes")
            os.mkdir(MouseController.dir_path)
        while True:
            cv2.imshow(MouseController.window_name, MouseController.img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                if MouseController.dir_path != None:
                    cv2.imwrite(os.path.join(MouseController.dir_path,'drawing.jpg'),MouseController.img)
                break
            # elif k == ord('a'):
            #     MouseController.request = 1 - MouseController.request

    def draw_event(event,x,y,flags,param):
        send_data = False
        ty = WIDTH - y
        if event == cv2.EVENT_LBUTTONDOWN:
            MouseController.draw = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if MouseController.draw:
                cv2.rectangle(MouseController.img,(x,y),(x+2,y+2),(255,0,0),1)
#            print(x,y)
        elif event == cv2.EVENT_LBUTTONUP:
            MouseController.draw = False
            send_data = True
            x *= scale[0]
            ty *= scale[1]
            MouseController.contours += x.to_bytes(2,'big') + ty.to_bytes(2,'big')
#            MouseController.commands += f"p 150\n"
        if MouseController.draw and not(MouseController.x == x and MouseController.y == y):
            x *= scale[0]
            ty *= scale[1]
            MouseController.contours += x.to_bytes(2,'big') + ty.to_bytes(2,'big')
            MouseController.x, MouseController.y = x,y
        if send_data:
            contours = MouseController.contours
            MouseController.contours = bytes(0)
            if MouseController.dir_path != None:
                with open(os.path.join(MouseController.dir_path,str(MouseController.contour_index)),'wb') as f:
                    f.write(contours)
            MouseController.contour_index += 1
            # r = requests.post(MouseController.url+"draw/", contours, headers={"content-type":"application/oct-stream"})#f" {x-MouseController.x} {y-MouseController.y}"{"d":(x-MouseController.x,y-MouseController.y,0,0)}
            # print(r.text)

#         if event == cv2.EVENT_LBUTTONDOWN:
#             MouseController.draw = True
            
# #            print("s",x,y)
#         elif event == cv2.EVENT_MOUSEMOVE:
#             if MouseController.request == 1:
#                 MouseController.coords.append((x,y))
#                 if MouseController.responded:
#                     old_coords = list(MouseController.coords)
#                     MouseController.coords = list()
#                     MouseController.responded = False
#                     data = ""
#                     for coord in old_coords:
#                         data += f"d {coord[0]},{coord[1]}"
#                     r = requests.post(MouseController.url+"displace/" ,{"coords":data})#f" {x-MouseController.x} {y-MouseController.y}"{"d":(x-MouseController.x,y-MouseController.y,0,0)}
#                     print(r.text)
#                     MouseController.responded = True
#                 MouseController.x = x
#                 MouseController.y = y
#             elif MouseController.request == 2:
# #                requests.post(MouseController.url+"set_position/",{"coord":(0,0,0,0)})
#                 MouseController.request = 0
#             if MouseController.draw:
#                 cv2.rectangle(MouseController.img,(x,y),(x+2,y+2),(255,0,0),1)
#                 print(x,y)
# #            print(x,y)
#         elif event == cv2.EVENT_LBUTTONUP:
#             MouseController.draw = False
#             print("e",x,y)

mc = MouseController()