from gpt_handler import GPTHandler
from linkedin_handler import LinkedinHandler
import requests


linkedin_handler = LinkedinHandler()
gpt_handler = GPTHandler()
message = input("Prompt: ")

answer = gpt_handler.ask_question(message)
print(answer)

linkedin_handler.post(answer)
#print(answer)



