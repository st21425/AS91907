from tkinter import *

class GUI():
    def __init__(self):
        self.root = Tk()
        self.root.title("Rogue Roller")
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.transparent_color = "#aabbcc"
        self.root.wm_attributes('-transparentcolor', self.transparent_color)

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

        self.font = "Cascadia-code  12"
        self.large_font = "Copperplate_Gothic 30"

        self.frames = {}
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["GameMenu"] = self.game()

        self.font = "Arial 16"
        self.large_font = "Arial 30"

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

        self.title_label = Label(frame, font =self.large_font, text = "Rogue Roller", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: self.show_frames("GameMenu"))
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=self.quit)
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    
    def shop(self):
        frame = Frame(self.container)
        return frame
    
    def game(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        sidebar_frame = self.sidebar(frame)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")

        game_frame = self.game_content(frame)
        game_frame.grid(row=0, column=1, sticky="nsew")


        


        return frame
    
    def sidebar(self, master):
        frame = Frame(master, width=600)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.sidebar_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        ####### PLACEHOLDERS #######
        self.requirement = 300 
        self.score = 1000
        self.mult = 1
        self.total = 1000

        self.requirement_label = Label(frame, font = self.font, text = f"Requirement: {self.requirement}", bg=self.sidebar_colour, fg=self.sidebar_text)
        self.requirement_label.grid(padx=100, pady=10, sticky=EW)

        self.total_label = Label(frame, font = self.font, text = f"Total: {self.total}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.total_label.grid(padx=75, pady=5, sticky=EW)

        self.scoring_label = Label(frame, font = self.font, text = f"{self.score} X {self.mult}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=75, pady=5, sticky=EW)

        self.shop_button = Button(frame, text="Shop", bg=self.sidebar_box_colour, fg=self.sidebar_text, font=self.font, command=lambda: self.show_frames("ShopMenu"))
        self.shop_button.grid(padx=75, pady=15, sticky=EW)

        self.menu_button = Button(frame, text="Menu", bg=self.sidebar_box_colour, fg=self.sidebar_text, font=self.font, command=lambda: self.show_frames("MainMenu"))
        self.menu_button.grid(padx=75, pady=15, sticky=EW)

        return frame
    
    def game_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(2)), weight=1)

        self.dice_image = PhotoImage(file="green_dice1.png")

        for x in range(3):
            for y in range(2):
                dice_button = Button(frame, image=self.dice_image)
                dice_button.grid(row=x, column=y)

        for x in range(3):
            for y in range(2):
                dice_button = Label(frame, text=f"{x}{y}", fg="white",font=self.font, bg=self.transparent_color, width=10, height=5)
                dice_button.grid(row=x, column=y)
        

        return frame
    
    def run(self):
        self.root.mainloop()
    def quit(self):
        self.root.destroy()

GAME_RUNNING = GUI()
GAME_RUNNING.run()