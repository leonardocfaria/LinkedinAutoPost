from openai import OpenAI

from linkedinautopost.constants.constants import (LLM_DEFAULT_MODEL,
                                                  QUERY_INITIAL_PROMPT)


class ChatGPT:
    def __init__(self):
        self.client = OpenAI()

    def ask_question(self, question):
        completion = self.client.chat.completions.create(
            model=LLM_DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": QUERY_INITIAL_PROMPT},
                {"role": "user", "content": question},
            ],
        )

        return completion.choices[0].message.content
