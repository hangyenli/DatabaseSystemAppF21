DROP SCHEMA IF EXISTS project;
CREATE SCHEMA project;

-- Application Data Schema

CREATE TABLE users (
    id   VARCHAR(36) PRIMARY KEY,
    name VARCHAR(127)
);

CREATE TABLE userNote (
    id     VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36),
    note   VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
);

CREATE TABLE userQuery (
    id     VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36),
    query  VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
);

CREATE TABLE userAccessedData (
    id             VARCHAR(36) PRIMARY KEY,
    userId         VARCHAR(36),
    accessedTable  VARCHAR(255),
    accessedColumn VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
);

-- Dataset Schema

CREATE TABLE eventLocation (
    id        VARCHAR(36) PRIMARY KEY,
    city      VARCHAR(127),
    county    VARCHAR(127),
    state     VARCHAR(3),
    latitude  DECIMAL(8, 6),
    longitude DECIMAL(8, 6)
);

CREATE TABLE eventFacility (
    id           VARCHAR(36) PRIMARY KEY,
    type         VARCHAR(255),
    facility     VARCHAR(255),
    direction    VARCHAR(255)
);

CREATE TABLE event (
    id              VARCHAR(36) PRIMARY KEY,
    organization    VARCHAR(255),
    eventLocationId VARCHAR(36),
    eventFacilityId VARCHAR(36),
    createTime      timestamp CHECK (createTime > '2000-01-01'),
    closeTime       timestamp CHECK (createTime > '2000-01-01'),
    description     VARCHAR(255),
    FOREIGN KEY (eventLocationId) REFERENCES eventLocation (id),
    FOREIGN KEY (eventFacilityId) REFERENCES eventFacility (id)
);

CREATE TABLE hateCrime (
    county                              VARCHAR(127),
    year                                INT,
    type                                VARCHAR(127),
    antiMale                            INT,
    antiFemale                          INT,
    antiTransgender                     INT,
    antiGenderIdentityExpression        INT,
    antiAge                             INT,
    antiWhite                           INT,
    antiBlack                           INT,
    antiAmericanIndianOrAlaskanNative   INT,
    antiAsian                           INT,
    antiNativeHawaiianOrPacificIslander INT,
    antiMultiRacialGroups               INT,
    antiOtherRace                       INT,
    antiJewish                          INT,
    antiCatholic                        INT,
    antiProtestant                      INT,
    antiIslamic                         INT,
    antiMultiReligiousGroups            INT,
    antiAtheismOrAgnosticism            INT,
    antiReligiousPracticeGenerally      INT,
    antiOtherReligion                   INT,
    antiBuddhist                        INT,
    antiEasternOrthodox                 INT,
    antiHindu                           INT,
    antiJehovahsWitness                 INT,
    antiMormon                          INT,
    antiOtherChristian                  INT,
    antiSikh                            INT,
    antiHispanic                        INT,
    antiArab                            INT,
    antiOtherEthnicityOrNationalOrigin  INT,
    antiNonHispanic                     INT,
    antiGayMale                         INT,
    antiGayFemale                       INT,
    antiGayMaleAndFemale                INT,
    antiHeterosexual                    INT,
    antiBisexual                        INT,
    antiPhysicalDisability              INT,
    antiMentalDisability                INT,
    totalIncidents                      INT,
    totalVictims                        INT,
    totalOffenders                      INT,
    PRIMARY KEY (county, year, type)
);
