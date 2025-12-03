import os
import platform
from dotenv import load_dotenv
from groq import Groq

from colored import *
from get_input import get_input
from screen import get_screen_text

# Enable ANSI colors on Windows terminal
if platform.system() == "Windows":
    try:
        import colorama
        colorama.init()
    except:
        pass

load_dotenv()

INTRO_TEXT = """
._   _  __   __ __    __
| \ | | \ \ / / \ \  / /
|  \| |  \ V /   \ \/ / 
| |\  |   | |    / /\ \  
|_| \_|   |_|   /_/  \_\     
""".strip()


def clear_screen():
    """Clear screen for both Linux and Windows."""
    os.system("cls" if platform.system() == "Windows" else "clear")


class GroqAI:
    model = "llama-3.3-70b-versatile"

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_llm_response(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        output = response.choices[0].message.content.strip()

        if output and (output[0] == output[-1]) and output.startswith(("'", '"')):
            output = output[1:-1]

        return output


def get_prompt():
    prompt = None
    try:
        prompt = get_input('>>> ').strip()
    except KeyboardInterrupt:
        cprint('>>>', "KeyboardInterrupt", color=RED)
    return prompt


def greet():
    cprint(INTRO_TEXT + '\n', color=YELLOW)
    cprint('[esc+enter]: submit the prompt\n[enter]:     enter a new line\n', color=MAGENTA)


def main(llm):
    messages = [
        {
            'role': 'system',
            'content': """
You are a helpful screen-aware CLI agent named nyx.
You respond to users in a short, concise and highly visible format for terminal output.
"""
        }
    ]

    while True:
        # try:
        prompt = get_prompt()

        if prompt is None:
            continue

        # commands
        if prompt.startswith('/screen'):
            screen_text = get_screen_text()
            prompt = f"screen data (ocr data): {screen_text}\nquery: {prompt[8:]}"

        if prompt == '/clear':
            clear_screen()
            greet()
            continue

        if prompt in ['/bye', '/exit']:
            break

        if prompt == '/empty':
            messages = []
            cprint('>>>', "Chat history cleared!!", color=MAGENTA)
            continue

        if prompt == '/help':
            cprint('>>>', "Available commands:", color=MAGENTA)
            cprint('>>>', "/screen - enable screen OCR", color=MAGENTA)
            cprint('>>>', "/clear  - clear the screen", color=MAGENTA)
            cprint('>>>', "/empty  - clear the messages", color=MAGENTA)
            cprint('>>>', "/bye    - exit", color=MAGENTA)
            cprint('>>>', "/help   - show this help", color=MAGENTA)
            continue

        # send request
        messages.append({'role': 'user', 'content': prompt})
        res = llm.get_llm_response(messages)
        messages.append({'role': 'assistant', 'content': res})

        cprint('>>>', res, color=CYAN)

        # except Exception as e:
        #     messages.append({'role': 'assistant', 'content': "Sorry I'm unable to respond"})
        #     cprint(f'>>> Exception: {str(e)}', color=RED)
            # cprint('>>>', "Sorry I'm unable to respond", color=RED)


if __name__ == '__main__':
    clear_screen()
    greet()

    llm = GroqAI()
    main(llm)
