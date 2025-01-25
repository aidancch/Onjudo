from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Sample functions (Replace these with your actual implementation)
def get_response(user_input):
    return f"AI Response: {user_input}"  # Replace with AI model's response

def send_listings_as_dictionary():
    return [
        {
            "address": "96 Bayside Court, Atherton, CA",
            "price": 1000000,
            "info": "6 bed | 7 ba | 1329 sqft",
            "description": "Beautiful modern home in Atherton."
        },
        {
            "address": "123 Luxury Lane, Beverly Hills, CA",
            "price": 5000000,
            "info": "8 bed | 10 ba | 9000 sqft",
            "description": "A luxurious mansion with a private pool."
        }
    ]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

@app.route('/api/listings', methods=['GET'])
def listings():
    return jsonify(send_listings_as_dictionary())

if __name__ == '__main__':
    app.run(debug=True)
