import os
from dotenv import load_dotenv
import global_state

load_dotenv()  # 加载.env文件
# utils: 
def str_to_bool(value):
    """convert string to bool"""
    true_values = {'true', 'yes', '1', 'on', 't', 'y'}
    false_values = {'false', 'no', '0', 'off', 'f', 'n'}
    
    if isinstance(value, bool):
        return value
        
    if not value:
        return False
        
    value = str(value).lower().strip()
    if value in true_values:
        return True
    if value in false_values:
        return False
    return True  # default return True


DOCKER_WORKPLACE_NAME = os.getenv('DOCKER_WORKPLACE_NAME', 'workplace_meta')
GITHUB_AI_TOKEN = os.getenv('GITHUB_AI_TOKEN', None)
AI_USER = os.getenv('AI_USER', "ai-sin")
LOCAL_ROOT = os.getenv('LOCAL_ROOT', os.getcwd())

DEBUG = str_to_bool(os.getenv('DEBUG', True))

DEFAULT_LOG = str_to_bool(os.getenv('DEFAULT_LOG', True))
LOG_PATH = os.getenv('LOG_PATH', None)
LOG_PATH = global_state.LOG_PATH
EVAL_MODE = str_to_bool(os.getenv('EVAL_MODE', False))
BASE_IMAGES = os.getenv('BASE_IMAGES', "ai-researcher-sandbox:latest")

COMPLETION_MODEL = os.getenv('COMPLETION_MODEL', "gpt-4o-2024-08-06") # gpt-4o-2024-08-06

def _default_embedding_model() -> str:
    """
    Prefer provider-compatible defaults:
    - Ollama endpoint configured -> local-friendly Gemma.
    - OpenRouter configured -> Qwen embeddings via OpenRouter.
    - Otherwise -> OpenAI-native fallback.
    """
    if os.getenv("OLLAMA_BASE_URL"):
        return "embeddinggemma:latest"
    if os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_BASE"):
        return "qwen/qwen3-embedding-8b"
    return "text-embedding-3-small"

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', _default_embedding_model())
CHEEP_MODEL = os.getenv('CHEEP_MODEL', "gpt-4o-mini-2024-07-18")
# BASE_URL = os.getenv('BASE_URL', None)

# GPUS = os.getenv('GPUS', "all")
GPUS = os.getenv('GPUS', None)
def _default_platform() -> str:
    arch = os.uname().machine.lower()
    if arch in ("arm64", "aarch64"):
        return "linux/arm64/v8"
    return "linux/amd64"

PLATFORM = os.getenv('PLATFORM', _default_platform())
USE_DOCKER = str_to_bool(os.getenv('USE_DOCKER', False))
USE_BROWSER_ENV = str_to_bool(os.getenv('USE_BROWSER_ENV', False))

FN_CALL = str_to_bool(os.getenv('FN_CALL', True))
API_BASE_URL = os.getenv('API_BASE_URL', None)
API_BASE_URL = os.getenv('OPENROUTER_API_BASE', API_BASE_URL)
API_BASE_URL = os.getenv('OPENAI_BASE_URL', API_BASE_URL)
ADD_USER = str_to_bool(os.getenv('ADD_USER', False))

NON_FN_CALL = str_to_bool(os.getenv('NON_FN_CALL', False))

NOT_SUPPORT_SENDER = ["mistral", "groq"]


MUST_ADD_USER = ["deepseek/deepseek-reasoner", "o1-mini"]
NOT_SUPPORT_FN_CALL = ["o1-mini", "deepseek/deepseek-reasoner"]
NOT_USE_FN_CALL = [ "deepseek/deepseek-chat"] + NOT_SUPPORT_FN_CALL

if EVAL_MODE:
    DEFAULT_LOG = False

_openrouter_key = os.getenv("OPENROUTER_API_KEY")
_openai_key = os.getenv("OPENAI_API_KEY")
if _openrouter_key and not _openai_key:
    # Provide OpenRouter key to OpenAI-compatible SDKs when a direct OpenAI key is absent.
    os.environ["OPENAI_API_KEY"] = _openrouter_key
if not API_BASE_URL and _openrouter_key:
    API_BASE_URL = "https://openrouter.ai/api/v1"


def get_llm_api_key() -> str | None:
    """Return an API key, preferring OPENAI_API_KEY then OPENROUTER_API_KEY."""
    return os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")

# if "deepseek" in COMPLETION_MODEL:
#     os.environ["http_proxy"] = "http://127.0.0.1:7890"
#     os.environ["https_proxy"] = "http://127.0.0.1:7890"
