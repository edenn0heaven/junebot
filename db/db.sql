CREATE TABLE IF NOT EXISTS daily_poems (
    date TEXT PRIMARY KEY,
    poem TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS saved_poems (
    user_id INTEGER NOT NULL,
    poem_id INTEGER NOT NULL,
    poem TEXT NOT NULL,

    PRIMARY KEY (user_id, poem_id)
);

CREATE TABLE IF NOT EXISTS last_poems (
    channel_id INTEGER PRIMARY KEY,
    message_id INTEGER NOT NULL
);