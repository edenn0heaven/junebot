def generate_poem(client, user: str, style: str = "love") -> str:

    response = client.chat.completions.create(
        model="openrouter/auto",
        temperature=1.1,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an award-winning poet.\n"
                    "Write ONLY the poem.\n"
                    "No titles, no explanations, no markdown, no extra text."
                ),
            },
            {
                "role": "user",
                "content": f"""
Write a 4-line original poem.

RECIPIENT NAME (STRICT - DO NOT MODIFY): {user}

Rules:
- The recipient's name must appear EXACTLY as written
- Never modify or stylize the name

Language: English
Theme: {style}

Poem rules:
- Write ONLY in English
- Exactly 4 lines
- Each line must be unique
- No repetition
- No placeholders
- Address the recipient directly
- Be emotional, vivid, poetic
- Avoid clichés

Return ONLY the poem.
""",
            },
        ],
    )

    poem = response.choices[0].message.content.strip()
    
    lines = [l.strip() for l in poem.splitlines() if l.strip()]
    if len(lines) != 4:
        return "\n".join(lines[:4])
    return poem