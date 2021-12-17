create table strategy
(
    name varchar(20) primary key
);
INSERT INTO strategy
VALUES ('fcfs');
INSERT INTO strategy
VALUES ('lcfs');

CREATE TABLE users
(
    id VARCHAR(36) PRIMARY KEY
);


create table userStrategy
(
    userId     varchar(36),
    strategyName varchar(36),
    primary key (userId, strategyName),
    foreign key (userId) references users (id),
    foreign key (strategyName) references strategy (name)
);



create table userApplicationAddress
(
    userId             varchar(36),
    applicationAddress varchar(36),
    primary key (userId, applicationAddress),
    foreign key (userId) references users (id)
);

create table session(
    userId             varchar(36),
    applicationAddress varchar(36),
        status  varchar(5),

    primary key (userId, applicationAddress),
    foreign key (userId, applicationAddress) references userApplicationAddress (userId, applicationAddress)



);

create table taskQueue
(
    id                 varchar(36),
    userId             varchar(36),
    applicationAddress varchar(36),
    query              varchar(512),
    timestamp          timestamp
        default CURRENT_TIMESTAMP ,
    primary key (id),
    foreign key (userId, applicationAddress) references userApplicationAddress (userId, applicationAddress)
);
