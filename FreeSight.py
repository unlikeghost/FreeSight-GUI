import os
import customtkinter
from PIL import Image
from typing import Dict
from utils import Headset  
from os import system as os_system
from json import load as load_json
from windows import (SOSWindow,
                     IoTWindow,
                     ChatWindow,
                     NoImplementedWindow,
                     ClaibrateWindow)
 

class FreeSight(customtkinter.CTk):
    def __init__(self, ip_server:str, port_server:int) -> None:
        super().__init__()
        
        iconpath:str = os.path.join('files', 'assets', 'icon.ico')
        appsjsonpath:str = os.path.join('files', 'apps.json')
        self.apps_json:dict = load_json(open(appsjsonpath, 'r'))
        self.index_app:Dict[int, str] = {index:app for index, app in enumerate(self.apps_json)}

        self.title('Free Sight')
        self.iconbitmap(iconpath)
        
        self.ip_server:str = ip_server
        self.port_server:int = port_server

        if DEBUG:
            self.full_screen:bool = False
            self.HEIGHT:int = config['graphics']['dev']['height']
            self.WIDTH:int = config['graphics']['dev']['width']
            
            self.geometry(f'{self.WIDTH}x{self.HEIGHT}+0+0')
            
            IMAGE_SIZE = ((self.WIDTH // 3)-35,
                          (self.HEIGHT // 2)-35)
            
        else:
            self.full_screen:bool = True
            self.attributes('-fullscreen', True)
            self.WIDTH:int = self.winfo_screenwidth()
            self.HEIGHT = self.winfo_screenheight()
            
            IMAGE_SIZE = ((self.WIDTH // 3)-35,
                          (self.HEIGHT // 2)-35)
            
            self.is_calibrated:bool = False
            
            self.bind('<Escape>', lambda _: self.destroy())

            if not self.is_calibrated:
                self.__create_calibration_window__()

        self.x_ref:float = 0.0
        
        self.apps_buttons:Dict[str, object] = {}
        
        for index, app in enumerate(self.apps_json):
            
            iconpath:str = self.apps_json[app]['icon']
            
            image = customtkinter.CTkImage(Image.open(iconpath), size=IMAGE_SIZE)
            
            self.apps_buttons[app] = customtkinter.CTkButton(master=self,
                                                            text='',
                                                            image=image,
                                                            )
            
            if index > (len(self.apps_json) // 2) - 1:
                row:int = 1
                column:int = (index - (len(self.apps_json) // 2)) % (len(self.apps_json) // 2 + 1)
            else:
                row:int= 0
                column:int= index
                
            self.apps_buttons[app].grid(row=row, column=column, padx=10, pady=10)
        
        self.apps_buttons['iot'].configure(border_color='red', border_width=5)
        
        self.bind('<Left>', self.switch_button)
        self.bind('<Right>', self.switch_button)
        self.bind('<Up>', self.switch_button)
        self.bind('<Down>', self.switch_button)
        self.bind('<Return>', self.launch_app)
        
        self.current_index_app:int = 0
        
        self.current_app:str = 'iot'
        
    def __create_calibration_window__(self):
        self.calibration_window = ClaibrateWindow(master=self, headset=Device,
                                                  full_screen=False)
        self.iconify()
        self.x_ref = self.calibration_window.calibrate()
        
        if self.x_ref:
            self.is_calibrated = True
            self.calibration_window.close()
            self.after_idle(self.deiconify)
    
    def switch_button(self, event):
        len_apps:int = len(self.apps_json)
        
        if event.keysym == 'Right':
            self.current_index_app:int = self.current_index_app + 1 if self.current_index_app < (len_apps - 1) else 0
            
            prev_app:str = self.index_app[self.current_index_app - 1] if self.current_index_app > 0 else self.index_app[len_apps - 1]
            next_app:str = self.index_app[self.current_index_app]
        
        elif event.keysym == 'Left':
            
            self.current_index_app:int = self.current_index_app - 1 if self.current_index_app > 0 else len_apps - 1
            
            prev_app:str = self.index_app[self.current_index_app + 1] if self.current_index_app < (len_apps - 1) else self.index_app[0]
            next_app:str = self.index_app[self.current_index_app]
        
        elif event.keysym == 'Up':
            
            self.current_index_app:int = self.current_index_app + 3 if self.current_index_app < (len_apps - 3) else self.current_index_app - 3
            
            prev_app:str = self.index_app[self.current_index_app - 3] if self.current_index_app > 2 else self.index_app[self.current_index_app + 3]
            next_app:str = self.index_app[self.current_index_app]
            
        elif event.keysym == 'Down':
            
            self.current_index_app:int = self.current_index_app - 3 if self.current_index_app > 2 else self.current_index_app + 3
            
            prev_app:str = self.index_app[self.current_index_app + 3] if self.current_index_app < (len_apps - 3) else self.index_app[self.current_index_app - 3]
            next_app:str = self.index_app[self.current_index_app]
        
        else:
            pass
        
        self.apps_buttons[prev_app].configure(border_color='', border_width=0)
        self.apps_buttons[next_app].configure(border_color='red', border_width=5)
        
        self.current_app:str = next_app
    
    def launch_app(self, _):
        
        if self.current_app == 'iot':
            self.top_level = IoTWindow(master=self, ip_server=IP_SERVER, port_server=PORT_SERVER,
                                       full_screen=self.full_screen)
            self.iconify()
            
        elif self.current_app == 'Chat':
            self.top_level = ChatWindow(master=self, ip_server=IP_SERVER, port_server=PORT_SERVER,
                                        full_screen=self.full_screen)
            self.iconify()
        
        elif self.current_app == 'SOS':
            self.top_level = SOSWindow(master=self, ip_server=IP_SERVER, port_server=PORT_SERVER,
                                       full_screen=self.full_screen)
            self.iconify()
        
        elif self.current_app == 'Tetris':
            tetris_path = os.path.join('Windows', 'Tetris.html')
            os_system(f'start {tetris_path}')
        
        elif self.current_app == 'Lectura':
            self.top_level = NoImplementedWindow(master=self,
                                                 full_screen=self.full_screen)
            self.iconify()
            
        elif self.current_app == 'TikTok':
            self.top_level = NoImplementedWindow(master=self,
                                                 full_screen=self.full_screen)
            self.iconify()
            

if __name__ == '__main__':
    
    from tomli import load as load_toml
    
    with open("settings.toml", mode="rb") as fp:
        config:dict = load_toml(fp)
    fp.close()
    
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')

    DEBUG:int = bool(config['mode']['dev'])
    
    IP_SOCKET:str = config['socket']['ip']
    PORT_SOCKET:int = config['socket']['port']
    
    IP_SERVER:str = config['server']['ip']
    PORT_SERVER:int = config['server']['port']
    
    Device = Headset(ip=IP_SOCKET, port=PORT_SOCKET)
    
    app = FreeSight(IP_SERVER, PORT_SERVER)
    app.mainloop()
    