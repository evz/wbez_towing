VPATH = raw:finished_files:build

include config.mk

SHPS = 'towing_300m_month.shp \
towing_400m_month.shp \
towing_500m_month.shp \
towing_750m_month.shp \
towing_1km_month.shp \
towing_2km_month.shp \
towing_3km_month.shp \
towing_300m_year.shp \
towing_400m_year.shp \
towing_500m_year.shp \
towing_750m_year.shp \
towing_1km_year.shp \
towing_2km_year.shp \
towing_3km_year.shp'

HEADERS = "type,date,wbez_category,primary_reason,reason_2,reason_3,reason_4,location,lat,lng"

.PHONY: all clean full_clean

clean:
	rm -Rf build/*

full_clean: 
	rm -Rf build/*
	rm -Rf finished_files/*

shps: $(SHPS)

towing.csv:
	@wget https://opendata.socrata.com/api/views/5a7j-xmzn/rows.csv?accessType=DOWNLOAD -O raw/$@
	@touch raw/$@

towing_cleaned.csv: towing.csv
	@python processors/open_csv.py raw/$(notdir $?) | \
		python processors/strip_whitespace.py | \
		python processors/make_latlng.py | \
		(echo $(HEADERS) ; tail -n +2) > build/$@

towing.table: towing_cleaned.csv
	csvsql build/$(notdir $?) \
		--db "postgresql://$(PG_USER):@$(PG_HOST):$(PG_PORT)/$(PG_DB)" --table wbez_towing --insert
	@touch build/$@

towing.geom: towing.table
	@psql -U $(PG_USER) -h $(PG_HOST) -d $(PG_DB) -c \
		"SELECT AddGeometryColumn('public', 'wbez_towing', 'geom', 4326, 'POINT', 2);"
	@psql -U $(PG_USER) -h $(PG_HOST) -d $(PG_DB) -c \
		"UPDATE wbez_towing SET geom=ST_GeometryFromText('POINT(' || lng || ' ' || lat || ')', 4326) \
		WHERE lng IS NOT NULL AND lat IS NOT NULL;"
	@touch build/$@

towing_300m_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00494560815341, 0.0027000027) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_400m_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00659414420455, 0.0036000036) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_500m_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00824268025569, 0.0045000045) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_750m_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0123640203835, 0.00675000675001) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_1km_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0164853605114, 0.00900000900001) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_2km_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0329707210228, 0.018000018) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_3km_month.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0494560815341, 0.027000027) as grid, \
		date_trunc('month', date) as month from wbez_towing group by month, grid"

towing_300m_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00494560815341, 0.0027000027) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_400m_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00659414420455, 0.0036000036) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_500m_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.00824268025569, 0.0045000045) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_750m_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0123640203835, 0.00675000675001) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_1km_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0164853605114, 0.00900000900001) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_2km_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0329707210228, 0.018000018) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

towing_3km_year.shp: towing.geom
	@pgsql2shp -f build/$@ -u $(PG_USER) -h $(PG_HOST) -d $(PG_DB) \
		"select count(*) as tow_count, st_snaptogrid(geom, 0.0494560815341, 0.027000027) as grid, \
		date_trunc('year', date) as year from wbez_towing group by year, grid"

%.geojson: %.shp
	@ogr2ogr -f GeoJSON build/$@ build/$(notdir $?); \

groups: %.geojson
	@python group_geojson.py
	@touch build/$@
