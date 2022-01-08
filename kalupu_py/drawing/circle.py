import cv2
import numpy as np

def translate(x,y):
    X,Y = 512,512
    xo, yo = 256,256
    return xo + x + yo + y*(-1)
def circle(radius=100,center=(256,256)):
    img = np.zeros((512,512,3),np.uint8)
    x, y = center[0]-radius, center[1]
    #for x_dir,y_dir in [(1,1),(-1,1),(1,-1),(-1,-1)]:
    for xi in range(-radius,radius):
        yi = int((radius**2-(xi)**2)**0.5)
        cv2.line(img,(center[0]+xi,center[1]+yi),(center[0]+x,center[1]+y),(255,255,0))
        print(250+x,260+y)
        cv2.imshow("img",img)
        cv2.waitKey(3)
        x,y = xi,yi
    for xi in reversed(range(-radius,radius)):
        yi = int((radius**2-(xi)**2)**0.5)
        cv2.line(img,(center[0]+xi,center[1]-yi),(center[0]+x,center[1]-y),(255,0,0))
        print(250+x,260-y)
        cv2.imshow("img",img)
        cv2.waitKey(3)
        x,y = xi,yi
    cv2.waitKey(0)
# img = np.zeros((512,512,3),np.uint8)
# while True:
#     x,y = int(input()),int(input())
#     cv2.circle(img,(x,y),1,(255,255,0))
#     cv2.imshow("img",img)
#     if cv2.waitKey(1) & 0xFF == 113:
#         break
circle()