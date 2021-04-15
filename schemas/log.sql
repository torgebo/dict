CREATE TABLE log (
       id		PRIMARY KEY,
       created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       user_id		INTEGER NOT NULL,
       message  	VARCHAR(512),
       CONSTRAINT unique_subject_name UNIQUE(subject_name)
);
