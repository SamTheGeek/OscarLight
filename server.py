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
        brightness -= DEFAULT_INCR

    while brightness <= MAX_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness += DEFAULT_INCR

def blink_all():
    all_lights_down(DEFAULT_INCR)
    all_lights_up(DEFAULT_INCR)
    
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
    incr = DEFAULT_INCR / 2
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
    command_queue.put("WAVE")
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
    light_id_arg = request.args.get('light')
    if not light_id_arg:
        command_queue.put("BLINK")
        return '{}'
    
    light_id = int(light_id_arg)

    if light_id < 0 or light_id >= 5:
        abort(400)

    command_queue.put("BLINK " + light_id_arg)
    return '{}'

@app.route('/sparkle')
def sparkle_endpoint():
    command_queue.put("SPARKLE")
    return '{}'

def test_loop():
    command = "STEADY"
    while True:
      if not command_queue.empty():
          command = command_queue.get()
      if command.startswith("BLINK"):
          command_parts = command.split()
          if len(command_parts) != 2:
              blink_all()
          else:
              # heaven forgive me for this
              blink_light(int(command_parts[1]))
      elif command == "UP":
          all_lights_up(DEFAULT_INCR)
          command = "STEADY"
      elif command == "DOWN":
          all_lights_down(DEFAULT_INCR)
          command = "STEADY"
      elif command == "WAVE":
          wave_lights()
      elif command == "SPARKLE":
          randomize()
          
if __name__ == '__main__':
    all_lights_up(DEFAULT_INCR / 5)
    p = multiprocessing.Process(target=test_loop)
    p.start()
    app.run(debug=True)
    p.join()
