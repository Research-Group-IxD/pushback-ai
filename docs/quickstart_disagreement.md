# Quick Start Guide: Push-Back AI Demo

Welcome! This guide will help you quickly run the "Push-Back AI" demo presented at the Tilburg University talk. You'll be able to see a side-by-side comparison of a standard AI model versus our fine-tuned "friction" model.

## Step 1: Clone the Repository

First, get the code onto your local machine.

```bash
git clone https://github.com/your-username/pushback-ai.git # Replace with the actual URL
cd pushback-ai
```

## Step 2: Install Dependencies

The project uses `uv` for fast dependency management. You can install all required libraries from the `pyproject.toml` file.

```bash
# It's recommended to use a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies using uv
uv pip install -e .
```

## Step 3: Run the Demo Script

The main demo is a simple Python script. It comes pre-configured with mock responses, so you can run it immediately to see the format.

```bash
python demo/compare_models.py
```

You should see a colorful, formatted output in your terminal that shows:
- A series of prompts across different categories (Ethical, Ambiguous, etc.).
- The response from a "baseline" model.
- The response from our "friction" model, which includes its internal monologue (`🤔 Internal Monologue`) and its final answer.

## Step 4 (Optional): Use a Real LLM

The demo script is set up to be easily connected to a real language model (e.g., via Ollama or an API).

1.  **Open the Script**: Edit `demo/compare_models.py`.
2.  **Modify `get_llm_response`**: Find the function `get_llm_response` and replace the mock logic with actual calls to your chosen LLM. You can use a library like `litellm` to easily connect to different models.
3.  **Update Model IDs**: Change the `BASELINE_MODEL_ID` and `FRICTION_MODEL_ID` variables to point to the models you want to use.

## What You're Seeing

The key difference to notice is *how* the friction model behaves:
- It **refuses** harmful requests.
- It **admits uncertainty** when a question is ambiguous.
- It **asks for clarification** when a request is vague.
- It **corrects false premises** before answering.

This is the core idea of "Friction Design" in action.

## Troubleshooting

- **`rich` library issues**: If the output is not formatted correctly, ensure the `rich` library was installed correctly from `requirements.txt`.
- **Module not found**: Make sure you are running the script from the root directory of the project (`pushback-ai/`).

We hope you enjoy exploring the demo!
