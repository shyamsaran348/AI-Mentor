import json
import sys
from pathlib import Path

def validate_jsonl(file_path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return False
        
    line_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_count += 1
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {line_count}: Invalid JSON. Error: {e}")
                return False
                
            if "messages" not in data:
                print(f"Line {line_count}: Missing 'messages' key in JSON object.")
                return False
                
            messages = data["messages"]
            if not isinstance(messages, list):
                print(f"Line {line_count}: 'messages' must be a list.")
                return False
                
            if len(messages) < 3:
                print(f"Line {line_count}: Each conversation must have at least a system, user, and assistant message.")
                return False
                
            # Verify the first message is the system prompt and contains context
            if messages[0].get("role") != "system":
                print(f"Line {line_count}: First message must have role 'system'.")
                return False
                
            sys_content = messages[0].get("content", "")
            if "[PROJECT CONTEXT START]" not in sys_content or "[PROJECT CONTEXT END]" not in sys_content:
                print(f"Line {line_count}: System prompt is missing the injected [PROJECT CONTEXT].")
                return False
                
    print(f"Success: {file_path} is valid JSONL format. Verified {line_count} samples.")
    return True

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    target_file = base_dir / "datasets" / "train.jsonl"
    if not validate_jsonl(target_file):
        sys.exit(1)
