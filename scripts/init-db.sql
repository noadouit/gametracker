DROP DATABASE IF EXISTS gametracker;
CREATE DATABASE gametracker CHARACTER SET utf8mb4;
USE gametracker;

CREATE TABLE players (
    player_id INT NOT NULL,
    username VARCHAR(100),
    email VARCHAR(200),
    registration_date DATE,
    country VARCHAR(100),
    level INT,
    CONSTRAINT pk_players PRIMARY KEY (player_id)
) ENGINE=InnoDB;

CREATE TABLE scores (
    score_id VARCHAR(20) NOT NULL,
    player_id INT,
    game VARCHAR(100),
    score INT,
    duration_minutes INT,
    played_at DATETIME,
    platform VARCHAR(50),
    CONSTRAINT pk_scores PRIMARY KEY (score_id),
    CONSTRAINT fk_scores_players 
        FOREIGN KEY (player_id) 
        REFERENCES players(player_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB;