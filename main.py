#region imports
import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BACKGROUND_COLOR = "#19233c"
#endregion 

#region app
class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__(fg_color = BACKGROUND_COLOR)
        self.geometry(f"850x500")
        self.title(" Compound interest calculator")
        self.ChangeTitleBar()

        # function
        self.CreateFrames()

        # protocol
        self.protocol("WM_DELETE_WINDOW", self.Destroy)
    
    def CreateFrames(self) -> None:
        '''Creates frames for the app'''
        self.input_frame = InputFrame(self)
        self.input_frame.place(relx = 0, rely = 0, relwidth = 0.4, relheight = 1)
        self.visual_frame = VisualFrame(self)
        self.visual_frame.place(relx = 0.4, rely = 0, relwidth = 0.6, relheight = 1)

    def Destroy(self) -> None:
        '''Handles exiting application'''
        self.destroy()
        self.quit()

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
#endregion

#region input frame
class InputFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius = 0, fg_color = BACKGROUND_COLOR, **kwargs)

        self.rowconfigure((0, 1, 2, 3, 4), weight = 1, uniform = "a")
        self.columnconfigure(0, weight = 3, uniform = "a")
        self.columnconfigure(1, weight = 2, uniform = "a")

        self.InitialWidgets()
        self.ContributionWidgets()
        self.TimeWidgets()
        self.InterestWidgets()

        # need to program function
        self.calculate_button = ctk.CTkButton(
            self,
            text = "Calculate",
            font = ("Helvetica", 15, "bold")
        )
        self.calculate_button.grid(row = 4, column = 0, columnspan = 2, pady = (10, 0))

    def InitialWidgets(self) -> None:
        self.initial_label = ctk.CTkLabel(
            self,
            text = "Initial Investment $",
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

    def ContributionWidgets(self) -> None:
        self.weeklyContribution_label = ctk.CTkLabel(
            self,
            text = "Weekly contribution $",
            font = ("Helvetica", 15, "bold"),
            text_color = "white"
        )
        self.weeklyContribution_label.grid(row = 1, column = 0, sticky = "e", padx = (0, 5))

        self.weeklyContribution_entry = ctk.CTkEntry(
            self,
            font = ("Helvetica", 15),
            width = 100,
            height = 30,
            state = "normal"
        )
        self.weeklyContribution_entry.grid(row = 1, column = 1, sticky = "w", padx = (5, 0))

    def TimeWidgets(self) -> None:
        self.time_label = ctk.CTkLabel(
            self,
            text = "Years invested",
            font = ("Helvetica", 15, "bold"),
            text_color = "white"
        )
        self.time_label.grid(row = 2, column = 0, sticky = "e", padx = (0, 5))

        self.time_entry = ctk.CTkEntry(
            self,
            font = ("Helvetica", 15),
            width = 100,
            height = 30,
            state = "normal"
        )
        self.time_entry.grid(row = 2, column = 1, sticky = "w", padx = (5, 0))

    def InterestWidgets(self) -> None:
        self.interest_label = ctk.CTkLabel(
            self,
            text = "Est interest rate %",
            font = ("Helvetica", 15, "bold"),   
            text_color = "white"
        )
        self.interest_label.grid(row = 3, column = 0, sticky = "e", padx = (0, 5))

        self.interest_entry = ctk.CTkEntry(
            self,
            font = ("Helvetica", 15),
            width = 100,
            height = 30,
            state = "normal"
        )
        self.interest_entry.grid(row = 3, column = 1, sticky = "w", padx = (5, 0))
#end region

#region visual frame
class VisualFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius = 0, fg_color = BACKGROUND_COLOR, **kwargs)

        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(figsize = (5, 5), dpi = 100)

        # theme
        self.fig.patch.set_facecolor(BACKGROUND_COLOR)  
        self.ax.set_facecolor(BACKGROUND_COLOR)
        self.ax.grid(True, linestyle="--", alpha=0.15, color="white")
        for spine in self.ax.spines.values():
            spine.set_color("#2d3a5f")

        self.PlotEmptyGraph()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def PlotEmptyGraph(self) -> None:
        """Sets up a clean, empty placeholder state for the graph."""
        self.ax.clear()
        
        # Set titles and labels
        self.ax.set_title(
            "Investment Growth Over Time", 
            fontname = "Helvetica", 
            fontsize = 14, 
            weight = "bold", 
            pad = 15
        )
        self.ax.set_xlabel(
            "Years", 
            fontname = "Helvetica", 
            fontsize = 11, 
            labelpad = 8)
        self.ax.set_ylabel(
            "Total Balance ($)", 
            fontname = "Helvetica", 
            fontsize = 11, 
            labelpad = 8)

        # Set placeholder limits so it looks like a real chart graph frame
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 1000)

#end region

if __name__ == "__main__":  
    app = App()
    app.mainloop()
