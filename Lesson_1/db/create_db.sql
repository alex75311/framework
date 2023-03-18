PRAGMA foreign_keys = off;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS person;
create table person (idperson INTEGER primary key autoincrement not null unique,
                     firstname varchar(32),
                     lastname varchar(32)
                     );
drop table if exists category;
create table category (id INTEGER primary key autoincrement not null unique,
                       name varchar(32)
                       );
commit transaction;
pragma foreign_keys = on;
