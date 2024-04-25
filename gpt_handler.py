from openai import OpenAI


class GPTHandler:
    CONTEXT = "You are required to make a Linkedin post about an event with the information provided"

    def __init__(self):
        self.client = OpenAI()

    def ask_question(self, question):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": self.CONTEXT},
                {"role": "user", "content": question}
            ]
        )

        return completion.choices[0].message.content

