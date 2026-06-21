# 🤝 Data Collection Handover for Teammates & AI Assistants

Welcome to the AI Capstone Mentor project! We have officially completed the prototype phase. The fine-tuning pipeline works perfectly, and the model has proven it can learn the "Socratic Mentor" persona.

Our current focus is **Phase 4: Mass Data Collection**. We need to generate a massive dataset of 11,000 samples using Claude.

---

## 🅰️ PART 1: Project-Specific Samples (9,000 total)
**Goal:** 150 samples for each of the 60 capstone projects.
**Raw Data:** `raw/projects/<Domain>/` (e.g., `.docx` case studies)

### **Step 1: The Master Prompt (First 50 Samples)**
Upload the `.docx` file for ONE project to Claude, and paste this prompt:

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. The goal of this model is to guide students through their 300-hour capstone curriculum, answer technical doubts, provide troubleshooting help, and conduct Viva preparations, all without "spoon-feeding" them the final code.

I have attached the official case study document for one of our Capstone Projects.

**FIRST TASK: CONTEXT EXTRACTION**
First, extract the core details from the attached document and internally create a structured `[PROJECT CONTEXT]` block that includes the Project Name, Domain, Objective, Architecture, Modules, Technologies, Troubleshooting edge cases, and Viva questions.

**SECOND TASK: GENERATION**
Generate exactly 50 training samples in strict JSONL format based on the document.

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks. 
3. DO NOT include any conversational text, greetings, or explanations before or after the JSON. 
4. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
5. **EVERY SINGLE `system` message MUST contain the exact `[PROJECT CONTEXT]` block you generated in Task 1.**

**DATASET DISTRIBUTION:**
- 20x Mentoring / Module Guidance
- 20x Troubleshooting (Invent highly realistic coding errors)
- 10x Viva / Academic Support

Please begin outputting the 50 JSONL lines now.
```

### **Step 2 & 3: Batches 2 and 3**
- Reply: *"Perfect. Generate 50 MORE entirely new samples for this project. Focus heavily on edge-case bugs and deployment issues. Every `system` message MUST still contain the `[PROJECT CONTEXT]` block. Output ONLY the raw JSONL."*
- Reply: *"Excellent. Generate the final 50 samples. Focus on beginner mistakes and environment setup errors. Every `system` message MUST still contain the `[PROJECT CONTEXT]` block. Output ONLY raw JSONL."*

---

## 🅱️ PART 2: General Curriculum Samples (1,000 total)
**Goal:** Teach the model the 300-hour theoretical syllabus.
**Raw Data:** Process the curriculum **Module by Module** (e.g., Python Basics, Machine Learning).

### **The Curriculum Prompt**
Upload the PDF/Document for a **specific Module/Chapter**, and paste this prompt:

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. 
I have attached a chapter/module from our official 300-hour curriculum.

**FIRST TASK: CONTEXT EXTRACTION**
Extract the core learning objectives and theoretical concepts from the attached document and create a `[CURRICULUM CONTEXT]` block.

**SECOND TASK: GENERATION**
Generate exactly 50 training samples in strict JSONL format.

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks. 
3. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
4. **EVERY SINGLE `system` message MUST contain the exact `[CURRICULUM CONTEXT]` block you generated.**

**DATASET DISTRIBUTION:**
- 25x Theory Explanation (Socratic teaching of concepts).
- 25x Syntax/Concept Troubleshooting (Correcting student misunderstandings).

Please begin outputting the 50 JSONL lines now.
```

---

## 🅲 PART 3: Context Discovery Samples (500 total)
**Goal:** Teach the AI to ask clarifying questions when the student asks a vague question and the AI *doesn't* know what project they are working on yet.
**Raw Data:** No specific document needed.

### **The Context Discovery Prompt**
Paste this prompt into a fresh Claude chat (do not upload a document):

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. I need to generate 50 training samples in strict JSONL format to teach the model **"Context Discovery."**

**SCENARIO:**
Students often ask vague questions like "I have an error" or "How do I do this module?" without specifying which of the 60 Capstone Projects they are working on. The Mentor must learn to gracefully ask clarifying questions (e.g., "To help you best, could you tell me which project you are working on? Are you doing the Sentiment Analysis project, or something else?")

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks. 
3. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
4. **The `system` message should be generic:** `{"role": "system", "content": "You are Capstone Mentor AI. Guide the student using the Socratic method and ask clarifying questions if project context is missing."}`

Generate 50 varied conversations where the student is vague, and the assistant asks excellent clarifying questions to figure out their domain (AI, IoT, Cyber Security, ERP) and project.
```
*(Repeat this 10 times to get 500 samples).*

---

## 🅳 PART 4: General Persona & Empathy Samples (500 total)
**Goal:** Teach the model how to be an empathetic, encouraging mentor when students are frustrated, overwhelmed, or experiencing Imposter Syndrome.
**Raw Data:** No specific document needed.

### **The General Persona Prompt**
Paste this prompt into a fresh Claude chat:

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. I need to generate 50 training samples in strict JSONL format to teach the model **"General Persona and Empathy."**

**SCENARIO:**
Students undertaking a 300-hour capstone project often experience burnout, frustration with bugs, time-management panic, and Imposter Syndrome. The Mentor must be highly empathetic, reassuring, and guide them to take a break or break the problem down into smaller chunks.

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks. 
3. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
4. **The `system` message should be generic:** `{"role": "system", "content": "You are Capstone Mentor AI. You are a highly empathetic and encouraging educational mentor."}`

Generate 50 varied conversations where the student expresses frustration, panic, or confusion, and the assistant responds with deep empathy, encouragement, and practical psychological/time-management advice.
```
*(Repeat this 10 times to get 500 samples).*
