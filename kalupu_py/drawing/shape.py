import cv2
import numpy as np
import polyline
import coord2command

draw_polyline = False
store_contours = False
contour_bytes_dir = "edge/nithin/"
img_name = "Dr._Karthick_Seshadri_Sir-removebg.png"
img = cv2.imread("edge/"+img_name)
window_name = "TrackBars"
save_image_name =  "edge/drawing_" + img_name

def empty(a):
    pass

cv2.namedWindow(window_name)
cv2.resizeWindow(window_name,10000,10000) # 0,26,77,177,0,172
cv2.createTrackbar("sig",window_name,1,10,empty)
cv2.createTrackbar("blur0",window_name,1,100,empty)
cv2.createTrackbar("blur1",window_name,1,100,empty)
cv2.createTrackbar("cthr0",window_name,1,100,empty)
cv2.createTrackbar("cthr1",window_name,1,100,empty)

    
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
while cv2.waitKey(1) != 113:
    blur0 = cv2.getTrackbarPos("blur0",window_name)
    if blur0%2 == 0:
        blur0 = blur0 - 1 
    blur1 = cv2.getTrackbarPos("blur1",window_name)
    if blur1%2 == 0:
        blur1 = blur1 - 1 
    cthr0 = cv2.getTrackbarPos("cthr0",window_name)
    cthr1 = cv2.getTrackbarPos("cthr1",window_name)
    imgblur = cv2.GaussianBlur(img,(blur0,blur1),1)
    img_edged = cv2.Canny(imgblur,cthr0,cthr1)
    cv2.imshow("img",img_edged)

if save_image_name != None:
    cv2.imwrite(save_image_name,img_edged)

if store_contours:
    points = ""
    contours, hierarchy = cv2.findContours(img_edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        points += "s "
        for i in cnt:
            points += f"{i[0][0]} {i[0][1]}\n"
        # print(cnt[0][0])
    with open("polyline.txt","w") as f:
        f.write(points)
    if draw_polyline:
        polyline.polyline()
if contour_bytes_dir != None:
    contours, hierarchy = cv2.findContours(img_edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    coord2command.coord2bytes(contours,contour_bytes_dir)