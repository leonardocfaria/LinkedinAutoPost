from openai import OpenAI

from linkedinautopost.constants.constants import (LLM_DEFAULT_MODEL,
                                                  QUERY_INITIAL_PROMPT)


class ChatGPT:
    def __init__(self):
        self.client = OpenAI()

    def ask_question(self, description, skills):
        final_question = "Event: " + description
        if skills:
            final_question += "\nSkills: "
            for skill in skills:
                final_question += f' {skill},'

        completion = self.client.chat.completions.create(
            model=LLM_DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": QUERY_INITIAL_PROMPT},
                {"role": "user", "content": final_question},
            ],
        )

        return completion.choices[0].message.content
