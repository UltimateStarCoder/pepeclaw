from agno.team import Team

from config import db, reasoning_model
from teams.code_team import code_team
from teams.docs_team import docs_team
from teams.deploy_team import deploy_team
from teams.payments_team import payments_team
from teams.research_team import research_team

fullstack_team = Team(
    id="fullstack-team",
    name="Full Stack Team",
    description="A team of sub-teams orchestrated to handle any task.",
    model=reasoning_model,
    members=[code_team, docs_team, deploy_team, payments_team, research_team],
    instructions=[
        "You are the lead architect of a full stack team.",
        "Delegate coding, debugging, and file operations to the Code Team.",
        "Delegate documentation lookup and framework questions to the Docs Team.",
        "Delegate deployment and infrastructure tasks to the Deploy Team.",
        "Delegate billing, Stripe, and invoice tasks to the Payments Team.",
        "Delegate deep analysis, knowledge synthesis, and research to the Research Team.",
        "If a sub-team fails or can't complete a task, re-delegate to a different sub-team.",
        "After any code modification, ensure the Code Team runs lint and type checks.",
    ],
    show_members_responses=True,
    markdown=True,
    db=db,
)
