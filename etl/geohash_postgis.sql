ALTER TABLE osm_pois_buffer_ref
ADD COLUMN geohash VARCHAR;

UPDATE osm_pois_buffer_ref
set geohash= ST_Geohash(buffer);


ALTER TABLE chn_province_bound
ADD COLUMN geohash VARCHAR;

UPDATE chn_province_bound
set geohash= ST_Geohash(ST_Transform(geom, 4316));

CREATE INDEX geolife_data_gh ON geolife_data USING btree(geohash);
CREATE INDEX chn_province_bound_gh ON chn_province_bound USING btree(geohash);
CREATE INDEX osm_pois_buffer_ref_gh ON osm_pois_buffer_ref USING btree(geohash);
