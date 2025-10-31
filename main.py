import os
from dotenv import load_dotenv
from groq import Groq

from colored import *
from get_input import get_input
from screen import get_screen_text

load_dotenv()

# INTRO_TEXT = """
# .________       ____     _______           __            ________        ____     _______          __                    
# |_   ___ `.   .'    `.  |_   __ \         /  \          |_   ___ `.    .'    `.  |_   __ \        /  \           _       
#   | |   `. \ /  .--.  \   | |__) |       / /\ \           | |   `. \  /  .--.  \   | |__) |      / /\ \         | |      
#   | |    | | | |    | |   |  __ /       / ____ \          | |    | |  | |    | |   |  __ /      / ____ \        | |      
#  _| |___.' / \  `--'  /  _| |  \ \_   _/ /    \ \_       _| |___.' /  \  `--'  /  _| |  \ \_  _/ /    \ \_      | |      
# |________.'   `.____.'  |____| |___| |____|  |____|     |________.'    `.____.'  |____| |___||____|  |____|     |_|      
#                                                                                                                 (_)      
# """.strip()
INTRO_TEXT = """
._   _  __   __ __    __
| \ | | \ \ / / \ \  / /
|  \| |  \ V /   \ \/ / 
| |\  |   | |    / /\ \  
|_| \_|   |_|   /_/  \_\     
""".strip()

class GroqAI:
    model = "llama-3.3-70b-versatile"

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def get_llm_response(self, messages):
        response = self.client.chat.completions.create(model=self.model, messages=messages)
        output = response.choices[0].message.content.strip()

        if output and (output[0] == output[-1]) and output.startswith(("'", '"')):
            output = output[1:-1]

        return output

def get_prompt():
	prompt = None
	try:
		prompt = get_input('>>> ').strip()
	except KeyboardInterrupt as e:
		cprint('>>>', "KeyboardInterrupt", color=RED)
	return prompt

def greet():
    cprint(INTRO_TEXT+'\n', color=YELLOW)
    cprint('[esc+enter]: submit the prompt\n[enter]:     enter a new line\n', color=MAGENTA)

def main(llm):
    messages = [
        {
            'role': 'system',
            'content': """
            You are an helpful screen-aware CLI agent named nyx.
            You respond to users in a short, concise and informative way, and you responses should be formated in a way that should be clearly visible on cli.
            """
        }
    ]
    
    while True:
        try:
            prompt = get_prompt()

            # check for commands
            if prompt==None: continue
            if prompt.startswith('/screen'):
                screen_text = get_screen_text()
                prompt = f"""
                screen data (ocr data): {screen_text}
                query: {prompt[8:]}
                """
            if prompt=='/clear': os.system('clear'); greet(); continue
            if prompt=='/bye' or prompt=='/exit': break
            if prompt=='/empty':
                messages = []
                cprint('>>>', "Chat history cleared!!", color=MAGENTA)
                continue
            if prompt=='/help':
                cprint('>>>', "Available commands:", color=MAGENTA)
                cprint('>>>', "/screen: enable agent to see your screen", color=MAGENTA)
                cprint('>>>', "/clear: clear the screen", color=MAGENTA)
                cprint('>>>', "/empty: clear the messages", color=MAGENTA)
                cprint('>>>', "/bye: exit the program", color=MAGENTA)
                cprint('>>>', "/help: show this help message", color=MAGENTA)
                continue

            messages.append({ 'role': 'user', 'content': prompt })
            res = llm.get_llm_response(messages)
            messages.append({ 'role': 'assistant', 'content': res }) 
            cprint('>>>', res, color=CYAN)
        except Exception as e:
            messages.append({ 'role': 'assistant', 'content': "Sorry I'm unable to responsed" })
            cprint('>>>', "Sorry I'm unable to responsed", color=RED)

if __name__ == '__main__':
    os.system('clear')
    greet()

    llm = GroqAI()
    main(llm)
