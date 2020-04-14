-- Table: public.geo_ops_metrics

-- DROP TABLE public.geo_ops_metrics;

CREATE TABLE public.geo_ops_metrics
(
  runid integer NOT NULL,
  start_time timestamp without time zone,
  spatial_index character varying(200),
  intersect_time numeric(38,8),
  join_time numeric(38,8),
  cluster_time numeric(38,8),
  stop_time timestamp without time zone,
  total_time numeric(38,8),
  user_id numeric(38,8)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.geo_ops_metrics
  OWNER TO postgres;
