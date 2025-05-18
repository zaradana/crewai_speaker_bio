#!/usr/bin/env python
import json
import os
import sys
import argparse
from crewai import Agent, Task, Crew
from typing import Dict, Optional
from pydantic import BaseModel, Field
from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from crewai.flow.flow import Flow, listen, start


class SpeakerIntroductionState(BaseModel):
    """State for the Speaker Introduction Flow"""

    speaker: str = ""
    company: str = ""
    event: str = ""
    speaker_introduction: str = ""
    company_showcase: str = ""
    final_introduction: str = ""


class SpeakerIntroductionFlow(Flow[SpeakerIntroductionState]):
    """Flow for creating speaker introductions for events"""

    def __init__(self):
        super().__init__()
        # Load agent configurations
        self.agent_configs = self._load_yaml_config(
            "src/speaker_introduction/config/agents.yaml"
        )
        self.task_configs = self._load_yaml_config(
            "src/speaker_introduction/config/tasks.yaml"
        )

    def _load_yaml_config(self, path: str) -> Dict:
        """Load YAML configuration file"""
        import yaml

        with open(path, "r") as file:
            return yaml.safe_load(file)

    def set_state(self, state: SpeakerIntroductionState):
        """Set the state"""
        self.state.speaker = state.speaker
        self.state.company = state.company
        self.state.event = state.event

    @start()
    def get_user_input(self):
        """Start the flow"""
        return self.state

    @listen(get_user_input)
    def create_speaker_introduction(self, state):
        """Research and create a personalized introduction for the speaker"""
        print("Researching and creating speaker introduction...")

        # Create the speaker introduction agent
        speaker_agent = Agent(
            role=self.agent_configs["speaker_introduction_agent"]["role"],
            goal=self.agent_configs["speaker_introduction_agent"]["goal"],
            backstory=self.agent_configs["speaker_introduction_agent"]["backstory"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
            llm = 'gpt-4o'
        )

        speaker_task = Task(
            config=self.task_configs["speaker_introduction_task"],
            agent=speaker_agent,
        )

        # Make the agent perform the task
        crew = Crew(agents=[speaker_agent], tasks=[speaker_task], verbose=True)
        result = crew.kickoff(
            inputs={
                "speaker": self.state.speaker,
                "company": self.state.company,
                "event": self.state.event,
            }
        )
        self.state.speaker_introduction = str(result)
        return self.state

    @listen(create_speaker_introduction)
    def create_company_showcase(self, state):
        """Research and create a showcase for the company"""
        print("Researching and creating company showcase...")

        # Create the company showcase agent
        company_agent = Agent(
            role=self.agent_configs["company_showcase_agent"]["role"],
            goal=self.agent_configs["company_showcase_agent"]["goal"],
            backstory=self.agent_configs["company_showcase_agent"]["backstory"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
            llm = 'gpt-4o'
        )

        # Format the task description with the input variables
        company_task = Task(
            config=self.task_configs["company_showcase_task"],
            agent=company_agent,
            output_key="company_showcase",
        )

        # Make the agent perform the task
        crew = Crew(agents=[company_agent], tasks=[company_task], verbose=True)
        result = crew.kickoff(
            inputs={
                "speaker": self.state.speaker,
                "company": self.state.company,
                "event": self.state.event,
            }
        )
        self.state.company_showcase = str(result)
        print("Company showcase created successfully")
        return self.state

    @listen(create_company_showcase)
    def create_final_introduction(self, state):
        """Create the final introduction combining speaker and company information"""
        print("Creating final introduction...")

        # Create the manager agent
        manager_agent = Agent(
            role=self.agent_configs["manager_agent"]["role"],
            goal=self.agent_configs["manager_agent"]["goal"],
            backstory=self.agent_configs["manager_agent"]["backstory"],
            allow_delegation=False,
            verbose=True,
            tools=[],
            llm = 'gpt-4o'
        )

        manager_task = Task(
            config=self.task_configs["summary_task"],
            agent=manager_agent,
        )

        # Make the agent perform the task with context
        crew = Crew(agents=[manager_agent], tasks=[manager_task], verbose=True)
        result = crew.kickoff(
            inputs={
                "speaker": self.state.speaker,
                "company": self.state.company,
                "event": self.state.event,
                "speaker_introduction": self.state.speaker_introduction,
                "company_showcase": self.state.company_showcase,
            }
        )
        self.state.final_introduction = str(result)

        print("Final introduction created successfully")
        return self.state

