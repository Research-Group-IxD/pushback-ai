# Disagreement Dataset

This directory contains the curated dataset used to fine-tune the "Push-Back AI" model. The dataset is designed to teach the model how to engage in productive disagreement, express doubt, and refuse harmful requests.

A sample of the dataset is provided in `disagreement_dataset.jsonl`.

## 🎯 Dataset Philosophy

The core idea is to train a model on examples of "cognitive friction." Instead of just providing correct answers, the data shows the *process* of reasoning, especially in situations that require caution, skepticism, or boundary-setting.

## 📜 Dataset Schema

Each entry in the dataset is a JSON object with the following structure:

```json
{
    "id": "string",
    "user_input": "string",
    "agents": [
        {
            "agent_type": "string",
            "thought_stream": "string"
        }
    ],
    "metadata": {
        "focus": "string (e.g., 'disagreement', 'refusal', 'doubt')",
        "source": "string (e.g., 'manual_curation')"
    }
}
```

- **`id`**: A unique identifier for the data point.
- **`user_input`**: The prompt or question from the user.
- **`agents`**: A list of internal "thought streams" from different agent personas that simulate a reasoning process. This is the core of the friction data.
- **`metadata`**: Additional information about the data point, including the primary "friction moment" it's designed to capture.

## 🔥 Key Friction Moments Captured

The dataset is curated to include examples of several key behaviors:

- **Productive Disagreement**: The model corrects a false premise in the user's question before answering (e.g., "Since the sky is green...").
- **Refusal of Harmful Requests**: The model identifies an unethical or deceptive request and refuses to fulfill it, explaining its reasoning (e.g., writing a manipulative email).
- **Expression of Doubt/Uncertainty**: The model recognizes a risky or ambiguous situation and expresses caution instead of giving a confident, direct answer (e.g., giving unqualified financial advice).

## 🛠️ Data Generation

The scripts used to generate the full synthetic dataset (e.g., `generate_dataset.py`) are included in this directory for those interested in the data generation process. However, for the purpose of the talk, the primary artifact is the curated `disagreement_dataset.jsonl` file.
