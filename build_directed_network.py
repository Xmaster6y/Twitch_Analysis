#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to build the nework
"""
import json
import os
import networkx as nx
import numpy as np
from itertools import filterfalse

pre_base = "graphs/"
sub_base = "_1D"
base = "./Streamers_fr" + sub_base + "/"
viewers_file = "viewers.json"

subjects = {}
start_m = np.inf
start_h = np.inf
start_d = np.inf
for streamer in os.listdir(base):
	if streamer != viewers_file:
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
			else:
				with open(base+streamer+"/"+name_file, 'r') as file:
					subjects[streamer] = json.load(file)

time_stamp = (start_d, start_h, start_m)
all_time_viewer_watch_lists = {}
stream_time = {}
viewer_lists_pre = {}
G = nx.DiGraph()
step=0
while True:
	viewer_lists = {}
	for streamer in os.listdir(base):
		if streamer != viewers_file:
			if os.listdir(base + streamer + "/"):
				for name_file in os.listdir(base + streamer + "/"):
					if name_file != "subjects.json":			
						L = name_file.split('-')
						d, h, m = int(L[2]), int(L[3]), int(L[4][:2])
						if (d, h, m) == time_stamp:
							with open(base+streamer+"/"+name_file, 'r') as file:
								data = json.load(file)
								viewers = data["chatters"]["moderators"] + data["chatters"]["viewers"]
								for viewer in viewers:
									try:
										viewer_lists[viewer].append(streamer) 
									except KeyError:
										viewer_lists[viewer] = [streamer,]
							try:
								stream_time[streamer] += 1
							except KeyError:
								stream_time[streamer] = 1
	if not viewer_lists:
		print("NO MORE VIEWERS!") 
		print(list(G.nodes.data())[:10])
		print(list(G.edges.data())[:10])
		break

	duplicates = list(filterfalse(lambda v:len(viewer_lists[v])<=1,viewer_lists.keys()))
	for duplicate in duplicates:
		del viewer_lists[duplicate]
	for viewer in viewer_lists:
		streamer = viewer_lists[viewer][0]
		try:
			G.nodes[streamer]["watched_time"] += 1
		except KeyError:
			G.add_node(streamer, watched_time=1)
		if viewer in viewer_lists_pre.keys():
			streamer_pre = viewer_lists_pre[viewer][0]
			try:
				G.edges[(streamer_pre,streamer)]["change"] += 1
			except KeyError:
				G.add_edge(streamer_pre,streamer,change=1)
		try:
			all_time_viewer_watch_lists[viewer].append(streamer)
		except KeyError:
			all_time_viewer_watch_lists[viewer] = [streamer,]
			
	viewer_lists_pre = viewer_lists
	(d, h, m) = time_stamp
	time_stamp = (d+(h+(m+15)//60)//24, (h+(m+15)//60)%24, (m+15)%60)
	step+=1



nx.readwrite.graphml.write_graphml(G, pre_base + "G_streamers_watch_time_link" + sub_base + ".graphml")
with open(pre_base + "streamers_watch_time_link" + sub_base + "_ST", "w") as file:
	json.dump(stream_time, file)
with open(pre_base + "streamers_watch_time_link" + sub_base + "_WT", "w") as file:
	json.dump(all_time_viewer_watch_lists, file)
with open(pre_base + "streamers_watch_time_link" + sub_base + "_sub", "w") as file:
	json.dump(subjects, file)



