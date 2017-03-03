import os

from flask import Flask, jsonify, request, abort 

LIGHT_IDS = ['7', '6', '5', '4', '1']
NUM_LIGHTS = 5
    
app = Flask(__name__) 

def set_light(light_id, brightness):
    os.system("echo " + LIGHT_IDS[light_id] + "=" + str(brightness)
              + " > /dev/servoblaster")
    
@app.route('/', methods=['GET'])
def get():
    light_id_arg = request.args.get('light_id')
    brightness_arg = request.args.get('brightness')
    
    if not light_id_arg or not brightness_arg:
        abort(400)

    light_id = int(light_id_arg)
    brightness = int(brightness_id_arg)

    if light_id < 0 or light_id >= 5 or brightness < 0 or brightness >= 900:
        abort(400)

    set_light(light_id, brightness)
        
    return '{}'

if __name__ == '__main__':
    for i in range(0, NUM_LIGHTS):
        set_light(i, 0)
 
    app.run(debug=True)
