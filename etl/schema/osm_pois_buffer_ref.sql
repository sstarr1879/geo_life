-- Table: public.osm_pois_buffer_ref

-- DROP TABLE public.osm_pois_buffer_ref;

CREATE TABLE public.osm_pois_buffer_ref
(
  lat numeric(38,8),
  lon numeric(38,8),
  osm_id double precision,
  code integer,
  fclass character varying(200),
  place_name character varying(200),
  uuid integer NOT NULL DEFAULT nextval('osm_pois_ref_uuid_seq'::regclass),
  geom geometry(Point,4326),
  buffer geometry(Polygon,4326),
  CONSTRAINT osm_pois__buffer_ref_pkey PRIMARY KEY (uuid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.osm_pois_buffer_ref
  OWNER TO postgres;

INSERT INTO osm_pois_buffer_ref(lat, lon, osm_id, code, fclass, place_name, uuid, geom, buffer)
SELECT p.lat, p.lon, p.osm_id, p.code, p.fclass, p.place_name, p.uuid, p.geom, ST_Buffer(p.the_geom, 0.0005)
FROM osm_pois_ref p;

CREATE INDEX osm_pois_buffer_ref_gix ON osm_pois_buffer_ref USING GIST (buffer);
