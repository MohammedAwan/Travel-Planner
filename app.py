# groq_travel_itinerary_app.py

import os
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json()
    destination = data.get('destination')
    duration = data.get('duration')
    travel_dates = data.get('travel_dates')
    accommodation = data.get('accommodation')
    budget = data.get('budget')
    interests = data.get('interests')
    pace = data.get('pace')
    dietary_restrictions = data.get('dietary_restrictions')
    special_requests = data.get('special_requests')

    prompt = (
        f"Generate a detailed travel itinerary for a trip to {destination} based on the following information:\n"
        f"Trip duration: {duration} days\n"
        f"Travel dates: {travel_dates}\n"
        f"Accommodation preferences: {accommodation}\n"
        f"Budget: {budget}\n"
        f"Interests and activities: {interests}\n"
        f"Preferred pace: {pace}\n"
        f"Dietary restrictions: {dietary_restrictions}\n"
        f"Special requests: {special_requests}\n"
        f"The itinerary should include daily schedules with recommended activities, places to visit, dining options, transportation details, and any relevant tips or information."
    )

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a professional travel planner."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }

        response = requests.post(GROQ_URL, json=payload, headers=headers)
        response.raise_for_status()

        itinerary = response.json()['choices'][0]['message']['content'].strip()
        return jsonify({'itinerary': itinerary})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
