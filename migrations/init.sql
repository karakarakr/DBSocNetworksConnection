CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE social_networks (
    id SERIAL PRIMARY KEY,
    soc_network VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    username VARCHAR(255) NOT NULL,
    description TEXT,
    followers INTEGER,
    verified BOOLEAN DEFAULT FALSE,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE
);