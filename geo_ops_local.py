# initial analytics
import pandas as pd
import psycopg2
import time
import random

conn = psycopg2.connect("local stuff")
conn.autocommit = True

def geo_ops(runid_int):  
    runid = runid_int
    print('running iteration: %s' % runid)
    randomUser = random.randint(1,181)
    print('random user: %s' % randomUser)
    spatial_index='r_tree'
    print('using spatial index: %s' % spatial_index)
    start_time_epoch = time.time()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_epoch))

    start = time.time()
    intersection_query = """SELECT osm.place_name, osm.fclass, osm.geom as pois_geom, chn.geom AS province_geom, 
        (st_intersection (osm.buffer, st_transform(chn.geom,4326))) AS intersection
        FROM osm_pois_buffer_ref osm, chn_province_bound chn
        limit 1000"""
    intersection_frame = pd.read_sql_query(intersection_query ,conn)
    elapsed_time_fl_iq = (time.time() - start) 
    print('Time for Intersection: {} s'.format(elapsed_time_fl_iq))

    start = time.time()
    join_query = """SELECT
        osm.fclass, osm.place_name,osm.buffer,
        geolife."user", geolife.time, geolife.lat, geolife.lon, geolife.geom
        FROM msft_trj AS geolife
        JOIN osm_pois_buffer_ref AS osm
        ON ST_Contains(osm.buffer, geolife.geom)
        limit 100000;"""
    join_frame = pd.read_sql_query(join_query ,conn)
    elapsed_time_fl_sj = (time.time() - start)
    print('Time for Spatial Join: {} s'.format(elapsed_time_fl_sj))

    start = time.time()
    #Use ST_ClusterDBSCAN with eps projection unit
    #geolife_data projection = 4326, so projection unit in decimal degrees
    #This will probably take forever because it's insane
    spatial_query = """SELECT *, ST_ClusterDBSCAN(geom, eps := .00005, minPoints := 1000)
                OVER(ORDER BY "user") AS cluster_id FROM msft_trj
                where cast(msft_trj."user" as varchar) = cast({randomUser} as varchar)
                """.format(randomUser=randomUser)
    spatial_clusters = pd.read_sql_query(spatial_query ,conn)
    print(spatial_clusters['user'].unique())
    user_id = str(spatial_clusters['user'].iloc[0])
    elapsed_time_fl_sc = (time.time() - start)
    print('Time for Spatial Clustering: {} s user_id = {}'.format(elapsed_time_fl_sc, user_id))

    end_time = time.time()
    elapsed_time_total = (end_time - start_time_epoch)
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
    print('Total time to run geo ops: {} s'.format(elapsed_time_total))
    cur = conn.cursor()
    tableid = 'geo_ops_metrics'
    # Try adding the user_id into the output
    cur.execute('INSERT INTO public.geo_ops_metrics (runid, user_id, spatial_index, start_time, intersect_time, join_time, cluster_time, stop_time, total_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                                                                    (runid, user_id, spatial_index, start_time, elapsed_time_fl_iq, elapsed_time_fl_sj, elapsed_time_fl_sc, end_time, elapsed_time_total))
    print('record written to database')
    print('----------------------------------------')

def main():
    i = 283
    while i < 1000:
        geo_ops(i)
        i +=1

main()
