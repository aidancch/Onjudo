import Manager
import initial

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", logger=False, engineio_logger=True)

# Sample data for random generation
STREET_NAMES = ["Oak", "Maple", "Pine", "Cedar", "Elm", "Willow", "Birch", "Spruce"]
CITIES = ["San Francisco", "Los Angeles", "San Jose", "Palo Alto", "Mountain View"]
DESCRIPTIONS = [
    "Stunning modern home with open floor plan and high-end finishes throughout.",
    "Charming traditional house with beautiful landscaping and updated kitchen.",
    "Luxurious estate featuring a resort-style backyard and gourmet kitchen.",
    "Contemporary design meets comfort in this exceptional property."
]
SCHOOLS = [
    ["Lincoln Elementary (9/10)", "Washington Middle (8/10)", "Jefferson High (9/10)"],
    ["Roosevelt Elementary (10/10)", "Kennedy Middle (9/10)", "Adams High (8/10)"],
    ["Madison Elementary (8/10)", "Monroe Middle (9/10)", "Wilson High (10/10)"]
]
AGENT_NAMES = ["John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis"]
OFFICE_NAMES = ["Luxury Realty", "Premier Properties", "Elite Estates", "Golden Gate Realty"]

manager = Manager.Manager()

def generate_random_properties(count=10):
    properties = []
    for i in range(count):
        # Generate random date within last 30 days
        list_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        
        property_data = {
            "id": i + 1,
            "price": random.randint(800000, 5000000),
            "beds": random.randint(2, 6),
            "baths": random.randint(2, 5),
            "sqft": random.randint(1500, 5000),
            "address": f"{random.randint(100, 999)} {random.choice(STREET_NAMES)} St, {random.choice(CITIES)}, CA",
            "description": random.choice(DESCRIPTIONS),
            "property_url": f"https://example.com/property/{i+1}",
            "status": "Active",
            "list_date": list_date,
            "neighborhoods": ["Downtown", "Financial District"],
            "agent_id": f"AG{random.randint(1000, 9999)}",
            "agent_name": random.choice(AGENT_NAMES),
            "agent_email": "agent@example.com",
            "agent_phones": ["+1 (415) 555-0123", "+1 (415) 555-0124"],
            "broker_id": f"BR{random.randint(1000, 9999)}",
            "office_name": random.choice(OFFICE_NAMES),
            "office_email": "office@example.com",
            "nearby_schools": random.choice(SCHOOLS),
            # "primary_photo": f"https://picsum.photos/seed/{i+1}/800/600"
            "primary_photo": "http://ap.rdcpix.com/f952121054dcc724fdaf6a8374641dd2l-b3138126835od-w480_h360_x2.webp?w=1080&q=75",
            "latitude": 37.441533,
            "longitude": -122.144146
        }
        properties.append(property_data)
    return properties

chat_history = []
# current_listings = generate_random_properties(12)  # Generate 12 properties
current_listings = initial.initial_list

@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    socketio.emit('initial_data', {
        'chat_history': chat_history,
        'listings': current_listings
    })
    chat_history.append({
        'content': "Hi! I'm Onjūdō, your real estate assistant. Whether you're buying, selling, or renting, I'm here to help. What can I do for you today?",
        'role': "assistant"
    })
    # Emit the AI response
    socketio.emit('ai_response', {'message': chat_history[0]['content']})
    socketio.emit('chat_update', {
                'chat_history': chat_history
            })

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

@socketio.on('user_message')
def handle_message(data):
    try:
        user_msg = data['message']
        print(f"Processing user message: {user_msg}")
        
        chat_history.append({
            'content': user_msg,
            'sender': 'user'
        })
        
        # Simulate AI response (replace with actual AI logic later)

        print("processing... ")

        ai_response = manager.get_response(user_msg)

        print("finished processing")

        chat_history.append({
            'content': ai_response['content'],
            'sender': 'assistant'
        })
        
        # print(f"Current chat history: {chat_history}")
        
        # Emit the AI response
        socketio.emit('ai_response', {'message': ai_response['content']})
        
        # Emit the updated chat history
        socketio.emit('chat_update', {
            'chat_history': chat_history
        })

        new_listings = manager.get_data()

        socketio.emit('listings_update', {
            'listings': new_listings
        })
        print("updated listings")
        print(type(new_listings))
        
    except Exception as e:
        import traceback, sys
        print(f"Error processing message: {e!r}")
        traceback.print_exc(file=sys.stdout)
        socketio.emit('error', {'message': 'Error processing your message'})

if __name__ == '__main__':
    print("Starting Socket.IO server...")
    socketio.run(app, debug=True, port=4000, allow_unsafe_werkzeug=True)

