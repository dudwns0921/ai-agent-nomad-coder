import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class TranslatorCrew:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config['news_hunter_agent'] # type: ignore[index]
        )
    
    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config['summarizer_agent'], # type: ignore[index]
        )
    
    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config['curator_agent'], # type: ignore[index]
        )

    @agent
    def translate_agent(self):
        return Agent(
            config=self.agents_config['translate_agent'], # type: ignore[index]
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config['content_harvesting_task'], # type: ignore[index]
        )
    
    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config['summarization_task'], # type: ignore[index]
        )
    
    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config['final_report_assembly_task'], # type: ignore[index]
        )

    @task
    def translate_final_report_task(self):
        return Task(
            config=self.tasks_config['translate_final_report_task'], # type: ignore[index]
        )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,  
            verbose=True
        )
    

TranslatorCrew().crew().kickoff({ "topic": "Technology" })