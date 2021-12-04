DROP SCHEMA IF EXISTS project;
CREATE SCHEMA project;

-- Application Data Schema

CREATE TABLE users (
    id   VARCHAR(31) PRIMARY KEY,
    name VARCHAR(127)
);

CREATE TABLE userNote (
    id     VARCHAR(31) PRIMARY KEY,
    userId VARCHAR(31),
    note   VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

CREATE TABLE userQuery (
    id     VARCHAR(31) PRIMARY KEY,
    userId VARCHAR(31),
    query  VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

CREATE TABLE userAccessedData (
    id             VARCHAR(31) PRIMARY KEY,
    userId         VARCHAR(31),
    accessedTable  VARCHAR(255),
    accessedColumn VARCHAR(255),
    FOREIGN KEY (userId) REFERENCES users (id)
                ON DELETE CASCADE
);

-- Dataset Schema

CREATE TABLE eventLocation (
    id        VARCHAR(31) PRIMARY KEY,
    city      VARCHAR(127),
    county    VARCHAR(127),
    state     VARCHAR(3),
    latitude  DECIMAL(8, 6),
    longitude DECIMAL(8, 6)
);

CREATE TABLE eventFacility (
    id           VARCHAR(31) PRIMARY KEY,
    type         VARCHAR(255),
    facility     VARCHAR(255),
    direction    VARCHAR(255)
);

CREATE TABLE event (
    id              VARCHAR(31) PRIMARY KEY,
    organization    VARCHAR(255),
    eventLocationId VARCHAR(31),
    eventFacilityId VARCHAR(31),
    createTime      timestamp,
    closeTime       timestamp,
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
