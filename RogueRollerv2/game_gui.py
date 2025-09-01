#Version 2
#Rogue roller is a roguelike yahtzee game
#Version 1: There is dice rolling, locking, scoring, game rounds
#and a dice shop to buy new dice
#Verion 2: Changed the way dice images were loaded to have multiple colours
#also added new gui option upon winning allowing user to add a new dice to the shop
from tkinter import *
from tkinter import ttk
import json
from game_logic import Logic

class GUI():    
    def __init__(self):
        self.logic = Logic()
        self.logic.next_round()
        #start the gui
        self.root = Tk()
        self.root.title("Rogue Roller")
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.faces_to_make = IntVar()
        self.faces_to_make.set(1)

        self.played = [0,0,0,0,0,0]

        with open("dice_types.json", "r") as file: 
                self.dice_type_info = json.load(file)

        #load images
        self.dice_image = PhotoImage(file="clear.png")
        #self.locked_dice_image = PhotoImage(file="green_dice_locked1.png")
        self.locked_dice_image = PhotoImage(file="lock_dice.png")
        self.shop_dice_image = self.dice_image.subsample(2)

        #open window in fullscreen
        self.root.state('zoomed')

        #declare colours and fonts
        self.button_colour = "#B6AADD"
        self.bg_colour = "#746aff"
        self.sidebar_colour = "#46444D"
        self.sidebar_box_colour = "#5A5A6D"
        self.sidebar_text = "#FFFFFF"

        self.font = "Arial 16"
        self.large_font = "Arial 30"

        #create the containter
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        #make a column for the sidebar and main content
        self.container.columnconfigure(0, weight=0)
        self.container.columnconfigure(1, weight=1)

        #make the sidebar and put it in the first column of the container
        self.sidebar_frame = self.sidebar(self.container)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        #declare used frames
        self.frames = {}
        self.frames["GameMenu"] = self.game()
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["LossScreen"] = self.game_lose()
        self.frames["ReplaceDice"] = self.replace_dice()
        self.frames["AddDice"] = self.add_dice()
        self.frames["AddFaces"] = self.add_faces()

        self.show_frames("MainMenu")
        #self.show_frames("AddDice")
    #set up the show frame function
    def show_frames(self, container):

        for frame_name, frame_instance in self.frames.items():
            #hide all frames
            frame_instance.grid_remove()

        #make the correct frame
        frame_to_show = self.frames[container]

        if container in ["MainMenu", "LossScreen", "AddDice", "AddFaces"]:
            #for the menus we hide the sidebar and show only the menu
            self.sidebar_frame.grid_remove()
            frame_to_show.grid(row=0, column=0, sticky="nsew", columnspan=2)
            frame_to_show.tkraise()
        else:
            #anythinhg else shows the sidebar and content
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            frame_to_show.grid(row=0, column=1, sticky="nsew")
            frame_to_show.tkraise()
    #create the main menu
    def menu(self):
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font =self.large_font, text = "Rogue Roller", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: [self.gui_reset(), self.update_sidebar(), self.show_frames("GameMenu"), self.sync_dice_buttons()])
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=lambda: self.quit())
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    #make the shop menu
    def shop(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        dice_frame = self.current_dice(frame)
        dice_frame.grid(row=0, column=1, sticky="nsew")

        shop_frame = self.shop_content(frame)
        shop_frame.grid(row=1, column=1, sticky="nsew")

        return frame
    #make the game menu
    def game(self):
        self.update_sidebar()
        #Declare values
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)

        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        game_frame = self.game_content(frame)
        game_frame.grid(row=0, column=1, sticky="nsew")

        return frame
    #make the game over menu
    def game_lose(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font =self.large_font, text = "Game Over", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: [self.gui_reset(), self.update_sidebar(), self.show_frames("GameMenu")])
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=lambda: self.quit())
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    #make the sidebar
    def sidebar(self, master):
        frame = Frame(master, width=600)
        frame.configure(bg=self.sidebar_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        ####### PLACEHOLDERS #######
        self.score = 0
        self.mult = 0
        self.round_requirement = 0
        self.total = 0
        self.money = 0
        self.max_hands = 5

        #make the labels for the sidebar
        self.requirement_label = Label(frame, font = self.font, text = f"Requirement: {self.round_requirement}", bg=self.sidebar_colour, fg=self.sidebar_text)
        self.requirement_label.grid(padx=100, pady=10, sticky=EW)

        self.total_label = Label(frame, font = self.font, text = f"Total: {self.total}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.total_label.grid(padx=75, pady=5, sticky=EW)

        self.scoring_label = Label(frame, font = self.font, text = f"Remaining Hands: {self.max_hands}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=75, pady=5, sticky=EW)

        self.money_label = Label(frame, font=self.font, text=f"Money: {self.money}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.money_label.grid(padx=75, pady=5, sticky=EW)

        self.menu_button = Button(frame, text="Menu", bg=self.sidebar_box_colour, fg=self.sidebar_text, font=self.font, command=lambda: self.show_frames("MainMenu"))
        self.menu_button.grid(padx=75, pady=15, sticky=EW)

        return frame
    #content of the game menu
    def game_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(3)), weight=1)

        self.dice_buttons = []
        self.update_sidebar()

        #make the dice in a 2x3 grid
        for y in range(2):
            for x in range(3):
                dice_type = self.dice["die" + str(x + 1 + y*3)]["type"]
                bg_colour = self.dice_type_info[dice_type]["colour"]
                self.dice_button = Button(frame, image=self.dice_image, text=self.played[x + y*3], bg=bg_colour, font=self.large_font, compound=CENTER, borderwidth=0, command=lambda value=(x +1 + y*3): self.toggle_dice(value))
                self.dice_button.grid(row=y, column=x, padx=100)
                self.dice_buttons.append(self.dice_button)
        
        play_button = Button(frame, text="Play Hand", bg=self.button_colour, font=self.large_font, compound=CENTER, borderwidth=0, command=lambda: self.play_turn())
        play_button.grid(row=2, column=1)
        
        return frame
    #makes the content for the new dice in the shop
    def shop_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(7)), weight=1)
        
        self.shop_label = Label(frame, font =self.large_font, text = "Shop", bg=self.bg_colour)
        self.shop_label.grid(padx=1, pady=15,sticky = NSEW, row=2, columnspan=7)

        self.items_in_shop = self.logic.new_shop_dice()
        self.shop_dice_buttons = []
        i = 0
        for item in self.items_in_shop:
            dice_type = item["type"]
            bg_colour = self.dice_type_info[dice_type]["colour"]
            self.shop_dice_button = Button(frame, text=f"{item['name']} \nCost: {item['cost']}", bg=bg_colour, font=self.font, compound=CENTER, borderwidth=0, image=self.dice_image, command=lambda value=i: self.buy_dice(value)
            )
            self.shop_dice_button.grid(row=3, column=i, padx=10)
            self.shop_dice_buttons.append(self.shop_dice_button)
            i += 1

            self.next_round_button = Button(frame, text="Next Round", bg=self.button_colour, font=self.large_font, command=lambda: [self.gui_next_round(), self.update_sidebar()])
            self.next_round_button.grid(row=3, column=3, padx=10, pady=10)

        return frame
    #current dice for the shop menu
    def current_dice(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(7)), weight=1)

        self.current_dice_label = Label(frame, font =self.large_font, text = "Current Dice", bg=self.bg_colour)
        self.current_dice_label.grid(padx=1, pady=15,sticky = NSEW, row=0, columnspan=7)

        #make the current dice in a line
        for x in range(6):
                dice_type = self.dice["die" + str(x + 1)]["type"]
                bg_colour = self.dice_type_info[dice_type]["colour"]
                self.dice_button = Button(frame, image=self.shop_dice_image, text= f"Dice {x + 1}", bg=bg_colour, font=self.font, compound=CENTER, borderwidth=0)
                self.dice_button.grid(column=x, row=1, padx=10)
        return frame
    #pick a dice to replace for new dice
    def replace_dice(self):
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(3)), weight=1)
        frame.columnconfigure(list(range(2)), weight=1)
        
        self.current_dice_label = Label(frame, font =self.large_font, text = "Select a dice to replace", bg=self.bg_colour)
        self.current_dice_label.grid(padx=1, pady=15,sticky = NSEW, row=0, columnspan=7)

        #display current dice in a 2x3 grid
        for y in range(2):
            for x in range(3):
                die = "die" + str(x +1 + y*3)
                dice = self.dice[die]
                faces = dice["sides"]
                dice_type = self.dice["die" + str(x + 1 + y*3)]["type"]
                bg_colour = self.dice_type_info[dice_type]["colour"]
                self.dice_button = Button(frame, image=self.dice_image, text= f"Dice {x +1 + y*3} \nFaces: {faces}", bg=bg_colour, font=self.font, compound=CENTER, borderwidth=0, wraplength=150, justify=CENTER, command = lambda value=(x +1 + y*3): self.dice_change(value))
                self.dice_button.grid(row=y+1, column=x, padx=100)

        return frame
    #run the game
    def run(self):
        self.root.mainloop()
    #end the game
    def quit(self):
        self.root.destroy()
    #updates the sidebar with new values
    def update_sidebar(self):
        data = self.logic.get_gui_data()
        self.requirement_label.config(text=f"Requirement: {data['requirement']}")
        self.total_label.config(text=f"Total: {data['total']}")
        self.scoring_label.config(text=f"Remaining Hands: {data['hands']}")
        self.money_label.config(text=f"Money: {data['money']}")
        self.played = data["played"]
        self.dice = data["dice"]
    def toggle_dice(self, die_number):
        self.locked = self.logic.lock_dice(die_number)

        dice = "die" + str(die_number)
        if self.locked[dice] == True:
            self.button_update = self.dice_buttons[die_number -1]
            self.button_update.config(image=self.locked_dice_image)
        #if locked unlock dice and change image
        else:
            self.button_update = self.dice_buttons[die_number -1]
            self.button_update.config(image=self.dice_image)
    def play_turn(self):
        self.logic.play_hand()
        self.update_sidebar()

        #update the dice
        for i in range(len(self.dice_buttons)):
            self.button_update = self.dice_buttons[i]
            self.button_update.config(text=self.played[i])

        # if no hands left, check requirement
        if self.logic.max_hands <= 0:
            if self.logic.requirement() == True:
                self.update_sidebar()
                self.show_frames("ShopMenu")
                self.refresh_shop_dice()
            else:
                self.show_frames("LossScreen")
    def gui_next_round(self):
        next_round = self.logic.next_round()
        if next_round == True:
            for i in range(6):
                self.button_update = self.dice_buttons[i]
                self.button_update.config(image=self.dice_image)
                self.show_frames("GameMenu")
        else: 
            self.show_frames("AddDice")
    def gui_reset(self):
        self.logic.game_reset()
        for i in range(6):
            self.button_update = self.dice_buttons[i]
            self.button_update.config(image=self.dice_image)
    def buy_dice(self, value):
        self.can_buy = self.logic.check_price(value)
        if self.can_buy == True:
            self.show_frames("ReplaceDice")
    def refresh_shop_dice(self):
        item = self.logic.get_gui_data()["shop_dice"]
        for i in range(len(self.shop_dice_buttons)):
            button_to_update = self.shop_dice_buttons[i]
            button_to_update.config(text=f"{item[i]['name']} \nCost: {item[i]['cost']}")
        return item
    def dice_change(self, value):
        self.logic.dice_change(value)
        self.show_frames("ShopMenu")
        self.update_sidebar()
    def add_dice(self):
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        
        self.add_dice_label = Label(frame, text = "You can now add a dice", font = self.large_font, bg =self.bg_colour)
        self.add_dice_label.grid(padx=10, pady=15, sticky = NSEW, row = 0)

        self.name_label = Label(frame, text = "Dice name", font = self.font, bg =self.bg_colour)
        self.name_label.grid(padx=10, pady=15, sticky = NSEW, row = 1)

        self.name_entry = Entry(frame, font = self.font)
        self.name_entry.grid(padx=400, pady=15, sticky = NSEW, row = 2)

        self.type_label = Label(frame, text = "Dice type", font = self.font, bg =self.bg_colour)
        self.type_label.grid(padx=10, pady=15, sticky = NSEW, row = 3)

        dice_types = []
        for dice_type in self.dice_type_info.keys():
            dice_types.append(dice_type)

        self.combo_default = StringVar()
        self.combo_default.set(dice_types[0])

        self.type_of_dice = ttk.Combobox(frame, font=self.font, values=dice_types, state="readonly", textvariable = self.combo_default)
        self.type_of_dice.grid(padx=400, pady=15, sticky=NSEW, row=4)

        self.faces_label = Label(frame, text = "Number of die faces (2-20)", font = self.font, bg =self.bg_colour)
        self.faces_label.grid(padx=10, pady=15, sticky = NSEW, row = 5)

        self.faces_entry = Entry(frame, font = self.font)
        self.faces_entry.grid(padx=400, pady=15, sticky = NSEW, row = 6)

        self.cost_label = Label(frame, text = "Cost of dice (1-5)", font = self.font, bg =self.bg_colour)
        self.cost_label.grid(padx=10, pady=15, sticky = NSEW, row = 7)

        self.cost_entry = Entry(frame, font = self.font)
        self.cost_entry.grid(padx=400, pady=15, sticky = NSEW, row = 8)

        self.continue_dice = Button(frame, text="Choose face numbers", bg=self.button_colour, font=self.font, command=lambda: self.check_new_dice())
        self.continue_dice.grid(padx=400, pady=10, sticky=NSEW, row = 9)

        

        return frame
    
    def check_new_dice(self):
        try:
            self.faces = int(self.faces_entry.get())
            self.dice_name = str(self.name_entry.get())
            self.dice_type = self.type_of_dice.get()
            self.dice_cost = int(self.cost_entry.get())
            print(self.dice_type)
            if self.faces < 2 or self.faces > 20:
                self.faces_label.config(text = "Choose a valid number of faces between 2 and 20")
                raise ValueError
            if self.dice_name.strip() == "":
                self.name_label.config(text = "Enter a dice name")
                raise ValueError
            if self.dice_cost < 1 or self.dice_cost > 5:
                self.cost_label.config(text = "Choose a valid cost between 1 and 5")
                raise ValueError
            
            self.faces_to_make.set(self.faces)
            self.make_faces()
            self.show_frames("AddFaces")
            
        except ValueError:
            self.continue_dice.config(text = "Ensure all boxes have been filled before you continue")

    def add_faces(self):
        self.faces = 1
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(list(range(22)), weight=1)

        self.add_dice_label = Label(frame, text = "Choose the faces for the dice", font = self.large_font, bg =self.bg_colour)
        self.add_dice_label.grid(padx=10, pady=15, sticky = NSEW, row = 0)

        self.values_label = Label(frame, text = "Enter the values for each face of the dice (0-100)", font = self.font, bg =self.bg_colour)
        self.values_label.grid(padx=10, pady=15, sticky = NSEW, row = 1)

        self.entries = Frame(frame)
        self.entries.grid()

        self.entry_widgets = []
        
        self.make_faces()

        self.submit_button = Button(frame, text="Submit Dice", bg=self.button_colour, font=self.font, command=lambda: self.submit_dice())
        self.submit_button.grid(padx=400, pady=10, sticky=NSEW, row = (self.faces + 3))

        return frame
    
    def make_faces(self):
        for widget in self.entries.winfo_children():
            widget.destroy()
        self.entry_widgets.clear()

        num = self.faces_to_make.get()
        for i in range(num):
            entry = Entry(self.entries)
            entry.grid(row=i, column=0, padx=10, pady=5, sticky=NSEW)
            self.entry_widgets.append(entry)
    
    def submit_dice(self):
        values = []
        for i in self.entry_widgets:
            try:
                value = int(i.get())
                if value < 0 or value > 100:
                    self.values_label.config(text = "Enter values between 0 and 100")
                    raise ValueError
                values.append(value)
            except ValueError:
                self.values_label.config(text = "Ensure all boxes have been filled with numbers before you continue")
                return
        self.new_dice = {}
        self.new_dice["name"] = self.dice_name
        self.new_dice["type"] = self.dice_type
        self.new_dice["sides"] = self.faces_to_make.get()
        self.new_dice["cost"] = self.dice_cost
        self.new_dice["values"] = values
        self.logic.add_dice(self.new_dice)

        self.show_frames("MainMenu")
#run the game
game = GUI()

game.run()
