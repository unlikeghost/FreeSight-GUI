import socket
from typing import List
from json import loads as json_loads
from pyautogui import press as pyautogui_press


class Headset:
    def __init__(self, ip:str, port:int) -> None:
        
        self.ip:str = ip
        self.port:int = port
        
        self.__init_socket__()
        
    def __init_socket__(self) -> None:
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = (self.ip, self.port)
        
        self.sock.bind(self.server_address)
        print("--------------------")
        print("-- UDP LISTENER-----")
        print("--------UP----------")
        print("IP:", self.ip)
        print("PORT:", self.port)
        print("--------------------")
    
    def calibrate_subject(self, x_start_sum:float, x_start_samples:int) -> bool:
        
        data, _ = self.sock.recvfrom(20000)
        obj:dict = json_loads(data.decode())
        if obj.get('type') == 'accelerometer':
            data, _ = self.sock.recvfrom(20000)
            aux_data:List[int] = obj.get('data')
            obj:dict = json_loads(data.decode())
            x_start_sum = aux_data[0]
            x_start_samples += 1
        
            return x_start_sum, x_start_samples
        
        return 0, 0 
    
    def move_mode(self, x_ref:float) ->None:
        
        x_start:float = x_ref
        z_prev:float = 0
        x_prev:float = 0
        space_pressed:bool = False
        left_once:bool = False
        right_once:bool = False
        
        while True:
            data, _ = self.sock.recvfrom(20000)
            obj:dict = json_loads(data.decode())
            
            if obj.get('type') == 'accelerometer':
                aux_data:List[int] = obj.get('data')
                x:int = aux_data[0]
                z:int = aux_data[2]
                
                if z > 0.5 and z_prev < z and not space_pressed:  # drop piece
                    pyautogui_press('down')
                    space_pressed:bool = True
                
                else:
                    if 0.075 + x_start < x < 0.2 + x_start and not left_once:  # short left
                        pyautogui_press('left')
                        left_once:bool = True
                        space_pressed:bool = False
                    elif -0.075 + x_start > x > -0.2 + x_start and not right_once:  # short right
                        pyautogui_press('right')
                        right_once = True
                        space_pressed = False
                    if x > 0.2 + x_start and x_prev < x:  # move left
                        pyautogui_press('left')
                        left_once:bool = False
                        space_pressed:bool = False
                    elif x < -0.2 + x_start and x_prev > x:  # move right
                        pyautogui_press('right')
                        right_once:bool = False
                        space_pressed:bool = False
                    elif -0.075 + x_start < x < 0.075 + x_start:  # head is neutral
                        left_once:bool = False
                        right_once:bool = False
                        space_pressed:bool = False
                    elif z < 0.5:
                        space_pressed:bool = False
                
                if z > 0.5:
                    space_pressed:bool = True
                x_prev:int = x
                z_prev:int = z
                    
            else:
                emg_data:List[int] = obj.get('data')
                fp2:float = emg_data[1]
                # to_continue:float = 0
                
                if fp2 < 0.9:
                    rotated:bool = False
                        
                elif (fp2 > 0.9) and not rotated:
                    pyautogui_press('enter')
                    rotated:bool = True