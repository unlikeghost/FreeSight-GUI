import customtkinter
from PIL import Image
from time import sleep
from os import path as os_path
from playsound import playsound
from windows.__base__ import WindowBase


class SOSWindow(WindowBase):
    def __init__(self, master, ip_server:str,
                 port_server:int, api_url:str='api/v1/public/send-chat',
                 full_screen:bool = False) -> None:
        super().__init__(master, ip_server, port_server, api_url, full_screen)
        
        self.top_level.title('Free Sight SOS')
        
        if full_screen:
            height:int = self.top_level.winfo_screenwidth()
            width:int = self.top_level.winfo_screenheight()
            self.IMAGE_SIZE:tuple = (width - 155,
                                     (height // 3)-35)
            font:tuple = ('Arial', 70)
            height_bar:int = 300
            
        else:
            width:int = 600
            height:int = 800
            self.IMAGE_SIZE:tuple = ((width // 2)-35,
                                     (height // 3)-35)
            font:tuple = ('Arial', 30)
            height_bar:int = 40
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
                
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
                                                    self.IMAGE_SIZE[1]//2)
                                            )
        
        
        self.cancel_button = customtkinter.CTkButton(master=self.top_level,
                                                     text='',
                                                     image=closeimage,
                                                     )
        self.cancel_button.grid(row=2, column=0, padx=10, pady=10,)
        self.cancel_button.configure(border_color='red', border_width=5)
        
        self.stop:bool = False
        self.top_level.bind('<Return>', self.__on_cacnel__)
        self.__fill_progress__()
        
    def __fill_progress__(self) -> None:
        for iteration in range(51):
            if self.stop:
                break
            value:float = iteration / 50
            self.progress.set(value)
            self.top_level.update()
            sleep(0.01)     
        else:
            self.__send_sos__()
        
        self.__on_close__()
        
    def __on_cacnel__(self, _) -> None:
        self.stop:bool = True
    
    def __send_sos__(self,) -> None:
        payload:str = f'msg=Nececito ayuda urgentemente!!!'
        self.http_post(self.url, payload)
        playsound(os_path.join('files', 'assets', 'sos', 'sos.mp3'))


if __name__ == '__main__':
    
    master = customtkinter.CTk()
    master.attributes('-fullscreen', True)
    chat = SOSWindow(master, '127.0.0.1', 8080,
                     full_screen=True)
                     
    master.mainloop()