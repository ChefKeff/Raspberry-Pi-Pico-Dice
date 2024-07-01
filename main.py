# This example shows you a simple, non-interrupt way of reading Pico Display's buttons with a loop that checks to see if buttons are pressed.

import time
from random import randint
from pimoroni import Button
import pngdec
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332
import json

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332, rotate=0)

display.set_backlight(1)
display.set_font("bitmap8")
png = pngdec.PNG(display)
png_paths = ["user.png", "clock.png", "dice.png", "wrench.png"]
png_placement = [[0, 0], [230, 0], [0, 150], [230, 150]]

delim = ','
with open("presets.json") as f:
    presets = json.load(f)


button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
    
class Dice():
    def __init__(self, number_of_sides):
        self.number_of_sides = number_of_sides
    
    def roll_dice(self):
        return randint(1, self.number_of_sides)


hand = [Dice(0), Dice(0), Dice(0), Dice(0), Dice(0)]
hand_string = ['D0', 'D0', 'D0', 'D0', 'D0']
history = []
line_placement = [{'x1': 8,
                   'y': 180,
                   'x2': 66},
                  {'x1': 70,
                   'y': 180,
                   'x2': 128},
                  {'x1': 132,
                   'y': 180,
                   'x2': 190},
                  {'x1': 194,
                   'y': 180,
                   'x2': 252},
                  {'x1': 256,
                   'x2': 314,
                   'y': 180}]

rick_mode = False
tova_mode = False
auto_roll = False
boot = False
auto_roll_string = 'off'


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
    
def check_hand_string(hand, hand_string):
    for i in range(len(hand)):
        if 'D' + str(hand[i].number_of_sides) != hand_string[i]:
            hand_string[i] = 'D' + str(hand[i].number_of_sides)
    
def hand_view(): # here goes the logic for adding dice to the player hand THIS IS DONE!
    hand_png_paths = ["back.png", "right.png", "add.png", "remove.png"]
    hand_png_placement = [[0,195], [275, 0], [275, 195], [275, 195]]
    clear()
    hand_idx = 0
    selected_no_sides = 0
    available_sides = [2, 4, 6, 8, 10, 12, 20]
    while True:
        if button_b.read(): # go back to main
            return  clear()
        if button_a.read(): # change the number of sides of the dice to add
            selected_no_sides = selected_no_sides + 1
            if selected_no_sides >= len(available_sides):
                selected_no_sides = 0
            clear()
        if button_x.read(): # traverse the hand
            hand_idx = hand_idx + 1
            if hand_idx == 5:
                hand_idx = 0
            clear()
        if button_y.read(): # add dice to hand
            if hand[hand_idx].number_of_sides == 0:
                hand[hand_idx] = Dice(available_sides[selected_no_sides])
                hand_idx = hand_idx + 1
                if hand_idx == 5:
                    hand_idx = 0
                clear()
            else:
                hand[hand_idx] = Dice(0)
                clear()
            check_hand_string(hand, hand_string)
        for i in range(len(hand_png_paths)-2):
            png.open_file(hand_png_paths[i])
            png.decode(hand_png_placement[i][0], hand_png_placement[i][1], scale=5)
        display.set_pen(GREEN)
        for line_idx in range(len(line_placement)):
            line_coords = line_placement[line_idx]
            if line_idx != hand_idx:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 2)
            else:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 8)
        for i in range(len(hand_string)):
            if hand_string[i] != 'D0':
                display.text(hand_string[i], line_placement[i]['x1'], line_placement[i]['y'] - 35, scale=3)
                
        display.text('D' + str(available_sides[selected_no_sides]), 0, 0, wordwrap=240, scale=4)
        if hand[hand_idx].number_of_sides == 0:
            png.open_file(hand_png_paths[2])
            png.decode(hand_png_placement[2][0], hand_png_placement[2][1], scale=5)
        else:
            png.open_file(hand_png_paths[3])
            png.decode(hand_png_placement[3][0], hand_png_placement[3][1], scale=5)
        display.update()

