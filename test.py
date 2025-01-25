import cohere
co = cohere.ClientV2(api_key="nz6fdh3FyK7sgrA25T17uyLTu33KNl16azQskw31")
res = co.chat_stream(
    model="command-r-plus-08-2024",
    messages=[{"role": "user", "content": "What is an LLM?"}],
)
for event in res:
    if event:
        if event.type == "content-delta":
            print(event.delta.message.content.text, end="")