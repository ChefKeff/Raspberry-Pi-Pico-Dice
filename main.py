# This example shows you a simple, non-interrupt way of reading Pico Display's buttons with a loop that checks to see if buttons are pressed.

import time
from random import randint
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

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

class Hand():
    dice = []
    
    def add_dice(number_of_sides):
        dice.append(Dice(number_of_sides))
    
class Dice():
    def __init__(number_of_sides):
        self.number_of_sides = number_of_sides
    
    def roll_dice(self):
        return randint(1, self.number_of_sides)


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
    
def hand_view(): # here goes the logic for  adding dice to the player hand
    clear()
    while True:
        if button_b.read():
            return  clear()
        display.set_pen(GREEN)
        display.text("<- back", 10, 167, wordwrap=240, scale=2)
        display.text("hand", 10, 45, wordwrap=240, scale=3)
        display.update()
        
        
def roll_view(): # here goes the logic for checking the dice in the hand and rolling the dice and summing the total of the dice. 
    clear()
    while True: 
        if button_b.read():
            return clear()
        if Hand.dice == []:
            display.set_pen(MAGENTA)
            display.text("<- back", 10, 167, wordwrap=240, scale=2)
            display.text("No dice! There are no dice in the player's hand. Please add some in the 'hand'-view from the main menu.", 10, 45, wordwrap=240, scale=2)
            display.update()
            
        else:
            display.set_pen(MAGENTA)
            display.text("roll", 10, 45, wordwrap=240, scale=3)
            display.update()
    
def history_view():
    clear()
    while True:
        display.set_pen(WHITE)
        display.text("history", 10, 45, wordwrap=240, scale=3)
        display.update()
    
    




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
        clear()
        display.set_pen(YELLOW)
        display.text("Button Y pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    else:
        display.set_pen(GREEN)
        display.text("hand", 10, 45, wordwrap=240, scale=3)
        display.set_pen(MAGENTA)
        display.text("roll", 10, 167, wordwrap=240, scale=3)
        display.set_pen(WHITE)
        display.text("history", 195, 45, wordwrap=240, scale=3)
        display.set_pen(CYAN)
        display.text("clear", 230, 167, wordwrap=240, scale=3)
        display.update()
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
