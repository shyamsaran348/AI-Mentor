# AI Capstone Mentor Project

## 📖 Project Overview
The **AI Capstone Mentor** is a specialized, fine-tuned Large Language Model (based on Qwen 2.5 7B) designed to act as a virtual, Socratic supervisor for students working on their 300-hour capstone projects. 

Rather than spoon-feeding code, this AI Mentor guides students through technical hurdles, architecture design, troubleshooting, and Viva preparation. It is deeply integrated with the official curriculum and 60 specific capstone project case studies across domains like AI, Cyber Security, ERP, and IoT.

## 🎯 Use Case
- **Mentoring & Module Guidance:** Directing students on their next steps based on official module definitions.
- **Troubleshooting:** Helping diagnose and resolve domain-specific errors (e.g., CORS errors, PyTorch OOM bugs) without just giving the solution.
- **Viva Preparation:** Testing students on the architecture and design choices they made to prepare them for their final academic review.
- **Context Discovery:** Asking clarifying questions when students ask vague questions to determine what project they are working on.

## 📊 Dataset Requirements (Production Goal)
To train the production-grade company model, we are constructing a massive JSONL dataset of ~11,000 diverse conversational interactions.

| Category | Quantity | Purpose |
|----------|----------|---------|
| **Project-Specific (60 Projects)** | 9,000 | Teaches exact architecture, bugs, and viva for every single project (150 samples per project). |
| **Context Discovery** | 500 | Teaches the model how to ask questions when it doesn't know the project yet. |
| **General Curriculum** | 1,000 | Teaches the 300-hour theoretical syllabus. |
| **General Persona** | 500 | Teaches the model how to be an empathetic, Socratic mentor. |
| **TOTAL** | **~11,000** | Final `train.jsonl` file. |

## ✅ Project Status & Checklist
- [x] **Phase 1 (Prototype): Dataset Format Design** - Constructed a 98-sample JSONL prototype.
- [x] **Phase 2 (Prototype): Environment Setup** - Kaggle T4 configuration and Unsloth pipeline built.
- [x] **Phase 3 (Prototype): Fine-Tuning Validation** - Successfully fine-tuned Qwen 2.5 7B on Kaggle. The model passed all tests (refused to write code, guided correctly, and adopted the persona).
- [ ] **Phase 4: Mass Data Collection** - Generating 11,000 samples using Claude (In Progress).
- [ ] **Phase 5: Production Fine-Tuning** - Training on a dedicated GPU for the full dataset.
- [ ] **Phase 6: UI/Platform Integration** - Exporting to GGUF and integrating with the frontend.

## 🤝 Handover / Collaboration
If you are a new collaborator or an AI agent (like Antigravity) assisting with this project, please read the [DATA_COLLECTION_HANDOVER.md](DATA_COLLECTION_HANDOVER.md) file to understand how to continue generating the 11,000-sample dataset.
