import customtkinter
from time import sleep
from os import path as os_path

class ClaibrateWindow:
    
    def __init__(self, headset, full_screen:bool=False) -> None:
        
        self.iter_for_calibration:int = 150
        
        self.headset = headset
        
        self.top_level = customtkinter.CTk()
        self.top_level.title('Free Sight Calibración de sujeto')
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
        
        self.top_level.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
        
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        
        calibration_label = customtkinter.CTkLabel(self.top_level,
                                                   text='Porfavor mantenga la vista en el centro de la pantalla',
                                                   font=font,
                                                   )
        calibration_label.grid(row=0, column=0, padx=10, pady=10,
                               sticky='nsew')
        
        self.progress = customtkinter.DoubleVar()
        self.progressbar = customtkinter.CTkProgressBar(self.top_level,
                                                        height=height_bar,
                                                        mode='determinate',
                                                        variable=self.progress,
                                                        )
        
        self.progressbar.grid(row=1, column=0, padx=10, pady=10,
                              sticky='nsew')
                
        self.top_level.protocol('WM_DELETE_WINDOW', self.close)
        
        # self.top_level.mainloop()

    def calibrate(self) -> float:
        
        self.x_start_sum:float = 0
        x_start_samples:float = 0
        
        for iteration in range(self.iter_for_calibration):
            ##PANTALLA DE CARGA
            value:float = iteration / self.iter_for_calibration
            self.progress.set(value)
            self.top_level.update()
            
            x_temp_sum, x_temp_samples = self.headset.calibrate_subject(self.x_start_sum, x_start_samples)
            self.x_start_sum += x_temp_sum
            x_start_samples += x_temp_samples
        
        return self.x_start_sum / self.iter_for_calibration  
        # return self.x_start_sum / self.iter_for_calibration
    
    def close(self) -> None:
        self.top_level.destroy()        