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
sub_base = "_1D"
base = "./Streamers_fr" + sub_base + "/"
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
if viewers_loaded:
		with open(base + viewers_file, 'r') as file:
			viewers = json.load(file)
for streamer in os.listdir(base):
	if streamer == viewers_file:
		with open(base + viewers_file, 'r') as file:
			viewers = json.load(file)
			viewers_loaded = True
		continue
	if viewers_loaded:
		if os.listdir(base + streamer + "/"):
			streamers.append(streamer)
		for name_file in os.listdir(base + streamer + "/"):
			try:
				with open(base+streamer+"/"+"subjects.json", 'r') as file:
					subjects[streamer] = json.load(file)
			except:
				subjects[streamer] = "No subject"
	else:
		if os.listdir(base + streamer + "/"):
			streamers.append(streamer)
		viewers[streamer] = []
		for name_file in os.listdir(base + streamer + "/"):
			if name_file == "subjects.json":
				with open(base+streamer+"/"+name_file, 'r') as file:
					subjects[streamer] = json.load(file)
			else:
				with open(base+streamer+"/"+name_file, 'r') as file:
					data = json.load(file)
					try:
						viewers[streamer] += data["chatters"]["moderators"]
					except:
						print(streamer)
						raise SystemExit
					viewers[streamer] += data["chatters"]["viewers"]
	viewers[streamer] = list(set(viewers[streamer]) - bot_set)
if not viewers_loaded:
	with open(base + viewers_file, 'w') as file:
		json.dump(viewers, file)

#print(viewers)

G_streamers = nx.Graph()
G_streamers.add_nodes_from([(streamers[i], {"viewers":len(viewers[streamers[i]]),"subject":" ".join(subjects[streamers[i]])}) for i in range(len(streamers))])
#G_streamers.add_nodes_from(streamers)

for i in range(len(streamers)):
	for j in range(i+1,len(streamers)):
		link = len(set(viewers[streamers[i]]) & set(viewers[streamers[j]]))
		if link:
			G_streamers.add_edge(streamers[i], streamers[j], weight=link)




nx.readwrite.graphml.write_graphml(G_streamers, pre_base + "G_streamers_one_time_link" + sub_base + ".graphml")


# plt.figure()
# nx.draw(G_streamers, with_labels=True, font_weight='bold')
# plt.show()
#print(G_streamers.nodes.data())



## Temporal Network (snapshots cumulated)

 
start_m = np.inf
start_h = np.inf
start_d = np.inf
for streamer in streamers:
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

viewers_t = {streamer : [] for streamer in streamers}
streamers_t = []
for hour in range(24):
	time_stamps = set()
	for streamer in streamers:
		if os.listdir(base + streamer + "/"):
			pending_subj = False
			for name_file in os.listdir(base + streamer + "/"):
				if name_file != "subjects.json":			
					L = name_file.split('-')
					d, h, m = int(L[2]), int(L[3]), int(L[4][:2])
					if int((d-start_d)*24+h-start_h+(m-start_m)/60) == hour:
						time_stamps.add((d, h, m))
						if not (streamer in streamers_t):
							streamers_t.append(streamer)
						with open(base+streamer+"/"+name_file, 'r') as file:
							data = json.load(file)
							try:
								viewers_t[streamer] += data["chatters"]["moderators"]
							except:
								print(streamer)
								raise SystemExit
							viewers_t[streamer] += data["chatters"]["viewers"]
		viewers_t[streamer] = list(set(viewers_t[streamer]) - bot_set)
	if len(time_stamps) != 4:
		print(sorted(time_stamps))
		print(f"N time stamps {len(time_stamps)}")
		print(f"Hour {hour}")
		raise SystemExit

	#print(viewers)

	G_streamers_t = nx.Graph()
	G_streamers_t.add_nodes_from([(streamers_t[i], {"viewers":len(viewers_t[streamers_t[i]]),"subject":"".join(subjects[streamers_t[i]])}) for i in range(len(streamers_t))])
	#G_streamers.add_nodes_from(streamers)

	for i in range(len(streamers_t)):
		for j in range(i+1,len(streamers_t)):
			link = len(set(viewers_t[streamers_t[i]]) & set(viewers_t[streamers_t[j]]))
			if link:
				G_streamers_t.add_edge(streamers_t[i], streamers_t[j], weight=link)




	nx.readwrite.graphml.write_graphml(G_streamers_t, pre_base + "G_streamers_one_time_link" + sub_base + f"_H{hour:02d}" + ".graphml")






