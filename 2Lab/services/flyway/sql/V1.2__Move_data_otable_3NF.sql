CREATE TEMP TABLE fixed_areaname_subjects as
select distinct outid,
                ukrptregname                                                   as regname,
                regexp_replace(ukrptareaname, '. ' || ukrpttername || '$', '') as areaname,
                ukrpttername                                                   as tername,
                ukrptname                                                      as ptname,
                ukrtest                                                        as name,
                ukrteststatus                                                  as status,
                ukrball100                                                     as ball100,
                ukrball12                                                      as ball12,
                ukrball                                                        as ball,
                ukradaptscale                                                  as adaptscale,
                NULL                                                           as langname,
                NULL                                                           as dpalevel
from odata
union
select outid,
       histptregname,
       regexp_replace(histptareaname, '. ' || histpttername || '$', ''),
       histpttername,
       histptname,
       histtest       as name,
       histteststatus as status,
       histball100    as ball100,
       histball12     as ball12,
       histball       as ball,
       NULL,
       histlang       as langname,
       NULL           as dpalevel
from odata
union
select outid,
       mathptregname,
       regexp_replace(mathptareaname, '. ' || mathpttername || '$', ''),
       mathpttername,
       mathptname,
       mathtest       as name,
       mathteststatus as status,
       mathball100    as ball100,
       mathball12     as ball12,
       mathball       as ball,
       NULL,
       mathlang       as langname,
       NULL           as dpalevel
from odata
union
select outid,
       physptregname,
       regexp_replace(physptareaname, '. ' || physpttername || '$', ''),
       physpttername,
       physptname,
       phystest       as name,
       physteststatus as status,
       physball100    as ball100,
       physball12     as ball12,
       physball       as ball,
       NULL,
       physlang       as langname,
       NULL           as dpalevel

from odata
union
select outid,
       chemptregname,
       regexp_replace(chemptareaname, '. ' || chempttername || '$', ''),
       chempttername,
       chemptname,
       chemtest       as name,
       chemteststatus as status,
       chemball100    as ball100,
       chemball12     as ball12,
       chemball       as ball,
       NULL,
       chemlang       as langname,
       NULL           as dpalevel

from odata
union
select outid,
       bioptregname,
       regexp_replace(bioptareaname, '. ' || biopttername || '$', ''),
       biopttername,
       bioptname,
       biotest       as name,
       bioteststatus as status,
       bioball100    as ball100,
       bioball12     as ball12,
       bioball       as ball,
       NULL,
       biolang       as langname,
       NULL          as dpalevel
from odata
union
select outid,
       geoptregname,
       regexp_replace(geoptareaname, '. ' || geopttername || '$', ''),
       geopttername,
       geoptname,
       geotest       as name,
       geoteststatus as status,
       geoball100    as ball100,
       geoball12     as ball12,
       geoball       as ball,
       NULL,
       geolang       as langname,
       NULL          as dpalevel
from odata
union
select outid,
       engptregname,
       regexp_replace(engptareaname, '. ' || engpttername || '$', ''),
       engpttername,
       engptname,
       engtest       as name,
       engteststatus as status,
       engball100    as ball100,
       engball12     as ball12,
       engball       as ball,
       NULL,
       NULL,
       engdpalevel   as dpalevel
from odata
union
select outid,
       fraptregname,
       regexp_replace(fraptareaname, '. ' || frapttername || '$', ''),
       frapttername,
       fraptname,
       fratest       as name,
       frateststatus as status,
       fraball100    as ball100,
       fraball12     as ball12,
       fraball       as ball,
       NULL,
       NULL,
       fradpalevel   as dpalevel
from odata
union
select outid,
       deuptregname,
       regexp_replace(deuptareaname, '. ' || deupttername || '$', ''),
       deupttername,
       deuptname,
       deutest       as name,
       deuteststatus as status,
       deuball100    as ball100,
       deuball12     as ball12,
       deuball       as ball,
       NULL,
       NULL,
       deudpalevel   as dpalevel
from odata
union
select outid,
       spaptregname,
       regexp_replace(spaptareaname, '. ' || spapttername || '$', ''),
       spapttername,
       spaptname,
       spatest       as name,
       spateststatus as status,
       spaball100    as ball100,
       spaball12     as ball12,
       spaball       as ball,
       NULL,
       NULL,
       spadpalevel   as dpalevel
from odata;

create temp table fixed_area_eo as
select distinct outid,
                eoregname                                                as regname,
                regexp_replace(eoareaname, '. ' || eotername || '$', '') as areaname,
                eotername                                                as tername,
                eoname,
                eotypename,
                eoparent,
                tertypename
from odata;

insert into place (regname, areaname, tername)
select distinct regname, areaname, tername
from odata
union
select distinct regname, areaname, tername
from fixed_areaname_subjects
union
select distinct regname, areaname, tername
from fixed_area_eo
--              where regname is not null
;
insert into eo (placeid, eoname)
select distinct placeid, eoname
from (select distinct regname, areaname, tername, eoname
      from fixed_area_eo
      union
      select regname, areaname, tername, ptname
      from fixed_areaname_subjects) as eos
         join place on
        eos.tername = place.tername
        and eos.areaname = place.areaname
        and eos.tername = place.tername;

insert into eduplace (eoid, eotypename, eoparent, tertypename)
select distinct eo.eoid, eotypename, eoparent, tertypename::ter
from fixed_area_eo
         join place on fixed_area_eo.regname = place.regname
    and fixed_area_eo.areaname = place.areaname
    and fixed_area_eo.tername = place.tername
         join eo on eo.eoname = fixed_area_eo.eoname
    and eo.placeid = place.placeid;

insert into participant (outid, placeid, birth, sextypename, regtypename, classprofilename,
                         classlangname, year)
select odata.outid,
       regplace.placeid,
       odata.birth,
       odata.sextypename::sex,
       odata.regtypename,
       odata.classprofilename,
       odata.classlangname::lang,
       odata.year
from odata
         join place regplace on
        odata.regname = regplace.regname
        and odata.areaname = regplace.areaname
        and odata.tername = regplace.tername;

insert into eduplace_participant (outid, eduplaceid)
select outid, eduplaceid
from fixed_area_eo
         join place
              on fixed_area_eo.regname = place.regname
                  and fixed_area_eo.areaname = place.areaname
                  and fixed_area_eo.tername = place.tername
         join eo
              on eo.placeid = place.placeid
                  and eo.eoname = fixed_area_eo.eoname
         join eduplace
              on eo.eoid = eduplace.eoid
                  and eduplace.eoparent = fixed_area_eo.eoparent;

insert into test (outid, eoid, name, status, ball100, ball12, ball, adaptscale, langname, dpalevel)
select outid,
       eo.eoid,
       name,
       fsub.status::teststatus,
       ball100,
       ball12,
       ball,
       adaptscale,
       langname::lang,
       dpalevel
from fixed_areaname_subjects as fsub
         join place pins on fsub.regname = pins.regname
    and fsub.areaname = pins.areaname
    and fsub.tername = pins.tername
         join eo on eo.placeid = pins.placeid
    and fsub.ptname = eo.eoname
where fsub.name is not null;
