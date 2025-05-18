#!/usr/bin/env python
import argparse
from dotenv import load_dotenv
from src.speaker_introduction.flow import (
    SpeakerIntroductionFlow,
    SpeakerIntroductionState,
)

load_dotenv()


def run_crew():
    """
    Run the traditional crew implementation.
    """
    parser = argparse.ArgumentParser(
        description="Run the Speaker Introduction Crew with specified inputs."
    )
    parser.add_argument(
        "--speaker", type=str, required=True, help="Name of the speaker"
    )
    parser.add_argument(
        "--company", type=str, required=True, help="Name of the company"
    )
    parser.add_argument(
        "--event", type=str, required=True, help="Name of the event"
    )

    args = parser.parse_args()

    # Create a new crew instance each time to avoid tool assignment issues
    flow = SpeakerIntroductionFlow()
    # Set the flow state before kickoff
    flow.set_state(SpeakerIntroductionState(
        speaker=args.speaker,
        company=args.company,
        event=args.event,
    ))
    result = flow.kickoff()

    return result.final_introduction
   

if __name__ == "__main__":
    run_crew()
