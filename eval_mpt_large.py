from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    PreTrainedModel,
    PreTrainedTokenizer,
)
from core import filter_code, run_eval, split_batch
import os
import torch

# TODO: move to python-dotenv
# add hugging face access token here
TOKEN = ""


@torch.inference_mode()
def generate_batch_completion(
    model: PreTrainedModel, tokenizer: PreTrainedTokenizer, prompt, batch_size
) -> list[str]:
    input_batch = [prompt for _ in range(batch_size)]
    mini_batch = split_batch(input_batch, 2)
    batch_completions = []

    for batch in mini_batch:
        inputs = tokenizer(batch, return_tensors="pt").to(model.device)
        input_ids_cutoff = inputs.input_ids.size(dim=1)

        generated_ids = model.generate(
            **inputs,
            use_cache=True,
            max_new_tokens=512,
            temperature=0.2,
            top_p=0.95,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,  # model has no pad token
        )

        batch_completions += tokenizer.batch_decode(
            [ids[input_ids_cutoff:] for ids in generated_ids],
            skip_special_tokens=True,
        )

    return [filter_code(completion) for completion in batch_completions]


if __name__ == "__main__":
    # adjust for n = 10 etc
    num_samples_per_task = 10
    out_path = "results/mpt_large/eval.jsonl"
    os.makedirs("results/mpt_large", exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(
        "mosaicml/mpt-30b",
        trust_remote_code=True,
        use_auth_token=TOKEN,
    )

    model = torch.compile(
        AutoModelForCausalLM.from_pretrained(
            "mosaicml/mpt-30b",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
            use_auth_token=TOKEN,
            device_map="auto",
            max_memory={
                0: "30GiB",
                1: "30GiB",
            },
        ).eval()
    )

    run_eval(
        model,
        tokenizer,
        num_samples_per_task,
        out_path,
        generate_batch_completion,
    )
