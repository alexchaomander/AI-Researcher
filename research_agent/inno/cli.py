"""
MetaChain CLI - Low-level agent execution interface.

DEPRECATED: This CLI is maintained for backwards compatibility.
Prefer using `ai-researcher` CLI for research tasks.

Usage:
    python -m research_agent.inno.cli agent --agent_func=get_dummy_agent --query="test"
"""
import os
import click
import importlib

from research_agent.inno import MetaChain
from research_agent.inno.util import debug_print


def get_default_model() -> str:
    """Get default model from environment."""
    return os.getenv('COMPLETION_MODEL', 'gpt-4o-2024-08-06')


@click.group()
def cli():
    """MetaChain CLI - Low-level agent execution interface.

    Note: For research tasks, prefer using `ai-researcher` CLI instead.
    """
    pass


@cli.command()
@click.option('--model', default=None, help='Model name (default: COMPLETION_MODEL env var)')
@click.option('--agent_func', default='get_dummy_agent', help='Agent function name from research_agent.inno.agents')
@click.option('--query', default='...', help='User query to the agent')
@click.argument('context_variables', nargs=-1)
def agent(model: str, agent_func: str, query: str, context_variables):
    """Run an agent with a given model, agent function, query, and context variables.

    Example:
        python -m research_agent.inno.cli agent --agent_func=get_weather_agent --query="What is the weather?"
    """
    model = model or get_default_model()

    context_storage = {}
    for arg in context_variables:
        if '=' in arg:
            key, value = arg.split('=', 1)
            context_storage[key] = value

    # Use correct import path
    agent_module = importlib.import_module('research_agent.inno.agents')
    try:
        agent_creator = getattr(agent_module, agent_func)
    except AttributeError:
        raise click.ClickException(
            f"Agent function '{agent_func}' not found. "
            "Check research_agent.inno.agents for available functions."
        )

    agent_instance = agent_creator(model)
    mc = MetaChain()
    messages = [{"role": "user", "content": query}]
    response = mc.run(agent_instance, messages, context_storage, debug=True)
    debug_print(
        True, response.messages[-1]['content'],
        title=f'Result of running {agent_instance.name} agent',
        color='pink3'
    )
    return response.messages[-1]['content']


if __name__ == '__main__':
    cli()

