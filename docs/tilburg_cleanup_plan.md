# Tilburg Talk Prep: Disagreement Model Focus

## Goal

Create a polished repo that walks attendees through the disagreement-focused friction model and dataset, providing everything they need to reproduce the demo, inspect the data, rerun training, and deploy the model locally or via Hugging Face.

## Audience Takeaways

- Understand friction-as-a-feature with a clear A/B baseline vs. disagreement model demo (including visible `<think>` reasoning).
- Inspect a curated synthetic dataset that showcases disagreement, doubt, and refusal behaviors.
- Follow lightweight QLoRA fine-tuning instructions tailored to the disagreement model on consumer hardware.
- Evaluate the fine-tuned model with provided prompts/scripts to see behavioral shifts and limitations.
- Deploy the resulting model via Hugging Face Hub and Ollama using documented steps.

## Repo Cleanup Checklist

### 1. Story & Positioning

- Document “friction design” philosophy and why disagreement matters in `README.md` (or dedicated doc linked from README).
- Provide concise overview of baseline vs. frictionful behavior; reference the Tilburg talk context.

### 2. Demo Assets (Baseline vs. Disagreement)

- Supply scripts/notebooks to run both baseline and fine-tuned models side by side.
- Include prompt set for demo showcasing hesitation, clarification, and refusal scenarios.
- Add optional tooling to surface `<think>...</think>` reasoning for the friction model.

### 3. Dataset Package (Disagreement Focus)

- Store curated synthetic dataset subset (JSONL) highlighting productive disagreement cases.
- Document schema (`user_input`, `agents`, `metadata`) and explain agent personas + friction moments.
- Provide micro-dataset sample for attendees to download quickly.
- Detail curation process (prompting, filtering) and quality notes.

### 4. Training Pipeline (QLoRA on Disagreement Model)

- Deliver reproducible training script/config (QLoRA, 4-bit quantization, LoRA rank 32–64).
- Document expected hardware (e.g., 24GB GPU) and estimated training time.
- Show data formatting (system/user messages, `<think>` reasoning, final answer separation).
- Include guidance on monitoring/early stopping and hyperparameter defaults.

### 5. Evaluation & Benchmarking

- Ship lightweight eval script comparing baseline vs. friction model on curated prompts.
- Capture metrics/anecdotes (e.g., refusal counts, uncertainty phrases) and note known limitations (over-refusal, tone shifts).
- Provide instructions for reproducing qualitative examples used in the talk.

### 6. Deployment & Distribution

- Document Hugging Face release steps: model card template, metadata, usage snippet.
- Include instructions/CLI for uploading disagreement model weights + dataset artifact to HF Hub.
- Document Ollama packaging: GGUF conversion script, `Modelfile` template, usage commands (`ollama pull`, `ollama run`).

### 7. Repository Hygiene

- Prune unrelated experiments; keep repo scoped to disagreement track.
- Align docs (README, docs/) with cleaned structure; ensure navigation is simple.
- Verify code style (black, mypy, pylint) and provide `make`/scripts to run formatting, type-checks, tests.
- Ensure tests (unit/integration) cover core utilities; add instructions to reach ≥90% coverage for relevant modules.

### 8. Talk Support Artifacts

- Prepare quick-start guide for attendees (e.g., `docs/quickstart_disagreement.md`).
- Provide reference prompts and troubleshooting tips for running the model locally.
- Optionally include slide-friendly graphics or diagrams illustrating pipeline stages.

## Next Steps

- Confirm priority ordering with Master Lonn.
- Tackle cleanup tasks in phases (story → data → code → deployment → polish).
- Run end-to-end dry run (data load → train → evaluate → deploy) before the Tilburg talk.
