# pip install Flask
# python app.py
# curl -X POST http://localhost:5000/add -H "Content-Type: application/json" -d '{"first_number": 10, "second_number": 20}'

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.json
    first_number = data.get('first_number')
    second_number = data.get('second_number')

    if first_number is None or second_number is None:
        return jsonify({"error": "Both first_number and second_number are required"}), 404

    try:
        sum_result = float(first_number) + float(second_number)
    except ValueError:
        return jsonify({"error": "Invalid numbers provided"}), 404

    return jsonify({"sum": sum_result})


def substract():
    return 1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

