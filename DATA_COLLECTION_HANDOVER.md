# 🤝 Data Collection Handover for Teammates & AI Assistants

Welcome to the AI Capstone Mentor project! We have officially completed the prototype phase. The fine-tuning pipeline works perfectly, and the model has proven it can learn the "Socratic Mentor" persona.

Our current focus is **Phase 4: Mass Data Collection**. We need to generate a massive dataset using Claude.

---

## 🅰️ PART 1: Project-Specific Samples (9,000 total)
**Goal:** 150 samples for each of the 60 capstone projects.
**Raw Data:** `raw/projects/<Domain>/` (e.g., `.docx` case studies)

Because Claude has strict output limits, generate them **50 at a time** in 3 batches.

### **Step 1: The Master Prompt (First 50 Samples)**
Upload the `.docx` file for ONE project to Claude, and paste this prompt:

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. The goal of this model is to guide students through their 300-hour capstone curriculum, answer technical doubts, provide troubleshooting help, and conduct Viva preparations, all without "spoon-feeding" them the final code. It must act like a Socratic teacher.

I have attached the official case study document for one of our Capstone Projects.

**FIRST TASK: CONTEXT EXTRACTION**
First, extract the core details from the attached document and internally create a structured `[PROJECT CONTEXT]` block that includes the Project Name, Domain, Objective, Architecture, Modules, Technologies, Troubleshooting edge cases, and Viva questions.

**SECOND TASK: GENERATION**
Generate exactly 50 training samples in strict JSONL format based on the document.

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks (no ```json). 
3. DO NOT include any conversational text, greetings, or explanations before or after the JSON. 
4. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
5. **EVERY SINGLE `system` message MUST contain the exact `[PROJECT CONTEXT]` block you generated in Task 1.**

**DATASET DISTRIBUTION (For these 50 samples):**
Generate diverse scenarios representing a student interacting with the mentor. Distribute them as follows:
- 15x Mentoring / Module Guidance (Student asks what to do next)
- 15x Troubleshooting (Invent highly realistic coding errors based on the tech stack. Guide them to the solution, don't write the code)
- 10x Viva / Academic Support (Mentor asks a tough architecture question)
- 10x Context Discovery (Student asks a vague question, mentor asks clarifying questions)

Please begin outputting the 50 JSONL lines now based on the attached document.
```

### **Step 2 & 3: Batches 2 and 3**
- Reply: *"Perfect. Generate 50 MORE entirely new samples for this project. Focus heavily on edge-case bugs and deployment issues. Every `system` message MUST still contain the `[PROJECT CONTEXT]` block. Output ONLY the raw JSONL."*
- Reply: *"Excellent. Generate the final 50 samples. Focus on beginner mistakes and environment setup errors. Every `system` message MUST still contain the `[PROJECT CONTEXT]` block. Output ONLY raw JSONL."*

---

## 🅱️ PART 2: General Curriculum Samples (1,000 total)
**Goal:** Teach the model the 300-hour theoretical syllabus.
**Raw Data:** Since a 300-hour curriculum is too massive to upload at once, you must process it **Module by Module** (e.g., Python Basics, Machine Learning, Cloud Deployment).

### **The Curriculum Prompt**
Upload the PDF/Document for a **specific Module/Chapter**, and paste this prompt:

```text
I am building a fine-tuning dataset for an "AI Capstone Mentor" LLM. 
I have attached a chapter/module from our official 300-hour curriculum.

**FIRST TASK: CONTEXT EXTRACTION**
Extract the core learning objectives and theoretical concepts from the attached document and create a `[CURRICULUM CONTEXT]` block.

**SECOND TASK: GENERATION**
Generate exactly 50 training samples in strict JSONL format based on this curriculum module.

**CRITICAL FORMATTING RULES:**
1. Output ONLY raw JSON objects. 
2. DO NOT wrap the output in markdown blocks (no ```json). 
3. Each line must be a standalone JSON object starting with `{"messages": [` and ending with `]}`.
4. **EVERY SINGLE `system` message MUST contain the exact `[CURRICULUM CONTEXT]` block you generated.**

**DATASET DISTRIBUTION:**
- 25x Theory Explanation (Student asks to explain a complex concept from the document. The mentor uses the Socratic method to guide them).
- 25x Syntax/Concept Troubleshooting (Student has a fundamental misunderstanding of a concept taught in this module. Mentor corrects them gently).

Please begin outputting the 50 JSONL lines now.
```
