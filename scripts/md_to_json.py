import os
import json
from pathlib import Path
import re

def parse_markdown_to_dict(md_content):
    """
    Very basic markdown parser that splits content by H2 (##) headers.
    The text before the first H2 is stored under 'Overview'.
    """
    lines = md_content.split('\n')
    parsed_data = {}
    current_key = "Overview"
    current_content = []

    for line in lines:
        if line.startswith("## "):
            parsed_data[current_key] = "\n".join(current_content).strip()
            current_key = line.replace("## ", "").strip()
            current_content = []
        else:
            current_content.append(line)
            
    parsed_data[current_key] = "\n".join(current_content).strip()
    
    # Remove empty keys if any
    if "Overview" in parsed_data and not parsed_data["Overview"]:
        del parsed_data["Overview"]
        
    return parsed_data

def main():
    project_dir = Path(__file__).parent.parent / "knowledge_packages" / "ai_project_5"
    if not project_dir.exists():
        print(f"Directory not found: {project_dir}")
        return

    md_files = [
        "project_summary.md",
        "architecture.md",
        "modules.md",
        "technologies.md",
        "troubleshooting.md",
        "viva.md"
    ]

    for md_file in md_files:
        md_path = project_dir / md_file
        if not md_path.exists():
            print(f"File not found: {md_path}")
            continue

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        json_data = parse_markdown_to_dict(content)
        
        json_file = md_file.replace(".md", ".json")
        json_path = project_dir / json_file
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
            
        print(f"Converted {md_file} -> {json_file}")

if __name__ == "__main__":
    main()
