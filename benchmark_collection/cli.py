"""
Benchmark Collection CLI - Tools for creating and managing research benchmarks.
"""
import click
import json
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
BENCHMARK_DIR = PROJECT_ROOT / 'benchmark' / 'final'


@click.group()
def cli():
    """Benchmark Collection - Create and manage research benchmarks."""
    pass


@cli.command()
def list_benchmarks():
    """List available benchmark configurations."""
    if not BENCHMARK_DIR.exists():
        click.echo("Benchmark directory not found.")
        return

    click.echo("Available benchmark categories:")
    for category_path in sorted(BENCHMARK_DIR.iterdir()):
        if category_path.is_dir():
            tasks = list(category_path.glob('*.json'))
            click.echo(f"\n  {category_path.name}/ ({len(tasks)} tasks)")
            for task in sorted(tasks)[:5]:
                click.echo(f"    - {task.name}")
            if len(tasks) > 5:
                click.echo(f"    ... and {len(tasks) - 5} more")


@cli.command()
@click.argument('category')
@click.argument('task_id')
def show(category: str, task_id: str):
    """Show details of a specific benchmark task."""
    benchmark_path = BENCHMARK_DIR / category / f'{task_id}.json'

    if not benchmark_path.exists():
        click.echo(f"Task not found: {category}/{task_id}")
        return

    with open(benchmark_path, 'r') as f:
        task = json.load(f)

    click.echo(f"\nTask: {task.get('instance_id', task_id)}")
    click.echo(f"Target: {task.get('target', 'N/A')[:100]}...")
    click.echo(f"Authors: {', '.join(task.get('authors', []))}")
    click.echo(f"Year: {task.get('year', 'N/A')}")
    click.echo(f"URL: {task.get('url', 'N/A')}")

    source_papers = task.get('source_papers', [])
    click.echo(f"\nSource Papers: {len(source_papers)}")
    for i, paper in enumerate(source_papers[:3], 1):
        click.echo(f"  {i}. {paper.get('reference', 'Unknown')}")

    click.echo(f"\nTask 1 (Detailed Idea): {task.get('task1', 'N/A')[:100]}...")
    click.echo(f"Task 2 (Reference-Based): {task.get('task2', 'N/A')[:100]}...")


if __name__ == '__main__':
    cli()
