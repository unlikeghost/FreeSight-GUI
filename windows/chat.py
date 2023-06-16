import customtkinter
from typing import List, Dict
from os import path as os_path
from windows.__base__ import WindowBase


class KeyChat(customtkinter.CTkButton):
    
    def __init__(self, letters:List[str], *args, **kwargs) -> None:
        super(KeyChat, self).__init__(*args, **kwargs)
                
        self.clicks:int = 0
        self.letters:List[str] = letters
        self.configure(text=' '.join(self.letters))

    def on_click(self) -> str:
        self.clicks += 1
        
        if self.clicks > len(self.letters) - 1:
            self.clicks = 0
        
        return self.letters[self.clicks - 1]

    def on_change(self) -> None:
        self.clicks:int = 0


class ChatWindow(WindowBase):
    
    def __init__(self, master, ip_server:str,
                 port_server:int, api_url:str='api/v1/public/send-chat',
                 full_screen: bool = False) -> None:
        super().__init__(master, ip_server, port_server, api_url, full_screen)
        
        self.top_level.title('Free Sight Chat')
        
        if full_screen:
            font:tuple = ('Arial', 85)
            font_text:tuple = ('Arial', 120)
        else:
            font:tuple = ('Arial', 30)
            font_text:tuple = font
        
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(2, weight=1)
        self.top_level.iconbitmap(os_path.join('files',
                                               'assets', 'icon.ico'))
        
        key_board = {
            1: ['1', ',', '.'],
            2:['2', 'a', 'b', 'c'],
            3:['3', 'd', 'e', 'f'],
            4:['4', 'g', 'h', 'i'],
            5:['5', 'j', 'k', 'l'],
            6:['6', 'm', 'n', 'o'],
            7:['7', 'p', 'q', 'r', 's'],
            8:['8', 't', 'u', 'v'],
            9:['9', 'w', 'x', 'y', 'z'],
            10:['0', '!', '?'],
            11:['Espacio'],
            12:['Enviar'],
            13:['Borrar'],
            14:['Salir']
        }
        
        self.key_mapping:Dict[str, customtkinter.CTkButton] = {}
        
        ## Frame del texto
        self.text_frame = customtkinter.CTkFrame(self.top_level)
        self.text_frame.grid(row=0, column=0, pady=10, sticky='nsew', columnspan=2)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_box = customtkinter.CTkEntry(self.text_frame,
                                               font=font_text,
                                               placeholder_text='Escriba aquí')
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.text_box.focus_force()
        
        ## Frame del teclado
        self.keyboard_frame = customtkinter.CTkFrame(self.top_level)
        self.keyboard_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        
        self.keyboard_frame.grid_columnconfigure(tuple(range(3)), weight=1)
        self.keyboard_frame.grid_rowconfigure(tuple(range(4)), weight=1)
        
        ##Frame de las acciones
        self.actions_frame = customtkinter.CTkFrame(self.top_level)
        self.actions_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew',
                                rowspan=4)
        self.actions_frame.grid_rowconfigure(0, weight=1)
        
        for key in key_board:
            if key < 11:
                self.key_mapping[key] = KeyChat(key_board[key],
                                                master=self.keyboard_frame,
                                                font=font,
                                                )
                row:int = (key - 1) // 3
                column:int = (key - 1) % 3
                columnspan:int = 1
            
            elif key == 11:
                self.key_mapping[key] = KeyChat(key_board[key],
                                                master=self.keyboard_frame,
                                                font=font,
                                                )
                row:int = (key - 1) // 3
                column:int = (key - 1) % 3
                columnspan:int = 2

            else:
                self.key_mapping[key] = KeyChat(key_board[key],
                                                master=self.actions_frame,
                                                font=font)
                row:int = key - 12
                column:int = 0
                columnspan:int = 1
            
            self.key_mapping[key].grid(row=row, column=column,
                                       padx=10, pady=10, sticky='nsew',
                                       columnspan=columnspan)
        
        self.key_mapping[1].configure(border_color='red', border_width=5)
        
        self.text:str = ''
        self.current_key_index:int = 1
        
        self.top_level.bind('<Left>', self.switch_button)
        self.top_level.bind('<Right>', self.switch_button)
        self.top_level.bind('<Return>', self.select_key)
        self.key_changed:bool = False

    def switch_button(self, event) -> None:
        
        len_keys = len(self.key_mapping)
        
        if event.keysym == 'Right':
            self.current_key_index:int = self.current_key_index + 1 if self.current_key_index < len_keys else 1
            prev_index_key:int = self.current_key_index - 1 if self.current_key_index > 1 else len_keys
            
        elif event.keysym == 'Left':
            self.current_key_index:int = self.current_key_index - 1 if self.current_key_index > 1 else len_keys
            prev_index_key:int = self.current_key_index + 1 if self.current_key_index < len_keys else 1
              
        self.key_mapping[prev_index_key].configure(border_color='', border_width=0)
        self.key_mapping[self.current_key_index].configure(border_color='red', border_width=5)
        self.key_changed:bool = True
        self.key_mapping[self.current_key_index].on_change()
                
    def select_key(self, _) -> None:
        value = self.key_mapping[self.current_key_index].on_click()
        
        if value == 'Borrar':
            self.text:str = self.text[:-1] if len(self.text) > 0 else ''
            self.__write_text__()
        
        elif value == 'Enviar':
            self.__send_text__()
            
        elif value == 'Espacio':
            self.text += ' '
            self.__write_text__()
        
        elif value == 'Salir':
            self.__on_close__()
        
        else:
            if self.key_changed == False:
                self.text = self.text[:-1] if len(self.text) > 0 else ''
                self.text += value
                self.__write_text__()
            else:
                self.text += value
                self.__write_text__()
                self.key_changed:bool = False
    
    def __write_text__(self) -> None:
        self.text_box.delete(0,'end')
        self.text_box.insert(0, self.text)
    
    def __send_text__(self) -> None:
        payload:str = f'msg={self.text}'
        self.http_post(self.url, payload)
        self.text:str = ''
        self.__write_text__()    
    
    
if __name__ == '__main__':
    root = customtkinter.CTk()
    root.title('Free Sight Chat Demo')
    root.attributes('-fullscreen', False)
    root.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
    
    root.iconify()
    
    chat = ChatWindow(root, '127.0.0.1', 8080,
                      full_screen=False)
    
    root.mainloop()