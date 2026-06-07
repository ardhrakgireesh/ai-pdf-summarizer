from groq import Groq
client=Groq(api_key="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")
file=open("sample.txt","r")
content=file.read()
file.close()
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Summarize this: " + content}
    ]
)

print(response.choices[0].message.content)