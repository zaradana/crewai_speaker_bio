from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class SpeakerIntroductionCrew:
    """CrewAI Speaker Introduction Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def manager_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["manager_agent"],
            tools=[],
            verbose=True,
        )

    @agent
    def speaker_introduction_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["speaker_introduction_agent"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def company_showcase_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["company_showcase_agent"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def speaker_introduction_task(self) -> Task:
        return Task(
            config=self.tasks_config["speaker_introduction_task"],
            agent=self.speaker_introduction_agent(),
            output_key="speaker_introductions"
        )

    @task
    def company_showcase_task(self) -> Task:
        return Task(
            config=self.tasks_config["company_showcase_task"],
            agent=self.company_showcase_agent(),
            output_key="company_showcase"
        )



    @task
    def summary_task(self) -> Task:
        return Task(
            config=self.tasks_config["summary_task"],
            agent=self.manager_agent(),
            context=[
                self.speaker_introduction_task(),
                self.company_showcase_task(),
            ]
        )

    @crew
    def crew(self) -> Crew:
        """Creates a Speaker Introduction Crew"""
        return Crew(
            agents=[
                self.speaker_introduction_agent(),
                self.company_showcase_agent(),
            ],
            tasks=[
                self.speaker_introduction_task(),
                self.company_showcase_task(),
                self.summary_task()
            ],
            process=Process.hierarchical,
            manager_agent=self.manager_agent(),
            verbose=True,
        )
