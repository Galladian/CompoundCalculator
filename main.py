import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int

class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__(fg_color = "#19233c")
        self.geometry(f"600x500")
        self.title(" Compound interest calculator")
        self.ChangeTitleBar()

        # function
        self.CreateFrames()
        self.mainloop()
    
    def CreateFrames(self) -> None:
        '''Creates frames for the app'''
        self.input_frame = InputFrame(self)
        self.input_frame.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)
        self.visual_frame = VisualFrame(self)
        self.visual_frame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

    def ChangeTitleBar(self) -> None:
        '''Changes title bar colour. NOTE: Only works on windows'''
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = 0x003c2319 # BGR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            KeyError("Function not excuted properly")
            pass

class InputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius = 0, **kwargs)

        self.rowconfigure((0, 1, 2, 3), weight = 1, uniform = "a")
        self.columnconfigure((0, 1), weight = 1, uniform = "a")

        self.initial_label = ctk.CTkLabel(
            self,
            text = "Initial Investment: $",
            font = ("Helvetica", 15, "bold"),
            text_color = "white"
        )
        self.initial_label.grid(row = 0, column = 0, sticky = "e", padx = (0, 5))

        self.initial_entry = ctk.CTkEntry(
            self,
            font = ("Helvetica", 15),
            width = 100,
            height = 30,
            state = "normal"
        )
        self.initial_entry.grid(row = 0, column = 1, sticky = "w", padx = (5, 0))

class VisualFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius = 0, **kwargs)

if __name__ == "__main__":  
    App()