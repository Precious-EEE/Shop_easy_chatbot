from flask import Flask, request, jsonify
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)

def query_db(query, args=(), one=False):
    # Mock function to simulate database query. Replace with your actual DB querying logic.
    if query.startswith("SELECT order_status"):
        return ("out for delivery", "tomorrow")  # Mock response for order status
    elif query.startswith("SELECT price"):
        return (49.99, "high-quality sound, a 12-hour battery life, available in black and blue")  # Mock response for product info
    elif query.startswith("SELECT * FROM orders"):
        return ("delayed", "2-3 days")  # Mock response for complaints
    return None

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    # Get the intent from Dialogflow request
    intent = req.get('queryResult').get('intent').get('displayName')

    # Handle Conversation Start
    if intent == 'ConversationStartIntent':
        response_text = "Hello! Welcome to ShopEasy. How can I assist you today?"

    # Handle Order Status intent
    elif intent == 'OrderStatusIntent':
        # Get order number from user input
        order_number = req.get('queryResult').get('parameters').get('order_number')
        result = query_db('SELECT order_status, expected_delivery FROM orders WHERE order_id = ?', [order_number], one=True)
        if result:
            response_text = f"Thank you! I'm checking the status of your order. One moment please...\nYour order #{order_number} is currently {result[0]} and should arrive by {result[1]}."
        else:
            response_text = "I couldn't find your order. Please check the order number and try again."

    # Handle Product Info intent
    elif intent == 'ProductInfoIntent':
        # Get product name from user input
        product_name = req.get('queryResult').get('parameters').get('product_name')
        result = query_db('SELECT price, description FROM products WHERE product_name = ?', [product_name], one=True)
        if result:
            response_text = f"The {product_name} is priced at ${result[0]:.2f}. It features {result[1]}."
        else:
            response_text = "Sorry, I couldn't find any information about that product."

    # Handle Complaint Handling intent
    elif intent == 'ComplaintHandlingIntent':
        # Get order number from user input
        order_number = req.get('queryResult').get('parameters').get('order_number')
        result = query_db('SELECT order_status, expected_delivery FROM orders WHERE order_id = ?', [order_number], one=True)
        if result:
            response_text = f"Thank you. Let me check...\nIt seems your order #{order_number} is {result[0]} and should be delivered within {result[1]}. We apologize for the inconvenience!"
        else:
            response_text = "I couldn't find your order. Please check the order number and try again."

    # Handle Troubleshooting intent
    elif intent == 'TroubleshootingIntent':
        error_message = req.get('queryResult').get('parameters').get('error_message')
        if error_message == "Incorrect password":
            response_text = "No worries! It happens. You can reset your password by following this password reset link. Would you like me to send a reset link to your email on file?"
        else:
            response_text = "I’m sorry to hear you're having trouble. Could you provide more details about the issue?"

    # Handle Conversation Closing intent
    elif intent == 'ConversationClosingIntent':
        response_text = "You're very welcome! If you need anything else, feel free to reach out. Have a great day shopping with ShopEasy!"

    # Default fallback intent
    else:
        response_text = "Sorry, I didn't understand that."

    # Return the response back to Dialogflow
    return jsonify({
        'fulfillmentText': response_text
    })

if __name__ == '__main__':
    app.run(debug=True)