def roll_view(): # here goes the logic for checking the dice in the hand and rolling the dice and summing the total of the dice. 
    hand_png_paths = ["back.png", "dice.png", "rickroll.png", "cat.png", "cat-black.png"]
    hand_png_placement = [[0, 195], [275, 195], [230, 0]]
    roll_hand = []
    preset_names = ['hand', 'p1', 'p2', 'p3', 'p4', 'p5']
    preset_idx = 0
    go_back = False
    count_empty = 0
    roll_idx = 0
    roll_mode = False
    global rick_mode
    global tova_mode
    global auto_roll
    created_hand = False
    loaded_preset = False
    cat_number = randint(3, 4)
    clear()
    while True:
        if button_b.read():
            return clear()
        
        if button_x.read():
            roll_hand = []
            preset_idx = preset_idx + 1
            if preset_idx == 5:
                preset_idx = 0
            created_hand = False
            clear()
            
        if preset_names[preset_idx] == 'hand' and created_hand == False:    
            for dice in hand:
                if dice.number_of_sides != 0:
                    roll_hand.append(dice)
                    created_hand = True
                
        elif preset_names[preset_idx] != 'hand' and created_hand == False:
            for preset_name, dice in presets.items():
                if preset_name == preset_names[preset_idx] and not created_hand:
                    for i in range(len(dice)):
                        if dice[i] != 0:
                            roll_hand.append(Dice(dice[i]))
                            created_hand = True
        
        for i in range(len(hand_png_paths)-3):
            png.open_file(hand_png_paths[i])
            png.decode(hand_png_placement[i][0], hand_png_placement[i][1], scale=5)
        display.set_pen(MAGENTA)
        
        if len(roll_hand) == 0:
            go_back = True
        else:
            go_back = False
        
        try:
            for i in range(len(rolls)):
                display.text(str(rolls[i]), line_placement[i]['x1'], line_placement[i]['y'] - 65, scale=3)
            display.text('sum: ' + str(sum(rolls)), 0, 50, scale=5)
            if rick_mode:
                png.open_file(hand_png_paths[2])
                png.decode(hand_png_placement[2][0], hand_png_placement[2][1], scale=10)
                display.set_pen(MAGENTA)
            if tova_mode:
                png.open_file(hand_png_paths[cat_number])
                png.decode(hand_png_placement[2][0], hand_png_placement[2][1], scale=10)
                display.set_pen(MAGENTA)
        except:
            print('no rolls yet')
        for line_idx in range(len(line_placement)):
            line_coords = line_placement[line_idx]
            display.line(line_coords['x1'], line_coords['y'] - 35, line_coords['x2'], line_coords['y'] - 35, 2)
        for i in range(len(roll_hand)):
            display.text('D' + str(roll_hand[i].number_of_sides), line_placement[i]['x1'], line_placement[i]['y'] - 10, scale=3)
        if button_y.read() and not go_back:
            if not roll_mode:
                cat_number = randint(3, 4)
                rolls = []
                clear()
                roll_mode = True
        while roll_mode:
            if auto_roll:
                for dice in roll_hand:
                    if not rick_mode and not tova_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(dice.roll_dice())
                    elif rick_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(1)
                    elif tova_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(dice.number_of_sides)
                if len(history) == 5:
                    history.pop(0)
                history.append(rolls)
                roll_mode = False
              
            display.update()
            display.set_pen(BLACK)
            display.clear()
            display.set_pen(MAGENTA)
            if not auto_roll:
                for line_idx in range(len(line_placement)):
                    line_coords = line_placement[line_idx]
                    if line_idx == roll_idx:
                        display.line(line_coords['x1'], line_coords['y'] - 35, line_coords['x2'], line_coords['y'] - 35, 8)
                    display.line(line_coords['x1'], line_coords['y'] - 35, line_coords['x2'], line_coords['y'] - 35, 2)
                        
                for i in range(len(roll_hand)):
                    display.text('D' + str(roll_hand[i].number_of_sides), line_placement[i]['x1'], line_placement[i]['y'] - 10, scale=3)
                
                for i in range(len(rolls)):
                    display.text(str(rolls[i]), line_placement[i]['x1'], line_placement[i]['y'] - 65, scale=3)
                dice = roll_hand[roll_idx]
                random = dice.roll_dice()
                display.text(str(random), line_placement[roll_idx]['x1'], line_placement[roll_idx]['y'] - 65, scale=3)         
                if button_y.read():
                    if not rick_mode and not tova_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(dice.roll_dice())
                            display.text(str(rolls[roll_idx]), line_placement[roll_idx]['x1'], line_placement[roll_idx]['y'] - 65, scale=3)
                    elif rick_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(1)
                            display.text(str(rolls[roll_idx]), line_placement[roll_idx]['x1'], line_placement[roll_idx]['y'] - 65, scale=3)
                    elif tova_mode:
                        if dice.number_of_sides != 0:
                            rolls.append(dice.number_of_sides)
                            display.text(str(rolls[roll_idx]), line_placement[roll_idx]['x1'], line_placement[roll_idx]['y'] - 65, scale=3)
                    if roll_idx == len(roll_hand)-1:
                        roll_idx = 0
                        clear()
                        if len(history) == 5:
                            history.pop(0)
                        history.append(rolls)
                        roll_mode = False
                    else:
                        roll_idx = roll_idx + 1
                    
                time.sleep(0.01)
            display.update()
            
        display.text(preset_names[preset_idx], 230, 0, scale=3)
                
        display.update()
    
