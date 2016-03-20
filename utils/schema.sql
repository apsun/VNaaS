create table novels(
    vndb_id integer primary key not null,
    name text not null collate nocase
);

create table characters(
    vndb_id integer primary key not null,
    name text not null collate nocase
);

create table novel_characters(
    novel_id integer not null,
    character_id integer not null,
    foreign key(novel_id) references novels(vndb_id),
    foreign key(character_id) references characters(vndb_id)
);

create table lines(
    id integer primary key not null,
    novel_id integer not null,
    character_id integer not null,
    line text not null,
    foreign key(novel_id) references novels(vndb_id),
    foreign key(character_id) references characters(vndb_id)
);
