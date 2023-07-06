from datasets import load_dataset
import json

# Load the human eval dataset.
dataset = load_dataset("openai_humaneval")["test"]

# Load the eval results.
def load_jsonl(fn: str) -> list[dict]:
    with open(fn, 'r') as json_file:    
        for l in json_file:
            yield json.loads(l)
            
# Check if the canonical solution is in the eval results.
def solution_in_completion(problem, eval_results):
    for r in eval_results:
        if problem["canonical_solution"].strip() in r["completion"]:
            return True
    return False

def count_contained(dataset, eval_results):
    return sum(1 if solution_in_completion(problem, eval_results) else 0 for problem in dataset)

models = [
    "replit_glaive",
    "replit",
    "wizard",
]

for model in models:
    eval_results = list(load_jsonl(f"results/{model}/eval.jsonl"))
    print(f"{model}: {count_contained(dataset, eval_results) / len(dataset) * 100:.2f}%")
