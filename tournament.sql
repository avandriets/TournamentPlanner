-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop database if exists tournament;

CREATE DATABASE tournament;

\c tournament;

DROP TABLE if exists Players;

CREATE TABLE Players
(
    id SERIAL PRIMARY KEY,
    name TEXT
);

DROP TABLE if exists Matches;

CREATE TABLE Matches
(
    id SERIAL PRIMARY KEY,
    winner INT,
    loser INT
);