from agno.agent import Agent

from config import db, default_model, learning_machine

try:
    from agno.tools.docker import DockerTools
    docker_tools = DockerTools()
except (ValueError, Exception):
    docker_tools = None

docker_agent = Agent(
    id="docker-agent",
    name="Docker Agent",
    model=default_model,
    instructions=[
        "You are a Docker assistant. Manage containers, images, volumes, and networks.",
        "Always check container status before performing destructive operations.",
        "If Docker is not running, inform the user to start Docker Desktop.",
    ],
    tools=[docker_tools] if docker_tools else [],
    db=db,
    learning=learning_machine,
    add_history_to_context=True,
    add_learnings_to_context=True,
    markdown=True,
)
