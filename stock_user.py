from flask import Flask, request, jsonify
import boto3
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'stock_user'
table = dynamodb.Table(table_name)

def create_order(order_id, script_code, price, order_type, profit_loss, ltp):
    """
    Inserts a new stock market order into the DynamoDB table.

    Parameters:
    - order_id (str): The unique ID for the order (Partition Key).
    - script_code (str): The code of the stock (Sort Key).
    - price (float): The price of the stock.
    - order_type (str): Type of order (e.g., buy or sell).
    - profit_loss (float): Profit or loss from the transaction.
    - LTP (float): Last Traded Price of the stock.

    Automatically adds created_date and modified_date.
    """
    
    current_datetime=datetime.now().isoformat()  # Current timestamp


    # Insert item into DynamoDB
    table.put_item(
        Item={
            'order_id': order_id,            # Partition Key (PK)
            'script_code': script_code,      # Sort Key (SK)
            'price': price,                  # Stock price
            'order_type': order_type,        # Buy or Sell
            'profit_loss': profit_loss,      # Profit or loss from the transaction
            'ltp': ltp,                      # Last traded price of the stock
            'created_date': current_datetime,    # Timestamp of creation
            'modified_date': current_datetime    # Timestamp of last modification
        }
    )
    return {'message': f"Order {order_id} for {script_code} created successfully."}

@app.route('/create_order', methods=['POST'])
def create_order_api():
    """
    API endpoint to create a new stock market order in the DynamoDB table.

    Expected POST data (JSON):
    - order_id: Unique ID for the order (Primary Key)
    - script_code: Stock code (Sort Key)
    - price: Price of the stock
    - order_type: Type of order (buy or sell)
    - profit_loss: Profit or loss from the transaction
    - LTP: Last traded price of the stock

    Returns:
    - Success message if the order is created.
    """
    
    # Parse the JSON data from the request
    data = request.json

    # Check if all required fields are present
    required_fields = ['order_id', 'script_code', 'price', 'order_type', 'profit_loss', 'ltp']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    # Create the order by calling the helper function
    result = create_order(
        order_id=data['order_id'],
        script_code=data['script_code'],
        price=int(data['price']),
        order_type=data['order_type'],
        profit_loss=int(data['profit_loss']),
        ltp=int(data['ltp'])
    )

    # Return a success message
    return jsonify(result), 201

@app.route('/get_order', methods=['POST'])
def get_order():
    """
    API endpoint to retrieve a stock market order from DynamoDB.

    Expected POST data (JSON):
    - order_id: Unique ID of the order (Partition Key)
    - script_code: Stock code (Sort Key)

    Returns:
    - The order details if found, otherwise an error message.
    """
    
    # Parse the JSON data from the request
    data = request.json
    order_id = data.get('order_id')
    script_code = data.get('script_code')

    if not order_id or not script_code:
        return jsonify({'error': 'order_id and script_code are required'}), 400

    # Retrieve the item from DynamoDB
    response = table.get_item(
        Key={
            'order_id': order_id,
            'script_code': script_code
        }
    )
    
    # Check if the item exists
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(item), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001,debug=True)