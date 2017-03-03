from flask import Flask, jsonify, request, abort 
import RPi.GPIO as GPIO
import time
 
ON = 1
OFF = 0
NLIGHTS = 5

indexes = [ 26, 16, 20, 21, 13 ]  
light_state = [ OFF for i in range(0, NLIGHTS) ]

gpio_start = 1
gpio_end = 27

GPIO.setmode(GPIO.BCM)
for x in range (gpio_start, gpio_end):
   GPIO.setup(x, GPIO.OUT)


 
app = Flask(__name__)

def blink(i, on_off):
    light_state[i] = on_off
    if on_off: 
        print('turning %d on' % i )    
        GPIO.output(indexes[i], True)
    else: 
        print('turning %d off' % i )    
        GPIO.output(indexes[i], False)
#-
 
def turn(i, on_off):
    light_state[i] = on_off
    if on_off: 
        print('turning %d on' % i )    
        GPIO.output(indexes[i], True)
    else: 
        print('turning %d off' % i )    
        GPIO.output(indexes[i], False)

 
@app.route('/oscarlight/v1/<int:light_id>', methods=['GET'])
def get(light_id):
    if light_id < 0 or light_id >= NLIGHTS:
        abort(404)
    return '{}' # jsonify(light_state[light_id])
 

@app.route('/oscarlight/v1/<int:light_id>', methods=['PUT'])
def put(light_id):
    if light_id < 0 or light_id >= NLIGHTS:
        print("bad light number")
        abort(404 , "light id was bad" )
        

    if not request.json:
        print("not json ")
        abort(400 , "not json" )

    print( "now trying") 

    on_off = request.json.get('switch')

    print( on_off ) 

    turn( light_id, on_off )
    return '{}' # jsonify(light_state[light_id])
    return jsonify(light_state[light_id])
 
 
if __name__ == '__main__':
    print('turning on the lights')
    for i in range(0, NLIGHTS):
        turn(i, ON)
 
    app.run(debug=True)
