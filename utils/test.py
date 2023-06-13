import json
import socket
import winsound
from typing import List


class Headset:
    def __init__(self, ip:str='127.0.0.1', port:int=12345):
        
        self.ip:str = ip
        self.port:int = port
        self.__init_socket__()
        
    def __init_socket__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (self.ip, self.port)
        self.sock.bind(server_address)
        
        print("--------------------")
        print("-- UDP LISTENER-----")
        print("--------UP----------")
        print("IP:", self.ip)
        print("PORT:", self.port)
        print("--------------------")
        
    def __printProgressBar__ (self, iteration:int, total:int, prefix:str='', suffix:str= '', decimals:int=1, length:int=100, fill:str= '█', printEnd:str="\r") -> None:
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()
    
    def calibrate_subject(self, 
                          progress_bar:bool=False) -> bool:
                
        print("Calibration period, remain neutral...")
        winsound.Beep(500, 500)
        
        x_start_sum:float = 0
        x_start_samples:float = 0
        for interation in range(150):
            data, _ = self.sock.recvfrom(20000)
            obj:dict = json.loads(data.decode())
            
            if obj.get('type') == 'accelerometer':
                aux_data:List[int] = obj.get('data')
                
                print(aux_data[0])
                x_start_sum += aux_data[0]
                x_start_samples += 1
                
                if progress_bar:
                    self.__printProgressBar__(iteration=interation, total=150, prefix='Progress:', suffix='Complete', length=50)

        return x_start_sum / x_start_samples
    
    def move_mode(self, x_ref:float) -> None:
        
        z_prev:float = 0
        x_prev:float = 0
        space_pressed:bool = False
        left_once:bool = False
        right_once:bool = False
                
        while True:
            data, _ = self.sock.recvfrom(20000)
            obj = json.loads(data.decode())
            
            if obj.get('type') == 'accelerometer':
                aux_data:List[int] = obj.get('data')
                x = aux_data[0]
                z = aux_data[2]
            
                if z > 0.5 and z_prev < z and not space_pressed:  # drop piece
                    print('space')
                    space_pressed = True
                
                else:
                    if 0.075 + x_ref < x < 0.2 + x_ref and not left_once:  # short left
                        print('left')
                        left_once:bool = True
                        space_pressed:bool = False
                    elif -0.075 + x_ref > x > -0.2 + x_ref and not right_once:  # short right
                        print('right')
                        right_once = True
                        space_pressed = False
                    elif x > 0.2 + x_ref and x_prev < x:  # move left
                        print('left')
                        left_once = False
                        space_pressed = False
                    elif x < -0.2 + x_ref and x_prev > x:  # move right
                        print('right')
                        right_once = False
                        space_pressed = False
                    elif -0.075 + x_ref < x < 0.075 + x_ref:  # head is neutral
                        left_once = False
                        right_once = False
                        space_pressed = False
                    elif z < 0.5:
                        space_pressed = False
                
                if z > 0.5:
                    space_pressed = True
                x_prev = x
                z_prev = z
            
            else:
                emg_data:List[int] = obj.get('data')
                fp2:float = emg_data[1]
                to_continue:float = 0
                
                for i in range(2, 8):
                    if emg_data[i] > 0.8:
                        to_continue += 1
                
                if (to_continue < 4):
                    if fp2 < 0.9:
                        rotated:bool = False
                        
                    elif (fp2 > 0.9) and not rotated:
                        print('up')
                        rotated:bool = True


if __name__ == "__main__":
    
    device = Headset()
    ref = device.calibrate_subject()
    
    print(ref)
    device.move_mode(x_ref=ref)
    