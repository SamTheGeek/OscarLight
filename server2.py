from flask import Flask, jsonify, request, abort 
import time
 
NLIGHTS = 25
light_state = [ 0 for i in range(0, NLIGHTS) ]
app = Flask(__name__)


def turn(i, on_off):
    light_state[i] = on_off
    open( '/dev/servoblaster' , 'w' ).write( '%d=%d%%' % (i, int(100*float(on_off))) )  

 
@app.route('/oscarlight/v1/<int:light_id>', methods=['GET'])
def get(light_id):
    if light_id < 0 or light_id >= NLIGHTS:
        abort(404)
    return '{}' 
 

@app.route('/oscarlight/v1/<int:light_id>', methods=['PUT'])
def put(light_id):
    if not request.json:
        abort(400 , "not json" )

    on_off = request.json.get('switch')

    turn( light_id, on_off )
    return '{}'
 
if __name__ == '__main__':
    for i in range(0, NLIGHTS):
        turn(i, 0)
    app.run(debug=True)
