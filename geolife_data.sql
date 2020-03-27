-- Table: public.geolife_data

DROP TABLE public.geolife_data;

CREATE TABLE public.geolife_data
(
  objectid integer NOT NULL,
  active_date timestamp,
  lat numeric(38,8),
  lon numeric(38,8),
  alt numeric(38,2),
  label_id character varying(200),
  user_id character varying(200),
  geometry point,
  CONSTRAINT geolife_data_pkey PRIMARY KEY (objectid)
)
