-- 사용할 데이터베이스: studydb
CREATE TABLE phonebook (
    phonebook_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    memo TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
