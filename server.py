import multiprocessing
import os
import random
import time

from flask import Flask, jsonify, request, abort 

# set to true to print light values instead of setting
DEV_MODE = False

DEFAULT_INCR = 0.01
LIGHT_BRIGHTS = [0.0, 0.0, 0.0, 0.0, 0.0]
LIGHT_IDS = [ '23', '24', '22', '25', '17']
MAX_BRIGHTNESS = 0.8
MIN_BRIGHTNESS = 0.0
NUM_LIGHTS = 5

app = Flask(__name__) 
command_queue = multiprocessing.Queue()

def set_light(light_id, brightness):
    LIGHT_BRIGHTS[light_id] = brightness
    if DEV_MODE:
        print LIGHT_IDS[light_id] + ": " + str(brightness)
    else:
        os.system("echo " + LIGHT_IDS[light_id] + "=" + str(brightness)
                  + " > /dev/pi-blaster")

def all_lights_up(incr):
    while True:
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] + incr)
        if done:
            return
        
def all_lights_down(incr):
    while True:
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] > MIN_BRIGHTNESS:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] - incr)
        if done:
            for i in range(5):
                set_light(i, 0)
            return

def blink_light(light_id):
    brightness = LIGHT_BRIGHTS[light_id]
    while brightness >= MIN_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness -= .01

    while brightness <= MAX_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness += .01
    
def wave_lights():
    count_downs = [0, 10, 20, 30, 40]
    turning_up = [False, False, False, False, False]   

    all_lights_up(DEFAULT_INCR)

    while True:
        for i in range(5):
            if count_downs[i] == 0:
                if not turning_up[i]:
                    set_light(i, LIGHT_BRIGHTS[i] - .005)
                    if (LIGHT_BRIGHTS[i] <= .1):
                        turning_up[i] = True
                else:
                    if (LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS):
                        set_light(i, LIGHT_BRIGHTS[i] + .005)
            else:
                count_downs[i] -= 1

        # this is the worst code I've written all year
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS:
                done = False
        if done:
            return

def randomize():
    incr = DEFAULT_INCR
    target_values = []
    for i in range(5):
        target_values.append(random.random())

    while True:
        done = True
        for i in range(5):
            if abs(LIGHT_BRIGHTS[i] - target_values[i]) < DEFAULT_INCR:
                continue
            elif LIGHT_BRIGHTS[i] < target_values[i]:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] + incr)
            elif LIGHT_BRIGHTS[i] > target_values[i]:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] - incr)
        if done:
            return
        
@app.route('/wave')
def wave_endpoint():
    wave_lights()
    return '{}'

@app.route('/up')
def up_endpoint():
    command_queue.put("UP")
    return '{}'

@app.route('/down')
def down_endpoint():
    command_queue.put("DOWN")
    return '{}'

@app.route('/blink')
def blink_endpoint():
    command_queue.put("BLINK")
    return '{}'

    light_id_arg = request.args.get('light')
    if not light_id_arg:
        all_lights_down(DEFAULT_INCR)
        all_lights_up(DEFAULT_INCR)
        return '{}'

    light_id = int(light_id_arg)

    if light_id < 0 or light_id >= 5:
        abort(400)

    blink_light(light_id)
    return '{}'

@app.route('/set')
def set_light_endpoint():
    light_id_arg = request.args.get('light')
    brightness_arg = request.args.get('bright')
    
    if not light_id_arg or not brightness_arg:
        abort(400)

    light_id = int(light_id_arg)
    brightness = float(brightness_arg)

    if light_id < 0 or light_id >= 5:
        abort(400)

    if brightness < MIN_BRIGHTNESS or brightness > MAX_BRIGHTNESS:
        abort(400)
        
    set_light(light_id, brightness)
        
    return '{}'

@app.route('/set_all')
def set_all_endpoint():
    brightness_arg = request.args.get('bright')

    if not brightness_arg:
        abort(400)

    brightness = float(brightness_arg)

    if brightness < MIN_BRIGHTNESS or brightness > MAX_BRIGHTNESS:
        abort(400)

    for i in range(5):
        set_light(i, brightness)

    return '{}'

@app.route('/rand')
def random_endpoint():
    randomize()
    return '{}'

@app.route('/sparkle')
def sparkle_endpoint():
    for i in range(10):
        randomize()
    all_lights_up(DEFAULT_INCR)
    return '{}'

def test_loop():
    command = "STEADY"
    while True:
      if not command_queue.empty():
          command = command_queue.get()
      if command == "BLINK":
          blink_light(0)
      elif command == "UP":
          all_lights_up(DEFAULT_INCR)
          command = "STEADY"
      elif command == "DOWN":
          all_lights_down(DEFAULT_INCR)
          command = "STEADY"

if __name__ == '__main__':
    all_lights_up(DEFAULT_INCR / 5)
    p = multiprocessing.Process(target=test_loop)
    p.start()
    app.run(debug=True)
    p.join()
