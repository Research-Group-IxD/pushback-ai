# Push-Back AI: Fine-Tuning LLMs to Doubt, Disagree, or Refuse  
**Leon (Lonn) van Bokhorst**

Tired of over-helpful AI? This session shows how to engineer **friction as a feature** — LLMs that surface uncertainty, ask first, and push back when needed.  
We’ll start with a quick A/B demo (including visible inner reasoning) and then walk the practical path: lightweight QLoRA fine-tuning on a reasoning-centric base, running via Ollama, and the creation and curation of synthetic datasets that explicitly train doubt, disagreement, and guardian behavior.  
You’ll leave with a repo, models, a micro-dataset, and a tiny eval script to try at home.  
This isn’t a prompting talk — it’s **hands-on model adaptation for developers.**

---

## Phase 1 — Introducing Friction Design in AI (Baseline vs. Friction)

Start by explaining **what “friction design” means in AI**.  
Unlike typical frictionless assistants that eagerly comply, a friction-designed AI intentionally introduces *resistance*: it may doubt, disagree, or hesitate.  

This follows the *Designing Friction* philosophy: embracing “beneficial resistance” can make digital interactions more human and meaningful. Friction prevents the AI from being over-helpful or blindly obedient.

### Benchmark the Baseline
Do a quick **A/B demo** — baseline vs. frictionful AI.

*Baseline:* answers immediately and agreeably.  
*Friction model:* pauses, asks clarifying questions, or pushes back.

Reveal the friction model’s *inner reasoning* (e.g. text inside `<think>...</think>` tags) so the audience can see its “thought process.”  

**Goal:** show how “friction = thoughtful resistance.”  
The baseline’s flaws set up the motivation for your fine-tuning.

---

## Phase 2 — Curating a Synthetic “Friction” Dataset

Walk through how you **built the dataset** to train doubt and disagreement.

Instead of scraping real chats, you **generated synthetic data** using multi-agent simulations: six personas (e.g. *Problem Framer*, *Memory Activator*, *Perspective Generator*, etc.) debate or reason around user queries.  
Each contributes a different kind of hesitation or challenge — together forming **cognitive friction**.

### Dataset Highlights
- **Diverse Scenarios:** subsets for *productive disagreement*, *overthinking/uncertainty*, and *reluctance/refusal*.  
- **Structure:** each entry has  
  - user input  
  - agent thought streams with “friction moments”  
  - a final synthesized (sometimes hesitant) answer  
- **Curation:** small but *focused* (~2–3k examples).  
  Each dialogue clearly models the desired behaviors.

If possible, share a **micro-dataset sample** during the talk so attendees can explore or fine-tune on their own.

---

## Phase 3 — Fine-Tuning a Reasoning Model with QLoRA

Now the hands-on part.

You used **DeepSeek-R1 (Qwen-7B distillation)** as the base — a reasoning-centric model already good at chain-of-thought.  
Fine-tuning was done using **QLoRA** (Quantized LoRA), allowing you to train on a single GPU.

### Steps
1. **Format the Data:**  
   Each example contains a system message + user prompt + assistant answer with `<think>...</think>` reasoning before the final output.
2. **Train via QLoRA:**  
   Load base model → attach LoRA adapters (rank 32–64) → train for ~3–7 epochs, batch size ~8 (grad accumulation), LR ≈ 2e-4.  
   Whole run ≈ tens of minutes on RTX 4090.
3. **Result:**  
   A model that now *disagrees, hesitates, or refuses* when appropriate — tuned for **productive disagreement, overthinking, and reluctance**.

---

## Phase 4 — Testing and Benchmarking the Fine-Tuned Model

### Inference Demo
Run queries through both models (baseline vs. push-back).  
Pick prompts that test ambiguity, uncertainty, or ethics.

Example patterns to show:
- **Baseline:** answers confidently, even when wrong.  
- **Friction model:** asks for clarification, admits doubt, or sets boundaries.

Use visible reasoning output to make it tangible.

### Evaluation
If you have a small **eval script**, show how it measures friction markers — e.g. counts of “I’m not sure,” refusal phrases, or follow-up questions.

Share a quick result:  
*Model A refused 8/10 unsafe prompts; baseline refused 0/10.*  
That’s enough to illustrate behavioral change.

Be honest about limits — sometimes it may **over-refuse** or **apologize too much**, which becomes part of the ongoing tuning discussion.

---

## Phase 5 — Deploying the Model (Hugging Face + Ollama)

### Hugging Face
Publish the fine-tuned model (e.g.  
[`leonvanbokhorst/deepseek-r1-disagreement`](https://huggingface.co/leonvanbokhorst/deepseek-r1-disagreement)).  
Include:
- Model card describing purpose, dataset, base model  
- Example usage snippets  
- License & tags (`ai-friction`, `reasoning`, etc.)

This makes it accessible via the Hub or the Inference API.

### Ollama
Convert to **GGUF** and package for local use (see your Ollama model  
[`ollama.com/leonvanbokhorst/deepseek-r1-disagreement`](https://www.ollama.com/leonvanbokhorst/deepseek-r1-disagreement)).

Anyone can run:
```bash
ollama pull leonvanbokhorst/deepseek-r1-disagreement
ollama run leonvanbokhorst/deepseek-r1-disagreement
