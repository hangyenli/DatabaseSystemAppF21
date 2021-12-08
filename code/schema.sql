-- Application Data Schema

CREATE TABLE users (
    id   VARCHAR(36) PRIMARY KEY
);
INSERT INTO users VALUES ('alice');
INSERT INTO users VALUES ('bob');

CREATE TABLE userNote (
    id     VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36),
    note   VARCHAR(256),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

CREATE TABLE userQuery (
    id     VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36),
    query  VARCHAR(256),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

CREATE TABLE userAccessedData (
    id             VARCHAR(36) PRIMARY KEY,
    userId         VARCHAR(36),
    accessedTable  VARCHAR(256),
    accessedColumn VARCHAR(256),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

-- Dataset Schema

CREATE TABLE eventLocation (
    id        VARCHAR(36) PRIMARY KEY,
    city      VARCHAR(512),
    county    VARCHAR(512),
    state     VARCHAR(4),
    latitude  DECIMAL(100, 20),
    longitude DECIMAL(100, 20)
);

CREATE TABLE eventFacility (
    id           VARCHAR(36) PRIMARY KEY,
    type         VARCHAR(2048),
    facility     VARCHAR(1024),
    direction    VARCHAR(1024)
);
CREATE INDEX FacilityByAttributes ON eventFacility (type, facility, direction);

CREATE TABLE event (
    id              VARCHAR(36) PRIMARY KEY,
    organization    VARCHAR(512),
    eventLocationId VARCHAR(36),
    eventFacilityId VARCHAR(36),
    createTime      timestamp CHECK (createTime > '2000-01-01'),
    closeTime       timestamp default null,
    FOREIGN KEY (eventLocationId) REFERENCES eventLocation (id) on delete cascade ,
    FOREIGN KEY (eventFacilityId) REFERENCES eventFacility (id) on delete cascade
);
