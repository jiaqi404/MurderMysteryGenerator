from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MuderMysteryGenerator():
    """MuderMysteryGenerator crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

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
    
    # @agent
    # def detail_enhancer(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['detail_enhancer'],
    #         verbose=True
    #     )
    
    # @agent
    # def english_to_chinese_translator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['english_to_chinese_translator'],
    #         verbose=True
    #     )
    
    @task
    def character_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['character_creation_task'],
        )
    
    @task
    def murder_case_outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['murder_case_outline_task'],
            output_file='plot_en.md'
        )
    
    # @task
    # def plot_weaving_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['plot_weaving_task'],
    #     )
    
    # @task
    # def detail_enhancement_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['detail_enhancement_task'],
    #         output_file='plot_en.md'
    #     )
    
    # @task
    # def structured_story_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['structured_story_task'],
    #         output_file='plot_en.md'
    #     )
    
    # @task
    # def english_to_chinese_translation_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['english_to_chinese_translation_task'],
    #         output_file='plot_cn.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the MuderMysteryGenerator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
