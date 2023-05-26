import customtkinter
from PIL import Image
from typing import List, Dict
from os import path as os_path
from requests import request
from string import ascii_uppercase as letters
from CTkMessagebox import CTkMessagebox


class ChatWindow:
    def __init__(self, master, ip_server:str, port_server:int,
                 full_screen:bool=False) -> None:
        
        self.top_level = customtkinter.CTkToplevel(master)
        self.master = master
        self.top_level.title('Free Sight Chat')
        # self.top_level.geometry(f'{width}x{height}')
        self.top_level.protocol('WM_DELETE_WINDOW', self.on_close)
        self.top_level.focus_force()
        
        self.url:str = f'http://{ip_server}:{port_server}/api/v1/public/send-chat'
        
        if full_screen:
            self.top_level.attributes('-fullscreen', True)
            height:int = self.top_level.winfo_screenwidth()
            width:int = self.top_level.winfo_screenheight()
            self.IMAGE_SIZE = (width - 155,
                               (height // 3)-35)
            font:tuple = ('Arial', 85)
            font_text:tuple = ('Arial', 120)
        else:
            width:int = 600
            height:int = 800
            self.IMAGE_SIZE = ((width // 2)-35,
                            (height // 3)-35)
            font:tuple = ('Arial', 30)
            font_text:tuple = font
        
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(2, weight=1)
        
        self.top_level.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
        
        keys:List[str] = [f'{i}' for i in range(10)]
        keys.extend(letters)
        keys.extend(['Espacio', 'Enviar\n(Salir)', 'Borrar'])
        
        self.letters_mapping:Dict[int, str] = {index:app for index, app in enumerate(keys)}
        
        self.text_frame = customtkinter.CTkFrame(self.top_level)
        self.text_frame.grid(row=0, column=0, pady=10, sticky='nsew')
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        
        self.numbers_frame = customtkinter.CTkFrame(self.top_level)
        self.numbers_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        self.letters_frame = customtkinter.CTkFrame(self.top_level)
        self.letters_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        
        self.actions_frame = customtkinter.CTkFrame(self.top_level)
        self.actions_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew',
                                rowspan=3)
        self.actions_frame.grid_rowconfigure(0, weight=1)
        
        self.text_box = customtkinter.CTkEntry(self.text_frame,
                                               font=font_text,
                                               placeholder_text='Escriba aquí')
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.text_box.focus_force()
                                              
        self.key_mapping:Dict[str, customtkinter.CTkButton] = {}
        
        letters_row:int = 0
        letters_column:int = 0
        actions_row:int = 0
        for number_button in self.letters_mapping:
            
            if number_button <= 9:
                
                self.key_mapping[number_button] = customtkinter.CTkButton(self.numbers_frame,
                                                                        text=number_button,
                                                                        font=font,
                                                                        )
                
                row:int = 0
                column:int = number_button
                columnspan:int = 1

                
            elif number_button <= len(keys) - 4 and number_button  > 9:
            
                self.key_mapping[number_button] = customtkinter.CTkButton(self.letters_frame,
                                                                          text=keys[number_button],
                                                                          font=font,
                                                                          )
                
                column:int = letters_column
                row:int = letters_row
                columnspan:int = 1
                
                letters_column = letters_column + 1 if letters_column < 9 else 0
                letters_row = letters_row + 1 if letters_column == 0 else letters_row
            
            elif number_button == len(keys) - 3:
                
                self.key_mapping[number_button] = customtkinter.CTkButton(self.letters_frame,
                                                                          text=keys[number_button],
                                                                          font=font,
                                                                          )
                
                row:int =  letters_row + 1
                column:int = 0
                columnspan:int = 10
            
            elif number_button > len(keys) - 4:

                self.key_mapping[number_button] = customtkinter.CTkButton(self.actions_frame,
                                                                          text=keys[number_button],
                                                                          font=font,
                                                                          )
                
                row:int = actions_row
                column:int = 0
                
                actions_row += 1
            
            self.key_mapping[number_button].grid(row=row, column=column, padx=10, pady=10, sticky='nsew',
                                                 columnspan=columnspan)

        self.key_mapping[10].configure(border_color='red', border_width=5)
                
        self.top_level.bind('<Left>', self.switch_button)
        self.top_level.bind('<Right>', self.switch_button)
        self.top_level.bind('<Return>', self.select_key)
        
        self.current_index_key:int = 10
        self.current_key:str = self.letters_mapping[self.current_index_key]
        
        self.text:str = ''
    
    def switch_button(self, event) -> None:
        
        len_keys = len(self.key_mapping)
        
        if event.keysym == 'Right':
            self.current_index_key:int = self.current_index_key + 1 if self.current_index_key < (len_keys - 1) else 0
            prev_index_key:int = self.current_index_key - 1 if self.current_index_key > 0 else len_keys - 1

        if event.keysym == 'Left':
            self.current_index_key:int = self.current_index_key - 1 if self.current_index_key > 0 else len_keys - 1
            prev_index_key:int = self.current_index_key + 1 if self.current_index_key < (len_keys - 1) else 0
        
        self.key_mapping[prev_index_key].configure(border_color='', border_width=0)
        self.key_mapping[self.current_index_key].configure(border_color='red', border_width=5)
        
        self.current_key:str = self.letters_mapping[self.current_index_key]
    
    def select_key(self, _) -> None:
        
        if self.current_key == 'Borrar':
            self.text:str = self.text[:-1] if len(self.text) > 0 else ''
            self.__write_text__()

        elif self.current_key == 'Espacio':
            self.text += ' '
            self.__write_text__()
        
        elif self.current_key == 'Enviar\n(Salir)':
            self.__send_text__()
        
        else:
            self.text += self.current_key
            self.__write_text__()
    
    def __write_text__(self) -> None:
        self.text_box.delete(0,'end')
        self.text_box.insert(0, self.text)
    
    def __send_text__(self) -> None:
        
        headers:Dict[str, str] = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        
        payload:str = f'msg={self.text}'

        response = request('POST',
                           self.url,
                           headers=headers,
                           data=payload)
        
        if response.status_code == 200:
            
            self.on_close()
        
        else:
            CTkMessagebox(title='Error', 
                          message='No se puede acceder al servidor, verifique su coneccion a internet',
                          icon='cancel')
                
    def on_close(self) -> None:
        self.top_level.destroy()
        self.master.deiconify()
    
    def close(self) -> None:
        self.top_level.destroy()