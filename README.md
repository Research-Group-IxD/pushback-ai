# Push-Back AI: A Friction-Driven Reasoning Model

<a href="https://doi.org/10.5281/zenodo.17580571"><img src="https://zenodo.org/badge/1079176866.svg" alt="DOI"></a>

This repository contains the source code, dataset, and resources for the "Push-Back AI" project, a fine-tuned language model that demonstrates **friction design**. Unlike typical AI assistants that aim for frictionless, immediate compliance, this model is trained to exhibit productive disagreement, doubt, and refusal.

This work is being prepared for a talk at **Tilburg Tech Tuesdays XXL**, an event co-hosted by Fontys ICT and Fresheads, where we will explore how introducing beneficial resistance can lead to safer, more thoughtful, and more trustworthy AI interactions.

## 🌟 Core Concepts: Friction as a Feature

The core idea behind this project is **Friction Design**. We believe that by intentionally designing moments of resistance, we can create AI systems that are:

- **More Thoughtful**: The model pauses, questions assumptions, and uses an internal monologue (`<think>...</think>`) to reason through doubt before answering.
- **Safer**: By refusing inappropriate or nonsensical requests, the model avoids generating harmful or misleading content.
- **More Trustworthy**: An AI that admits uncertainty ("I'm not sure about that...") is more reliable than one that confidently hallucinates.

This repository provides everything you need to explore this concept, from the synthetic dataset used for training to the scripts for running and evaluating the fine-tuned model.

## 🚀 Quick Start: Demo

To see the friction model in action, you can run a side-by-side comparison with a baseline model.

1.  **Install Dependencies**:
    ```bash
    # Install uv (if you don't have it)
    pip install uv

    # Create and sync your virtual environment
    uv venv
    uv pip install -e .
    ```

2.  **Configure Models**:
    Open `demo/compare_models.py` and replace the placeholder model IDs with the models you want to test. By default, it uses mock responses.

3.  **Run the Demo**:
    ```bash
    python demo/compare_models.py
    ```

This will print a formatted comparison in your terminal, showing how the friction model's responses (including its internal monologue) differ from the baseline.

## 📊 The Disagreement Dataset

The behavior of the friction model was taught using a curated, synthetic dataset of dialogues focused on disagreement, doubt, and refusal.

- **Schema**: Each entry includes `user_input`, a series of `agents`' internal thoughts, and `metadata`.
- **Content**: The dialogues showcase scenarios where agents challenge the user's premise, express uncertainty, or refuse to comply with a request.
- **Availability**: A sample of the dataset is available in this repository, with the full version hosted on Hugging Face.

For more details, see the [Dataset README](src/friction_reasoning/dataset/README.md).

## 🛠️ Training Pipeline

The model was fine-tuned using QLoRA (Quantized Low-Rank Adaptation) on a 7B parameter base model. This approach allows for efficient training on consumer-grade hardware (e.g., a single 24GB GPU).

The full training pipeline is available in `src/friction_reasoning/model_training/`.

## 📦 Deployment

The fine-tuned model is designed for easy deployment and can be run locally using Ollama or accessed via the Hugging Face Hub.

- **Hugging Face**: [Link to be added]
- **Ollama**: [Instructions to be added]

## 🗂️ Repository Structure

```
.
├── ADVISE.md
├── docs/
│   └── tilburg_cleanup_plan.md
├── src/
│   └── friction_reasoning/
│       ├── agents/           # Agent personas for data generation
│       ├── dataset/          # Dataset generation and documentation
│       ├── llm/              # LiteLLM client and prompts
│       └── model_training/   # Training, evaluation, and deployment scripts
├── tests/                    # Unit and integration tests
└── README.md
```

## 🙏 Acknowledgments

This project builds upon the foundational work of many researchers and open-source contributors. We are grateful for the tools and knowledge shared by the community. 
