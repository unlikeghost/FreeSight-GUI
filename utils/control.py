import socket
from typing import List
from json import loads as json_loads


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
    
    def calibrate_subject(self, x_start_sum:float) -> bool:
        
        data, _ = self.sock.recvfrom(20000)
        obj:dict = json_loads(data.decode())
        if obj.get('type') == 'accelerometer':
            data, _ = self.sock.recvfrom(20000)
            aux_data:List[int] = obj.get('data')
            obj:dict = json_loads(data.decode())
            x_start_sum = aux_data[0]
        
        return x_start_sum 