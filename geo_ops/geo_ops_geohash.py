# initial analytics
import pandas as pd
import psycopg2
import time
from creds import creds

conn = psycopg2.connect( host=creds['hostname'], user=creds['username'], password=creds['password'], dbname=creds['database'] )
conn.autocommit = True

def geo_ops(runid_int):
    runid = runid_int
    print('running iteration: %s' % runid)
    spatial_index='r_tree'
    print('using spatial index: %s' % spatial_index)
    start_time_epoch = time.time()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(start_time_epoch))

    start = time.time()
    intersection_query = """SELECT osm.place_name, osm.fclass, osm.geohash as pois_geohash, chn.geohash AS province_geohash,
    (st_intersection (osm.buffer, st_transform(chn.geom,4326))) AS intersection
    FROM osm_pois_buffer_ref osm, chn_province_bound chn
    limit 1000"""
    intersection_frame = pd.read_sql_query(intersection_query ,conn)
    elapsed_time_fl_iq = (time.time() - start) 
    print('Time for Intersection: {} s'.format(elapsed_time_fl_iq))

    start = time.time()
    join_query = """SELECT
      osm.fclass, osm.place_name,osm.buffer,
      geolife.user_id, geolife.active_date, geolife.lat, geolife.lon, geolife.geohash
    FROM geolife_data AS geolife
    JOIN osm_pois_buffer_ref AS osm
    ON concat(osm.geohash,'%') like geolife.geohash
    limit 100000;"""
    join_frame = pd.read_sql_query(join_query ,conn)
    elapsed_time_fl_sj = (time.time() - start)
    print('Time for Spatial Join: {} s'.format(elapsed_time_fl_sj))

    start = time.time()
#Use ST_ClusterDBSCAN with eps projection unit
#geolife_data projection = 4326, so projection unit in decimal degrees
#This will probably take forever because it's insane
    spatial_query = """SELECT geohash, count(*) FROM geolife_data
                where user_id=cast(floor(random() * 182 + 1)::integer as varchar)
                group by geohash
                having count(*) >= 1000
                """
    spatial_clusters = pd.read_sql_query(spatial_query ,conn)
    elapsed_time_fl_sc = (time.time() - start)
    print('Time for Spatial Clustering: {} s'.format(elapsed_time_fl_sc))

    end_time = time.time()
    elapsed_time_total = (end_time - start_time_epoch)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(end_time))
    print('Total time to run geo ops: {} s'.format(elapsed_time_total))
    cur = conn.cursor()

    tableid = 'geo_ops_metrics'

    cur.execute('INSERT INTO public.geo_ops_metrics (runid, spatial_index, start_time, intersect_time, join_time, cluster_time, stop_time, total_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (runid, spatial_index,start_time, elapsed_time_fl_iq, elapsed_time_fl_sj, elapsed_time_fl_sc, end_time, elapsed_time_total))
    print('record written to database')
    print('----------------------------------------')

def main():
    i = 0
    while i <1000:
        geo_ops(i)
        i +=1

main()
