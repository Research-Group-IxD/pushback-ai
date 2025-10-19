Planning the "Push-Back AI" Talk (Friction, Fine-Tuning, and Deployment)
Phase 1: Introducing Friction Design in AI (Baseline vs. Friction)
Start by explaining what “friction design” means in AI. Emphasize that unlike typical “frictionless” assistants that eagerly comply, a friction-designed AI intentionally introduces a bit of resistance – it might disagree, express doubt, or hesitate when appropriate. This idea comes from the Designing Friction philosophy: embracing the non-positive aspects (uncertainty, disagreement, complexity) makes digital interactions more human and meaningful
GitHub
. In other words, adding “beneficial resistance” can prevent an AI from being over-helpful or blindly obedient
ollama.com
.
Benchmark the Baseline: To illustrate this, prepare a quick A/B demo of baseline vs. frictionful AI. For example, take a question or request and show how a standard model responds versus your fine-tuned “push-back” model. The baseline model will likely answer immediately and agreeably, even if it’s unsure, while the friction-trained model may pause, ask clarifying questions, or politely push back instead of just spitting out an answer. Highlight these differences side-by-side. (You can even reveal the friction model’s internal reasoning during the demo – e.g. show the text it generates inside <think>...<\/think> tags – to let the audience see how it’s reasoning through doubt before answering.) This A/B comparison with visible reasoning will dramatically set the stage for why friction is valuable.
Explain “Friction” Benefits: Briefly discuss why we want an AI to sometimes disagree or refuse. For instance, a frictionless AI might confidently give wrong info or comply with problematic requests, whereas a friction-enabled AI can catch itself (“I’m not sure about that”) or refuse unethical instructions. This makes it safer and more trustworthy. Connect this back to human behavior: in real teamwork, a colleague who questions or challenges ideas constructively can lead to better outcomes than one who always says “yes”
GitHub
. By the end of this section, the audience should grok that “friction = thoughtful resistance”, and see the baseline’s shortcomings that your fine-tuned model aims to fix.
Phase 2: Curating a Synthetic “Friction” Dataset
Next, walk through how you built a dataset to train these behaviors. Your approach was to curate a synthetic dialogue dataset that explicitly includes doubt, disagreement, and hesitation. Explain that instead of scraping real chats, you generated training data using AI itself – a sort of multi-agent simulation. In your project, you configured six AI agent personas (e.g. a skeptical Problem Framer, an emotional Memory Activator, a contrarian Perspective Generator, etc.) that debate or reason around user questions
GitHub
. Each agent contributes a different perspective or hesitation, so the final dialogues capture rich cognitive friction – the kind of back-and-forth a single AI should internalize. This synthetic approach let you create examples of the AI struggling, doubting, or pushing back, which are exactly the behaviors you want to teach.
Key steps/considerations for the dataset:
Diverse “Friction” Scenarios: You assembled multiple subsets of data, each targeting a flavor of friction. For example, one subset focuses on productive disagreement (the assistant respectfully challenges false assumptions), another on overthinking/uncertainty (the assistant shows its internal debate or confusion), and others on reluctance/refusal (the assistant sets boundaries or says “I can’t do that”)
GitHub
. By combining these, you cover the spectrum of doubt, disagreement, and guarded responses. Each dialogue example typically has a user question, a series of agent thought streams exploring it (with noted “friction moments”), and a final answer that synthesizes a possibly hesitant or cautious reply
huggingface.co
.
Quality and Curation: Since the data is AI-generated, mention how you curated it. You might note that you iterated on prompts or agent behaviors to get believable “friction” dialogues, and filtered out low-quality gibberish. The result is a relatively small but focused dataset (on the order of only a few thousand examples in total – e.g. ~2.4k examples in the disagreement set alone
huggingface.co
). Stress that size isn’t huge here – it’s the quality and specificity that count. Each example vividly demonstrates the model thinking twice or politely arguing, which is exactly what we need to fine-tune those traits.
(If applicable, mention that you’ll be sharing a “micro-dataset” sample with the audience. This could be a subset of the full dataset so they can see what entries look like or even try fine-tuning on a smaller scale themselves.)
Phase 3: Fine-Tuning a Reasoning Model with QLoRA
Now dive into the fine-tuning process – the core “hands-on model adaptation” part. You chose a strong reasoning-centric base model as the foundation: for instance, DeepSeek-R1 (a distilled Qwen-7B model known for good reasoning and long-context abilities)
GitHub
. Explain that this base already had a propensity for chain-of-thought, which makes it easier to train it to “think aloud” and hesitate as needed. To keep things efficient, you used QLoRA (Quantized LoRA) for fine-tuning: basically loading the model in 4-bit precision and training lightweight LoRA adapters on top
GitHub
. This approach dramatically reduces memory requirements while still letting you nudge the model’s behavior. (For example, your config uses LoRA rank 32 or 64 with specific target transformer layers
GitHub
GitHub
 – just enough capacity to learn the new “friction” behaviors without full re-training.)
