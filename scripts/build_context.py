import json
import os
from pathlib import Path

def build_project_context(project_dir):
    """
    Reads the 6 JSON files from the project directory and builds the consolidated context block.
    """
    project_dir = Path(project_dir)
    
    def load_json(filename):
        filepath = project_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    summary = load_json('project_summary.json')
    metadata = load_json('metadata.json')
    architecture = load_json('architecture.json')
    modules = load_json('modules.json')
    technologies = load_json('technologies.json')
    troubleshooting = load_json('troubleshooting.json')
    viva = load_json('viva.json')

    # Build the context block
    context_lines = []
    context_lines.append("[PROJECT CONTEXT START]")
    
    # Project Name and Domain
    context_lines.append(f"Project Name: {metadata.get('project_name', 'Unknown')}")
    context_lines.append(f"Domain: {metadata.get('domain', 'Unknown')}")
    context_lines.append(f"Objective: {summary.get('Objective', '')}")
    
    # Architecture
    official_arch = architecture.get('Official Architecture (Derived from Project Document)', '')
    suggested_arch = architecture.get('Suggested Implementation (For Mentoring Guidance)', '')
    context_lines.append(f"Architecture (Official): {official_arch}")
    context_lines.append(f"Architecture (Suggested): {suggested_arch}")
    
    # Modules
    mods = modules.get('modules', [])
    mod_strings = [f"{m['module_id']}. {m['name']}" for m in mods]
    context_lines.append(f"Modules: {', '.join(mod_strings)}")
    
    # Technologies
    techs = []
    for category, items in technologies.items():
        if category.lower() == "overview": continue
        # Items are newline separated strings with bullets, let's clean them up
        cleaned_items = [i.replace('* ', '').strip() for i in items.split('\n') if i.strip()]
        techs.extend(cleaned_items)
    context_lines.append(f"Technologies: {', '.join(techs)}")
    
    # Troubleshooting
    issues = []
    for issue_title, issue_content in troubleshooting.items():
        if issue_title.lower() == "overview": continue
        issues.append(f"{issue_title}: {issue_content.split('Solution:')[1].strip() if 'Solution:' in issue_content else issue_content}")
    context_lines.append(f"Troubleshooting: {'; '.join(issues)}")
    
    # Viva
    questions = []
    for q, a in viva.items():
        if q.lower() == "overview": continue
        questions.append(f"{q} - {a}")
    context_lines.append(f"Viva: {'; '.join(questions)}")
    
    context_lines.append("[PROJECT CONTEXT END]")
    
    return "\n".join(context_lines)

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    context = build_project_context(base_dir / "knowledge_packages" / "ai_project_5")
    print(context)
