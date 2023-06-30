CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name TEXT,
    author TEXT,
    year INTEGER,
    genre TEXT,
    visible BOOLEAN
);

CREATE TABLE loans (
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    date DATE
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books,
    user_id INTEGER REFERENCES users,
    score INTEGER,
    comment TEXT
);

CREATE TABLE wishlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT,
    author TEXT
);