from gpt_handler import GPTHandler
from linkedin_handler import LinkedinHandler

linkedin_handler = LinkedinHandler()
gpt_handler = GPTHandler()

answer = gpt_handler.ask_question("The event was thew AWS summit yesterday, it gave me opportunities to network and learn about AWS")

print(answer)

linkedin_handler.post(answer)

