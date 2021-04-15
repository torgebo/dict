CREATE TABLE subject (
       id		PRIMARY KEY,
       created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       subject_name  	VARCHAR(160),
       user_id		INTEGER NOT NULL,
       CONSTRAINT unique_subject_name UNIQUE(subject_name)
);
