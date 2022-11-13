CREATE TABLE IF NOT EXISTS mainmenu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS shop (
    id integer PRIMARY KEY AUTOINCREMENT,
    title varchar NOT NULL,
    photo blob NOT NULL,
    description text,
    price integer NOT NULL,
    isActive boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    time integer NOT NULL
);
