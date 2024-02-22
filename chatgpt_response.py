from typing import Optional

from openai import OpenAI
import sys

def chatgpt_response_str(client: OpenAI,
                         prompt: str, model: str = "gpt-3.5-turbo",
                         temperature: float = 0.15,
                         system_context: Optional[str] = None) -> str:
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
    messages_with_context = [
        {
            "role": "system",
            "content": str(system_context)
        }
    ] + messages if system_context else messages

    response = client.chat.completions.create(
        model=model,
        messages=messages_with_context,
            temperature=temperature,
        max_tokens=len(prompt) + 500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print(chatgpt_response_str(OpenAI(), prompt=f"How do animals, like elephants, use their trunks for various tasks?",
                               system_context=f"Explain the answer to the question "
                                              f"in not more than 5 sentences."
                                              f"Your target audience is a kid "
                                              f"aged between 10 and 15. "))
