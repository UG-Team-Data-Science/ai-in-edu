import json
import re

from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"
model = "meta-llama/Meta-Llama-3-8B-Instruct"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def format_history(message, history, system_prompt):
    chat_history = [{"role": "system", "content": system_prompt}]
    for query, response in history:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})
    chat_history.append({"role": "user", "content": message})
    return chat_history


def prompt_model(
    message,
    history=None,
    system_prompt="You are a powerful annotator of bibliographic data",
):
    chat_history = format_history(message, history if history else [], system_prompt)
    response = client.chat.completions.create(model=model, messages=chat_history)
    return response.choices[0].message.content


def get_json_from_text(response):
    entries = re.findall(r"\{.+?\}", response, re.DOTALL)
    json_object = {}

    if len(entries) == 1:  # this is a simplification
        json_string = entries[0]
        try:
            json_object = json.loads(json_string)
        except json.JSONDecodeError:
            pass
    return json_object
