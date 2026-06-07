from groq import Groq

client = Groq(api_key="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")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "which ai is more better you,claud,chatgpt or gemini.choose only one and give reason for your choice"}
    ]
)

print(response.choices[0].message.content)