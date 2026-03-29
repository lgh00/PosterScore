import os
import argparse
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

def extract_txt_figure(paper_path: str, model: str):
    """
    Extract text and figure from the paper pdf file.
    """
    pass


def main():
    parser = argparse.ArgumentParser(description = "PosterScore: A tool to score posters")
    parser.add_argument("--paper_path", type=str, required=True, help="Path to the paper pdf file")
    parser.add_argument("--poster_path", type=str, required=True, help = "Path to the poster's image file")
    parser.add_argument("--model", type=str, default="doubao-seed-2-0-lite-260215", choices=["doubao-seed-2-0-lite-260215", "gpt-4o-2024-08-06", "gpt-4.1-2025-04-14", "gpt-4.1-mini-2025-04-14", "claude-sonnet-4-20250514", "claude-opus-4.5", "gemini-2.5-pro", "glm-4.6v", "glm-4.5v", "glm-4v", "moonshot-v1-8k-vision-preview", "MiniMax-M2", "qwen3-vl-plus"], help="model to score the poster")
    args = parser.parse_args()
    # check .env file
    if not env_path.exists():
        raise ValueError(f"Please set .env file {env_path}")
    # check paper path
    if not Path(args.paper_path).exists():
        raise ValueError(f"Please set paper path {args.paper_path}")
    # check poster path
    if not Path(args.poster_path).exists():
        raise ValueError(f"Please set poster path {args.poster_path}")

    # check api key
    required_keys = {"ark": "ARK_API_KEY", "openai": "OPENAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GOOGLE_API_KEY", "zhipu": "ZHIPU_API_KEY", "moonshot": "MOONSHOT_API_KEY", "Minimax": "MINIMAX_API_KEY", "Alibaba": "ALIBABA_API_KEY"}
    model_providers = {"doubao-seed-2-0-lite-260215": "ark","claude-sonnet-4-20250514": "anthropic", "claude-opus-4.5": "anthropic", "claude-opus-4-5-20251101": "anthropic", "gemini": "google", "gemini-2.5-pro": "google", "gpt-4o-2024-08-06": "openai", "gpt-4.1-2025-04-14": "openai", "gpt-4.1-mini-2025-04-14": "openai","glm-4.6": "zhipu", "glm-4.6v": "zhipu", "glm-4.5": "zhipu", "glm-4.5-air": "zhipu", "glm-4.5v": "zhipu", "glm-4": "zhipu", "glm-4v": "zhipu","kimi-k2-turbo-preview": "moonshot", "moonshot-v1-8k-vision-preview": "moonshot","qwen3-max": "Alibaba", "qwen3-vl-plus": "Alibaba","MiniMax-M2":"Minimax"}

    need_key = required_keys[model_providers[args.model]]
    if not os.getenv(need_key):
        raise ValueError(f"Please set {need_key}")
    
    extract_txt_figure(args.paper_path, args.model)
    print(args)

if __name__ == "__main__":
    main()