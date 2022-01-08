import requests
import os
import sys
import argparse
import cv2
import numpy as np
# parser = argparse.ArgumentParser()
# parser.add_argument('--dir-name',type=str, default="10")
# parser.add_argument('--draw-on',type=str,default="paper")
# parser.add_argument('--paper-scale', type=str, default="1 1", help='confidence threshold')
# parser.add_argument('--paper-size', type=str, default="")
# opt = parser.parse_args()
# kwags = vars(opt)
# print(kwags)
class Draw:
    def __init__(self,dir_name="0"):
        self.dir_name = dir_name #"../drawing/edge/drawing_nithin"+"_contour_bytes/" #amma_nanna_ #kwags["dir-name"]
        self.draw_on =  "img" #kwags["draw-on"]
        self.scale = (1,1)
        self.url = "http://192.168.43.80/"
        self.img = cv2.imread(os.path.join(self.dir_name,"drawing.jpg"))
        self.WIDTH, self.HEIGHT,_ = self.img.shape
        self.img = np.zeros((self.WIDTH,self.HEIGHT,3),np.uint8)

    def x_in_limits(self,a):
        return a >= 0 and a < self.WIDTH
    def y_in_limits(self,a):
        return a >= 0 and a < self.HEIGHT

    def draw_contour_on_paper(self,contour):
        r = requests.post(self.url+"draw/",
            {"contour":contour,"scale_x":self.scale[0],"scale_y":self.scale[1],"down":180,"up":170})#, headers={"content-type":"application/oct-stream"}
        print(r.text)

    def draw_contour_on_img(self,contour):
        if len(contour)%4 == 0:
            i = 0
    #        print("Contour : ")
            while i < len(contour):
                x = int.from_bytes(contour[i:i+2],'big')#//scale[0]
                y = self.HEIGHT - (int.from_bytes(contour[i+2:i+4],'big'))#//scale[1]
                if self.x_in_limits(x) and self.y_in_limits(y):
                    cv2.rectangle(self.img,(x,y),(x+2,y+2),(255,0,0))
                    cv2.imshow("img",self.img)
                    cv2.waitKey(1)
                else:
                    print(x,y)
                i+=4
        else:
            print("Malfarmed contour")
    def draw(self):
        for contour_index in range(len(os.listdir(d.dir_name))-1):
            with open(os.path.join(d.dir_name,str(contour_index)),'rb') as f:
                contour = f.read()
                if self.draw_on == "img" or self.draw_on == "both":
                    self.draw_contour_on_img(contour)
                if self.draw_on == "both" or self.draw_on == "paper":
                    self.draw_contour_on_paper(contour)
        cv2.waitKey(0)
        if d.draw_on == "paper" or d.draw_on == "both":
            #final_state_commands = "p 160m 0 0"
            final_state_commands = "p 160"
            r = requests.post(d.url+"pass_commands/",{"commands":final_state_commands})
        #     x = 0
        #     draw_contour_on_paper(x.to_bytes(2,'big')*2)
for i in range(7):
    d = Draw(str(i))
    d.draw()