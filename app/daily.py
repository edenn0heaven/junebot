from db.database import get_daily_poem, save_daily_poem
from app.poems import generate_poem

def get_today_poem(client):
    poem = get_daily_poem()

    if poem is not None:
        return poem

    poem = generate_poem(
        client=client,
        user="Everyone",
        style="love",
    )

    save_daily_poem(poem)
    return poem