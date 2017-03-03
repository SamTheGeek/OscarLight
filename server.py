import os

from flask import Flask, jsonify, request, abort 

LIGHT_IDS = ['7', '6', '5', '4', '1']
MAX_BRIGHTNESS = 800
MIN_BRIGHTNESS = 0
NUM_LIGHTS = 5

app = Flask(__name__) 

def set_light(light_id, brightness):
    os.system("echo " + LIGHT_IDS[light_id] + "=" + str(brightness)
              + " > /dev/servoblaster")
    
@app.route('/set_light')
def set_one_light():
    light_id_arg = request.args.get('light_id')
    brightness_arg = request.args.get('brightness')
    
    if not light_id_arg or not brightness_arg:
        abort(400)

    light_id = int(light_id_arg)
    brightness = int(brightness_arg)

    if light_id < 0 or light_id >= 5:
        abort(400)

    if brightness < MIN_BRIGHTNESS or brightness > MAX_BRIGHTNESS:
        abort(400)
        
    set_light(light_id, brightness)
        
    return '{}'

@app.route('/blink_light')
def blink_one_light():
    light_id_arg = request.args.get('light_id')

    if not light_id_arg:
        abort(400)

    light_id = int(light_id_arg)
        
    if light_id < 0 or light_id >= 5:
        abort(400)

    while brightness >= MIN_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness -= 2

    while brightness <= MAX_BRIGHTNESS:
        set_light(light_id, brightness)
        brightness += 2
        
    return '{}'

if __name__ == '__main__':
    for i in range(0, NUM_LIGHTS):
        set_light(i, MAX_BRIGHTNESS)
 
    app.run(debug=True)
