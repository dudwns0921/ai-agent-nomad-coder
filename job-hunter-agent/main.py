import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.knowledge import Knowledge
from models import JobList, RankedJobList, ChosenJob
from tools import web_search_tool

resume_knowledge = Knowledge(
    collection_name="resume",
    sources=[TextFileKnowledgeSource(file_paths=["resume.txt"])]
)


@CrewBase
class JobHunterAgent:

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def job_search_agent(self):
        return Agent(
            config=self.agents_config["job_search_agent"], # type: ignore[index]
            tools=[
                web_search_tool
            ]
        )
    
    @agent
    def job_matching_agent(self):
        return Agent(
            config=self.agents_config["job_matching_agent"], # type: ignore[index]
            knowledge=resume_knowledge
        )
    
    @agent
    def resume_optimization_agent(self):
        return Agent(
            config=self.agents_config["resume_optimization_agent"], # type: ignore[index]
            knowledge=resume_knowledge
        )
    
    @agent
    def company_research_agent(self):
        return Agent(
            config=self.agents_config["company_research_agent"] # type: ignore[index]
        )
    
    @agent
    def interview_prep_agent(self):
        return Agent(
            config=self.agents_config["interview_prep_agent"], # type: ignore[index]
            knowledge=resume_knowledge
        )

    @task
    def job_extraction_task(self):
        return Task(
            config=self.tasks_config["job_extraction_task"], # type: ignore[index]
            output_pydantic=JobList
        )
    
    @task
    def job_matching_task(self):
        return Task(
            config=self.tasks_config["job_matching_task"], # type: ignore[index]
            output_pydantic=RankedJobList
        )
    
    @task
    def job_selection_task(self):
        return Task(
            config=self.tasks_config["job_selection_task"], # type: ignore[index]
            output_pydantic=ChosenJob
        )
    
    @task
    def resume_rewriting_task(self):
        return Task(
            config=self.tasks_config["resume_rewriting_task"], # type: ignore[index]
            context=[
                self.job_selection_task()
            ]
        )
    
    @task
    def company_research_task(self):
        return Task(
            config=self.tasks_config["company_research_task"], # type: ignore[index]
            context=[
                self.job_selection_task()
            ]
        )
    
    @task
    def interview_prep_task(self):
        return Task(
            config=self.tasks_config["interview_prep_task"], # type: ignore[index]
            context=[
                self.job_selection_task(),
                self.resume_rewriting_task(),
                self.company_research_task()
            ]
        )
    @crew

    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )
    
JobHunterAgent().crew().kickoff(
    inputs={
        'level': 'junior',
        'position': 'web frontend developer',
        'location': 'seoul'
    }
)