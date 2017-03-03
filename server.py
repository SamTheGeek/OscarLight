from flask import Flask, jsonify, request, abort 

LIGHT_IDS = [
 
app = Flask(__name__) 

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
    return '{}'

if __name__ == '__main__':
    for i in range(0, NLIGHTS):
        turn(i, ON)
 
    app.run(debug=True)
