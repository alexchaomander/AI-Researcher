"""
Benchmark Collection CLI - Tools for creating and managing research benchmarks.
"""
import click
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@click.group()
def cli():
    """Benchmark Collection - Create and manage research benchmarks."""
    pass


@cli.command()
@click.option('--query', '-q', required=True,
              help='Search query for papers')
@click.option('--max-results', '-n', default=100,
              help='Maximum number of results to fetch')
@click.option('--output', '-o', default='papers.json',
              help='Output file for results')
def crawl(query: str, max_results: int, output: str):
    """Crawl papers from arXiv based on search query."""
    click.echo(f"Crawling papers for query: {query}")
    click.echo(f"Max results: {max_results}")

    # Change to benchmark_collection directory
    benchmark_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(benchmark_dir)

    # Import and run crawler
    try:
        from benchmark_collection import utils
        click.echo("Crawler functionality available. Run 0_crawl_paper.py directly for full features.")
    except ImportError as e:
        click.echo(f"Note: Some dependencies may be missing: {e}")

    click.echo(f"Output will be saved to: {output}")


@cli.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input JSON file with paper data')
@click.option('--output', '-o', default='innovation_graph',
              help='Output directory for innovation graph')
def create_graph(input_file: str, output: str):
    """Create an innovation graph from crawled papers."""
    click.echo(f"Creating innovation graph from: {input_file}")
    click.echo(f"Output directory: {output}")

    # Change to benchmark_collection directory
    benchmark_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(benchmark_dir)

    click.echo("Graph creation functionality available. Run 1_create_inno_graph.py directly for full features.")


@cli.command()
def list_benchmarks():
    """List available benchmark configurations."""
    benchmark_final = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'benchmark', 'final'
    )

    if not os.path.exists(benchmark_final):
        click.echo("Benchmark directory not found.")
        return

    click.echo("Available benchmark categories:")
    for category in os.listdir(benchmark_final):
        category_path = os.path.join(benchmark_final, category)
        if os.path.isdir(category_path):
            tasks = [f for f in os.listdir(category_path) if f.endswith('.json')]
            click.echo(f"\n  {category}/ ({len(tasks)} tasks)")
            for task in sorted(tasks)[:5]:
                click.echo(f"    - {task}")
            if len(tasks) > 5:
                click.echo(f"    ... and {len(tasks) - 5} more")


@cli.command()
@click.argument('category')
@click.argument('task_id')
def show(category: str, task_id: str):
    """Show details of a specific benchmark task."""
    import json

    benchmark_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'benchmark', 'final', category, f'{task_id}.json'
    )

    if not os.path.exists(benchmark_path):
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
