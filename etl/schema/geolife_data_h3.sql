-- Table: public.geolife_data

DROP TABLE public.geolife_data;

CREATE TABLE public.geolife_data
(
  objectid integer,
  active_date timestamp without time zone,
  lat numeric(38,8),
  lon numeric(38,8),
  alt numeric(38,2),
  label_id character varying(200),
  user_id character varying(200),
  geohash character varying(200),
  h3 character varying(200)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.geolife_data
  OWNER TO postgres;

-- Index: public.geolife_data_gh

-- DROP INDEX public.geolife_data_gh;

CREATE INDEX geolife_data_h3
  ON public.geolife_data
  USING btree
  (h3 COLLATE pg_catalog."default");
