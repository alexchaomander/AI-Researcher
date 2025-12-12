import os
import json
import tarfile
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from research_agent.inno.registry import register_tool
from research_agent.inno.environment.docker_env import DockerEnv
from research_agent.constant import GITHUB_AI_TOKEN


@register_tool("clone_repo")
def clone_repo(repo_url: str, env: DockerEnv, dest_dir: Optional[str] = None, branch: Optional[str] = None) -> str:
    """
    Clone a git repository into the working directory.
    Args:
        repo_url: HTTPS git URL (GitHub supported). If a PAT is available, it will be used.
        dest_dir: Optional destination directory name under the current working dir.
        branch: Optional branch name.
    """
    try:
        target = dest_dir or Path(repo_url).stem.replace(".git", "")
        token = os.getenv("GITHUB_AI_TOKEN", GITHUB_AI_TOKEN or "")
        url = repo_url
        if token and "github.com" in repo_url and "@" not in repo_url:
            url = repo_url.replace("https://", f"https://{token}@")
        branch_flag = f"-b {branch}" if branch else ""
        cmd = f"cd {env.docker_workplace} && git clone {branch_flag} {url} {target}"
        return env.run_command(cmd)
    except Exception as e:
        return f"Error cloning repo: {e}"


@register_tool("download_repo_tar")
def download_repo_tar(repo_url: str, env: DockerEnv, dest_dir: Optional[str] = None) -> str:
    """
    Download a repository as a tarball (works for GitHub HTTPS URLs) and extract it.
    Useful when git/pat is unavailable. Uses curl + tar inside the sandbox.
    """
    try:
        target = dest_dir or Path(repo_url).stem
        workdir = Path(env.docker_workplace)
        tar_path = workdir / f"{target}.tar.gz"
        # GitHub tarball URL heuristic
        tar_url = repo_url.rstrip("/").replace(".git", "") + "/archive/refs/heads/main.tar.gz"
        cmd = f"cd {workdir} && curl -L '{tar_url}' -o {tar_path.name} && tar -xzf {tar_path.name} && rm {tar_path.name}"
        resp = env.run_command(cmd)
        return resp
    except Exception as e:
        return f"Error downloading tarball: {e}"


@register_tool("download_hf_dataset")
def download_hf_dataset(dataset_id: str, env: DockerEnv, split: str = "train", limit: Optional[int] = None, local_dir: str = "datasets") -> str:
    """
    Download a Hugging Face dataset to a local directory inside the sandbox.
    Args:
        dataset_id: e.g., 'HuggingFaceH4/MATH-500'
        split: dataset split to load
        limit: optional number of examples to save
        local_dir: relative dir under /workplace to store data
    """
    try:
        py_cmd = f"""
import json
from datasets import load_dataset
from pathlib import Path
ds = load_dataset("{dataset_id}", split="{split}")
if {limit}:
    ds = ds.select(range({limit}))
out_dir = Path("{env.docker_workplace}") / "{local_dir}" / "{dataset_id.replace('/', '_')}"
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "data.jsonl"
ds.to_json(out_path)
print(f"saved {{len(ds)}} records to {{out_path}}")
"""
        cmd = f"python - <<'PY'\n{py_cmd}\nPY"
        return env.run_command(cmd)
    except Exception as e:
        return f"Error downloading dataset: {e}"


@register_tool("pdf_to_markdown")
def pdf_to_markdown(pdf_path: str, env: DockerEnv, max_pages: int = 5) -> str:
    """
    Convert a PDF to markdown using docling (first N pages to keep output small).
    """
    try:
        py_cmd = f"""
import sys
from pathlib import Path
from docling.document_converter import DocumentConverter

pdf = Path("{pdf_path}")
if not pdf.exists():
    print(f"File not found: {{pdf}}")
    sys.exit(1)
converter = DocumentConverter()
result = converter.convert(pdf)
md = result.document.export_to_markdown()
pages = md.split("\\f")
md_out = "\\n\\n".join(pages[:{max_pages}])
print(md_out[:8000])
"""
        cmd = f"python - <<'PY'\n{py_cmd}\nPY"
        return env.run_command(cmd)
    except Exception as e:
        return f"Error converting PDF: {e}"
