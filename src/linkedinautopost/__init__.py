from linkedinautopost.facade.chat_gpt import ChatGPT
from linkedinautopost.facade.linkedin import LinkedIn


def main():
    linkedin_handler = LinkedIn()
    gpt_handler = ChatGPT()
    message = input("Prompt: ")

    answer = gpt_handler.ask_question(message)
    print(answer)

    linkedin_handler.post(answer)
    # print(answer)
