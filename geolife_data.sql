-- Table: public.geolife_data

-- DROP TABLE public.geolife_data;

CREATE TABLE public.geolife_data
(
  objectid integer,
  active_date timestamp without time zone,
  lat numeric(38,8),
  lon numeric(38,8),
  alt numeric(38,2),
  label_id character varying(200),
  user_id character varying(200),
  uuid integer NOT NULL DEFAULT nextval('geolife_data_uuid_seq'::regclass),
  geom geometry(Point,4326),
  CONSTRAINT geolife_data_pkey PRIMARY KEY (uuid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.geolife_data
  OWNER TO postgres;

-- CREATE INDEX [indexname] ON [tablename] USING GIST ( [geometrycolumn] );

CREATE INDEX geolife_data_gix ON geolife_data USING GIST (geom);
