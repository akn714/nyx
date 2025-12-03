### Reading list
- https://adasci.org/building-a-screen-aware-ai-with-screenenv-and-tesseract
- https://github.com/niuzaisheng/ScreenAgent
- [x] https://medium.com/@sumitgrakhonde/from-clicks-to-commands-a-visual-ai-that-understands-your-screen-768d60c788c9


### Tasks
- [x] adding history feature
- [ ] giving ability to run bash commands
	```
	import os
	import subprocess

	# Using os.system()
	os.system("ls -l")
	
	# Using subprocess.run()
	subprocess.run(["ls", "-l"])
	```
- [ ] Enabling voice conversation using tts
- [ ] Connecting the agent with different tools and services
- [ ] Making a central knowledge base of the agent so that I can communicate with the agent anywhere (like telegram, discord, cli or laptop) and the agent remembers every conversation along with which conversation was done on which platform
- [ ] Using local llms to make the agent faster
- [ ] Making the agent time aware, like if I say him 'remind me of these tasks tomorrow before closing the laptop' then next day if I ask for updates then he can remind of my tasks
- [ ] Giving ability to control mouse cursor and keyboard to control pc when it is asked for it.
- [ ] Giving a Directory access to agent to keep all its stuff, like persona, user data, memory of the agent, etc.
- **Future Plans**:
	- Giving control of pc to control every software on system through MCP.

