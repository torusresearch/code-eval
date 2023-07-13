from human_eval.data import write_jsonl, read_problems
from transformers import (
    PreTrainedModel,
    PreTrainedTokenizer,
)
from tqdm import tqdm
import itertools
import os
import typing

BatchGenerator = typing.Callable[
    [PreTrainedModel, PreTrainedTokenizer, str, int], list[str]
]


# reference: https://github.com/declare-lab/instruct-eval/blob/main/human_eval/main.py#L35
def filter_code(completion: str) -> str:
    # The program tends to overwrite, we only take the first function
    completion = completion.lstrip("\n")
    return completion.split("\n\n")[0]


def fix_indents(text: str) -> str:
    return text.replace("\t", "    ")


def split_batch(samples: list[str], size=4):
    mini_batches = []

    for i in range(0, len(samples), size):
        mini_batches.append(samples[i : i + size])

    return mini_batches


def run_eval(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizer,
    num_samples_per_task: int,
    out_path: str,
    generate_batch_completion: BatchGenerator,
    is_starcoder: bool = False,
):
    # resume previous evaluation, if any
    complete = 0
    if os.path.exists(out_path):
        with open(out_path, "r") as f:
            lines = f.readlines()
            complete = len(lines) // num_samples_per_task
    
    problems = read_problems()
    # problems = dict(itertools.islice(problems.items(), 20))
    
    if complete >= len(problems):
        raise ValueError("Already completed evaluation")
    
    pbar = tqdm(total=len(problems) * num_samples_per_task, initial=complete*num_samples_per_task)

    for i, task_id in enumerate(problems):
        if i < complete:
            continue
        
        if is_starcoder:
            prompt = problems[task_id]["prompt"].replace("    ", "\t")
        else:
            prompt = problems[task_id]["prompt"]

        batch_completions = generate_batch_completion(
            model, tokenizer, prompt, num_samples_per_task
        )

        for sample in batch_completions:
            result = dict(
                task_id=task_id,
                completion=sample,
            )
            write_jsonl(out_path, [result], append=True)

        pbar.update(num_samples_per_task)

