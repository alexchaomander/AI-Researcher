"""
AI-Researcher CLI - Main entry point for autonomous research tasks.
"""
import click
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)


@click.group()
@click.version_option(version='0.2.0', prog_name='ai-researcher')
def cli():
    """AI-Researcher - Autonomous Scientific Innovation System.

    A system that automates the entire research lifecycle from literature
    review to paper writing.
    """
    pass


@cli.command()
@click.option('--category', '-c', required=True,
              type=click.Choice(['vq', 'gnn', 'reasoning', 'recommendation', 'diffu_flow']),
              help='Research category')
@click.option('--instance-id', '-i', required=True,
              help='Instance ID of the benchmark task')
@click.option('--model', '-m', default=None,
              help='LLM model to use (default: from COMPLETION_MODEL env var)')
@click.option('--task-level', '-l', default='task1',
              type=click.Choice(['task1', 'task2']),
              help='Task level: task1 (detailed idea) or task2 (reference-based)')
@click.option('--port', '-p', default=12380,
              help='Port for Docker communication')
@click.option('--max-iter', default=0,
              help='Maximum iteration times (0 for unlimited)')
@click.option('--no-docker', is_flag=True,
              help='Run without Docker container')
def run(category: str, instance_id: str, model: str, task_level: str,
        port: int, max_iter: int, no_docker: bool):
    """Run an autonomous research task.

    Example:
        ai-researcher run -c vq -i one_layer_vq -l task1
    """
    from research_agent.constant import COMPLETION_MODEL

    model = model or COMPLETION_MODEL
    instance_path = f"benchmark/final/{category}/{instance_id}.json"

    # Check if instance exists
    full_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        instance_path
    )
    if not os.path.exists(full_path):
        click.echo(f"Error: Task not found: {instance_path}")
        click.echo(f"Run 'ai-researcher list -c {category}' to see available tasks.")
        sys.exit(1)

    click.echo(f"Starting AI-Researcher task:")
    click.echo(f"  Category: {category}")
    click.echo(f"  Instance: {instance_id}")
    click.echo(f"  Level: {task_level}")
    click.echo(f"  Model: {model}")
    click.echo(f"  Docker: {'disabled' if no_docker else 'enabled'}")
    click.echo("")

    if no_docker:
        os.environ['USE_DOCKER'] = 'false'

    # Change to research_agent directory
    research_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(research_dir)

    if task_level == 'task1':
        from research_agent.run_infer_plan import main
        main(
            instance_path=f"../{instance_path}",
            container_name='ai_researcher',
            task_level='task1',
            model=model,
            workplace_name='workplace',
            cache_path='cache',
            port=port,
            max_iter_times=max_iter,
            category=category
        )
    else:
        from research_agent.run_infer_idea import main
        main(
            instance_path=f"../{instance_path}",
            container_name='ai_researcher',
            model=model,
            workplace_name='workplace',
            cache_path='cache',
            port=port,
            max_iter_times=max_iter,
            category=category
        )


@cli.command()
@click.option('--category', '-c', default=None,
              type=click.Choice(['vq', 'gnn', 'reasoning', 'recommendation', 'diffu_flow']),
              help='Filter by category')
def list(category: str):
    """List available benchmark tasks."""
    benchmark_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'benchmark', 'final'
    )

    if not os.path.exists(benchmark_dir):
        click.echo("Benchmark directory not found.")
        return

    categories = [category] if category else os.listdir(benchmark_dir)

    for cat in categories:
        cat_path = os.path.join(benchmark_dir, cat)
        if not os.path.isdir(cat_path):
            continue

        tasks = [f[:-5] for f in os.listdir(cat_path) if f.endswith('.json')]
        click.echo(f"\n{cat}/ ({len(tasks)} tasks)")
        for task in sorted(tasks):
            click.echo(f"  - {task}")


@cli.command()
def config():
    """Show current configuration."""
    from research_agent.constant import (
        COMPLETION_MODEL, CHEEP_MODEL, EMBEDDING_MODEL,
        API_BASE_URL, BASE_IMAGES, GPUS
    )

    click.echo("Current AI-Researcher Configuration:")
    click.echo(f"  Completion Model: {COMPLETION_MODEL}")
    click.echo(f"  Cheap Model: {CHEEP_MODEL}")
    click.echo(f"  Embedding Model: {EMBEDDING_MODEL}")
    click.echo(f"  API Base URL: {API_BASE_URL or 'default'}")
    click.echo(f"  Docker Image: {BASE_IMAGES}")
    click.echo(f"  GPUs: {GPUS}")

    # Check API key status
    api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
    click.echo(f"  API Key: {'configured' if api_key else 'NOT SET'}")

    ollama = os.getenv('OLLAMA_BASE_URL')
    click.echo(f"  Ollama: {ollama or 'not configured'}")


@cli.command()
def doctor():
    """Check system requirements and configuration."""
    import shutil

    click.echo("AI-Researcher System Check")
    click.echo("=" * 40)

    # Python version
    py_version = sys.version.split()[0]
    py_ok = py_version.startswith('3.11') or py_version.startswith('3.12') or py_version.startswith('3.13')
    click.echo(f"Python: {py_version} {'OK' if py_ok else 'WARNING (3.11 recommended)'}")

    # Docker
    docker = shutil.which('docker')
    click.echo(f"Docker: {'found' if docker else 'NOT FOUND'}")

    # API Keys
    openrouter = bool(os.getenv('OPENROUTER_API_KEY'))
    openai = bool(os.getenv('OPENAI_API_KEY'))
    click.echo(f"OpenRouter API Key: {'configured' if openrouter else 'not set'}")
    click.echo(f"OpenAI API Key: {'configured' if openai else 'not set'}")

    # Ollama
    ollama_url = os.getenv('OLLAMA_BASE_URL')
    if ollama_url:
        import requests
        try:
            resp = requests.get(f"{ollama_url}/api/version", timeout=2)
            click.echo(f"Ollama: running (v{resp.json().get('version', 'unknown')})")
        except:
            click.echo(f"Ollama: configured but not responding at {ollama_url}")
    else:
        click.echo("Ollama: not configured")

    # Key dependencies
    click.echo("\nKey Dependencies:")
    deps = ['litellm', 'chromadb', 'playwright', 'gradio']
    for dep in deps:
        try:
            __import__(dep)
            click.echo(f"  {dep}: OK")
        except ImportError:
            click.echo(f"  {dep}: NOT INSTALLED")

    click.echo("\n" + "=" * 40)
    if (openrouter or openai) and py_ok:
        click.echo("System is ready to run AI-Researcher!")
    else:
        click.echo("Please address the issues above before running.")


if __name__ == '__main__':
    cli()
