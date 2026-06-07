from groq import Groq
client=Groq(api_key="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")
print("Welcome to my AI Text Summarizer!")
print("-----------------------------------")
user_text=input("Enter the paragraph to summarize:")
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Summarize this in 3 bullet points: " + user_text}
    ]
)
print("\nHere is your summary:")
print(response.choices[0].message.content)
