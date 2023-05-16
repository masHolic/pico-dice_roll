from machine import Pin, I2C, PWM
import time
import random
import _thread

# https://files.seeedstudio.com/wiki/XIAO-RP2040/img/micropython/XIAO-RP2040-MicroPython-Grove.zip
from ssd1306 import SSD1306_I2C
# https://github.com/backy0175/pico-examples/blob/main/Button/PushButton.py
from PushButton import Debounced


class Dice:
    def __init__(self, x: int, y: int, size: int, number=1):
        self.x = x
        self.y = y
        self.dice_size = size
        self.spot_size = size // 8
        self.number = max(1, min(number, 6))
        self.spots = {}
        # spots location
        # 7 is a big spot
        # [0] , ------ , [1]
        # [2] , [6][7] , [3]
        # [4] , ------ , [5]
        self.spots[0] = {"x": int(self.x + (self.dice_size / 4) - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[1] = {"x": int(self.x + (self.dice_size / 4) * 3 - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[2] = {"x": int(self.x + (self.dice_size / 4) - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) * 2 - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[3] = {"x": int(self.x + (self.dice_size / 4) * 3 - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) * 2 - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[4] = {"x": int(self.x + (self.dice_size / 4) - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) * 3 - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[5] = {"x": int(self.x + (self.dice_size / 4) * 3 - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 4) * 3 - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[6] = {"x": int(self.x + (self.dice_size / 2) - (self.spot_size / 2)),
                         "y": int(self.y + (self.dice_size / 2) - (self.spot_size / 2)),
                         "w": self.spot_size,
                         "h": self.spot_size,
                         "c": 1}
        self.spots[7] = {"x": int(self.x + (self.dice_size / 2) - self.spot_size),
                         "y": int(self.y + (self.dice_size / 2) - self.spot_size),
                         "w": self.spot_size * 2,
                         "h": self.spot_size * 2,
                         "c": 1}

    def __str__(self):
        return f'[x: {self.x}, y: {self.y}, spots:{self.number}]'

    def __eq__(self, other):
        return self.number == other.number

    def __lt__(self, other):
        return self.number < other.number

    def __gt__(self, other):
        return self.number > other.number

    def __hash__(self):
        return super().__hash__()

    def show(self):
        self.show_outline()
        self.show_spots()

    def show_outline(self):
        display.hline(self.x + 2, self.y, self.dice_size - 4, 1)
        display.hline(self.x + 2, self.y + self.dice_size - 1, self.dice_size - 4, 1)
        display.vline(self.x, self.y + 2, self.dice_size - 4, 1)
        display.vline(self.x + self.dice_size - 1, self.y + 2, self.dice_size - 4, 1)
        display.pixel(self.x + 1, self.y + 1, 1)
        display.pixel(self.x + self.dice_size - 2, self.y + 1, 1)
        display.pixel(self.x + 1, self.y + self.dice_size - 2, 1)
        display.pixel(self.x + self.dice_size - 2, self.y + self.dice_size - 2, 1)

    def show_spots(self):
        if self.number == 1:
            display.fill_rect(self.spots[7]["x"], self.spots[7]["y"], self.spots[7]["w"], self.spots[7]["h"], self.spots[7]["c"])
        elif self.number == 2:
            display.fill_rect(self.spots[0]["x"], self.spots[0]["y"], self.spots[0]["w"], self.spots[0]["h"], self.spots[0]["c"])
            display.fill_rect(self.spots[5]["x"], self.spots[5]["y"], self.spots[5]["w"], self.spots[5]["h"], self.spots[5]["c"])
        elif self.number == 3:
            display.fill_rect(self.spots[0]["x"], self.spots[0]["y"], self.spots[0]["w"], self.spots[0]["h"], self.spots[0]["c"])
            display.fill_rect(self.spots[5]["x"], self.spots[5]["y"], self.spots[5]["w"], self.spots[5]["h"], self.spots[5]["c"])
            display.fill_rect(self.spots[6]["x"], self.spots[6]["y"], self.spots[6]["w"], self.spots[6]["h"], self.spots[6]["c"])
        elif self.number == 4:
            display.fill_rect(self.spots[0]["x"], self.spots[0]["y"], self.spots[0]["w"], self.spots[0]["h"], self.spots[0]["c"])
            display.fill_rect(self.spots[1]["x"], self.spots[1]["y"], self.spots[1]["w"], self.spots[1]["h"], self.spots[1]["c"])
            display.fill_rect(self.spots[4]["x"], self.spots[4]["y"], self.spots[4]["w"], self.spots[4]["h"], self.spots[4]["c"])
            display.fill_rect(self.spots[5]["x"], self.spots[5]["y"], self.spots[5]["w"], self.spots[5]["h"], self.spots[5]["c"])
        elif self.number == 5:
            display.fill_rect(self.spots[0]["x"], self.spots[0]["y"], self.spots[0]["w"], self.spots[0]["h"], self.spots[0]["c"])
            display.fill_rect(self.spots[1]["x"], self.spots[1]["y"], self.spots[1]["w"], self.spots[1]["h"], self.spots[1]["c"])
            display.fill_rect(self.spots[4]["x"], self.spots[4]["y"], self.spots[4]["w"], self.spots[4]["h"], self.spots[4]["c"])
            display.fill_rect(self.spots[5]["x"], self.spots[5]["y"], self.spots[5]["w"], self.spots[5]["h"], self.spots[5]["c"])
            display.fill_rect(self.spots[6]["x"], self.spots[6]["y"], self.spots[6]["w"], self.spots[6]["h"], self.spots[6]["c"])
        elif self.number == 6:
            display.fill_rect(self.spots[0]["x"], self.spots[0]["y"], self.spots[0]["w"], self.spots[0]["h"], self.spots[0]["c"])
            display.fill_rect(self.spots[1]["x"], self.spots[1]["y"], self.spots[1]["w"], self.spots[1]["h"], self.spots[1]["c"])
            display.fill_rect(self.spots[2]["x"], self.spots[2]["y"], self.spots[2]["w"], self.spots[2]["h"], self.spots[2]["c"])
            display.fill_rect(self.spots[3]["x"], self.spots[3]["y"], self.spots[3]["w"], self.spots[3]["h"], self.spots[3]["c"])
            display.fill_rect(self.spots[4]["x"], self.spots[4]["y"], self.spots[4]["w"], self.spots[4]["h"], self.spots[4]["c"])
            display.fill_rect(self.spots[5]["x"], self.spots[5]["y"], self.spots[5]["w"], self.spots[5]["h"], self.spots[5]["c"])

    def roll(self):
        self.number = random.randint(1, 6)


def press_button(button):
    global dt_pushed
    dt_pushed = time.ticks_ms()
    print('pressed ', button)

    global button_wait
    global status
    if button_wait:
        button_wait = False

    elif status == 'wait':
        status = 'select'

    elif status == 'select':
        global next_dice_number
        next_dice_number += 1
        if next_dice_number > DICE_MAX:
            next_dice_number = 1

    elif status == 'roll':
        # global speed
        global next_speed
        if next_speed == 'fast':
            next_speed = 'manual'
        elif next_speed == 'slow':
            next_speed = 'fast'
        elif next_speed == 'manual':
            next_speed = 'slow'


def sound_dice():
    global dice_se
    for i in reversed(range(4, 16)):
        hz = random.randint(1100, 1150)
        buzzer.freq(hz)
        du = 1768
        buzzer.duty_u16(int(du * i / 10))
        time.sleep(0.01)
        buzzer.deinit()
        aaa = random.randint(8, 15)
        time.sleep(i * aaa / 1000)
    dice_se = False
    _thread.exit


def sound_repdigit():
    global repdigit_se
    freqs = [1567, 1318, 1567, 1318, 1567, 1318]
    for freq in freqs:
        buzzer.freq(freq)
        buzzer.duty_u16(256 * 16)
        time.sleep(0.05)
        buzzer.deinit()
        time.sleep(0.05)
    repdigit_se = False
    _thread.exit


def show_info():
    display.fill_rect(120, 47, 8, 9, 1)
    display.pixel(120, 47, 0)
    display.pixel(120, 47 + 8, 0)
    display.pixel(120 + 7, 47, 0)
    display.pixel(120 + 7, 47 + 8, 0)
    display.text(MODE_DISPLAY[next_speed], 120, 48, 0)

    display.text(f'{repdigit_count: >5}', 80, 48, 1)
    display.text(f'{roll_count:>16d}', 0, 57, 1)


# Hardware Setup
buzzer = PWM(Pin(29, Pin.OUT))

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=200000)
display = SSD1306_I2C(128, 64, i2c)
WIDTH = 127
HEIGHT = 63

p1 = Debounced(27, Pin.PULL_UP)
p1.debouncedIRQ(press_button, Pin.IRQ_FALLING)


status = 'wait'
button_wait = False

TIMER = 5
dt_pushed = time.ticks_ms()
countdown = TIMER

MARGIN = 3
DICE_MAX = 16
dice_number = 1
next_dice_number = 1
dice_count = 1

roll_count = 0
repdigit_count = 0
repdigit = False

speed = 'slow'
next_speed = 'slow'
MANUAL_ROLL = {'fast': False, 'slow': False, 'manual': True}
SPIN_MOTION = {'fast': False, 'slow': True, 'manual': True}
VISUAL_CONFIRM = {'fast': 0, 'slow': 1, 'manual': 0}
REPDIGIT_WAIT = {'fast': True, 'slow': True, 'manual': False}
MODE_DISPLAY = {'fast': "F", 'slow': "S", 'manual': "M"}

dices = []

print('START')

while True:
    if status == 'wait':
        display.fill(0)
        dice_size = 58
        if not dices:
            x = MARGIN
            y = MARGIN
            dices.append(Dice(x, y, dice_size))

        display.text('Push', 95, 57, 1)
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
        elif dice_number <= 6:
            dice_size = 28
            row = 2
            col = 4
        else:
            dice_size = 18
            row = 3
            col = 6

        dice_count = 1
        if not dices:
            for i in range(row):
                for j in range(col):
                    x = MARGIN + ((dice_size + MARGIN) * j)
                    y = MARGIN + ((dice_size + MARGIN) * i)
                    dices.append(Dice(x, y, dice_size))
                    dice_count += 1
                    if dice_count > dice_number:
                        break
                else:
                    continue
                break
        for dice in dices:
            dice.show()

        expect = 6 ** (dice_number - 1)
        display.text(f'{expect:>16d}', 0, 48, 1)

        dt_now = time.ticks_ms()
        countdown = TIMER - (dt_now - dt_pushed) / 1000
        countdown_width = (39 / 5) * (5 - countdown)
        display.rect(85, 56, 43, 8, 1)
        display.pixel(85, 56, 0)
        display.pixel(85, 56 + 7, 0)
        display.pixel(85 + 42, 56, 0)
        display.pixel(85 + 42, 56 + 7, 0)
        display.fill_rect(87, 58, int(countdown_width), 4, 1)
        display.show()

        time.sleep(0.1)

        if countdown <= 0:
            status = 'roll'

    elif status == 'roll':
        if speed != next_speed:
            speed = next_speed
            display.fill(0)
            for dice in dices:
                dice.show()
            show_info()
            display.show()

        if MANUAL_ROLL[speed]:
            button_wait = True
        while button_wait:
            time.sleep(0.1)

        if SPIN_MOTION[speed]:
            # dummy spinning dice
            dice_se = True
            _thread.start_new_thread(sound_dice, ())
            while dice_se:
                display.fill(0)
                for dice in dices:
                    dice.roll()
                    dice.show()

                show_info()
                display.show()

        display.fill(0)
        for dice in dices:
            dice.roll()
            dice.show()
        roll_count += 1

        if min(dices) == max(dices):
            print(f'repdigit! {roll_count=}')
            repdigit_count += 1
            repdigit = True
        else:
            repdigit = False

        show_info()
        display.show()

        if repdigit:
            repdigit_se = True
            _thread.start_new_thread(sound_repdigit, ())
            if REPDIGIT_WAIT[speed]:
                button_wait = True
            while button_wait or repdigit_se:
                time.sleep(0.1)
        else:
            time.sleep(VISUAL_CONFIRM[speed])
