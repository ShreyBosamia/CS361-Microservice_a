CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
	date DATE NOT NULL,
    consumed_weight FLOAT NOT NULL,
	consumed_fat FLOAT NOT NULL,
	consumed_carbs FLOAT NOT NULL,
	consumed_protein FLOAT NOT NULL,
	consumed_cal FLOAT NOT NULL,
    user_id SERIAL NOT NULL,
	FOREIGN KEY(user_id) REFERENCES users(id),
    food_id SERIAL NOT NULL,
	FOREIGN KEY(food_id) REFERENCES foods(id)
)

-- example insert statement (users table and foods table must exist, with corresponding data)
INSERT INTO logs (date, consumed_weight, consumed_fat, consumed_carbs, consumed_protein, consumed_cal, user_id, food_id)
VALUES 
('2024-11-24', 1, 2, 18, 4, 106, 1, 10),
('2024-11-24', 1, 2, 4, 24, 130, 1, 12),
('2024-11-24', 1, 10, 22, 20, 258, 1, 13),
('2024-11-24', 85, 4.5, 2, 24, 144.5, 1, 15),
('2024-11-25', 1, 2, 18, 4, 106, 1, 10),
('2024-11-25', 1, 2, 4, 24, 130, 1, 12),
('2024-11-25', 1, 10, 22, 20, 258, 1, 13),
('2024-11-25', 85, 4.5, 2, 24, 144.5, 1, 15);