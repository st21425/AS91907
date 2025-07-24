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

        self.frames = {}
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["GameMenu"] = self.game()

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

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font="Arial 12", command=lambda: self.show_frames("GameMenu"))
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    
    def shop(self):
        frame = Frame(self.container)
        return frame
    
    def game(self):
        frame = Frame(self.container)
        return frame
    
    def run(self):
        self.root.mainloop()
    
game  = GUI()
game.run()