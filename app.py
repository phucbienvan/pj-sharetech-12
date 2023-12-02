import openai
import os
import gradio as gr
import json
import prompt_handler

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("api_key")

system_prompt = prompt_handler.get_prompt()

def generate_data(image_url):

    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    response = openai.ChatCompletion.create(**data)
    data = response["choices"][0]["message"]["content"]

    data = json.loads(data)

    data_json = {
        "Menu Name" : data.get("menuName"),
        "Description": data.get("description"),
        "nutrients": data.get("nutrients"),
    }

    return data_json["Menu Name"], data_json["Description"], data_json["nutrients"]

outputs = [
    gr.Textbox(label="Menu Name"),
    gr.Textbox(label="description"),
    gr.JSON(label="Nutrients"),
]

app = gr.Interface(fn=generate_data, inputs="text", outputs=outputs)
app.launch()
