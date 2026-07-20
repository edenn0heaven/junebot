from openai import OpenAI

def analyze_poem(client: OpenAI, poem: str) -> str:
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
Analyze this poem in detail:

--- POEM START ---
{poem}
--- POEM END ---

Provide a structured explanation:

1. Overall meaning
Explain what the poem is about and what message it conveys.

2. Main emotions
Describe the feelings expressed and how they are created.

3. Imagery and symbolism
Explain important images, metaphors, and symbols.

4. Literary techniques
Identify techniques such as:
- metaphors
- comparisons
- repetition
- personification
- sound patterns
- word choices

5. Structure and rhythm
Explain the poem's form, line structure, pacing, and rhythm.

6. Strengths
Explain what works particularly well.

7. Improvements
Give constructive advice to make the poem stronger.

8. Final evaluation
Give a short overall assessment.

Be detailed, and educational, but keep your analysis concise and within the character limit. Do not include sections that do not contain any meaningful content.
"""
            },
        ],
    )

    content = response.choices[0].message.content

    if not content:
        return "I could not generate an analysis for this poem."

    return content.strip()

def split_message(text: str, limit: int = 2000):
    return [text[i:i + limit] for i in range(0, len(text), limit)]