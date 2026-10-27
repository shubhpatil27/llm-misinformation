import ollama

MODEL = "llama3.1:latest"


def ask_llm(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"]


if __name__ == "__main__":

    test_prompt = """
Evaluate this factual claim:

"Ridley Scott is not the director of the film Alien."

Respond with SUPPORTS or REFUTES and briefly explain.
"""

    answer = ask_llm(test_prompt)

    print("\nLLM RESPONSE:")
    print(answer)