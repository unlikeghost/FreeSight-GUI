import customtkinter
from PIL import Image
from time import sleep
from typing import Dict
from os import path as os_path
from playsound import playsound
from requests import request
from CTkMessagebox import CTkMessagebox


class SOSWindow:
    #TODO: Arreglar la salida para que no suene la alarma si se cancela la carga
    
    def __init__(self, master, ip_server:str, port_server:int,
                 full_screen:bool=False) -> None:
        
        self.top_level = customtkinter.CTkToplevel(master)
        self.master = master
        self.top_level.title('Free Sight SOS')
        self.top_level.protocol('WM_DELETE_WINDOW', self.on_close)
        self.top_level.focus_force()
        
        self.url:str = f'http://{ip_server}:{port_server}/api/v1/public/send-chat'
        
        if full_screen:
            self.top_level.attributes('-fullscreen', True)
            height:int = self.top_level.winfo_screenwidth()
            width:int = self.top_level.winfo_screenheight()
            self.IMAGE_SIZE = (width - 155,
                               (height // 3)-35)
            font:tuple = ('Arial', 70)
            height_bar:int = 300
            
        else:
            width:int = 600
            height:int = 800
            self.IMAGE_SIZE = ((width // 2)-35,
                            (height // 3)-35)
            font:tuple = ('Arial', 30)
            height_bar:int = 40
        
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        
        self.top_level.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
        
        info_label = customtkinter.CTkLabel(self.top_level,
                                            text='Para cancelar SOS, presione el botón de cerrar',
                                            font=font,
                                            )
        info_label.grid(row=0, column=0, padx=10, pady=10,
                        sticky='nsew')
        
        self.progress = customtkinter.DoubleVar()
        self.progressbar = customtkinter.CTkProgressBar(self.top_level,
                                                        height=height_bar,
                                                        mode='determinate',
                                                        variable=self.progress,
                                                        )
        self.progressbar.grid(row=1, column=0, padx=10, pady=10,
                              sticky='nsew')
        
        closeimage = customtkinter.CTkImage(Image.open(os_path.join('files', 'assets', 'close.png')),
                                            size = (self.IMAGE_SIZE[0]//2,
                                                    self.IMAGE_SIZE[1]//2))
        
        self.cancel_button = customtkinter.CTkButton(master=self.top_level,
                                                     text='',
                                                     image=closeimage,
                                                     )
        self.cancel_button.grid(row=2, column=0, padx=10, pady=10,)
        self.cancel_button.configure(border_color='red', border_width=5)
        
        self.top_level.bind('<Return>', self.on_cancel)
        
        self.fill_progress()
    
    def fill_progress(self) -> None:
        
        for iteration in range(51):
            value:float = iteration / 50
            self.progress.set(value)
            self.top_level.update()
            sleep(0.1)
            
        else:
            self.__send_sos__()
    
    def __send_sos__(self) -> None:
        headers:Dict[str, str] = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        
        payload:str = f'msg=Nececito ayuda urgentemente!!!'
        
        # try:
        #     request('POST',
        #             self.url,
        #             headers=headers,
        #             data=payload)
        
        # except:
        #     pass
        
        # playsound(os_path.join('files', 'assets', 'sos', 'sos.mp3'))
        self.on_close()        
        
    def on_close(self,) -> None:
        self.master.deiconify()
        self.top_level.destroy()
    
    def on_cancel(self, event) -> None:
        self.on_close()
        
    def close(self) -> None:
        self.top_level.destroy()