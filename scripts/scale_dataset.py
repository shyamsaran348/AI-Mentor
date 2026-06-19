import json
import os
import random
import time
import requests
import subprocess
from pathlib import Path
from build_context import build_project_context

# Configuration
# Compatible with OpenAI, Groq, OpenRouter, Anthropic (with tweaks)
# Using standard OpenAI-compatible completions endpoint format as default
API_KEY = os.environ.get("LLM_API_KEY")
API_URL = os.environ.get("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions") 
MODEL_NAME = os.environ.get("LLM_MODEL", "llama3-70b-8192")

TARGET_SAMPLES = 200
BATCH_SIZE = 10 # Number of samples to generate per API call

def load_few_shot_examples(filepath):
    examples = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            # Find user and assistant turns
            user_msg = next(m["content"] for m in data["messages"] if m["role"] == "user")
            asst_msg = next(m["content"] for m in data["messages"] if m["role"] == "assistant")
            examples.append({"user": user_msg, "assistant": asst_msg})
    return examples

def generate_batch(context_block, category, few_shot_subset):
    if not API_KEY:
        print("Error: LLM_API_KEY environment variable is not set.")
        return []

    prompt = f"""
You are generating high-quality training data for an educational Capstone Mentor AI.
The AI is strictly bounded by the following project context. It must NEVER hallucinate facts outside this context.

{context_block}

TASK:
Generate {BATCH_SIZE} unique conversation pairs (user and assistant) for the category: {category}

Here are some good examples of the expected tone and format:
"""
    for ex in few_shot_subset:
        prompt += f"\nUser: {ex['user']}\nAssistant: {ex['assistant']}\n"
    
    prompt += f"""
RULES:
1. Ensure the user asks diverse, edge-case, and deeply technical questions related to the {category} category.
2. Ensure the assistant provides highly accurate mentoring guidance based solely on the context.
3. Return the response STRICTLY as a JSON array of objects. Do not include markdown formatting like ```json or any introductory text. 

Example Output Format:
[
  {{"user": "...", "assistant": "..."}},
  {{"user": "...", "assistant": "..."}}
]
"""

    if "generativelanguage.googleapis.com" in API_URL or "gemini" in MODEL_NAME.lower():
        # Gemini API format
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }
        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
            response.raise_for_status()
            result_text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        except Exception as e:
            print(f"Gemini API Error: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                print(f"Response: {response.text}")
            return []
    else:
        # Standard OpenAI-compatible format (Groq, OpenRouter, etc.)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "response_format": {"type": "json_object"} if "openai" in API_URL else None
        }
        if payload["response_format"] is None:
            del payload["response_format"]

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result_text = response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"API Error during batch generation: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                print(f"Response: {response.text}")
            return []
        
    # Cleanup potential markdown wrapper
    try:
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
            
        data = json.loads(result_text.strip())
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        elif isinstance(data, dict) and "conversations" in data:
             return data["conversations"]
        return data
    except Exception as e:
        print(f"JSON Parsing Error during batch generation: {e}")
        return []

def main():
    base_dir = Path(__file__).parent.parent
    project_dir = base_dir / "knowledge_packages" / "ai_project_5"
    datasets_dir = base_dir / "datasets"
    train_file = datasets_dir / "train.jsonl"
    
    # 1. Build context
    context_block = build_project_context(project_dir)
    system_prompt = "You are Capstone Mentor AI. Your responsibility is to mentor students using ONLY the provided project context. Do not invent project details. Use the provided context as the source of truth. If context is missing, ask clarifying questions. Behave like an educational mentor.\n\n" + context_block

    # 2. Load existing 20 samples to use as few-shot
    if not train_file.exists():
        print(f"Error: Base {train_file} not found. Run generate_dataset.py first.")
        return
        
    all_examples = load_few_shot_examples(train_file)
    current_count = len(all_examples)
    print(f"Loaded {current_count} existing samples as few-shot baseline.")

    needed = TARGET_SAMPLES - current_count
    if needed <= 0:
        print("Dataset already at or above target size.")
        return

    # Categories distribution
    categories = [
        {"name": "Mentoring / Module Guidance", "weight": 0.25},
        {"name": "Troubleshooting", "weight": 0.25},
        {"name": "Viva / Academic Support", "weight": 0.15},
        {"name": "Report Writing", "weight": 0.15},
        {"name": "Curriculum Mapping", "weight": 0.10},
        {"name": "Context Discovery / Clarification", "weight": 0.10}
    ]

    print(f"Generating {needed} new samples in batches of {BATCH_SIZE}...")
    
    generated_count = 0
    with open(train_file, 'a', encoding='utf-8') as f:
        while generated_count < needed:
            # Pick a category based on weight
            cat = random.choices(categories, weights=[c["weight"] for c in categories])[0]["name"]
            
            # Pick 3 random few-shot examples
            few_shot = random.sample(all_examples, min(3, len(all_examples)))
            
            print(f"Generating batch for '{cat}'...")
            new_samples = generate_batch(context_block, cat, few_shot)
            
            for s in new_samples:
                if "user" in s and "assistant" in s:
                    # Inject system prompt
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": s["user"]},
                        {"role": "assistant", "content": s["assistant"]}
                    ]
                    f.write(json.dumps({"messages": messages}) + "\n")
                    f.flush()
                    generated_count += 1
                    if generated_count >= needed:
                        break
            
            # Rate limiting sleep
            time.sleep(2)

    print(f"\nSuccessfully appended {generated_count} new samples to {train_file}")
    
    # 3. Validate
    print("Running validation...")
    val_script = base_dir / "scripts" / "validate_dataset.py"
    subprocess.run(["python3", str(val_script)])

if __name__ == "__main__":
    main()
