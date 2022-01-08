import time
import requests
class Grid:
    def __init__(self,rows,cols,cell_size,position=(0,0),direction="forward"):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.position = position
        self.direction = direction
    def set_position(self,position):
        self.position = position
    def toggle_direction(self):
        if self.direction == "forward":
            self.direction = "backward"
        else:
            self.direction = "forward"
    def forward_next_cell(self):
        if self.position == (self.rows-1,self.cols-1):
            return None
        if self.position[0]%2 == 0:
            if self.position[1] == self.cols-1:
                return (self.position[0]+1,self.cols-1)
            return (self.position[0],self.position[1]+1)
        else:
            if self.position[1] == 0:
                return (self.position[0]+1,0)
            return (self.position[0],self.position[1]-1)
    def backward_next_cell(self):
        if self.position == (0,0):
            return None
        if self.position[0]%2 == 0:
            if self.position[1] == 0:
                return (self.position[0]-1,0)
            return (self.position[0],self.position[1]-1)
        else:
            if self.position[1] == self.cols-1:
                return (self.position[0]-1,self.cols-1)
            return (self.position[0],self.position[1]+1)
    def move_to_next_cell(self):
        if self.direction == "forward":
            next_cell = self.forward_next_cell()
        else:
            next_cell = self.backward_next_cell()
        if next_cell == None:
            return None
        else:
            self.position = next_cell
            return next_cell


class Arm:
    def __init__(self,grid,pserver_address="http://localhost:8766/"):
        self.server_address = pserver_address
        self._position = (0,0,0,0)
        self.grid = grid

    def position(self):
        return self._position
    def wait(self):
        not_available = True
        wait_time = 1
        while not_available:
            try:
                response = requests.get(self.server_address+"available/")
                if response.text == "Yes":
                    not_available = False
                elif response.text == "No":
                    print("Connected but not available")
                else:
                    print(f"Unexpected response : {response.text}")
            except requests.exceptions.ConnectionError:
                print(f"Connection Error. I'll try after {wait_time}s")
                if wait_time < 10:
                    wait_time *= 2
            time.sleep(wait_time)
    def _request(self,_path,f,data={}):
        try:
            response = requests.post(self.server_address+_path,data)
            return f(response)
        except requests.exceptions.ConnectionError:
            print(f"Connection Error.")
        return False
    def _accept_yes(response):
        return response.text == "Yes"
    def _accept_blank(response):
        return response.text == ""
    def _add_displacement(self,x,y,z,a):
        self._position = (self._position[0]+x,self._position[1]+y,self._position[2]+z,self._position[3]+a)
    def displace(self,x=0,y=0,z=0,a=0):
        # coord = {"x":x,"y":y,"z":z}

        if self._request("displace/",Arm._accept_yes,coord):
            self._add_displacement(x,y,z,a)
            print(self._position)
    def move_to(self,x,y):
        # position = self._position
        # self.displace(x=(x-position[0]),y=(y-position[1]))
        if self._request("pass_commands/",Arm._accept_yes,{"commands":f"m {x} {y}"}):
            return "ok"
        self._position = (x,y,self._position[2],self._position[3])

    def move_to_next_cell(self):
        next_cell = self.grid.move_to_next_cell()
        if next_cell == None:
            return False
        self.move_to(next_cell[0]*self.grid.cell_size[0],next_cell[1]*self.grid.cell_size[1])
        return True


    def pick(self,angle):
        return self._request("pick/",Arm._accept_blank,str(angle))

# g = Grid(3,5,(100,100))
# current_cell = (0,0)
# while current_cell != None:
#     print(current_cell)
#     current_cell = g.move_to_next_cell()
# current_cell = ''
# g.toggle_direction()
# while current_cell != None:
#     print(current_cell)
#     current_cell = g.move_to_next_cell()



# g = Grid(3,3,(300,300),direction="forward")
# a = Arm(g,"http://192.168.43.80/")

# c = a.move_to_next_cell()
# while c:
#     c = a.move_to_next_cell()
# a.grid.toggle_direction()
# print('direction')
# c = True
# while c:
#     print(c)
#     c = a.move_to_next_cell()
