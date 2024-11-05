# Develop a Python API which will do subtraction of two numbers

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/sub',methods = ['POST'])


def sub_numbers ():
    data = request.json
    first_number = data.get('first_number')
    second_number=data.get('second_number')
    
    if first_number is None or second_number is None:
        return jsonify({"error":"Both firsr_number and second_number required"}),404
    
    try:
        sum_result = float(first_number) - float(second_number)
    except ValueError:
        return jsonify({"error":"Invalid Numbers are provided"}),404
    return jsonify({"sum":sum_result}),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    

