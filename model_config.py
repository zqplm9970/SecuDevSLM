from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
import torch

def load_model_and_tokenizer(model_name, device='cuda:7', eval_mode=True):
    try:
        try:
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                resume_download=True,
                use_cache=True
            ).to(device)
        except Exception as e:
            if 'Unrecognized configuration class' in str(e) and 'T5Config' in str(e):
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    trust_remote_code=True,
                    resume_download=True,
                    use_cache=True
                ).to(device)
            else:
                raise e

        if eval_mode:
            model.eval()

        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        return model, tokenizer

    except Exception as e:
        return None, None

def load_models_sequentially(model_list):
    failed_models = []
    for model_name in model_list:
        tokenizer, model = load_model_and_tokenizer(model_name)
        if tokenizer is None or model is None:
            failed_models.append(model_name)
    return failed_models


if __name__ == "__main__":
    model_list = [
        "google/gemma-2-2b-jpn-it", "microsoft/phi-2", "ibm-granite/granite-3.0-2b-base",
        "Qwen/Qwen2.5-1.5B", "google/flan-t5-xl", "Qwen/Qwen2-1.5B", "google/gemma-2-2b",
        "HuggingFaceTB/SmolLM2-1.7B", "google/flan-t5-large", "Qwen/Qwen1.5-1.8B",
        "tensoropera/Fox-1-1.6B", "google/gemma-2b", "stabilityai/stablelm-3b-4e1t",
        "Qwen/Qwen2-0.5B", "microsoft/phi-1_5", "google/codegemma-1.1-2b",
        "google/recurrentgemma-2b", "HuggingFaceTB/SmolLM-135M", "openai-community/gpt2",
        "allenai/OLMo-1B-hf", "BEE-spoke-data/smol_llama-220M-GQA", "gpt2", "Qwen/Qwen2.5-0.5B",
        "google/flan-t5-base", "HuggingFaceTB/SmolLM-360M", "HuggingFaceTB/SmolLM2-360M",
        "google/flan-t5-small", "ibm-granite/granite-3.0-1b-a400m-base",
        "openai-community/gpt2-medium", "EleutherAI/pythia-160m", "HuggingFaceTB/SmolLM2-135M",
        "microsoft/phi-1", "princeton-nlp/Sheared-LLaMA-1.3B", "openai-community/gpt2-large",
        "vonjack/MobileLLM-125M-HF", "HuggingFaceTB/SmolLM-1.7B",
        "EleutherAI/gpt-neo-1.3B", "facebook/opt-1.3b", "stabilityai/stablelm-2-1_6b",
        "amd/AMD-Llama-135m", "Qwen/Qwen1.5-0.5B", "EleutherAI/pythia-410m", "keeeeenw/MicroLlama",
        "openai-community/gpt2-xl", "TinyLlama/TinyLlama_v1.1", "EleutherAI/gpt-neo-125m",
        "pints-ai/1.5-Pints-16K-v0.1", "M4-ai/TinyMistral-248M-v3", "meta-llama/Llama-3.2-1B",
        "bigscience/bloom-1b7", "bigscience/bloom-1b1", "BEE-spoke-data/smol_llama-101M-GQA",
        "distilbert/distilgpt2", "pints-ai/1.5-Pints-2K-v0.1", "bigscience/bloom-560m",
        "instruction-pretrain/InstructLM-500M"
    ]
    failed_models = load_models_sequentially(model_list)

    for failed_model in failed_models:
        print(failed_model)
