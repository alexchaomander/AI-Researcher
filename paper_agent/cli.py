"""
Paper Agent CLI - Generate academic papers from research results.
"""
import click
import asyncio
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
PAPER_AGENT_DIR = Path(__file__).parent

# Available research fields (shared constant)
RESEARCH_FIELDS = ['vq', 'gnn', 'rec', 'diffu_flow', 'reasoning']

# Section composer mapping
SECTION_COMPOSERS = {
    'abstract': ('paper_agent.abstract_composing', 'abstract_composing'),
    'introduction': ('paper_agent.introduction_composing', 'introduction_composing'),
    'related_work': ('paper_agent.related_work_composing_using_template', 'related_work_composing'),
    'methodology': ('paper_agent.methodology_composing_using_template', 'methodology_composing'),
    'experiments': ('paper_agent.experiments_composing', 'experiments_composing'),
    'conclusion': ('paper_agent.conclusion_composing', 'conclusion_composing'),
}


@click.group()
def cli():
    """Paper Agent - Autonomous academic paper generation."""
    pass


@cli.command()
@click.option('--research-field', '-f', required=True,
              type=click.Choice(RESEARCH_FIELDS),
              help='Research field/domain')
@click.option('--instance-id', '-i', required=True,
              help='Instance ID for the research task')
@click.option('--output-dir', '-o', default=None,
              help='Output directory (default: {field}/target_sections/{instance_id})')
def generate(research_field: str, instance_id: str, output_dir: str):
    """Generate a complete academic paper from research results."""
    from paper_agent.writing import writing

    click.echo(f"Generating paper for {research_field}/{instance_id}...")

    asyncio.run(writing(research_field, instance_id))

    output_path = output_dir or f"{research_field}/target_sections/{instance_id}"
    click.echo(f"Paper generated in: {output_path}")


@cli.command()
@click.option('--research-field', '-f', required=True,
              type=click.Choice(RESEARCH_FIELDS),
              help='Research field/domain')
@click.option('--instance-id', '-i', required=True,
              help='Instance ID for the research task')
@click.option('--section', '-s', required=True,
              type=click.Choice(list(SECTION_COMPOSERS.keys())),
              help='Section to generate')
def section(research_field: str, instance_id: str, section: str):
    """Generate a specific section of the paper."""
    import importlib

    click.echo(f"Generating {section} for {research_field}/{instance_id}...")

    module_name, func_name = SECTION_COMPOSERS[section]
    module = importlib.import_module(module_name)
    composer_func = getattr(module, func_name)

    asyncio.run(composer_func(research_field, instance_id))

    click.echo(f"Section {section} generated successfully.")


@cli.command()
def list_fields():
    """List available research fields and their templates."""
    click.echo("Available research fields:")
    for field in RESEARCH_FIELDS:
        field_path = PAPER_AGENT_DIR / field
        if field_path.exists():
            click.echo(f"  - {field}")
        else:
            click.echo(f"  - {field} (templates not found)")


if __name__ == '__main__':
    cli()
