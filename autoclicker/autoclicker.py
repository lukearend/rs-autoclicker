# Runescape autoclicker
# Luke Arend 2019

from time import time, sleep
from itertools import count
import numpy as np
import pyautogui
from pynput.mouse import Listener

def add_jitter(value, jitter):
    return value + jitter * (2 * np.random.random() - 1)

def move_to(position, duration=1.0, 
            duration_jitter=0.05, position_jitter=None):
    duration = duration if duration_jitter is None else add_jitter(duration, duration_jitter)
    x, y = position if position_jitter is None else map(add_jitter, position, position_jitter)
    pyautogui.moveTo(x, y, duration, pyautogui.easeInOutQuad)

def click(duration=0.1, jitter=0.05, button='left'):
    duration = duration if jitter is None else add_jitter(duration, jitter)
    pyautogui.mouseDown(button=button)
    pause(duration)
    pyautogui.mouseUp(button=button)

def point_and_click(position, duration=1.0, button='left',
                    click_duration=0.1, pause_duration=0.25, 
                    duration_jitter=0.05, position_jitter=None, 
                    click_jitter=0.05, pause_jitter=0.05):
    move_to(position, duration, duration_jitter=duration_jitter, position_jitter=position_jitter)
    pause(pause_duration, jitter=pause_jitter)
    click(duration=click_duration, jitter=click_jitter, button=button)

def point_and_clicks(positions, durations, buttons,
                     click_duration=0.1, pause_duration=0.25, 
                     duration_jitter=0.05, position_jitter=None,
                     click_jitter=0.05, pause_jitter=0.05):
    for i, (position, duration, button) in enumerate(zip(positions, durations, buttons)):
        if i > 0:
            pause(pause_duration, jitter=pause_jitter)
        point_and_click(position, duration, button,
                        click_duration=click_duration, pause_duration=pause_duration,
                        click_jitter=click_jitter, pause_jitter=pause_jitter)

def pause(duration=0.25, jitter=0.05):
    duration = duration if jitter is None else add_jitter(duration, jitter)
    sleep(duration)

def splash(max_reps=None):
    npc = pyautogui.position()
    curse = (-227, 822)
    for rep in count(1):
        move_to(curse, 1.0, duration_jitter=0.2, position_jitter=(5, 5))
        pause(0.25, jitter=0.1)
        click()
        pause(0.25, jitter=0.1)
        move_to(npc, 1.0, duration_jitter=0.2, position_jitter=(5, 5))
        pause(0.25, jitter=0.1)
        click()
        pause(0.25, jitter=0.1)

        if max_reps is not None and rep == max_reps:
            return

# starting position: right bank stall
# upstairs in lumbridge castle with 
# camera zoomed all the way in and pointing
# northward so the walls were verticcal
def bank_to_cows():
    positions = [(-239.31640625, 900.4921875),
                 (-624.60546875, 877.8828125),
                 (-645.51953125, 869.32421875),
                 (-759.0390625, 838.2890625),
                 (-761.4140625, 896.9765625),
                 (-193.1953125, 626.9921875),
                 (-187.92578125, 632.8984375),
                 (-184.78515625, 665.6796875),
                 (-228.25390625, 597.71484375),
                 (-288.546875, 604.87109375),
                 (-253.421875, 659.80078125)]
    durations = [0.1,
                 2.5871710777282715,
                 4.8258957862854,
                 11.288201808929443,
                 1.8242170810699463,
                 7.610334873199463,
                 1.562474012374878,
                 17.493016958236694,
                 13.005393981933594,
                 13.499263048171997,
                 13.43225383758545,
                 12.917989253997803]
    buttons = ['left',
               'left',
               'left',
               'left',
               'right',
               'left',
               'left',
               'left',
               'left',
               'left',
               'left',
               'left']
    point_and_clicks(positions, durations, buttons)

# starting position: row 1 column 0 of the four
# squares west of the cows gate in lumbridge
# with camera zoomed all the way in and pointing
# northward so the fences were vertical
def cows_to_bank():
    positions = [(-251.07421875, 767.9609375),
                 (-317.61328125, 684.6015625),
                 (-328.9609375, 707.7265625),
                 (-320.13671875, 674.1484375),
                 (-243.19921875, 731.66015625),
                 (-213.78125, 700.046875),
                 (-231.05859375, 709.21484375),
                 (-319.1328125, 670.5546875),
                 (-301.33203125, 701.53125),
                 (-850.2578125, 813.390625),
                 (-655.41796875, 859.3203125),
                 (-664.38671875, 902.48046875),
                 (-235.7109375, 620.20703125),
                 (-621.73046875, 656.90234375),
                 (-628.5234375, 686.70703125),
                 (-317.51953125, 809.18359375),
                 (-322.47265625, 910.0546875),
                 (-408.453125, 603.8828125)]
    durations = [0.1,
                 3.4318418502807617,
                 6.878136157989502,
                 2.3167240619659424,
                 16.866669178009033,
                 12.87103009223938,
                 7.7779741287231445,
                 10.85182499885559,
                 13.938787937164307,
                 15.221340894699097,
                 3.251631021499634,
                 1.5860509872436523,
                 4.5908849239349365,
                 11.429309844970703,
                 3.094219923019409,
                 2.968647003173828,
                 2.0696771144866943,
                 2.4643380641937256]
    buttons = ['left',
               'left',
               'left',
               'left',
               'left',
               'left',
               'left',
               'left',
               'left',
               'right',
               'left',
               'left',
               'right',
               'left',
               'right',
               'left',
               'left',
               'left']
    point_and_clicks(positions, durations, buttons)

def cows_bank_run():
    cows_to_bank()
    bank_to_cows()

class Recorder():
    def __init__(self):
        self.counter = 0
        self.tic = None
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def on_click(self, x, y, button, pressed):
        if pressed:
            if self.counter == 0:
                print('clicked at ({}, {}) with {}'.format(x, y, button))
            else:
                print('moved for {} sec to click at ({}, {}) with {}'.format(time() - self.tic, x, y, button))
            self.tic = time()
            self.counter += 1

def main():
    # Recorder()
    splash(80)
    # cows_to_bank()
    # bank_to_cows()

if __name__ == '__main__':
    main()

