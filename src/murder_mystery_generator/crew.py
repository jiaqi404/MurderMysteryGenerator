from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MurderMysteryGenerator():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ------------------ Creare agents from the config files ------------------
    @agent
    def crime_scene_investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['crime_scene_investigator'],
            verbose=True
        )

    @agent
    def casting_director(self) -> Agent:
        return Agent(
            config=self.agents_config['casting_director'],
            verbose=True
        )
    
    @agent
    def plot_weaver(self) -> Agent:
        return Agent(
            config=self.agents_config['plot_weaver'],
            verbose=True
        )

    # ------------------ Creare tasks from the config files ------------------
    @task
    def detailed_crime_scene_task(self) -> Task:
        return Task(
            config=self.tasks_config['detailed_crime_scene_task'],
            output_file='outputs/crime_scene.md'
        )

    @task
    def character_modification_task(self) -> Task:
        return Task(
            config=self.tasks_config['character_modification_task'],
            output_file='outputs/characters.md'
        )
    
    @task
    def murder_case_outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['murder_case_outline_task'],
            output_file='outputs/murder_case_outline.md'
        )
    
    # ------------------ Create crew using agents & tasks ------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential, # Execute tasks in sequential order
            verbose=True,
        )