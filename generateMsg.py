import os import openai
import wandb
import dotenv

openai.api_key = dotenv.dotenv_values(".env")["OPENAI_APIKEY"]

run = wandb.init(project='python gpt-3 discord bot')
prediction_table = wandb.Table(columns=["prompt", "completion"])


def generate(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['text']
