from flask import Flask, jsonify, request, abort 
import time
 
NLIGHTS = 25
light_state = [ 0 for i in range(0, NLIGHTS) ]

 
app = Flask(__name__)

# server2.py mo like server ew .py

def turn(i, on_off):
    light_state[i] = on_off
    # echo 3=0 > /dev/servoblaster
    open( '/dev/servoblaster' , 'w' ).write( '%d=%d%%' % (i, int(100*float(on_off))) )  

 
@app.route('/oscarlight/v1/<int:light_id>', methods=['GET'])
def get(light_id):
    if light_id < 0 or light_id >= NLIGHTS:
        abort(404)
    return '{}' # jsonify(light_state[light_id])
 

@app.route('/oscarlight/v1/<int:light_id>', methods=['PUT'])
def put(light_id):
    #if light_id < 0 or light_id >= NLIGHTS:
    #    print("bad light number")
    #    abort(404 , "light id was bad" )
        

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
        turn(i, 0)
 
    app.run(debug=True)
