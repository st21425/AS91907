dies = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}

def lock_dice(die_number):
    global dies
    dice = "die" + die_number # 
    if dies[dice] == False:
        dies[dice] = True    

num = str(1)
lock_dice(num)
print(dies["die1"])