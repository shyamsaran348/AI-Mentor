import json
from pathlib import Path
from build_context import build_project_context

def main():
    base_dir = Path(__file__).parent.parent
    project_dir = base_dir / "knowledge_packages" / "ai_project_5"
    train_file = base_dir / "datasets" / "train.jsonl"
    output_file = base_dir / "datasets" / "browser_prompt.txt"
    
    context_block = build_project_context(project_dir)
    
    # Load first 3 samples
    examples = []
    with open(train_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 3: break
            data = json.loads(line)
            examples.append(data)
            
    prompt = f"""I am building a fine-tuning dataset for an AI Capstone Mentor. I need you to generate exactly 20 new training samples in strict JSONL format. 

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks (no ```json). 
3. DO NOT include any conversational text, greetings, or explanations before or after the JSON. 
4. Each line must be a standalone JSON object starting with {{"messages": [ and ending with ]}}.

**THE PROJECT CONTEXT:**
{context_block}

**FEW-SHOT EXAMPLES (Mimic this exact tone and structure):**
{json.dumps(examples[0], indent=None)}
{json.dumps(examples[1], indent=None)}
{json.dumps(examples[2], indent=None)}

**GENERATION REQUIREMENTS FOR THE 20 NEW SAMPLES:**
Generate 20 brand new conversations. Every single `system` message MUST contain the exact Project Context block provided above. 
Distribute the 20 samples as follows:
- 6 Mentoring / Module Guidance
- 6 Troubleshooting (invent realistic student coding errors based on the context)
- 4 Viva / Academic Support
- 4 Context Discovery (student asks a vague question, mentor asks clarifying questions)

Begin outputting the raw JSONL now.
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
        
    print(f"Created browser prompt at {output_file}")

if __name__ == "__main__":
    main()
