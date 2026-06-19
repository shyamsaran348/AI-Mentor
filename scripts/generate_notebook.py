import json

cells = []

def add_md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(text):
    cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in text.split("\n")]})

add_md("# Phase 3: Capstone Mentor AI Fine-Tuning\nThis notebook fine-tunes the Qwen 2.5 7B Instruct model using your `train.jsonl` dataset.\n\n### Step 1: Install Dependencies\nWe use Unsloth because it makes training twice as fast and uses significantly less memory.")
add_code("!pip install \"unsloth[kaggle-new] @ git+https://github.com/unslothai/unsloth.git\"")

add_md("### Step 2: Load the Base Model from Hugging Face\nThis downloads the 15GB model directly to Kaggle's servers in about 60 seconds.")
add_code("from unsloth import FastLanguageModel\nimport torch\n\nmax_seq_length = 2048 # Good for our prompt length\n\nmodel, tokenizer = FastLanguageModel.from_pretrained(\n    model_name = \"unsloth/Qwen2.5-7B-Instruct-bnb-4bit\", # 4-bit compressed version\n    max_seq_length = max_seq_length,\n    dtype = None,\n    load_in_4bit = True,\n)\n\n# Configure LoRA Adapters (which layers to train)\nmodel = FastLanguageModel.get_peft_model(\n    model,\n    r = 16,\n    target_modules = [\"q_proj\", \"k_proj\", \"v_proj\", \"o_proj\", \"gate_proj\", \"up_proj\", \"down_proj\"],\n    lora_alpha = 16,\n    lora_dropout = 0,\n    bias = \"none\",\n    use_gradient_checkpointing = \"unsloth\",\n    random_state = 3407,\n    use_rslora = False,\n    loftq_config = None,\n)")

add_md("### Step 3: Load and Format the Dataset\nUpload your `train.jsonl` file to Kaggle, then run this cell.")
add_code("from datasets import load_dataset\nfrom unsloth.chat_templates import get_chat_template\n\n# Ensure you uploaded train.jsonl to the Kaggle working directory!\ndataset = load_dataset(\"json\", data_files=\"/kaggle/input/datasets/shyamsaranp/fine-tune-data/train.jsonl\", split=\"train\")\n\ntokenizer = get_chat_template(\n    tokenizer,\n    chat_template = \"chatml\", # Qwen uses ChatML format\n)\n\ndef format_chat_template(examples):\n    texts = [tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=False) for msg in examples[\"messages\"]]\n    return {\"text\": texts}\n\ndataset = dataset.map(format_chat_template, batched=True)\nprint(f\"Loaded and formatted {len(dataset)} samples successfully!\")")

add_md("### Step 4: Start Fine-Tuning\nThis will take roughly **5 to 10 minutes** for 100 samples. Watch the progress bar below!")
add_code("from trl import SFTTrainer\nfrom transformers import TrainingArguments\nfrom unsloth import is_bfloat16_supported\n\ntrainer = SFTTrainer(\n    model = model,\n    processing_class = tokenizer,\n    train_dataset = dataset,\n    dataset_text_field = \"text\",\n    max_seq_length = max_seq_length,\n    dataset_num_proc = 2,\n    packing = False,\n    args = TrainingArguments(\n        per_device_train_batch_size = 2,\n        gradient_accumulation_steps = 4,\n        warmup_steps = 5,\n        max_steps = 60, # Adjust depending on dataset size. 60 is good for testing.\n        learning_rate = 2e-4,\n        fp16 = not is_bfloat16_supported(),\n        bf16 = is_bfloat16_supported(),\n        logging_steps = 1,\n        optim = \"adamw_8bit\",\n        weight_decay = 0.01,\n        lr_scheduler_type = \"linear\",\n        seed = 3407,\n        output_dir = \"outputs\",\n    ),\n)\n\ntrainer_stats = trainer.train()")

add_md("### Step 5: Test It Live\nTest the newly fine-tuned model!")
add_code("FastLanguageModel.for_inference(model) # Enable native 2x faster inference\n\n# Quick test message\ntest_messages = [\n    {\"role\": \"system\", \"content\": \"You are Capstone Mentor AI. Answer strictly based on the context...\"},\n    {\"role\": \"user\", \"content\": \"I am stuck on module 3, what should I use?\"}\n]\n\ninputs = tokenizer.apply_chat_template(\n    test_messages,\n    tokenize = True,\n    add_generation_prompt = True,\n    return_tensors = \"pt\",\n).to(\"cuda\")\n\noutputs = model.generate(input_ids = inputs, max_new_tokens = 256, use_cache = True)\nprint(tokenizer.batch_decode(outputs)[0])")

add_md("### Step 6: Export the LoRA Adapters\nSave the weights so you can download them from Kaggle.")
add_code("model.save_pretrained(\"lora_capstone_mentor\")\ntokenizer.save_pretrained(\"lora_capstone_mentor\")\nprint(\"Saved! You can now download the lora_capstone_mentor folder.\")")

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.12"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

with open("kaggle_finetune_qwen.ipynb", "w") as f:
    json.dump(notebook, f, indent=4)
