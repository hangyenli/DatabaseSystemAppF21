create schema if not exists project;

create table users
(
    id   varchar(36) primary key,
    name varchar(128)
);

create table userNote
(
    id     varchar(36) primary key,
    userId varchar(36),
    note   varchar(256),
    foreign key (userId) references users (id)
);

create table userQuery
(
    id     varchar(36) primary key,
    userId varchar(36),
    query  varchar(256),
    foreign key (userId) references users (id)
);

create table userAccessedData
(
    id             varchar(36) primary key,
    userId         varchar(36),
    accessedTable  varchar(256),
    accessedColumn varchar(256),
    foreign key (userId) references users (id)
);
