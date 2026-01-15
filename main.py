from dotenv import load_dotenv
import os
import argparse
from agent import Agent
from utils import scan_codebase
import json

# Load environment variables from .env if present
load_dotenv()

# Get base_url and api_key from environment, with defaults
BASE_URL = os.getenv('AI_API_ENDPOINT', 'https://api.llm7.io/v1')
API_KEY = os.getenv('AI_API_KEY', 'unused')

broken_access_control_system = """You are a very experienced cyber security code reviewer, you are very skilled to spot broken access control vulnerabilities based on application flow. Your task is to find broken access control vulnerabilities. Report it in the format of Name, Summary, Vulnerable Code."""
business_logic_system = """You are a very experienced cyber security code reviewer, you are very skilled to spot business logic vulnerabilities based on application flow in banking application. Your task is to find business logic vulnerabilities. Report it in the format of Name, Summary, Vulnerable Code."""

def main():
    parser = argparse.ArgumentParser(description="SAST LLM Multi-Agent Scanner")
    parser.add_argument('--scan-path', '-s', type=str, required=True, help='Path to the codebase to scan (absolute or relative)')
    args = parser.parse_args()

    # Use the provided path, resolve to absolute if needed
    if os.path.isabs(args.scan_path):
        project_root = args.scan_path
    else:
        project_root = os.path.abspath(args.scan_path)

    user_message = scan_codebase(project_root)

    # Instantiate agents
    analyzer = Agent(
        model="default",
        system_message=business_logic_system,
        base_url=BASE_URL,
        api_key=API_KEY
    )

    analyzer_reply = analyzer.chat(user_message)
    print("Analyzer findings:")
    print(analyzer_reply)

if __name__ == "__main__":
    main()
