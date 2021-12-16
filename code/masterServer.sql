create table strategy
(
    id   VARCHAR(36) PRIMARY KEY,
    name varchar(20)
);
INSERT INTO strategy
VALUES ('71e56d8e-f665-40ca-b812-3b820dd671cb', 'fcfs');
INSERT INTO strategy
VALUES ('4a1cacb0-8c0f-48ca-b301-26e7c3f939cf', 'lcfs');

CREATE TABLE users
(
    id VARCHAR(36) PRIMARY KEY
);
INSERT INTO users
VALUES ('alice');
INSERT INTO users
VALUES ('bob');

create table userStrategy
(
    userId     varchar(36),
    strategyId varchar(36),
    primary key (userId, strategyId),
    foreign key (userId) references users (id),
    foreign key (strategyId) references strategy (id)
);

INSERT INTO userStrategy
VALUES ('alice', '71e56d8e-f665-40ca-b812-3b820dd671cb');
INSERT INTO userStrategy
VALUES ('bob', '71e56d8e-f665-40ca-b812-3b820dd671cb');


create table userApplicationAddress
(
    userId             varchar(36),
    applicationAddress varchar(36),
    primary key (userId, applicationAddress),
    foreign key (userId) references users (id)
);


create table taskQueue
(
    id                 varchar(36),
    userId             varchar(36),
    applicationAddress varchar(36),
    query              varchar(36),
    timestamp          date,
    primary key (id),
    foreign key (userId, applicationAddress) references userApplicationAddress (userId, applicationAddress)
);
