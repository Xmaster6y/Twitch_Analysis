#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to build the nework
"""
import json
import os
import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt

pre_base = "graphs/"
base = "./Streamers_fr_1W/"
viewers_file = "viewers.json"
bot_set = {'anotherttvviewer', 'v_and_k', 'ladybugx3', 'painfullest', 'commanderroot',
		 'wizebot', 'kaxips06', 'nightbot','spiketrapclair', 'rimastino', 'anthropologydept',
		 'streamelements', 'luki4fun_bot_master', 'feet', 'lanarayyyy', 'feet', 'wzbot',
		 'virgoproz', 'itsvodoo', 'lukanard'}
streamers = []
viewers = {}
subjects = {}
viewers_loaded = True
filtering = False
 
start_m = np.inf
start_h = np.inf
start_d = np.inf
for streamer in os.listdir(base):
	for name_file in os.listdir(base + streamer + "/"):
		if name_file != "subjects.json":
			L = name_file.split('-')
			d, h, m = int(L[2]), int(L[3]), int(L[4][:2])
			if d < start_d:
				start_d = d
				start_h = h
				start_m = m
			elif d == start_d:
				if h < start_h:
					start_h = h
					start_m = m
				elif h == start_h:
					if m < start_m:
						start_m = m

subjects = {}
for streamer in os.listdir(base):
	with open(base+streamer+"/subjects.json", 'r') as file:
		subjects[streamer] = json.load(file)
							

for day in range(7):
	time_stamps = set()
	viewers = {}
	streamers = []
	for streamer in os.listdir(base):
		if os.listdir(base + streamer + "/"):
			for name_file in os.listdir(base + streamer + "/"):
				if name_file != "subjects.json":			
					L = name_file.split('-')
					d, h, m = int(L[2]), int(L[3]), int(L[4][:2])
					if int((d-start_d)+(h-start_h)/24+(m-start_m)/(24*60)) == day:
						time_stamps.add((d, h, m))
						if not (streamer in streamers):
							streamers.append(streamer)
						with open(base+streamer+"/"+name_file, 'r') as file:
							data = json.load(file)
							try:
								viewers[streamer] += data["chatters"]["moderators"]
							except:
								viewers[streamer] = data["chatters"]["moderators"]
							viewers[streamer] += data["chatters"]["viewers"]
						viewers[streamer] = list(set(viewers[streamer]) - bot_set)
	if len(time_stamps) != 96:
		print(sorted(time_stamps))
		print(f"N time stamps {len(time_stamps)}")
		print(f"Day {day}")
		raise SystemExit
		

	#print(viewers['daazii_'])
	#print(subjects['daazii_'])
	G_streamers = nx.Graph()
	G_streamers.add_nodes_from([(streamers[i], {"viewers":len(viewers[streamers[i]]),"subject":"".join(subjects[streamers[i]])}) for i in range(len(streamers))])
	#G_streamers.add_nodes_from(streamers)

	for i in range(len(streamers)):
		for j in range(i+1,len(streamers)):
			link = len(set(viewers[streamers[i]]) & set(viewers[streamers[j]]))
			if link:
				G_streamers.add_edge(streamers[i], streamers[j], weight=link)




	nx.readwrite.graphml.write_graphml(G_streamers, pre_base + "G_streamers_one_time_link_1W_D"+ f"{day:01d}" + ".graphml")






