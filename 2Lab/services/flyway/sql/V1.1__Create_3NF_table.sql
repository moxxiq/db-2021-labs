drop table if exists participant, place, eduinst, test, participant_place, eduinst, place_type cascade;
drop type if exists lang, teststatus cascade;

CREATE TYPE lang AS ENUM (
    'українська', 'інша', 'польська', 'угорська', 'російська', 'молдовська', 'румунська');

CREATE TYPE teststatus AS ENUM (
    'Зараховано', 'Анульовано', 'Не подолав поріг', 'Не з’явився');

CREATE TABLE participant
(
    outid            character varying(36) NOT NULL
        constraint participant_pkey primary key,
    birth            smallint              NOT NULL,
    sextypename      sex                   NOT NULL,
    regtypename      text                  NOT NULL,
    classprofilename text,
    classlangname    lang,
    year             smallint              NOT NULL
);

CREATE TABLE place
(
    regname  text,
    areaname text,
    tername  text,
    placeid  serial
        constraint place_pkey primary key,
    unique (regname, areaname, tername)
);

CREATE TABLE eduinst
(
    eoname        text
        constraint eduinst_pkey primary key,
    eotypename    text,
    eoparent      text,
    place_placeid serial
        references place (placeid)
);

CREATE TABLE test
(
    subjectname       text,
    status            teststatus,
    ball100           numeric,
    ball12            numeric,
    ball              numeric,
    adaptscale        integer,
    langname          lang,
    testid            serial
        constraint test_pkey primary key,
    participant_outid character varying(36) NOT NULL
        references participant (outid),
    place_placeid     serial
        references place (placeid),
    unique (subjectname, participant_outid)
);

CREATE TABLE participant_place
(
    participant_outid character varying(36) NOT NULL
        references participant (outid),
    place_placeid     serial
        references place (placeid),
    unique (participant_outid, place_placeid)
);

CREATE TABLE place_type
(
    place_placeid serial unique
        references place (placeid),
    tertypename   ter
);
