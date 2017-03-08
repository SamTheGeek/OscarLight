import os
import random

from flask import Flask, jsonify, request, abort 

LIGHT_IDS = [ '23', '24', '22', '25', '17']
LIGHT_BRIGHTS = [0.0, 0.0, 0.0, 0.0, 0.0]
MAX_BRIGHTNESS = 0.8
MIN_BRIGHTNESS = 0.0
HALF_BRIGHTNESS = (MAX_BRIGHTNESS + MIN_BRIGHTNESS) / 2
INCR = 0.015
NUM_LIGHTS = 5

app = Flask(__name__) 

def set_light(light_id, brightness):
    LIGHT_BRIGHTS[light_id] = brightness
    os.system("echo " + LIGHT_IDS[light_id] + "=" + str(brightness)
              + " > /dev/pi-blaster")

def all_lights_up():
    while True:
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] < MAX_BRIGHTNESS:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] + INCR)
        if done:
            return

def all_lights_down():
    while True:
        done = True
        for i in range(5):
            if LIGHT_BRIGHTS[i] > MIN_BRIGHTNESS:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] - INCR)
        if done:
            for i in range(5):
                set_light(i, 0)
            return

def all_lights_half():
    while True:
        done = True
        for i in range(5):
            if (LIGHT_BRIGHTS[i] > HALF_BRIGHTNESS):
                done = False
                set_light(i, LIGHT_BRIGHTS[i] - INCR)
            else LIGHT_BRIGHTS[i] < HALF_BRIGHTNESS:
                done = False
                set_light(i, LIGHT_BRIGHTS[i] + INCR)
        if done:
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

    all_lights_up()

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
    for i in range(5):
        set_light(i, random.random())

@app.route('/wave')
def wave_endpoint():
    wave_lights()
    return '{}'

@app.route('/up')
def up_endpoint():
    all_lights_up()
    return '{}'

@app.route('/down')
def down_endpoint():
    all_lights_down()
    return '{}'

@app.route('/half')
def down_endpoint():
    all_lights_half()
    return '{}'

@app.route('/blink')
def blink_endpoint():
    light_id_arg = request.args.get('light')
    if not light_id_arg:
        all_lights_down()
        all_lights_up()
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
    for i in range(200):
        randomize()
    all_lights_up()
    return '{}'
    
if __name__ == '__main__':
    all_lights_up()
    app.run(debug=True)
