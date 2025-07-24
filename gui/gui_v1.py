from tkinter import *

class GUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Rogue Roller")
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.state('zoomed')#open window in fullscreen

        self.container = Frame(self.root)
        self.container.grid(row = 0, column = 0, sticky = "nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.button_colour = "#B6AADD"
        self.bg_colour = "#746aff"
        self.sidebar_colour = "#46444D"
        self.sidebar_box_colour = "#5A5A6D"
        self.sidebar_text = "#FFFFFF"

        self.frames = {}
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["GameMenu"] = self.game()
        self.frames["Sidebar"] = self.sidebar()

        self.show_frames("MainMenu")
    
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def menu(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font = "Arial 30", text = "Rogue Roller", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font="Arial 12", command=lambda: self.show_frames("GameMenu"))
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font="Arial 12", command=self.quit)
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    
    def shop(self):
        frame = Frame(self.container)
        return frame
    
    def game(self):
        frame = Frame(self.container)
        
        sidebar = self.sidebar()
        sidebar.pack(side="left", fill="y")

        


        return frame
    
    def sidebar(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        ####### PLACEHOLDERS #######
        self.requirement = 300 
        self.score = 1000
        self.mult = 1
        self.total = 1000

        self.requirement_label = Label(frame, font = "Arial 12", text = f"Requirement: {self.requirement}", bg=self.bg_colour)
        self.requirement_label.grid(padx=1, pady=10, sticky=EW)

        self.scoring_label = Label(frame, font = "Arial 12", text = f"{self.score} X {self.mult}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=1, pady=10, sticky=EW)
        return frame
    
    def run(self):
        self.root.mainloop()
    def quit(self):
        self.root.destroy()

GAME_RUNNING = GUI()
GAME_RUNNING.run()