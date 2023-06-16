import sys
import socket
from typing import List
from json import loads as json_loads
from pyautogui import press as pyautogui_press


class Headset:
    
    def __init__(self, ip:str, port:int) -> None:
        self.ip:str = ip
        self.port:int = port
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(0.5)
        server_address = (self.ip, self.port)
        self.sock.bind(server_address)
        server_up:bool = self.__init_socket__()
        if not server_up:
            print(f'Port is not open,check your headset connectionon {server_address}:')
            sys.exit()
        print("*"*20)
        print("UDP LISTENER".center(20, '-'))
        print("UP".center(20, '-'))
        print(f"IP:{self.ip}".center(20, '-'))
        print(f"PORT:{self.port}".center(20, '-'))
        print("*"*20)
        
        self.stop:bool = False
        
    def __init_socket__(self) -> None:
        try: self.sock.recvfrom(20000)
        except socket.timeout: return False
        return True

    def calibrate_subject(self, subject_data:dict) -> dict:
        
        raw_data, _ = self.sock.recvfrom(20000)
        data:dict = json_loads(raw_data.decode())

        if data.get('type') == 'accelerometer':
            aux_data:List[int]= data.get('data')
            subject_data['x']+= aux_data[0]
            subject_data['z']+= aux_data[2]
            subject_data['acc_iters']+= 1
            return subject_data
        
        if data.get('type') == 'emg':
            emg_data:List[int] = data.get('data')    
            subject_data['fp1'] = emg_data[0]
            subject_data['fp2'] = emg_data[1]
            subject_data['emg_iters']+= 1
            return subject_data
        
        return dict.fromkeys(subject_data, 0)

    def control_mode(self, subject_data:dict) -> None:
        
        FP1_REF:float = subject_data['fp1'] + 0.85
        FP2_REF:float = subject_data['fp2'] + 0.85
        
        LEFT_REF:float = subject_data['x'] + 0.2
        RIGHT_REF:float = subject_data['x'] - 0.2
        NEUTRAL_REF:float = subject_data['x'] + -0.075
        NEUTRAL_REF2:float = subject_data['x'] + 0.075
        
        DOWN_REF:float = subject_data['z'] + 0.05
        
        x_prev:float = 0
        z_prev:float = 0
        
        once_left:bool = False
        once_right:bool = False
        
        while True:
            raw_data, _ = self.sock.recvfrom(20000)
            data:dict = json_loads(raw_data.decode())
            
            if data.get('type') == 'accelerometer':
                
                aux_data:List[float] = data.get('data')
                x:float = aux_data[0]
                z:float = aux_data[2]
                
                if z > DOWN_REF and z_prev < z:
                    pyautogui_press('down')
                    
                else:
                    if NEUTRAL_REF2 < x < LEFT_REF and x_prev < x:
                        if not once_left:
                            pyautogui_press('left')
                            once_left:bool = True
                        else:
                            pyautogui_press('left')
                    
                    elif NEUTRAL_REF > x > RIGHT_REF and x_prev > x:
                        
                        if not once_right:
                            pyautogui_press('right')
                            once_right:bool = True
                        else:
                            pyautogui_press('right')
                    
                    elif NEUTRAL_REF < x < NEUTRAL_REF2:
                        once_left:bool = False
                        once_right:bool = False
                            
                x_prev:float = x
                z_prev:float = z
            
            elif data.get('type') == 'emg':
                
                emg_data:List[int] = data.get('data')
                fp1:float = emg_data[0]
                fp2:float = emg_data[1]
                
                if (fp2 < FP2_REF) and (fp1 < FP1_REF):
                    go_enter:bool = False
                
                elif (fp2 > FP1_REF) and (fp1 > FP2_REF) and not go_enter:
                    pyautogui_press('enter')
                    go_enter:bool = True
            
            if self.stop:
                break
        
    def close(self) -> None:
        self.stop = True
        
        
if __name__ == '__main__':
    from typing import Dict
    
    device = Headset("127.0.0.1", 12345)
            
    data: Dict[str, float] = {
        'acc_iters': 0,
        'x': 0,
        'z': 0,
        'emg_iters': 0,
        'fp1': 0,
        'fp2': 0,
    }
    
    for iteration in range(200):
        data:Dict[str, float] = device.calibrate_subject(data)
        
    data['x']:float = data['x'] / data['acc_iters']
    data['z']:float = data['z'] / data['acc_iters']
    data['fp1']:float = data['fp1'] / data['emg_iters']
    data['fp2']:float = data['fp2'] / data['emg_iters']
    
    print(data)

    device.control_mode(data)