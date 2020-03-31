-- Table: public.osm_pois_ref

-- DROP TABLE public.osm_pois_ref;

CREATE TABLE public.osm_pois_ref
(
  lat numeric(38,8),
  lon numeric(38,8),
  osm_id integer NOT NULL,
  code integer,
  fclass character varying(200),
  place_name character varying(200),
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.osm_pois_ref
  OWNER TO postgres;

ALTER TABLE public.osm_pois_ref ADD COLUMN uuid SERIAL PRIMARY KEY;

ALTER TABLE public.osm_pois_ref ADD COLUMN geom GEOMETRY(point, 4326);
UPDATE public.osm_pois_ref SET geom = ST_SETSRID(ST_MakePoint(cast(lon as float), cast(lat as float)),4326);
