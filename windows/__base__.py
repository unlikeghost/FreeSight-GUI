import customtkinter
from typing import Dict
from os import path as os_path
from requests import request
from requests.exceptions import InvalidURL
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError


class WindowBase:
    """Clase base para las ventanas de la aplicación.
    """
    def __init__(self,
                 master,
                 ip_server:str, port_server:int, api_url:str,
                 full_screen:bool=False) -> None:
        
        self.master = master
        self.top_level = customtkinter.CTkToplevel()
        self.top_level.iconbitmap(os_path.join('files', 'assets', 'icon.ico'))
        self.top_level.focus_force()
        
        self.url:str = f'http://{ip_server}:{port_server}/{api_url}'
        
        self.top_level.protocol('WM_DELETE_WINDOW', self.__on_close__)
        self.top_level.attributes('-fullscreen', full_screen)
    
    def __on_close__(self) -> None:
        """Metodo que se ejecuta al cerrar la ventana.
        """
        self.top_level.destroy()
        self.master.deiconify()
    
    def http_post(self, url:str, payload:str,
         headers:Dict[str, str]={'Content-Type': 'application/x-www-form-urlencoded'}
         ) -> bool:
        """Metodo para enviar una peticion POST a un servidor.

        Args:
            url (str): URL del servidor.
            payload (str): Datos a enviar.
            headers (dict, optional): Headers para la peticion  Defaults to {'Content-Type': 'application/x-www-form-urlencoded'}.

        Returns:
            bool: True si la peticion fue exitosa, False en caso contrario.
        """
        try:
            request('POST', url, headers=headers,
                data=payload,
                timeout=0.5)
        
        except ConnectTimeout:return False
        
        except ConnectionError:return False
        
        except InvalidURL:return False
        
        else:return True