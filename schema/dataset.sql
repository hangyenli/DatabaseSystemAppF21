create schema if not exists project;

create table eventLocation
(
    id        varchar(36) primary key,
    city      varchar(128),
    county    varchar(128),
    state     varchar(128),
    latitude  decimal(8, 6),
    longitude decimal(8, 6)
);

create table eventFacility
(
    id           varchar(36) primary key,
    type         varchar(256),
    facilityName varchar(256),
    direction    varchar(256)
);

create table event
(
    id              varchar(36) primary key,
    organization    varchar(256),
    eventLocationId varchar(32),
    eventFacilityId varchar(32),
    createTime      timestamp,
    closeTime       timestamp,
    description     varchar(256),
    foreign key (eventLocationId) references eventLocation (id),
    foreign key (eventFacilityId) references eventFacility (id)
);

create table hateCrime
(
    county                              varchar(128),
    year                                int,
    type                                varchar(128),
    antiMale                            int,
    antiFemale                          int,
    antiTransgender                     int,
    antiGenderIdentityExpression        int,
    antiAge                             int,
    antiWhite                           int,
    antiBlack                           int,
    antiAmericanIndianOrAlaskanNative   int,
    antiAsian                           int,
    antiNativeHawaiianOrPacificIslander int,
    antiMultiRacialGroups               int,
    antiOtherRace                       int,
    antiJewish                          int,
    antiCatholic                        int,
    antiProtestant                      int,
    antiIslamic                         int,
    antiMultiReligiousGroups            int,
    antiAtheismOrAgnosticism            int,
    antiReligiousPracticeGenerally      int,
    antiOtherReligion                   int,
    antiBuddhist                        int,
    antiEasternOrthodox                 int,
    antiHindu                           int,
    antiJehovahsWitness                 int,
    antiMormon                          int,
    antiOtherChristian                  int,
    antiSikh                            int,
    antiHispanic                        int,
    antiArab                            int,
    antiOtherEthnicityOrNationalOrigin  int,
    antiNonHispanic                     int,
    antiGayMale                         int,
    antiGayFemale                       int,
    antiGayMaleAndFemale                int,
    antiHeterosexual                    int,
    antiBisexual                        int,
    antiPhysicalDisability              int,
    antiMentalDisability                int,
    totalIncidents                      int,
    totalVictims                        int,
    totalOffenders                      int,
    primary key (county, year, type)
);
