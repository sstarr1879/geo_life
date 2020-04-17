# geo_life 

Exploration of Spatial Index performance for common geospatial analytics. 

### Repository Structure

* etl: scripts relating to schema and processing data
* geo_ops: scripts for running geospatial analytics. Specifically: intersection, spatial join, and clustering.
* metrics_analysis: final analytics and visualization of performance

### Data 

* geolife data: microsoft GPS data for 182 users approximately 24 million points (lat, lon, timestamp)
* open street map places of interest across china (with a 20m spatial buffer)
* China province boundaries

### Workflow

![dfd](/etl/Geolife_Flow.png)

* Use NiFi to populate postgres database with appropriate spatial index
* run geospatial operations (from EC2 or local compute) and write results to geo_ops_metrics table in postgresql.
* evaluate benchmarking metrics

### Requirements

* NiFi
* Linux VM (Ubuntu 16.04 LTE) with Python3
* AWS Free Tier Resources (Postgresql RDS, EC2 t2.micro, S3, Simple Query Service)
