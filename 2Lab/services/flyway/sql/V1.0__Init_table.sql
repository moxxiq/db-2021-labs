DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sex') THEN
        CREATE TYPE sex AS ENUM ('жіноча', 'чоловіча');
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ter') THEN
        CREATE TYPE ter AS ENUM ('місто', 'село');
    END IF;
END
$$; 

create table if not exists odata
(
    outid            varchar(36) not null
        constraint odata_pkey
            primary key,
    birth            smallint,
    sextypename      sex,
    regname          text,
    areaname         text,
    tername          text,
    regtypename      text,
    tertypename      ter,
    classprofilename text,
    classlangname    text,
    eoname           text,
    eotypename       text,
    eoregname        text,
    eoareaname       text,
    eotername        text,
    eoparent         text,
    ukrtest          text,
    ukrteststatus    text,
    ukrball100       numeric,
    ukrball12        numeric,
    ukrball          numeric,
    ukradaptscale    integer,
    ukrptname        text,
    ukrptregname     text,
    ukrptareaname    text,
    ukrpttername     text,
    histtest         text,
    histlang         text,
    histteststatus   text,
    histball100      numeric,
    histball12       numeric,
    histball         numeric,
    histptname       text,
    histptregname    text,
    histptareaname   text,
    histpttername    text,
    mathtest         text,
    mathlang         text,
    mathteststatus   text,
    mathball100      numeric,
    mathball12       numeric,
    mathball         numeric,
    mathptname       text,
    mathptregname    text,
    mathptareaname   text,
    mathpttername    text,
    phystest         text,
    physlang         text,
    physteststatus   text,
    physball100      numeric,
    physball12       numeric,
    physball         numeric,
    physptname       text,
    physptregname    text,
    physptareaname   text,
    physpttername    text,
    chemtest         text,
    chemlang         text,
    chemteststatus   text,
    chemball100      numeric,
    chemball12       numeric,
    chemball         numeric,
    chemptname       text,
    chemptregname    text,
    chemptareaname   text,
    chempttername    text,
    biotest          text,
    biolang          text,
    bioteststatus    text,
    bioball100       numeric,
    bioball12        numeric,
    bioball          numeric,
    bioptname        text,
    bioptregname     text,
    bioptareaname    text,
    biopttername     text,
    geotest          text,
    geolang          text,
    geoteststatus    text,
    geoball100       numeric,
    geoball12        numeric,
    geoball          numeric,
    geoptname        text,
    geoptregname     text,
    geoptareaname    text,
    geopttername     text,
    engtest          text,
    engteststatus    text,
    engball100       numeric,
    engball12        numeric,
    engdpalevel      text,
    engball          numeric,
    engptname        text,
    engptregname     text,
    engptareaname    text,
    engpttername     text,
    fratest          text,
    frateststatus    text,
    fraball100       numeric,
    fraball12        numeric,
    fradpalevel      text,
    fraball          numeric,
    fraptname        text,
    fraptregname     text,
    fraptareaname    text,
    frapttername     text,
    deutest          text,
    deuteststatus    text,
    deuball100       numeric,
    deuball12        numeric,
    deudpalevel      text,
    deuball          numeric,
    deuptname        text,
    deuptregname     text,
    deuptareaname    text,
    deupttername     text,
    spatest          text,
    spateststatus    text,
    spaball100       numeric,
    spaball12        numeric,
    spadpalevel      text,
    spaball          numeric,
    spaptname        text,
    spaptregname     text,
    spaptareaname    text,
    spapttername     text,
    year             smallint
);