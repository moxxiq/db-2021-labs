insert into place (regname, areaname, tername)
select distinct regname, areaname, tername
from odata
union
select ukrptregname,
       regexp_replace(ukrptareaname, '. ' || ukrpttername || '$', ''),
       ukrpttername
from odata
union
select histptregname,
       regexp_replace(histptareaname, '. ' || histpttername || '$', ''),
       histpttername
from odata
union
select mathptregname,
       regexp_replace(mathptareaname, '. ' || mathpttername || '$', ''),
       mathpttername
from odata
union
select physptregname,
       regexp_replace(physptareaname, '. ' || physpttername || '$', ''),
       physpttername
from odata
union
select chemptregname,
       regexp_replace(chemptareaname, '. ' || chempttername || '$', ''),
       chempttername
from odata
union
select bioptregname,
       regexp_replace(bioptareaname, '. ' || biopttername || '$', ''),
       biopttername
from odata
union
select geoptregname,
       regexp_replace(geoptareaname, '. ' || geopttername || '$', ''),
       geopttername
from odata
union
select engptregname,
       regexp_replace(engptareaname, '. ' || engpttername || '$', ''),
       engpttername
from odata
union
select fraptregname,
       regexp_replace(fraptareaname, '. ' || frapttername || '$', ''),
       frapttername
from odata
union
select deuptregname,
       regexp_replace(deuptareaname, '. ' || deupttername || '$', ''),
       deupttername
from odata
union
select spaptregname,
       regexp_replace(spaptareaname, '. ' || spapttername || '$', ''),
       spapttername
from odata
union
select eoregname,
       regexp_replace(eoareaname, '. ' || eotername || '$', ''),
       eotername
from odata
on conflict do nothing;

delete
from place
where tername is null
   or areaname is null
   or regname is null;

insert into place_type (place_placeid, tertypename)
select distinct place.placeid, odata.tertypename
from odata
         join place
              on odata.regname = place.regname
                  and odata.areaname = place.areaname
                  and odata.tername = place.tername
on conflict do nothing ;

insert into participant(outid, birth, sextypename, regtypename, classprofilename, classlangname, year)
select distinct outid, birth, sextypename, regtypename, classprofilename, classlangname::lang, year
from odata
on conflict do nothing;

insert into participant_place (participant_outid, place_placeid)
select distinct odata.outid, place.placeid
from odata
         join place
              on odata.regname = place.regname
                  and odata.areaname = place.areaname
                  and odata.tername = place.tername
on conflict do nothing ;

insert into eduinst(eoname, eotypename, eoparent, place_placeid)
select distinct odata.eoname, odata.eotypename, odata.eoparent, place.placeid
from odata
         join place
              on odata.regname = place.regname
                  and odata.areaname = place.areaname
                  and odata.tername = place.tername
where eoname is not NULL
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, adaptscale, participant_outid, place_placeid)
select ukrtest, ukrteststatus::teststatus, ukrball100, ukrball12, ukrball, ukradaptscale, odata.outid, place.placeid
from odata
         join place
              on odata.ukrptregname = place.regname
                  and odata.ukrptareaname = place.areaname
                  and odata.ukrpttername = place.tername
where ukrtest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select histtest, histteststatus::teststatus, histball100, histball12, histball, histlang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.histptregname = place.regname
                  and odata.histptareaname = place.areaname
                  and odata.histpttername = place.tername
where histtest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select mathtest, mathteststatus::teststatus, mathball100, mathball12, mathball, mathlang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.mathptregname = place.regname
                  and odata.mathptareaname = place.areaname
                  and odata.mathpttername = place.tername
where mathtest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select phystest, physteststatus::teststatus, physball100, physball12, physball, physlang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.physptregname = place.regname
                  and odata.physptareaname = place.areaname
                  and odata.physpttername = place.tername
where phystest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select chemtest, chemteststatus::teststatus, chemball100, chemball12, chemball, chemlang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.chemptregname = place.regname
                  and odata.chemptareaname = place.areaname
                  and odata.chempttername = place.tername
where chemtest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select biotest, bioteststatus::teststatus, bioball100, bioball12, bioball, biolang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.bioptregname = place.regname
                  and odata.bioptareaname = place.areaname
                  and odata.biopttername = place.tername
where biotest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, langname, participant_outid, place_placeid)
select geotest, geoteststatus::teststatus, geoball100, geoball12, geoball, geolang::lang, odata.outid, place.placeid
from odata
         join place
              on odata.geoptregname = place.regname
                  and odata.geoptareaname = place.areaname
                  and odata.geopttername = place.tername
where geotest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, participant_outid, place_placeid)
select engtest, engteststatus::teststatus, engball100, engball12, engball, odata.outid, place.placeid
from odata
         join place
              on odata.engptregname = place.regname
                  and odata.engptareaname = place.areaname
                  and odata.engpttername = place.tername
where engtest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, participant_outid, place_placeid)
select fratest, frateststatus::teststatus, fraball100, fraball12, fraball, odata.outid, place.placeid
from odata
         join place
              on odata.fraptregname = place.regname
                  and odata.fraptareaname = place.areaname
                  and odata.frapttername = place.tername
where fratest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, participant_outid, place_placeid)
select deutest, deuteststatus::teststatus, deuball100, deuball12, deuball, odata.outid, place.placeid
from odata
         join place
              on odata.deuptregname = place.regname
                  and odata.deuptareaname = place.areaname
                  and odata.deupttername = place.tername
where deutest is not null
on conflict do nothing;

insert into test(subjectname, status, ball100, ball12, ball, participant_outid, place_placeid)
select spatest, spateststatus::teststatus, spaball100, spaball12, spaball, odata.outid, place.placeid
from odata
         join place
              on odata.spaptregname = place.regname
                  and odata.spaptareaname = place.areaname
                  and odata.spapttername = place.tername
where spatest is not null
on conflict do nothing;
