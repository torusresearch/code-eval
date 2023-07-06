def instruct_prompt(prompt: str) -> str:
    return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nComplete the following Python code without any tests or explanation\n{prompt}\n\n### Response:"""


def standard_prompt(prompt: str) -> str:
    return f"""Complete the following Python code without any tests or explanation\n{prompt}"""


def replit_glaive_prompt(prompt: str) -> str:
    return f"""Below is an instruction that describes a task, paired with an input that provides further context.\n Write a response that appropriately completes the request.\n\n ### Instruction:\nWrite a program to perform the given task.\n\n Input:\n{prompt}\n\n### Response:"""

def replit_orca_prompt(prompt: str) -> str:
    return f"""You are an assistant that solves programming tasks.\nComplete the following code snippet:\n{prompt}\n"""

def replit_leetcode_prompt(prompt: str) -> str:
    return prompt
