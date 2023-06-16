import customtkinter
from PIL import Image
from typing import Dict
from os import path as os_path
from json import load as load_json
from json import dump as dump_json 
from windows.__base__ import WindowBase


class IoTWindow(WindowBase):
    
    def __init__(self, master, ip_server:str,
                 port_server:int, api_url:str='api/v1/public/send-iot',
                 full_screen:bool = False) -> None:
        super().__init__(master, ip_server, port_server, api_url, full_screen)
        
        self.top_level.title('Free Sight IOT')
        
        if full_screen:
            height:int = self.top_level.winfo_screenwidth()
            width:int = self.top_level.winfo_screenheight()
            self.IMAGE_SIZE = (width - 155,
                               (height // 3)-35)
        else:
            width:int = 600
            height:int = 800
            self.IMAGE_SIZE = ((width // 2)-35,
                               (height // 2)-35)
        
        iotjsonpath:str = os_path.join('files', 'assets', 'iot', 'status.json')
        self.status_iot:Dict[str, str] = load_json(open(iotjsonpath, 'r'))
        
        self.buttons_mapping:Dict[int, str] = {index:app for index, app in enumerate(['Foco 1', 'Foco 2'])}
        
        self.key_mapping:Dict[str, customtkinter.CTkButton] = {}
        
        for  index, button in enumerate(self.buttons_mapping):
            
            satus_button = self.status_iot[self.buttons_mapping[button]]['status']
            
            iconpath:str = os_path.join('files', 'assets', 'iot', f'{satus_button}.png')
            
            image = customtkinter.CTkImage(Image.open(iconpath), size=self.IMAGE_SIZE)
            
            self.key_mapping[button] = customtkinter.CTkButton(master=self.top_level,
                                                                text='',
                                                                image=image,
                                                                )
            
            self.key_mapping[button].grid(row=0, column=index, padx=10, pady=10,
                                          sticky='nsew')
        
        self.top_level.grid_rowconfigure(0, weight=1)
        
        closeimage = customtkinter.CTkImage(Image.open(os_path.join('files', 'assets', 'close.png')),
                                            size =(self.IMAGE_SIZE[0]//2,
                                                   self.IMAGE_SIZE[1]//2))
        
        self.key_mapping[2] = customtkinter.CTkButton(master=self.top_level,
                                                      image=closeimage,
                                                      text='',
                                                      command=self.__on_close__)
        self.key_mapping[2].grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.key_mapping[0].configure(border_color='red', border_width=5)
                
        self.top_level.bind('<Left>', self.switch_button)
        self.top_level.bind('<Right>', self.switch_button)
        self.top_level.bind('<Return>', self.select_key)
        
        self.current_index_key:int = 0
        self.current_key:str = self.key_mapping[self.current_index_key]
    
    def __on_close__(self) -> None:
        dump_json(self.status_iot, open(os_path.join('files', 'assets', 'iot', 'status.json'), 'w'))
        self.master.deiconify()
        self.top_level.destroy()
    
    def switch_button(self, event) -> None:
        
        len_keys = len(self.key_mapping)
        
        if event.keysym == 'Right':
            
            self.current_index_key = self.current_index_key + 1 if self.current_index_key < (len_keys - 1) else 0
            prev_index_key:int = self.current_index_key - 1 if self.current_index_key > 0 else len_keys - 1

        if event.keysym == 'Left':
            self.current_index_key:int = self.current_index_key - 1 if self.current_index_key > 0 else len_keys - 1
            prev_index_key:int = self.current_index_key + 1 if self.current_index_key < (len_keys - 1) else 0

        self.key_mapping[prev_index_key].configure(border_color='', border_width=0)
        self.key_mapping[self.current_index_key].configure(border_color='red', border_width=5)
        
        self.current_key:str = self.key_mapping[self.current_index_key]
    
    def select_key(self, _) -> None:
        
        if self.current_index_key == 2:
            self.__on_close__()
            
        else:
            name:str = self.buttons_mapping[self.current_index_key]
            self.status_iot[name]['status'] = 'on' if self.status_iot[name]['status'] == 'off' else 'off'
            status_iot_foco1:int = 1 if self.status_iot['Foco 1']['status'] == 'on' else 0
            status_iot_foco2:int = 1 if self.status_iot['Foco 2']['status'] == 'on' else 0
            
            payload:str = f'led_1=Cocina&led_2=Habitacion&status_1={status_iot_foco1}&status_2={status_iot_foco2}'

            self.http_post(self.url, payload)
    
            new_status = self.status_iot[name]['status']
            
            iconpath:str = os_path.join('files', 'assets', 'iot', f'{new_status}.png')
            
            image = customtkinter.CTkImage(Image.open(iconpath),
                                           size=self.IMAGE_SIZE)
            
            self.key_mapping[self.current_index_key].configure(image=image,)


if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title('Free Sight Chat Demo')
    root.attributes('-fullscreen', False)
    root.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
    
    root.iconify()
    
    chat = IoTWindow(root, '127.0.0.1', 8080,
                      full_screen=True)
    
    root.mainloop()