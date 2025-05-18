#!/usr/bin/env python
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.speaker_introduction.flow import (
    SpeakerIntroductionFlow,
    SpeakerIntroductionState,
)

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/introduce', methods=['POST'])
def introduce():
    """
    Endpoint to run the Speaker Introduction Crew.
    """
    data = request.json
    speaker = data.get('speaker')
    company = data.get('company')
    event = data.get('event')

    if not speaker or not company or not event:
        return jsonify({"error": "Missing required fields: speaker, company, and event"}), 400

    # Create a new crew instance each time to avoid tool assignment issues
    flow = SpeakerIntroductionFlow()
    # Set the flow state before kickoff
    flow.set_state(SpeakerIntroductionState(
        speaker=speaker,
        company=company,
        event=event,
    ))
    result = flow.kickoff()

    return jsonify({"introduction": result.final_introduction})

if __name__ == "__main__":
    app.run(debug=True)
