import customtkinter as ctk
try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = "#19233c")
        self.geometry(f"600x500")
        self.title(" Compound interest calculator")
        self.ChangeTitleBar()

        self.mainloop()

    def ChangeTitleBar(self) -> None:
        '''Changes title bar colour. NOTE: Only works on windows'''
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x003c2319
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            KeyError("Function not excuted properly")
            pass

if __name__ == "__main__":  
    App()