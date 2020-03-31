- Table: public.chn_province_bound

-- DROP TABLE public.chn_province_bound;

CREATE TABLE public.chn_province_bound
(
  fid character varying(200),
  the_geom character varying(2000000),
  gbcode90 integer,
  name_py character varying(200),
  name_hz character varying(200)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.chn_province_bound
  OWNER TO postgres;

ALTER TABLE public.chn_province_bound ADD COLUMN geom GEOMETRY(multipolygon, 2333);
UPDATE public.chn_province_bound SET geom = ST_GeomtryFromText(the_geom,2333);

CREATE INDEX chn_province_bound_gix ON chn_province_bound USING GIST (geom);
