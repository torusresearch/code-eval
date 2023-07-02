# code-eval

## What

This is a repo I use to run human-eval on code models, adjust as needed. Some scripts adjusted from wizardcoder repo. The code is duplicated, mostly to handle edge cases around model tokenizing and loading (might eventually clean it up).

## Results
 
| model                                                               | pass@1 | pass@10 | screenshot                                                                                              |
| ------------------------------------------------------------------- | ------ | ------- | ------------------------------------------------------------------------------------------------------- |
| [WizardCoder](https://huggingface.co/WizardLM/WizardCoder-15B-V1.0) | 57%    | 68.9%   | ![wizardcoder](https://github.com/abacaj/code-eval/assets/7272343/0b941ff8-b474-4236-bbc0-89d925bbd34e) |



## Setup

Create python environment

```sh
python -m venv env && source env/bin/activate
```

Install dependencies

```sh
pip install -r requirements.txt
```

Run the eval script

```sh
# adjust file name for various models:
# models/eval_wizard.py
# models/eval_opencode.py
# models/eval_replit.py

python models/eval_wizard.py
```

Process the jsonl file to extract code samples from model completions

```sh
# adjust args for various models:
# --path results/wizard --out_path results/wizard/eval.jsonl
# --path results/opencode --out_path results/opencode/eval.jsonl
# --path results/replit --out_path results/replit/eval.jsonl

python process_eval.py --path results/wizard --out_path results/wizard/processed.jsonl --add_prompt
```

Then get the results

```sh
# adjust file for various models:
# results/wizard/processed.jsonl
# results/opencode/processed.jsonl
# results/replit/processed.jsonl

evaluate_functional_correctness results/wizard/processed.jsonl
```
