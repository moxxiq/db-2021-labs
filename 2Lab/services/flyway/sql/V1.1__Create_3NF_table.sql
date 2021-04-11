drop table if exists eduplace_participant, participant, place, eduplace, test, eo;
drop type if exists lang, teststatus cascade;

CREATE TYPE lang AS ENUM (
    'українська', 'інша', 'польська', 'угорська', 'російська', 'молдовська', 'румунська');

CREATE TYPE teststatus AS ENUM (
    'Зараховано', 'Анульовано', 'Не подолав поріг', 'Не з’явився');

CREATE TABLE place
(
    placeid  serial primary key,
    regname  text,
    areaname text,
    tername  text,
    unique (regname, areaname, tername)
);

CREATE TABLE eo
(
    eoid    serial primary key,
    placeid serial references place (placeid),
    eoname  text,
    unique (placeid, eoname)
);

CREATE TABLE eduplace
(
    eduplaceid  serial primary key,
    eoid        serial references eo (eoid),
    eotypename  text,
    eoparent    text,
    tertypename ter,
    unique (eoid, eotypename, eoparent)
);

CREATE TABLE participant
(
    outid            character varying(36) primary key,
    placeid          serial references place (placeid),
    birth            smallint NOT NULL,
    sextypename      sex      NOT NULL,
    regtypename      text     NOT NULL,
    classprofilename text,
    classlangname    lang,
    year             smallint NOT NULL
);

CREATE TABLE eduplace_participant
(
    eduplaceid  serial references eduplace (eduplaceid),
    outid character varying(36) references participant (outid),
    unique (eduplaceid, outid)
);

CREATE TABLE test
(
    testid     serial primary key,
    outid      character varying(36) NOT NULL references participant (outid),
    eoid       serial references eo (eoid),
    name       text,
    status     teststatus,
    ball100    numeric,
    ball12     numeric,
    ball       numeric,
    adaptscale integer,
    langname   lang,
    dpalevel   text,
    unique (outid, name)
);
