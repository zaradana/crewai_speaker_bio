#!/usr/bin/env python
import sys
import argparse
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

from src.speaker_introduction.crew import SpeakerIntroductionCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew with specified inputs.
    """
    parser = argparse.ArgumentParser(description="Run the Speaker Introduction Crew with specified inputs.")
    parser.add_argument("--speaker_name", type=str, required=True, help="Name of the speaker")
    parser.add_argument("--company_name", type=str, required=True, help="Name of the company")
    parser.add_argument("--event_context", type=str, required=True, help="Context of the event")

    args = parser.parse_args()

    inputs = {
        "speaker_name": args.speaker_name,
        "company_name": args.company_name,
        "event_context": args.event_context,
    }

    try:
        crew_instance = SpeakerIntroductionCrew().crew()
        result = crew_instance.kickoff(inputs=inputs, verbose=False)
        return result
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        exit(1)


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
