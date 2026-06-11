DROP TABLE IF EXISTS todos;
DROP TABLE IF EXISTS users;
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     email VARCHAR(255) NOT NULL UNIQUE,
--     first_name VARCHAR(255) NOT NULL,
--     last_name VARCHAR(255) DEFAULT NULL,
--     hashed_password VARCHAR(255) NOT NULL,
--     is_active BOOLEAN DEFAULT false,
--     role VARCHAR(255) NOT NULL
-- );


-- CREATE TABLE todos (
--     id SERIAL PRIMARY KEY,
--     title VARCHAR(225) NOT NULL,
--     description VARCHAR(225) NOT NULL,
--     priority INTEGER NOT NULL,
--     complete BOOLEAN NOT NULL,
--     owner_id INTEGER NOT NULL,
--     FOREIGN KEY (owner_id) REFERENCES users(id)
-- );