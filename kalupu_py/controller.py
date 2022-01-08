import cv2
import time
from nithin.arm import Arm
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import urllib.parse
class DetectionHandler(BaseHTTPRequestHandler):
    # def __init__(self):
    #     self.working = True
    #     super().__init__()
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def capture(self):
        return "Cap"
    def arm_action_completed(self):
        self.server.context["arm_action_completed"] = True
    def stop_working(self):
        #self.
        self.server.context["working"] = False
        return "Stopped"
    def do_GET(self):
        # logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        # self.wfile.write("GET request for {}".format(self.path).encode('utf-8')
        path_dict = {"/capture":self.capture,"/stop_working":self.stop_working}
        if self.path in path_dict:
            message = path_dict[self.path]()
        else:
            message = "Invalid path"
        self.wfile.write(message.encode('utf-8'))
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_data = post_data.decode('utf-8')
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data)
        post_data = urllib.parse.parse_qs(post_data) # dict of post_data
        

        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        path_dict = {"/arm_action_completed":self.arm_action_completed}
        if self.path in path_dict:
            message = path_dict[self.path](post_data)
        else:
            message = "Invalid path"
        self.wfile.write(message.encode('utf-8'))

class ClassHandler:
    def __init__(self):
        self.action_map = [] # self.handle_class0,self.handle_class1...
    def handle_class(self,cls,*args,**kwargs):
        try:
            return self.action_map[cls](*args[1:],**kwargs)
        except IndexError:
            print(f"Note: No action set for class {cls}")
class GroundNutClassHandler(ClassHandler):
    def __init__(self,arm):
        self.action_map = [self.handle_nut,self.handle_nut,self.handle_nut,self.handle_nut]#,self.handle_shell,self.handle_innernut]
        self.arm = arm
    def handle_nut(self,displace=None):
        #if displace == None:
#            displace = (1,0,0)
        position = self.arm.position()
        return self.arm.displace(*displace) and self.arm.pick(180) and self.arm.move_to(10,10) and self.arm.move_to(position[0],position[1])
        #return self.arm.displace(*displace)
    def handle_shell(self,displace=None):
        if displace == None:
            displace = (-1,0,0)
        return self.arm.displace(*displace)
    def handle_innernut(self,displace=None):
        if displace == None:
            displace = (1,0,0)
        return self.arm.displace(*displace)
    def handle_many(self,displace=None):
        if displace == None:
            displace = (0,1,0)
        return self.arm.displace(*displace)

class Controller(HTTPServer):
    def __init__(self,source,server_name="",port=8765):
        self.source = source
        self.arm = Arm()
        self.area = Area()
        self.arm.wait()
        self.class_handler = GroundNutClassHandler(self.arm)
        super().__init__((server_name,port),DetectionHandler)
        self.context = {"working":True,"arm_action_completed":True}

    def handle_detections(self,img,det,parameters, show=False,save=False,print_det=True):
        labelled_image = img
        classwise_count = dict()
        for c in det[:, -1].unique():
            classwise_count[c] = (det[:, -1] == c).sum()  # detections per class
            # s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
        if len(classwise_count.keys()) == 1:
            self.class_handler.handle_class(int(list(classwise_count.keys())[0]))
#            self.handle_request()
        else:
            for *xyxy, conf, cls in reversed(det):
                # xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                # line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                tr, tl, br, bl = xyxy
                tr, tl, br, bl = int(tr), int(tl), int(br), int(bl)
                cls, conf = int(cls), float(conf)
                if print_det:
                    print(cls,conf,tr,tl,br,bl)
                if save or show:
                    labelled_image = cv2.rectangle(labelled_image,(tr,tl),(br,bl),(255,0,0),2)
        source = parameters["source"]
        if save:
            cv2.imwrite(source[:-4]+"_label.jpg",labelled_image)
        if show:
            cv2.imshow("stream",labelled_image)
            cv2.waitKey(1)
    
    def move_to_next_frame(self):

    # def get_source():
    #     source = os.path.join("nithin","images",str(int(time.time()))+".jpg")
    #     succ, img = cap.read()
    #     if not succ:
    #         return False
    #     cv2.imwrite(source,img)
    #     return source
    # def arm_action_completed(self):
    #     return self.context["arm_action_completed"]
    def is_working(self):
        return self.context["working"]
# s = Controller("",8000)
# while s.is_working():
#     s.handle_request()













