import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:1b"

SYSTEM_PROMPT = (
    "You are a friendly study buddy for school students. "
    "Explain concepts simply in short, clear answers. "
    "If the student writes in Hinglish or Hindi, reply in the same style."
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]


def ask_gemma(question):
    history.append({"role": "user", "content": question})
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": history, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        answer = r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        history.pop()
        return "Ollama chal nahi raha. Pehle Ollama app start karo."
    except Exception as e:
        history.pop()
        return f"Error aaya: {e}"

    history.append({"role": "assistant", "content": answer})
    return answer


print("=" * 38)
print("      GEMMA AI STUDY BUDDY")
print("      Student Learning Assistant")
print("=" * 38)
print("Powered by Gemma (local, via Ollama)")
print("Type 'exit' to close.\n")

while True:
    question = input("Your study question: ").strip()

    if question.lower() == "exit":
        print("Keep learning. Goodbye!")
        break

    if not question:
        print("Please enter a question.")
        continue

    print("\nThinking...\n")
    print(ask_gemma(question))
    print()