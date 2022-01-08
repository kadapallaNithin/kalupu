import cv2
import numpy as np
def split_pair(s):
    p = s.split(' ')
    return int(p[0]), int(p[1])
def polyline():
    img = np.zeros((512,512,3),np.uint8)
    ink = (255,255,255)
    transparent = (0,200,0)
    points = open("polyline.txt").read().split("\n")
    color = ink
#    if points[0][0] == 'm':
    x,y = split_pair(points[0][2:])
    # else:
    #     x,y = split_pair(points[0])
    for point in points[1:]:
        if point == '':
            pass
        elif point[0] == 's':
            xi,yi = split_pair(point[2:])
            cv2.line(img,(x,y),(xi,yi),transparent)
            x,y = xi, yi
        elif point == 'e':
            pass
        else:
            xi,yi = split_pair(point)
            cv2.line(img,(x,y),(xi,yi),ink)
            x,y = xi, yi
        cv2.imshow("img",img)
        cv2.waitKey(1)
    cv2.waitKey(0)
#polyline()