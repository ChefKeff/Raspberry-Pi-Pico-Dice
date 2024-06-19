# This example shows you a simple, non-interrupt way of reading Pico Display's buttons with a loop that checks to see if buttons are pressed.

import time
from random import randint
from pimoroni import Button
import pngdec
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_RGB332, rotate=0)

display.set_backlight(1)
display.set_font("bitmap8")
png = pngdec.PNG(display)
png_paths = ["user.png", "clock.png", "dice.png", "wrench.png"]
png_placement = [[0,0],[230,0],[0,150],[230,150]]


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
hand_string = ['__','__','__','__','__']
history = []


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
    
def check_hand_string(hand, hand_string):
    for i in range(len(hand)):
        if 'D' + str(hand[i].number_of_sides) != hand_string[i]:
            hand_string[i] = 'D' + str(hand[i].number_of_sides)
    
def hand_view(): # here goes the logic for adding dice to the player hand
    hand_png_paths = ["back.png"]
    hand_png_placement = [[0,195]]
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
    clear()
    hand_string = []
    hand_idx = 0
    selected_no_sides = 0
    available_sides = [2, 4, 6, 8, 10, 12, 20]
    for dice in hand:
        if dice.number_of_sides == 0:
            hand_string.append('D0')
        else:
            hand_string.append('D' + str(dice.number_of_sides))
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
                clear()
            else:
                hand[hand_idx] = Dice(0)
                clear()
            check_hand_string(hand, hand_string)
        for i in range(len(hand_png_paths)):
            png.open_file(hand_png_paths[i])
            png.decode(hand_png_placement[i][0], hand_png_placement[i][1], scale=5)
        display.set_pen(GREEN)
        for line_idx in range(len(line_placement)):
            line_coords = line_placement[line_idx]
            print(line_coords)
            if line_idx != hand_idx:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 2)
            else:
                display.line(line_coords['x1'], line_coords['y'], line_coords['x2'], line_coords['y'], 8)
        for i in range(len(hand_string)):
            if hand_string[i] != 'D0':
                display.text(hand_string[i], line_placement[i]['x1'], line_placement[i]['y'] - 35, scale=3)
                
        display.text('D' + str(available_sides[selected_no_sides]), 10, 45, wordwrap=240, scale=2)
        display.text("h_idx" + str(hand_idx), 195, 45, wordwrap=240, scale=2)
        display.update()

def roll_view(): # here goes the logic for checking the dice in the hand and rolling the dice and summing the total of the dice. 
    clear()
    count_empty = 0
    roll_mode = False
    while True:
        for dice in hand:
            if dice.number_of_sides == 0:
                count_empty = count_empty + 1
        if button_b.read():
            return clear()
        #if count_empty > 4:
        #    display.set_pen(MAGENTA)
        #    display.text("<- back", 10, 167, wordwrap=240, scale=2)
        #    display.text("No dice! There are no dice in the player's hand. Please add some in the 'hand'-view from the main menu.", 10, 45, wordwrap=240, scale=2)
        #    display.update()
            
        display.set_pen(MAGENTA)
        if button_y.read():
            if not roll_mode:
                clear()
                roll_mode = True
            elif roll_mode:
                rolls = []
                roll_string = []
                dice_on_hand = []
                for dice in hand:
                    if dice.number_of_sides != 0:
                        dice_on_hand.append(dice.number_of_sides)
                        rolls.append(dice.roll_dice())
                        
                for i in range(len(rolls)):
                    roll_string.append('D' + str(dice_on_hand[i]) + ': ' + str(rolls[i]))
                    
                history.append(roll_string)
                
                roll_string.append('sum of rolls: ' + str(sum(rolls)))
                display.text(str(roll_string), 10, 45, wordwrap=185, scale=3)
                display.update()
                roll_mode = False
        display.update()
    
def history_view():
    clear()
    while True:
        display.set_pen(WHITE)
        display.text("history", 10, 45, wordwrap=240, scale=3)
        display.text(str(history), 10, 45, wordwrap=240, scale=3)
        display.update()
        if button_b.read():
            return clear()
    
    




# set up
clear()

while True:
    if button_a.read():
        hand_view()
    elif button_b.read():
        roll_view()
    elif button_x.read():
        history_view()
    elif button_y.read():
        settings_view()
    else:
        # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
        # You can use Thonny to transfer PNG Images to your Pico.
        for i in range(len(png_paths)):
            png.open_file(png_paths[i])
            png.decode(png_placement[i][0], png_placement[i][1], scale=10)
        # Decode our PNG file and set the X and Y
        display.update()
    
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
