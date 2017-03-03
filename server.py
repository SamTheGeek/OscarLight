import os

from flask import Flask, jsonify, request, abort 

LIGHT_IDS = [7, 6, 5, 4, 1]
NUM_LIGHTS = 5
    
app = Flask(__name__) 

def set_light(light_id, brightness):
    os.system("echo " + LIGHT_IDS[light_id] + "=" + brightness
              + " > /dev/servoblaster")
    
@app.route('/', methods=['PUT'])
def put(light_id):
    light_id = request.args.get('light_id')
    brightness = request.args.get('brightness')
     
    if not light_id or light_id < 0 or light_id >= 5:
        abort(400)

    if not brightness or brightness < 0 or brightness >= 900:
        abort(400)

    set_light(light_id, brightness)
        
    return '{}'

if __name__ == '__main__':
    for i in range(0, NLIGHTS):
        set_light(i, 0)
 
    app.run(debug=True)
