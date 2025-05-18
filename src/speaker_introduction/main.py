#!/usr/bin/env python
import sys
from dotenv import load_dotenv
import argparse

load_dotenv()

from src.speaker_introduction.crew import SpeakerIntroductionCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    parser = argparse.ArgumentParser(description="Run the Speaker Introduction Crew with specified inputs.")
    parser.add_argument("--speaker_name", type=str, default="João Moura", help="Name of the speaker")
    parser.add_argument("--company_name", type=str, default="CrewAI", help="Name of the company")
    parser.add_argument("--event_context", type=str, default="AI Tinkerers Hackathon", help="Context of the event")

    args = parser.parse_args()

    inputs = {
        "speaker_name": args.speaker_name,
        "company_name": args.company_name,
        "event_context": args.event_context,
    }

    # Create a new crew instance each time to avoid tool assignment issues
    crew_instance = SpeakerIntroductionCrew().crew()
    result = crew_instance.kickoff(inputs=inputs)
    print("\n=== FINAL RESULT ===\n")
    print(result)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        SpeakerIntroductionCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SpeakerIntroductionCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        SpeakerIntroductionCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    run()
