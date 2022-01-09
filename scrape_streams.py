#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to get French streamers and viewers
"""

from requests_html import AsyncHTMLSession
import requests
import json
import os
import asyncio
import pause
from datetime import datetime, date
import argparse
import aiohttp
import asyncio
import time



async def get_streamers(session, url, not_streamers):
    streamers = []
    subjects = []
    while True:
        with await session.get(url) as resp:
            print(resp.status_code)
            for link in resp.html.links:
                if len(link.split('/'))==2 and not(link in not_streamers):
                    streamers.append(link[1:])
            subjects += list(map(lambda x:x.text,resp.html.find('div.meta')[0::2]))
            if resp.status_code != 200:
                print('Retrying')
                await asyncio.sleep(0.001)
            else:
                print('Success!')
                break
    if not streamers:
        print(f"No streamer at this url {url}")
    return streamers, subjects

async def get_viewers(session, streamer):
    async with session.get(f"https://tmi.twitch.tv/group/user/{streamer}/chatters") as resp:
        print(resp.status)
        data = await resp.json()
        return data

async def get_streams(N_pages, not_streamers, file_dump, file_subjects, base):
    session = AsyncHTMLSession()
    tasks = []
    for page in range(1, N_pages+1):
        url = f"https://twitchtracker.com/channels/live/french?page={page}"
        tasks.append(asyncio.ensure_future(get_streamers(session, url, not_streamers)))

    streamers_list, subjects_list = zip(*(await asyncio.gather(*tasks)))
    streamers = sum(streamers_list, start=[])
    subjects = sum(subjects_list, start=[])

    async with aiohttp.ClientSession() as session:
        tasks = []
        for streamer in streamers:
            try:
                os.mkdir(base+f"{streamer}/")
            except FileExistsError:
                pass
            tasks.append(asyncio.ensure_future(get_viewers(session, streamer)))

        data_list = await asyncio.gather(*tasks)
        for streamer, subject, data in zip(streamers,subjects,data_list):
            with open(base+f"{streamer}/"+file_dump, "w") as file:
                json.dump(data,file)
            with open(base+f"{streamer}/"+file_subjects,"w+") as file:
                try:
                    subjects_existing = json.load(file)
                    json.dump(subjects_existing+subjects,file)
                except:
                    json.dump(subject,file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--step', type=int, help='Time interval (in min)')
    parser.add_argument('--start_h', type=int, help='Starting hour')
    parser.add_argument('--start_m', type=int, help='Starting minute')
    parser.add_argument('--end_h', type=int, help='Ending hour')
    parser.add_argument('--end_m', type=int, help='Ending minute')
    parser.add_argument('--days', type=int, help='Days to run')
    parser.add_argument('-n', type=int, help='Number of pages to scrape')
    parser.add_argument('--n_times', type=int, help='Number times to scrape (overright end)')

    not_streamers = ['/languages', '/subscribers', '/statistics','/','/api','/games', '/clips',]
    file_dump = "first_dump.json"
    file_subjects = "subjects.json"
    base = "./Streamers_fr/"
    debug = True

    args = parser.parse_args()
    if debug == True:
        N_pages = 10
        day, month, year = date.today().strftime("%d/%m/%Y").split('/')
        pause.until(datetime(int(year), int(month), int(day), 00, 00))

        print("Asynchronus")
        start_time = time.time()
        asyncio.run(get_streams(N_pages, not_streamers, file_dump, file_subjects, base))
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        day, month, year = date.today().strftime("%d/%m/%Y").split('/')
        pause.until(datetime(int(year), int(month), int(day), 00, 00))

        start_h = args.start_h
        if start_h is None:
            start_h = 0
        start_m = args.start_m
        if start_m is None:
            start_m = 0
        step = args.step
        if step is None:
            step = 1
        days = args.days
        if days is None:
            days = 1
        N_pages = args.n
        if N_pages is None:
            N_pages = 5
        N_times = args.n_times
        if N_times is None:
            end_h = args.end_h
            if end_h is None:
                end_h = 23
            end_m = args.end_m
            if end_m is None:
                end_m = 59
            for j in range(days):
                for i in range(((end_h-start_h)*60+end_m-start_m)//step):
                    pause.until(datetime(int(year), int(month), int(day)+j, start_h+(start_m+i*step)//60, (start_m+i*step)%60))
                    file_dump = f"{year}-{month}-{int(day)+j}-{start_h+(start_m+i*step)//60}-{(start_m+i*step)%60:02d}_dump.json"
                    asyncio.run(get_streams(N_pages, not_streamers, file_dump, file_subjects, base))
        else:
            for j in range(days):
                for i in range(N_times):
                    pause.until(datetime(int(year), int(month), int(day)+j, start_h+(start_m+i*step)//60, (start_m+i*step)%60))
                    file_dump = f"{year}-{month}-{int(day)+j}-{start_h+(start_m+i*step)//60}-{(start_m+i*step)%60:02d}_dump.json"
                    asyncio.run(get_streams(N_pages, not_streamers, file_dump, file_subjects, base))