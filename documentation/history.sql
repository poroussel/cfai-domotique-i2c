CREATE TABLE history (
 id serial PRIMARY KEY,
 tmstamp timestamp without time zone NOT NULL DEFAULT now(),
 name VARCHAR (255) NOT NULL,
 value VARCHAR (255) NOT NULL
);
