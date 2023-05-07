from machine import Pin, I2C
import time
import math

# https://files.seeedstudio.com/wiki/XIAO-RP2040/img/micropython/XIAO-RP2040-MicroPython-Grove.zip
from ssd1306 import SSD1306_I2C
# https://github.com/backy0175/pico-examples/blob/main/Button/PushButton.py
from PushButton import Debounced

import random


class Dice:
    def __init__(self, x: int, y: int, size: int, spots=1):
        self.x = x
        self.y = y
        self.dice_size = size
        self.spot_size = size // 8
        self.spots = max(1, min(spots, 6))
        print(f'{spots=}, {self.spots=}')
#        self.show()

    def __str__(self):
        return f'[x: {self.x}, y: {self.y}, spots:{self.spots}]'

    def __eq__(self, other):
        return self.spots == other.spots

    def __lt__(self, other):
        return self.spots < other.spots

    def __gt__(self, other):
        return self.spots > other.spots

    def __hash__(self):
        return super().__hash__()

    def show(self):
        self.show_outline()
        self.show_spots()

    def show_outline(self):
        display.rect(self.x, self.y, self.dice_size, self.dice_size, 1)
        display.fill_rect(self.x, self.y, 2, 2, 0)
        display.fill_rect(self.x + self.dice_size - 2, self.y, 2, 2, 0)
        display.fill_rect(self.x, self.y + self.dice_size - 2, 2, 2, 0)
        display.fill_rect(self.x + self.dice_size - 2, self.y + self.dice_size - 2, 2, 2, 0)
        display.pixel(self.x, self.y, 0)
        display.pixel(self.x + self.dice_size - 1, self.y, 0)
        display.pixel(self.x, self.y + self.dice_size - 1, 0)
        display.pixel(self.x + self.dice_size-1, self.y + self.dice_size - 1, 0)

        display.pixel(self.x + 1, self.y + 1, 1)
        display.pixel(self.x + self.dice_size - 2, self.y + 1, 1)
        display.pixel(self.x + 1, self.y + self.dice_size - 2, 1)
        display.pixel(self.x + self.dice_size - 2, self.y + self.dice_size - 2, 1)

    def show_spots(self):
        if self.spots == 1:
            display.fill_rect(int(self.x + (self.dice_size / 2) - self.spot_size), int(self.y + (self.dice_size / 2) - self.spot_size), self.spot_size * 2, self.spot_size * 2, 1)
        elif self.spots == 2:
            display.fill_rect(int(self.x + (self.dice_size / 3) * 2 - self.spot_size / 2), int(self.y + (self.dice_size / 3) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 3) - self.spot_size / 2), int(self.y + (self.dice_size / 3) * 2 - self.spot_size / 2), self.spot_size, self.spot_size, 1)
        elif self.spots == 3:
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 2) - self.spot_size / 2), int(self.y + (self.dice_size / 2) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 3 - self.spot_size / 2), self.spot_size, self.spot_size, 1)
        elif self.spots == 4:
            display.fill_rect(int(self.x + (self.dice_size / 3) - self.spot_size / 2), int(self.y + (self.dice_size / 3) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 3) * 2 - self.spot_size / 2), int(self.y + (self.dice_size / 3) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 3) - self.spot_size / 2), int(self.y + (self.dice_size / 3) * 2 - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 3) * 2 - self.spot_size / 2), int(self.y + (self.dice_size / 3) * 2 - self.spot_size / 2), self.spot_size, self.spot_size, 1)
        elif self.spots == 5:
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 2 - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 2- self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 3- self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 3- self.spot_size / 2), self.spot_size, self.spot_size, 1)
        elif self.spots == 6:
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) - self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 2- self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 2- self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 3- self.spot_size / 2), self.spot_size, self.spot_size, 1)
            display.fill_rect(int(self.x + (self.dice_size / 4) * 3 - self.spot_size / 2), int(self.y + (self.dice_size / 4) * 3- self.spot_size / 2), self.spot_size, self.spot_size, 1)

    def roll(self):
        self.spots = random.randint(1, 6)


i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)
display = SSD1306_I2C(128, 64, i2c)
screen_width = 127
screen_height = 63


def press_button(button):
    global dt_pushed
    dt_pushed = time.ticks_ms()
    print('pressed ', button)

    global status
    if status == 'wait':
        status = 'select'

    elif status == 'select':
        global next_dice_number
        next_dice_number += 1
        if next_dice_number > dice_max:
            next_dice_number = 1
#        print(f'{next_dice_number=}')

    elif status == 'roll':
        global speed
        if speed == 'fast':
            speed = 'slow'
        elif speed == 'slow':
            speed = 'fast'


p1 = Debounced(27, Pin.PULL_UP)
p1.debouncedIRQ(press_button, Pin.IRQ_FALLING)

status = 'wait'

next_dice_number = 1
timer = 5
dt_pushed = time.ticks_ms()
countdown = timer

margin = 3
dice_number = 1
dice_count = 1
dice_max = 16

roll_count = 0
match_count = 0

speed = 'slow'
roll_time = {'fast': 1, 'slow': 20}
roll_wait = {'fast': 0, 'slow': 2}

dices = []

while True:
    if status == 'wait':
        display.fill(0)
        dice_size = 58
        if not dices:
            x = margin
            y = margin
            dices.append(Dice(x, y, dice_size))

        display.text('Push', 95, 55, 1)
        for dice in dices:
            dice.show()
        display.show()

    elif status == 'select':
        display.fill(0)
        if dice_number != next_dice_number:
            dice_number = next_dice_number
            dices.clear()
        if dice_number == 1:
            dice_size = 58
            row = 1
            col = 1
        elif dice_number == 2:
            dice_size = 44
            row = 1
            col = 2
        elif dice_number == 3:
            dice_size = 39
            row = 1
            col = 3
        elif dice_number <= 7:
            dice_size = 28
            row = 2
            col = 4
        elif dice_number <= 12:
            dice_size = 18
            row = 3
            col = 4
        else:
            dice_size = 18
            row = 3
            col = 6

        dice_count = 1
        if not dices:
            for i in range(row):
                for j in range(col):
                    x = margin + (margin * j) + (dice_size * j)
                    y = margin + (margin * i) + (dice_size * i)
                    dices.append(Dice(x, y, dice_size))
                    dice_count += 1
                    if dice_count > dice_number:
                        break
                else:
                    continue
                break
        for dice in dices:
            dice.show()
        display.show()

        expect = 1 / (1 / (6 ** (dice_number - 1)))
        display.text(f'{expect: >5}', 88, 47, 1)

        dt_now = time.ticks_ms()
        countdown = timer - (dt_now - dt_pushed) / 1000
        display.text(f'{countdown:.2f}', 95, 55, 1)

        display.show()

        if countdown <= 0:
            status = 'roll'
            continue
        time.sleep(0.1)

    if status == 'roll':
        display.fill(0)
        display.text(f'{roll_count: >5}', 85, 55, 1)

        for i in range(roll_time[speed]):
            display.fill(0)
            for dice in dices:
                dice.roll()
                dice.show()
            display.text(f'{match_count: >5}', 88, 47, 1)
            display.text(f'{roll_count: >5}', 88, 55, 1)
            display.show()
        time.sleep(roll_wait[speed])

        if min(dices) == max(dices):
            print(f'match! {roll_count=}')
            match_count += 1
            display.text(f'{match_count: >5}', 85, 47, 1)
            display.show()
            time.sleep(2)

        roll_count += 1
        display.text(f'{match_count: >5}', 85, 47, 1)
        display.text(f'{roll_count: >5}', 85, 55, 1)
        display.show()
