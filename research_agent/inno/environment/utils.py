from research_agent.inno.util import run_command_in_container
from research_agent.constant import DOCKER_WORKPLACE_NAME
import os
import shutil

def setup_metachain():
    cmd = "pip list | grep metachain"
    response = run_command_in_container(cmd)
    if response['status'] == 0:
        print("Metachain is already installed.")
        return
    cmd = f"cd /{DOCKER_WORKPLACE_NAME}/metachain && pip install -e ."
    response = run_command_in_container(cmd)
    if response['status'] == 0:
        print("Metachain is installed.")
        return
    else:
        raise Exception(f"Failed to install metachain. {response['result']}")


def setup_dataset(category: str, local_workplace: str):
    # 构建目标路径
    dataset_candidate_path = os.path.join(local_workplace, "dataset_candidate")
    force = os.getenv("FORCE_DATASET_SETUP", "false").lower() in {"1", "true", "yes", "on"}
    
    # 检查目标目录是否存在
    if os.path.exists(dataset_candidate_path):
        if not force:
            print("dataset_candidate exists")
            return {
                "copied": False,
                "source_path": None,
                "dest_path": dataset_candidate_path,
                "skipped": True,
                "reason": "already_exists",
            }
        shutil.rmtree(dataset_candidate_path)
    
    # 检查源目录是否存在
    source_path = os.path.normpath(os.path.join(os.path.dirname(__file__), f"../../benchmark/process/dataset_candidate/{category}"))
    if not os.path.exists(source_path):
        print(f"warning: dataset source path {source_path} not found; skipping dataset setup")
        return {
            "copied": False,
            "source_path": source_path,
            "dest_path": dataset_candidate_path,
            "warning": "source_path_missing",
        }
    
    try:
        # 复制整个目录内容到 dataset_candidate
        shutil.copytree(source_path, dataset_candidate_path)
        print(f"copy {source_path} to {dataset_candidate_path} success")
        return {
            "copied": True,
            "source_path": source_path,
            "dest_path": dataset_candidate_path,
        }
    except Exception as e:
        raise Exception(f"copy {source_path} to {dataset_candidate_path} failed: {str(e)}")


def dataset_integrity_report(local_workplace: str):
    dataset_candidate_path = os.path.join(local_workplace, "dataset_candidate")
    if not os.path.exists(dataset_candidate_path):
        return {
            "exists": False,
            "path": dataset_candidate_path,
            "files": 0,
            "total_bytes": 0,
            "has_metaprompt": False,
        }
    total_files = 0
    total_bytes = 0
    has_metaprompt = False
    for root, _, files in os.walk(dataset_candidate_path):
        for filename in files:
            total_files += 1
            full_path = os.path.join(root, filename)
            try:
                total_bytes += os.path.getsize(full_path)
            except OSError:
                continue
            if filename == "metaprompt.py":
                has_metaprompt = True
    return {
        "exists": True,
        "path": dataset_candidate_path,
        "files": total_files,
        "total_bytes": total_bytes,
        "has_metaprompt": has_metaprompt,
    }