def history_view():
    history_png_paths = ["back.png", "bin.png"]
    history_png_placement = [[0, 195], [275, 195]]
    clear()
    cleared = False
    while True:
        display.set_pen(WHITE)
        i = 0
        for roll in history[::-1]:
            display.text(str(roll) + ' sum: ' + str(sum(roll)), 10, 45 + i, wordwrap=310, scale=3)
            i = i + 30
        display.update()
        for i in range(len(history_png_paths)):
            png.open_file(history_png_paths[i])
            png.decode(history_png_placement[i][0], history_png_placement[i][1], scale=5)
        if button_b.read():
            return clear()
        if button_y.read():
            while len(history) > 0:
                history.pop(0)
            cleared = True
        while cleared:
            display.set_pen(BLACK)
            display.clear()
            display.set_pen(WHITE)
            display.text('history cleared', 0, 0, wordwrap=100, scale=4)
            display.update()
            time.sleep(1)
            return clear()
        
        
def presets_view(): # here goes the logic for creating presets
    hand_png_paths = ["back.png", "save.png", "add.png", "remove.png"]
    hand_png_placement = [[0,195], [275, 0], [275, 195], [275, 195]]
    curr_preset = [Dice(0), Dice(0), Dice(0), Dice(0), Dice(0)]
    preset_string = ["D0", "D0", "D0", "D0", "D0"]
    preset_names = ["p1", "p2", "p3", "p4", "p5"]
    number_saved_presets = len(presets)
    clear()
    hand_idx = 0
    selected_no_sides = 0
    available_sides = [2, 4, 6, 8, 10, 12, 20]
    pres_name_idx = 0
    loaded_preset = False
    
    while True:
        # check presets in the json
        for preset_name, dice in presets.items():
            if dice != [0,0,0,0,0] and preset_name == preset_names[pres_name_idx] and not loaded_preset:
                for i in range(5):
                    curr_preset[i-1] = Dice(dice[i])
                    preset_string[i-1] = "D" + str(dice[i])
                loaded_preset = True
                
        if button_b.read(): # go back to main
            return  clear()
        if button_a.read(): # change the number of sides of the dice to add
            selected_no_sides = selected_no_sides + 1
            if selected_no_sides >= len(available_sides):
                selected_no_sides = 0
            clear()
        if button_x.read(): # save the preset and reset the preset hand
            presets[preset_names[pres_name_idx]] = [
                curr_preset[0].number_of_sides,
                curr_preset[1].number_of_sides,
                curr_preset[2].number_of_sides,
                curr_preset[3].number_of_sides,
                curr_preset[4].number_of_sides
                ]
            with open("presets.json", "w") as f:
                json.dump(presets, f)
            
            pres_name_idx = pres_name_idx + 1
            if pres_name_idx == 5:
                pres_name_idx = 0
                    
            curr_preset = [Dice(0), Dice(0), Dice(0), Dice(0), Dice(0)]
            preset_string = ["D0", "D0", "D0", "D0", "D0"]
            
            hand_idx = 0
            
            loaded_preset = False
                    
            
            clear()
            
                
                
        if button_y.read(): # add dice to hand
            if curr_preset[hand_idx].number_of_sides == 0:
                curr_preset[hand_idx] = Dice(available_sides[selected_no_sides])
                hand_idx = hand_idx + 1
                if hand_idx == 5:
                    hand_idx = 0
                clear()
            else:
                curr_preset[hand_idx] = Dice(0)
                hand_idx = hand_idx + 1
                if hand_idx == 5:
                    hand_idx = 0
                clear()
            check_hand_string(curr_preset, preset_string)
        for i in range(len(hand_png_paths)-2):
            png.open_file(hand_png_paths[i])
            png.decode(hand_png_placement[i][0], hand_png_placement[i][1], scale=5)
        display.set_pen(GREEN)
        for line_idx in range(len(line_placement)):
            line_coords = line_placement[line_idx]
            if line_idx != hand_idx:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 2)
            else:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 8)
        for i in range(len(hand_string)):
            if preset_string[i] != 'D0':
                display.text(preset_string[i], line_placement[i]['x1'], line_placement[i]['y'] - 35, scale=3)
                
        display.text('D' + str(available_sides[selected_no_sides]), 0, 0, wordwrap=240, scale=4)
        display.text(preset_names[pres_name_idx], 230, 0, scale=3)
        if curr_preset[hand_idx].number_of_sides != 0:
            png.open_file(hand_png_paths[3])
            png.decode(hand_png_placement[3][0], hand_png_placement[3][1], scale=5)
        else:
            png.open_file(hand_png_paths[2])
            png.decode(hand_png_placement[2][0], hand_png_placement[2][1], scale=5)
        display.update()
            
        
