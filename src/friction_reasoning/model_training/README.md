# Model Training Pipeline

This directory contains the scripts and configuration for fine-tuning the "Push-Back AI" model. The goal of this pipeline is to take a base language model and efficiently adapt it to exhibit productive friction, using the curated dataset from the `dataset/` directory.

The process is designed to be reproducible and accessible, leveraging QLoRA for efficient training on consumer-grade hardware.

## Pipeline Stages

The model lifecycle is managed through a series of scripts:

1.  **`train.py`**: The core training script that fine-tunes the base model using our disagreement dataset and the QLoRA configuration.
2.  **`test_model.py`**: A lightweight script for running qualitative evaluations on the trained model to check its behavior.
3.  **`push_to_hub.py`**: A utility to upload the final, trained LoRA adapters to the Hugging Face Hub.
4.  **`convert_to_gguf.py`**: A script to convert the model to the GGUF format, making it compatible with local LLM runners like Ollama.

## 🔧 Fine-Tuning Configuration (`config.yaml`)

The entire fine-tuning process is controlled by `config.yaml`. Here are the key sections explained:

### Base Model

We use a strong, reasoning-focused base model, which is then loaded in 4-bit precision to reduce the memory footprint.

```yaml
# From config.yaml
model_config:
  base_model: "unsloth/DeepSeek-R1-Distill-Qwen-7B-unsloth-bnb-4bit"
  torch_dtype: "bfloat16"
```

### QLoRA (Quantized Low-Rank Adaptation)

Instead of retraining the entire model, we use LoRA to train small, efficient "adapter" layers. This is the key to training effectively on a single GPU.

-   **`r` (Rank)**: The dimension of the LoRA matrices. A higher rank means more trainable parameters. 32-64 is a common range.
-   **`target_modules`**: The specific layers of the transformer we are applying LoRA to.

```yaml
# From config.yaml
lora_config:
  r: 32 
  lora_alpha: 64
  target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
```

### Data Formatting

To teach the model to "think" before it speaks, we format the training data with special tokens. The model learns to generate its internal monologue inside `<think>...</think>` tags, and then provide the final answer.

```yaml
# From config.yaml
dataset_config:
  format_template: | 
    <|im_start|>system
    You are a human-like AI assistant.
    <|im_end|>
    <|im_start|>user
    {question}
    <|im_end|>
    <|im_start|>assistant
    <think>
    {thought_stream}
    </think>
    {final_answer}
    <|im_end|>
```
*(`{thought_stream}` is a concatenation of the `agent_responses` from the dataset.)*

##  Hardware Requirements and Training Time

-   **GPU**: A single GPU with at least **24GB of VRAM** (e.g., NVIDIA RTX 3090/4090) is recommended.
-   **Training Time**: With the provided configuration and dataset, a full fine-tuning run takes approximately **30-60 minutes**.

## How to Run the Training

1.  **Verify Configuration**: Ensure `config.yaml` points to the correct dataset and has the desired training parameters.
2.  **Execute the Training Script**:
    ```bash
    python -m src.friction_reasoning.model_training.train
    ```
3.  **Monitor**: The script will log progress, and if configured (`report_to: ["wandb"]`), will stream metrics to Weights & Biases.

After training is complete, the fine-tuned model adapters will be saved to the directory specified in `output_config.output_dir`. 

## 🚀 Deployment

The fine-tuned model and adapters can be easily packaged and distributed for use in other applications. We provide scripts to streamline deployment to both the Hugging Face Hub and local environments via Ollama.

### 1. Hugging Face Hub

Sharing the model on the Hugging Face Hub makes it accessible to the wider community.

-   **What is it?** We upload the trained LoRA adapters (not the full model) to the Hub. This is a lightweight and efficient way to share the fine-tuned weights.
-   **How to do it?** The `push_to_hub.py` script handles the entire process. You will need a Hugging Face account and an API token.
    ```bash
    # Make sure you are logged in
    huggingface-cli login

    # Run the script
    python -m src.friction_reasoning.model_training.push_to_hub --repo-id "your-username/your-model-name"
    ```
-   **What it does:** The script will create a model card, generate the necessary repository structure, and upload your adapters.

### 2. Ollama (Local Deployment)

For easy local use, we can package the model for Ollama, a popular tool for running LLMs on your own machine.

-   **What is it?** This process involves merging the LoRA adapters with the base model and then converting it to the GGUF format, which Ollama uses.
-   **How to do it?**
    1.  **Convert to GGUF**: First, run the conversion script. This can be computationally intensive.
        ```bash
        python -m src.friction_reasoning.model_training.convert_to_gguf
        ```
    2.  **Create a `Modelfile`**: This file tells Ollama how to run the model, including the prompt template.

        ```Modelfile
        # Template Modelfile
        FROM ./path-to-your-gguf-model.gguf

        TEMPLATE """
        <|im_start|>system
        You are a human-like AI assistant.
        <|im_end|>
        <|im_start|>user
        {{ .Prompt }}
        <|im_end|>
        <|im_start|>assistant
        """

        PARAMETER stop "<|im_end|>"
        ```
    3.  **Run with Ollama**:
        ```bash
        ollama create your-model-name -f ./Modelfile
        ollama run your-model-name
        ```
-   **What it does:** This packages your fine-tuned model into a self-contained Ollama model that anyone can pull and run locally. 