Outline the fine-tuning steps for the audience, to demystify the process:
Prepare the Training Data: You converted the synthetic dialogues into a suitable format (e.g. a chat-style prompt with special tokens). In your case, each example was formatted with a system message and the user question, then the assistant’s answer including a <think>...<\/think> section containing the chain-of-thought, followed by the final answer
GitHub
GitHub
. This teaches the model to internally "think" (the friction steps) before giving the outward answer. Ensure the audience understands how you included those markers so the model learns to separate reasoning from its final response.
Configure QLoRA Training: Load the base model and attach LoRA adapters. With 4-bit quantization, even a 7B model fits on a single GPU (your setup: an RTX 4090 24GB ran it comfortably). Share a few training hyperparameters – e.g. you fine-tuned for around 3-7 epochs, small batch (effectively 8 with grad accumulation), at a learning rate ~2e-4
GitHub
. Highlight that the entire fine-tune was fast (in your case, on the order of tens of minutes
GitHub
), showing that lightweight fine-tuning is feasible even for individuals. Mention any tools you used (Unsloth trainer, Transformers, etc.) and how you monitored training (loss curves or early stopping when it converged).
Result – A Friction-Capable Model: The output of training is a new model (base + LoRA weights) that embodies the behaviors from the dataset. Summarize the expected capabilities: Now this model will occasionally disagree or say “I’m unsure” where appropriate, instead of always being a yes-man. According to your model card, it’s explicitly tuned for “productive disagreement, overthinking, and reluctance”
GitHub
. Note that because it’s trained on niche data, it might not be as factually accurate or verbose as a general model – its purpose is to inject a bit of critical thinking. This helps set expectations before the live testing.
Phase 4: Testing and Benchmarking the Fine-Tuned Model
After training, demonstrate how you evaluated the model’s behavior versus the original. In the talk, you’ll want to show some concrete examples of the model in action. Here’s how you can structure the testing/benchmark part:
Inference Demonstration: Run a few example queries through the fine-tuned model and through the baseline model (or another assistant) to compare outputs. Use queries that stress test uncertainty or ethics. For instance, ask a factually tricky question or a request that should be refused. The fine-tuned model should respond with caution or a follow-up question, whereas the baseline might answer straight away (possibly incorrectly or without hesitation). Another idea is to ask an ambiguous personal question – the friction-model might say “I have some concerns about that” or seek clarification, showing it doesn’t just people-please. By presenting these side by side, you can quantitatively “benchmark” the difference (at least anecdotally).
Qualitative Analysis: Encourage the audience to notice the qualitative changes. Does the push-back model ask for clarification when a query is vague? Does it inject phrases like “I’m not entirely sure” or politely refuse an inappropriate request? These are successes. You can point out an example where the baseline gave a misleading answer with full confidence, whereas the new model admitted uncertainty – a win for honesty and safety. If you have a small evaluation script (as promised), mention that you used it to systematically test a set of scenarios. For example, your eval script might run both models on a list of prompts and count how often the fine-tuned model says phrases indicating uncertainty, or how often it avoids a known trap that the baseline falls into. Any simple metric or result from that (even “Model A refused 8/10 harmful prompts while Model B refused 0/10”) will give weight to your claims.
Discussion of Results: Be frank about the outcomes. The audience will appreciate hearing not just successes but also limitations. You might say: “Our friction-model does sometimes swing too far and over-apologize or over-refuse trivial questions – this is an open tuning challenge.” Also note it’s not meant for factual QA or other tasks outside its training – it specializes in tone and style more than knowledge
GitHub
. This sets realistic boundaries for where this push-back AI is useful. The key takeaway in this phase is that the fine-tuning achieved the desired behavioral change, which you can clearly show with a few before-and-after examples.
Phase 5: Deploying the Model (Hugging Face Hub and Ollama)
Finally, cover how you packaged and deployed the fine-tuned model, making it easy for others (the attendees) to use after the talk. There are two main avenues you promised: Hugging Face and Ollama.
Hugging Face Model Release: Explain that you’ve published the fine-tuned model on Hugging Face Hub for accessibility. This involves using a script or the huggingface_hub API to push your model weights and model card. Mention the name of the model on HF (for example, leonvanbokhorst/deepseek-r1-disagreement for the version focusing on disagreement, or the combined “mixture-of-friction” model). The Hub provides a nice README (model card) describing the model’s purpose and training data
GitHub
GitHub
. Cite that in the talk: “You can find the model on Hugging Face – it’s Apache 2.0 licensed and tagged with ai-friction so others can try it out.” By releasing on HF, attendees can download it or even use the web Inference API if enabled. Point out that the model card also credits the base model and has usage examples, making it self-contained for others to experiment.
Ollama Deployment: Many developers appreciate running models locally, so you also integrated with Ollama (a local LLM runner). Describe the steps you took: you likely converted the model to GGUF format (using a script like convert_to_gguf.py in your repo) so that it’s optimized for llama.cpp backends
GitHub
. Then you created an Ollama package (with a template defining how the chat prompt should be formatted, including the special tokens). The result is that anyone with Ollama can do ollama pull leonvanbokhorst/deepseek-r1-disagreement and start chatting with the model. Emphasize how cool this is: the friction model can run on a local machine and still exhibit those disagreement/doubting behaviors. According to the Ollama model listing, it explicitly “introduces beneficial resistance in AI interactions” by leveraging the Designing Friction principles
ollama.com
. Live-demo an Ollama query if possible, or at least show the command to run it. This part assures the audience that the model isn’t just a research artifact – it’s packaged for real-world use.
Sharing the Goods: Let the audience know that all resources will be shared. The Hugging Face link and the Ollama model are available immediately. Also, the GitHub repo (which you’ll provide) contains the code for data generation, fine-tuning scripts, and even the exact synthetic dataset (perhaps on HF as friction-disagreement-v2 etc.). This means attendees can review how the dataset was created or even try to extend it. By deploying the model publicly, you invite them to try prompting it themselves after the session (maybe give a warning that the model is 7B and not a GPT-4 replacement, but it’s fun for this specific purpose).
Conclusion & Takeaways
Wrap up by tying back to the promise: you’ve shown the journey of creating a push-back AI, from concept to implementation. The audience saw: an initial problem (over-helpful AI) and the concept of friction, the creation of a custom dataset to teach the AI new tricks, the technical fine-tuning process (QLoRA on a 7B model), and the results – a model that truly doubts, disagrees, or refuses when it should. They also learned how to deploy such a model so it’s accessible to others.
End with clear takeaways for the developers present. For example:
Friction as a Feature: Don’t always optimize your AI for speed or cheerfulness – sometimes a strategic pause or “Are you sure?” makes it more trustworthy. We can design for that quality intentionally
GitHub
.
Synthetic Data Generation: You can generate specialized training data (even with just existing models) to fine-tune behaviors that you want. It’s a viable approach when real data is scarce for niche behaviors.
Lightweight Fine-Tuning: Techniques like LoRA/QLoRA allow individual developers to fine-tune large models on consumer hardware in a short time, unlocking customized AI behavior without needing massive compute.
Evaluation Matters: It’s important to test the fine-tuned model against a baseline to ensure it’s doing what we expect (and not breaking other abilities). We saw how the push-back model excelled in certain scenarios, but also where it might need tweaks – an iterative process.
Resources to Explore: Encourage them to explore the shared repo and models. For instance, they can inspect the Friction Reasoning dataset structure or even run the tiny eval script included to see how the model reacts to sample prompts. All the links (GitHub, dataset on HF, model on HF, Ollama) will be provided for them to try at home.
By covering these steps in your talk, you will have delivered on your promise: the audience gets a full walkthrough of how to fine-tune an LLM to push back – and leaves with the code, model, and data to experiment on their own. Good luck, and have fun demonstrating a less agreeable, more thoughtful AI assistant! 
GitHub