def settings_view():
    settings_png_paths = ["back.png", "rick_icon.png", "tova_icon.png"]
    settings_png_placement = [[0, 195], [0, 0]]
    global rick_mode
    global tova_mode
    global auto_roll
    global auto_roll_string
    clear()
    while True:
        for i in range(len(settings_png_paths)-2):
            png.open_file(settings_png_paths[i])
            png.decode(settings_png_placement[i][0], settings_png_placement[i][1], scale=5)
        display.set_pen(YELLOW)
        display.text("auto roll", 180, 0, wordwrap=240, scale=3)
        display.text(auto_roll_string, 180, 45, wordwrap=240, scale=3)
        display.text("Rick mode", 0, 0, wordwrap=240, scale=3)
        display.text("presets", 180, 195, wordwrap=240, scale=3)
        display.update()
        if button_b.read():
            return clear()
        if button_x.read():
            auto_roll = not auto_roll
        if button_a.read():
            rick_mode = not rick_mode
        if button_y.read():
            presets_view()
        
        if rick_mode:
            display.set_pen(BLACK)
            display.clear()
            png.open_file(settings_png_paths[1])
            png.decode(settings_png_placement[1][0], settings_png_placement[1][1], scale=1)
            display.set_pen(YELLOW)
        elif not rick_mode:
            display.set_pen(BLACK)
            display.clear()
        if auto_roll:
            auto_roll_string = 'on'
        elif not auto_roll:
            auto_roll_string = 'off'
    




# set up
clear()

while True:
    if boot:
        start = time.time()
        while time.time() < start + 4:
            # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
            # You can use Thonny to transfer PNG Images to your Pico.
            png.open_file("rick_splash.png")

            # Decode our PNG file and set the X and Y
            png.decode(0, 0, scale=1)
            display.update()
        boot = False
        clear()
    if button_a.read():
        hand_view()
    elif button_b.read():
        roll_view()
    elif button_x.read():
        history_view()
    elif button_y.read():
        settings_view()
    if not boot:
        # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
        # You can use Thonny to transfer PNG Images to your Pico.
        for i in range(len(png_paths)):
            png.open_file(png_paths[i])
            png.decode(png_placement[i][0], png_placement[i][1], scale=10)
        # Decode our PNG file and set the X and Y
        display.update()
    
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
