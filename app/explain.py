from openai import OpenAI

async def get_poem(channel):
    messages = [message async for message in channel.history(limit=2)]
    if len(messages) < 2:
        return None
    return messages[1].content

async def explain_poem(client: OpenAI, poem: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        temperature=0.3,
        max_tokens=250,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert poetry critic, literature professor, "
                    "and creative writing teacher.\n"
                    "Your role is to explain poems clearly and deeply.\n"
                    "Do not just summarize the poem. Teach the reader how "
                    "the poem works.\n"
                    "Analyze meaning, emotions, structure, and writing "
                    "techniques.\n"
                    "Your analysis MUST NOT exceed 1500 characters, and still be comprehensive and as helpful as possible."
                ),
            },
            {   
                "role": "user",
                "content": f"""
                Explain this poem in detail: {poem}
                Provide a structured explanation:"""
            }])
    return response.choices[0].message.content