#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import psycopg2
import json
import codecs
import psycopg2.extras
import db_config as config

def get_personal_map(personal_map_id):
	try:
		# Получаем карту пользователя:
		if config.debug==True:
			print("""select json from personal_map where id=%(personal_map_id)d""" % {"personal_map_id":int(personal_map_id)})
		cur.execute("""select json from personal_map where id=%(personal_map_id)d""" % {"personal_map_id":int(personal_map_id)})
		personal_map = cur.fetchone()[0]
	except:
		print ("I am unable fetch data from db");sys.exit(1)
	return personal_map


# ======================================= main() ===========================

out_file=sys.argv[1]

try:
	if config.debug:
		print("connect to: dbname='" + config.db_name + "' user='" +config.db_user + "' host='" + config.db_host + "' password='" + config.db_passwd + "'")
	conn = psycopg2.connect("dbname='" + config.db_name + "' user='" +config.db_user + "' host='" + config.db_host + "' password='" + config.db_passwd + "'")
	cur = conn.cursor()
except:
    print ("I am unable to connect to the database");sys.exit(1)

# Берём карту пользователя:
personal_map=get_personal_map(config.personal_map_id)

if config.debug:
	print("\npersonal_map:", personal_map)

jdata=json.loads(personal_map)

#print ("\ndecoded:", codecs.getreader('utf8')(personal_map))

if config.debug:
	print("\njdata:", jdata)


result_json_data={}
result_json_data["type"]="FeatureCollection"
result_json_data["features"]=[]

for point in jdata["points"]:
	entry={}
	entry["type"]="Feature"
	entry["geometry"]={}
	entry["geometry"]["type"]="Point"
	entry["geometry"]["coordinates"]=[]
	entry["geometry"]["coordinates"].append(point["lon"])
	entry["geometry"]["coordinates"].append(point["lat"])
	entry["properties"]={}
	entry["properties"]["name"]=point["name"]
	entry["properties"]["description"]=point["description"]
	if point["color"] == 0:
		entry["properties"]["color"]="blue"
	elif point["color"] == 1:
		entry["properties"]["color"]="red"
	else:
		entry["properties"]["color"]="green"
	entry["properties"]["coordinates"]="%f, %f" % (point["lon"], point["lat"])
	result_json_data["features"].append(entry)

if config.debug:
	print("fire_test = %s" % json.dumps(result_json_data))

f=open(out_file,"w+")
if config.prefix != "":
	f.write(config.prefix)
f.write(json.dumps(result_json_data))
f.close()



