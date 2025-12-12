"""
Paper Agent CLI - Generate academic papers from research results.
"""
import click
import asyncio
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@click.group()
def cli():
    """Paper Agent - Autonomous academic paper generation."""
    pass


@cli.command()
@click.option('--research-field', '-f', required=True,
              type=click.Choice(['vq', 'gnn', 'rec', 'diffu_flow', 'reasoning']),
              help='Research field/domain')
@click.option('--instance-id', '-i', required=True,
              help='Instance ID for the research task')
@click.option('--output-dir', '-o', default=None,
              help='Output directory (default: {field}/target_sections/{instance_id})')
def generate(research_field: str, instance_id: str, output_dir: str):
    """Generate a complete academic paper from research results."""
    from paper_agent.writing import writing

    click.echo(f"Generating paper for {research_field}/{instance_id}...")

    # Change to paper_agent directory for relative paths
    paper_agent_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(paper_agent_dir)

    asyncio.run(writing(research_field, instance_id))

    output_path = output_dir or f"{research_field}/target_sections/{instance_id}"
    click.echo(f"Paper generated in: {output_path}")


@cli.command()
@click.option('--research-field', '-f', required=True,
              type=click.Choice(['vq', 'gnn', 'rec', 'diffu_flow', 'reasoning']),
              help='Research field/domain')
@click.option('--instance-id', '-i', required=True,
              help='Instance ID for the research task')
@click.option('--section', '-s', required=True,
              type=click.Choice(['abstract', 'introduction', 'related_work',
                               'methodology', 'experiments', 'conclusion']),
              help='Section to generate')
def section(research_field: str, instance_id: str, section: str):
    """Generate a specific section of the paper."""
    click.echo(f"Generating {section} for {research_field}/{instance_id}...")

    paper_agent_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(paper_agent_dir)

    # Import and run the appropriate section composer
    if section == 'abstract':
        from paper_agent.abstract_composing import abstract_composing
        asyncio.run(abstract_composing(research_field, instance_id))
    elif section == 'introduction':
        from paper_agent.introduction_composing import introduction_composing
        asyncio.run(introduction_composing(research_field, instance_id))
    elif section == 'related_work':
        from paper_agent.related_work_composing_using_template import related_work_composing
        asyncio.run(related_work_composing(research_field, instance_id))
    elif section == 'methodology':
        from paper_agent.methodology_composing_using_template import methodology_composing
        asyncio.run(methodology_composing(research_field, instance_id))
    elif section == 'experiments':
        from paper_agent.experiments_composing import experiments_composing
        asyncio.run(experiments_composing(research_field, instance_id))
    elif section == 'conclusion':
        from paper_agent.conclusion_composing import conclusion_composing
        asyncio.run(conclusion_composing(research_field, instance_id))

    click.echo(f"Section {section} generated successfully.")


@cli.command()
def list_fields():
    """List available research fields and their templates."""
    paper_agent_dir = os.path.dirname(os.path.abspath(__file__))

    fields = ['vq', 'gnn', 'rec', 'diffu_flow']
    click.echo("Available research fields:")
    for field in fields:
        field_path = os.path.join(paper_agent_dir, field)
        if os.path.exists(field_path):
            click.echo(f"  - {field}")
        else:
            click.echo(f"  - {field} (templates not found)")


if __name__ == '__main__':
    cli()
