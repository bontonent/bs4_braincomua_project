CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    product_article VARCHAR(50) UNIQUE,
    title TEXT,
    price INTEGER,
    brand VARCHAR(100),
    color VARCHAR(50),
    count_feedback INTEGER,
    display_diagonal VARCHAR(20),
    display_resolution VARCHAR(50),
    memory VARCHAR(20),
    describe JSONB
);
