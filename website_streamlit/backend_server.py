from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client
# Try to get API key from environment variable first, then from application.properties
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    # Try to read from application.properties file
    try:
        properties_path = os.path.join(
            os.path.dirname(__file__), 
            "springboot_backend", 
            "src", 
            "main", 
            "resources", 
            "application.properties"
        )
        with open(properties_path, 'r') as f:
            for line in f:
                if line.startswith('openai.api.key='):
                    openai_api_key = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"Warning: Could not read application.properties: {e}")

if not openai_api_key:
    print("ERROR: OPENAI_API_KEY not found!")
    print("Please set OPENAI_API_KEY environment variable or ensure it's in application.properties")
    client = None
else:
    print(f"✅ OpenAI API key loaded (starts with: {openai_api_key[:10]}...)")
    client = OpenAI(api_key=openai_api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message or not message.strip():
            return jsonify({'reply': 'No message provided.'}), 400
        
        if not client:
            return jsonify({'reply': 'OpenAI API key not configured. Please set OPENAI_API_KEY environment variable or ensure it\'s in application.properties.'}), 500
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant in the sector of finance and investments."},
                {"role": "user", "content": message}
            ]
        )
        
        reply = response.choices[0].message.content
        return jsonify({'reply': reply}), 200
        
    except Exception as e:
        error_message = f"Error processing chat request: {str(e)}"
        print(f"Error: {error_message}")
        return jsonify({'reply': error_message}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    print("=" * 50)
    print("Starting RoboInvesting Backend Server")
    print("=" * 50)
    print("Server will run on: http://localhost:8080")
    print("API endpoint: http://localhost:8080/api/chat")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8080, debug=True)

