# this is simple chat using gradio
import json
import json
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from utils.pushover_utils import send_push
from utils.logger import get_logger
from config.app_config import AppConfig
import gradio as gr

logger = get_logger(__name__, AppConfig.LOG_LEVEL)
# Read config
API_KEY = AppConfig.GITHUB_API_KEY
BASE_URL = AppConfig.GITHUB_BASE_URL
MODEL = AppConfig.GITHUB_MODEL_NAME

#API_KEY = AppConfig.LLAMA_API_KEY
#BASE_URL = AppConfig.LLAMA_BASE_URL
#MODEL = AppConfig.LLAMA_MODEL_NAME

# Create client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def record_user_details(email, name="Name not provided", notes="No notes provided"):
    logger.info(f"Recording user details: Email={email}, Name={name}, Notes={notes}")
    send_push(f"New user details recorded:\nEmail: {email}\nName: {name}\nNotes: {notes}", title="User Details Recorded")
    return f"Details recorded for {email}"

def record_unknown_question(question):
    logger.info(f"Recording unknown question: {question}")
    send_push(f"Unknown question recorded:\n{question}", title="Unknown Question Recorded")
    return "Your question has been recorded. We'll get back to you soon!"

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Use this tool to record that user is interested in being in touch and provided an e-mail address",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The user's email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "The user's name (optional)"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Any additional notes about the user (optional)"
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Use this tool to record a question that the assistant was not able to answer, so that it can be reviewed and used to improve the system in the future.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question that the assistant was not able to answer"
                    }
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }
    }
]    

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results


def get_summary():
    with open("./data/summary.txt", "r") as f:
        summary = f.read()
    return summary

name = "Puru D"
summary = get_summary()

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

system_prompt += f"\n\n## Summary:\n{summary}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            tools=tools
        )
        # Beautified JSON output
        logger.debug(f"Raw response:\n{json.dumps(response.model_dump(), indent=2)}")
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "tool_calls":
            logger.debug(f"Tool calls in response:\n{json.dumps([tc.model_dump() for tc in response.choices[0].message.tool_calls], indent=2)}")
            messsge = response.choices[0].message
            tool_calls = messsge.tool_calls
            tool_results = handle_tool_calls(tool_calls)
            messages.append(messsge)
            messages.extend(tool_results)
        else:
            done = True
    return response.choices[0].message.content

gr.ChatInterface(fn=chat, title="Puru D's Personal Website Chatbot", description="Ask me anything about my career, background, skills and experience!").launch()

    
