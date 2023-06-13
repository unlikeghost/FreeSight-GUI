import customtkinter
from PIL import Image
from time import sleep
from os import path as os_path


class NoImplementedWindow:
    def __init__(self, master,
                 full_screen:bool=False
                 ) -> None:
        
        self.top_level = customtkinter.CTkToplevel(master)
        self.master = master
        self.top_level.title('Free Sight :(')
        self.top_level.protocol('WM_DELETE_WINDOW', self.on_close)
        self.top_level.focus_force()
        
        if full_screen:
            self.top_level.attributes('-fullscreen', True)
            height:int = self.top_level.winfo_screenwidth()
            width:int = self.top_level.winfo_screenheight()
            self.IMAGE_SIZE = ((width // 3)-35,
                               (height // 3)-35)
            font:tuple = ('Arial', 70)
            height_bar:int = 100
            
        else:
            width:int = 600
            height:int = 800
            self.IMAGE_SIZE = ((width // 2)-35,
                            (height // 3)-35)
            font:tuple = ('Arial', 30)
            height_bar:int = 40
        
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(1, weight=1)
        
        info_label = customtkinter.CTkLabel(self.top_level,
                                            text='Feature no implementada aun,\nespere la barra de progreso para cerrar ventana',
                                            font=font,
                                            )
        info_label.grid(row=0, column=0, padx=10, pady=10,
                        sticky='nsew')
        
        cat_image_path:str = os_path.join('files', 'assets', 'apps', 'NoImplementedWindow.png')
            
        cat_image = customtkinter.CTkImage(Image.open(cat_image_path),
                                           size=self.IMAGE_SIZE)
        
        cat_label = customtkinter.CTkLabel(self.top_level,
                                            text='',
                                            image=cat_image
                                            )
        cat_label.grid(row=1, column=0, padx=10, pady=10,
                       sticky='nsew')
        
        self.progress = customtkinter.DoubleVar()
        self.progressbar = customtkinter.CTkProgressBar(self.top_level,
                                                        height=height_bar,
                                                        mode='determinate',
                                                        variable=self.progress,
                                                        )
        self.progressbar.grid(row=2, column=0, padx=10, pady=10,
                              sticky='nsew')
    
        self.fill_progress()
    
    def fill_progress(self) -> None:
        
        for iteration in range(31):
            value:float = iteration / 30
            self.progress.set(value)
            self.top_level.update()
            sleep(0.1)
        
        self.on_close()
    
    def on_close(self,) -> None:
        self.master.deiconify()
        self.top_level.destroy()