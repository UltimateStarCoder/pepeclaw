from agno.team import Team

from config import db, reasoning_model
from teams.dev_team import dev_team
from teams.docs_team import docs_team
from teams.deploy_team import deploy_team
from teams.payments_team import payments_team

fullstack_team = Team(
    id="fullstack-team",
    name="Full Stack Team",
    description="A team of sub-teams orchestrated to handle any task.",
    model=reasoning_model,
    members=[dev_team, docs_team, deploy_team, payments_team],
    instructions=[
        "You are the lead architect of a full stack team.",
        "Delegate tasks to the most appropriate sub-team based on the work needed.",
        "If a sub-team fails or can't complete a task, re-delegate to a different sub-team.",
        "After any code modification, ensure the Dev Team runs lint and type checks.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
