import ast
import yaml
from openai import OpenAI
import argparse

parser = argparse.ArgumentParser(description="SysPmt is a Python-based tool designed to convert pseudo-code written in a Python-like syntax into precise and actionable system prompts for Large Language Models (LLMs). This tool is intended to help developers and prompt engineers who are adept at programming but may need assistance in crafting effective system prompts for LLMs.")
parser.add_argument('-c','--config', default='config.yaml', help='YAML configuration file path (default: config.yaml)')
parser.add_argument('-p','--prompt', default='prompt.pmt', help='Prompt file path (default: prompt.pmt)')
args = parser.parse_args()

config_file = args.config
prompt_file = args.prompt

api_key = 'sk-OPENAI_API_KEY'

def load_config():
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

config = load_config()

def load_pmt_file(filename):
    with open(filename, "r") as file:
        code = file.read()
    return code

def format_argument(arg, variables):
    if isinstance(arg, ast.Constant):
        return repr(arg.value)
    elif isinstance(arg, ast.Name):
        return variables.get(arg.id, arg.id)
    return str(arg)

def translate_call(node, variables):
    if isinstance(node.func, ast.Name):
        function_name = node.func.id
        arguments = ", ".join(format_argument(arg, variables) for arg in node.args)
        return f"{config['translations'].get(function_name, function_name)} {arguments}"

def translate_assign(node, variables):
    target = node.targets[0].id
    value = format_argument(node.value, variables)
    variables[target] = value
    return config['messages']['assign'].format(var=target, value=value)

def translate_node(node, variables):
    if isinstance(node, ast.If):
        condition = translate_call(node.test, variables)
        body_statements = "\n".join(translate_node(n, variables) for n in node.body)
        else_statements = "\n".join(translate_node(n, variables) for n in node.orelse)
        return (f"{config['messages']['if_condition'].format(condition=condition)}\n{body_statements}\n"
                f"{config['messages']['else_condition']}\n{else_statements}")
    elif isinstance(node, ast.Expr):
        return translate_call(node.value, variables) + "."
    elif isinstance(node, ast.Assign):
        return translate_assign(node, variables) + "."
    return ""

def translate_code_from_file(filename):
    code = load_pmt_file(filename)
    tree = ast.parse(code)
    variables = {}
    return "\n".join(translate_node(n, variables) for n in tree.body)

def send_to_chatgpt(translated_text):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are tasked to generate a precise and detailed system prompt based on the user's specific input provided in the message. Analyze the user's requirements and context to create an actionable and accurate system prompt that LLM can utilize to produce relevant responses. Ensure that the prompt addresses all key aspects conveyed by the user and is structured to guide the response effectively."},
            {"role": "user", "content": translated_text}
        ]
    )
    response_message = completion.choices[0].message.content
    return response_message

translated_text = translate_code_from_file(prompt_file)
system_prompt = send_to_chatgpt(translated_text)
print(system_prompt)
