#!/bin/bash
# Level 1: Detailed Idea Description Task
# Provide comprehensive descriptions of specific research ideas

set -e

current_dir=$(dirname "$(readlink -f "$0")")
cd "$current_dir"

# Load environment variables from .env if it exists
if [ -f "../.env" ]; then
    set -a
    source "../.env"
    set +a
fi

# Set defaults if not provided in .env
export DOCKER_WORKPLACE_NAME="${DOCKER_WORKPLACE_NAME:-workplace_paper}"
export BASE_IMAGES="${BASE_IMAGES:-ai-researcher-sandbox:latest}"
export COMPLETION_MODEL="${COMPLETION_MODEL:-openrouter/google/gemini-2.5-pro-preview-05-20}"
export CHEEP_MODEL="${CHEEP_MODEL:-openrouter/google/gemini-2.5-pro-preview-05-20}"
export GPUS="${GPUS:-\"device=0\"}"

# Task configuration - override these as needed
category="${CATEGORY:-vq}"
instance_id="${INSTANCE_ID:-one_layer_vq}"
port="${PORT:-12380}"
max_iter="${MAX_ITER_TIMES:-0}"

echo "Running Level 1 (Detailed Idea) task:"
echo "  Category: $category"
echo "  Instance: $instance_id"
echo "  Model: $COMPLETION_MODEL"
echo "  Docker Image: $BASE_IMAGES"
echo ""

python run_infer_plan.py \
    --instance_path "../benchmark/final/${category}/${instance_id}.json" \
    --container_name test_eval \
    --task_level task1 \
    --model "$COMPLETION_MODEL" \
    --workplace_name workplace \
    --cache_path cache \
    --port "$port" \
    --max_iter_times "$max_iter" \
    --category "${category}"
