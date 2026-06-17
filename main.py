#region imports
import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import numpy as np
import quirks

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

        # data
        self.initial_investment = ctk.StringVar(value = "0")
        self.weekly_contribution = ctk.StringVar(value = "0")
        self.years_invested = ctk.StringVar(value = "0")
        self.interest_rate = ctk.StringVar(value = "0")

        self.year_list: list[int] = []
        self.balance_list: list[float] = []
        self.contribution_list: list[float] = []

        # function
        self.CreateFrames()

        # protocol
        self.bind("<Return>", lambda event: self.Calculate())
        self.protocol("WM_DELETE_WINDOW", self.Destroy)
    
    def CreateFrames(self) -> None:
        '''Creates frames for the app'''
        self.input_frame = InputFrame(
            self, 
            self.initial_investment, 
            self.weekly_contribution, 
            self.years_invested, 
            self.interest_rate
        )
        self.input_frame.place(relx = 0, rely = 0, relwidth = 0.4, relheight = 1)
        self.visual_frame = VisualFrame(self)
        self.visual_frame.place(relx = 0.4, rely = 0, relwidth = 0.6, relheight = 1)

    def Calculate(self) -> None:
        '''Calculates the compound interest and updates the lists of years, total balance, and contributions'''
        try:
            initial = float(self.initial_investment.get())
            contribution = float(self.weekly_contribution.get())
            months = int(float(self.years_invested.get()) * 12)
            interest_rate = float(self.interest_rate.get()) / 100

            if months <= 0:
                raise ValueError("Years invested must be greater than 0.")
            
        except ValueError as e:
            self.year_list = []
            self.balance_list = []
            self.contribution_list = []
            self.visual_frame.PlotEmptyGraph()
            self.input_frame.output_label.configure(text = str(e))
            return
        
        total_balance = initial
        total_contributions = initial

        monthly_contribution = contribution * (52 / 12)
        monthly_interest_rate = interest_rate / 12

        # initial values
        self.year_list = [0.0]
        self.balance_list = [round(total_balance, 2)]
        self.contribution_list = [round(total_contributions, 2)]

        for month in range(1, months + 1):
            # calculate interest for the month and add contribution
            interest_earned = total_balance * monthly_interest_rate
            total_balance += interest_earned + monthly_contribution
            total_contributions += monthly_contribution

            # log data
            if month % 12 == 0 or month == months:
                if(total_contributions < 0):
                    total_contributions = 0

                if(total_balance < 0):
                    total_balance = 0

                current_year = month / 12
                self.year_list.append(current_year)
                self.balance_list.append(round(total_balance, 2))
                self.contribution_list.append(round(total_contributions, 2))
        
        self.visual_frame.PlotGraph(self.year_list, self.contribution_list, self.balance_list)

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
    def __init__(self, master, initial_investment: str, weekly_contribution: str, 
                 years_invested: str, interest_rate: str, **kwargs):
        # frame setup
        super().__init__(master, corner_radius = 0, fg_color = BACKGROUND_COLOR, **kwargs)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight = 1, uniform = "a")
        self.rowconfigure(9, weight = 2, uniform = "a")
        self.columnconfigure(0, weight = 3, uniform = "a")

        self.font = ("sans-serif", 15, "bold")
        self.vcmd = (self.register(quirks.CheckIfFloat), '%P')

        # create widgets
        input_configs = [
            {"label": "Initial Investment $", "var": initial_investment, "row": 0},
            {"label": "Weekly contribution $", "var": weekly_contribution,"row": 2},
            {"label": "Years invested", "var": years_invested, "row": 4},
            {"label": "Est interest rate %", "var": interest_rate, "row": 6}
        ]

        for config in input_configs:
            self.LabelCreator(config["label"], config["row"])
            self.EntryCreator(config["var"], config["row"] + 1)

        self.ModifiableWidgets(master)
    
    def ModifiableWidgets(self, master) -> None:
        '''Creates widgets that will be called'''
        self.calculate_button = ctk.CTkButton(
            self,
            text = "Calculate",
            font = self.font,
            command = master.Calculate
        )
        self.calculate_button.grid(row = 8, column = 0, columnspan = 2, pady = (10, 0))

        self.output_label = self.LabelCreator("", 9)

    def LabelCreator(self, text: str, row: int) -> ctk.CTkLabel:
        '''Creates a label with consistent styling'''
        label = ctk.CTkLabel(
            self,
            text = text,
            font = self.font,
            text_color = "white"
        )
        label.grid(row = row, column = 0, sticky = "nsew", padx = (5, 5))

        return label

    def EntryCreator(self, text_variable: str, row: int) -> None:
        '''Creates an entry with consistent styling'''
        entry = ctk.CTkEntry(
            self,
            font = self.font,
            width = 200,
            height = 35,
            state = "normal",
            textvariable = text_variable,
            validate = "key",         
            validatecommand = self.vcmd
        )
        entry.grid(row = row, column = 0, columnspan = 2, sticky = "ew", padx = (5, 0))
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

        # data containers
        self.years_data = []
        self.balance_data = []
        self.contribution_data = []

        self.annotation_box = self.ax.annotate(
            "", xy = (0, 0), xytext = (10, 10),
            textcoords = "offset points",
            bbox = dict(boxstyle = "round,pad=0.5", fc = "#1e2942", ec = "#2d3a5f", alpha = 0.95),
            color = "white", 
            fontname = "sans-serif",
            fontsize = 9,
            arrowprops = dict(arrowstyle = "->", color = "#98c379")
        )
        self.annotation_box.set_visible(False)

        self.PlotEmptyGraph()
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.get_tk_widget().pack(fill = "both", expand = True, padx = 10, pady = 10)
        self.canvas.mpl_connect("motion_notify_event", self.OnHover)

    def ApplyGraphStyling(self) -> None:
        '''Applies consistent styling to the graph, including titles, labels, and grid.'''
        self.ax.set_title(
            "Investment Growth Over Time", 
            fontname = "sans-serif", 
            fontsize = 14, 
            weight = "bold", 
            pad = 15
        )
        self.ax.set_xlabel(
            "Years", 
            fontname = "sans-serif", 
            fontsize = 11, 
            labelpad = 8
        )
        self.ax.set_ylabel(
            "Total Balance ($)", 
            fontname = "sans-serif", 
            fontsize = 11, 
            labelpad = 8
        )

        # spine and grid styling
        self.fig.subplots_adjust(left=0.18)
        self.ax.yaxis.set_major_formatter(FuncFormatter(quirks.FinancialFormat))
        self.ax.grid(True, linestyle="--", alpha=0.15, color="white")
        for spine in self.ax.spines.values():
            spine.set_color("#2d3a5f")

    def PlotEmptyGraph(self) -> None:
        '''Leaves the graph in placeholder state'''
        self.ax.clear()
        self.ApplyGraphStyling()
        
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 1000)
    
    def PlotGraph(self, years: list[float], contribution: list[float], balance: list[float]) -> None:
        '''Plots the graph with the provided data'''
        self.years_data = years
        self.balance_data = balance
        self.contribution_data = contribution

        self.ax.clear()
        self.ApplyGraphStyling()

        self.annotation_box = self.ax.annotate(
            "", xy = (0, 0), xytext = (10, 10),
            textcoords = "offset points",
            bbox = dict(boxstyle = "round,pad=0.5", fc = "#1e2942", ec = "#2d3a5f", alpha = 0.95),
            color = "white", 
            fontname = "sans-serif",
            fontsize = 9,
            arrowprops = dict(arrowstyle = "->", color = "#98c379")
        )
        self.annotation_box.set_visible(False)

        # plots contributions and balance with distinct colors and styles
        self.ax.plot(
            years, 
            contribution, 
            color = "#e06c75", 
            linestyle = "--",
            linewidth = 2, 
            label = "Total Principal"
        )

        self.ax.plot(
            years, 
            balance, 
            color = "#98c379", 
            linewidth = 3, 
            label = "Total Value"
        )

        if years:
            self.ax.set_xlim(0, max(years))
            self.ax.set_ylim(0, max(balance) * 1.1)

        self.ax.legend(loc = "upper left", frameon = False, prop = {"family": "sans-serif", "size": 10})
        self.canvas.draw()

    def OnHover(self, event) -> None:
        '''Displays the annotation box with details when hovering over the graph.'''
        
        # ensures data exists
        if not self.years_data or event.inaxes != self.ax or event.xdata is None:
            if self.annotation_box.get_visible():
                self.annotation_box.set_visible(False)
                self.canvas.draw_idle()
            return

        try:
            # update annotation position
            index = np.argmin(np.abs(np.array(self.years_data) - event.xdata))
            
            target_x = self.years_data[index]
            target_y = self.balance_data[index]
            self.annotation_box.xy = (target_x, target_y)

            canvas_width = self.canvas.get_width_height()[0]
            if event.x > (canvas_width * 0.65):
                offset_x = -130
            else:
                offset_x = 10

            y_axis_ceiling = self.ax.get_ylim()[1]
            if target_y > (y_axis_ceiling * 0.80):
                offset_y = -90  
            else:
                offset_y = 10

            self.annotation_box.set_position((offset_x, offset_y))

            # format message
            year_text = f"Year {target_x:.1f}" if target_x % 1 != 0 else f"Year {int(target_x)}"
            text = (
                f"{year_text}\n"
                f"───────────────────\n"
                f"Total Value: ${target_y:,.2f}\n"
                f"Principal: ${self.contribution_data[index]:,.2f}" 
            )
            
            self.annotation_box.set_text(text)
            self.annotation_box.set_visible(True)
            self.canvas.draw_idle()  
            
        except Exception as e:
            print(f"Error on hover execution: {e}")

#end region

if __name__ == "__main__":  
    app = App()
    app.mainloop()
