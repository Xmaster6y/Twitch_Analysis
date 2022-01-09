#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to get French streamers and viewers /!\ No more than the 100 best current streamers
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
from twitchAPI.twitch import Twitch




async def get_viewers(session, streamer):
    async with session.get(f"https://tmi.twitch.tv/group/user/{streamer}/chatters") as resp:
        print(resp.status)
        data = await resp.json()
        return data

async def get_streams(file_dump, file_subjects, base, N_streamers=100, lang='fr'):
    token_file = './secret.token'
    pass_file= './secret.pass'
    assert os.path.exists(token_file)
    with open(token_file) as f:
        token_str = f.readlines()[0][:-1]
    assert os.path.exists(pass_file)
    with open(pass_file) as f:
        pass_str = f.readlines()[0][:-1]
    twitch = Twitch(token_str, pass_str)

    data = twitch.get_streams(language=lang, first=N_streamers)["data"]
    streamers = []
    subjects = []
    for raw_info  in data:
        streamers.append(raw_info["user_login"])
        subjects.append(raw_info["game_name"])

    async with aiohttp.ClientSession() as session:
        tasks = []
        for streamer in streamers:
            try:
                os.mkdir(base+f"{streamer}/")
            except FileExistsError:
                pass
            tasks.append(asyncio.ensure_future(get_viewers(session, streamer.lower())))

        data_list = await asyncio.gather(*tasks)
        for streamer, subject, data in zip(streamers,subjects,data_list):
            with open(base+f"{streamer}/"+file_dump, "w") as file:
                json.dump(data,file)
            with open(base+f"{streamer}/"+file_subjects,"w+") as file:
                try:
                    subjects_existing = json.load(file)
                    json.dump(subjects_existing+[subject,],file)
                except:
                    json.dump([subject,],file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--step', type=int, help='Time interval (in min)')
    parser.add_argument('--start_h', type=int, help='Starting hour')
    parser.add_argument('--start_m', type=int, help='Starting minute')
    parser.add_argument('--duration', type=int, help='Duration in minutes')
    parser.add_argument('--days', type=int, help='Days to run')
    parser.add_argument('-n', type=int, help='Number of streamer (max 100 for more see the scraping script)')
    parser.add_argument('--n_times', type=int, help='Number times to scrape (overright duration)')

    file_dump = "first_dump.json"
    file_subjects = "subjects.json"
    base = "./Streamers_fr/"
    debug = False

    args = parser.parse_args()
    if debug:
        day, month, year = date.today().strftime("%d/%m/%Y").split('/')
        pause.until(datetime(int(year), int(month), int(day), 00, 00))

        print("Asynchronus")
        start_time = time.time()
        asyncio.run(get_streams(file_dump, file_subjects, base, N_streamers=5))
        print("--- %s seconds ---" % (time.time() - start_time))
    else:
        now = datetime.now()
        year, month, day = now.year, now.month, now.day

        start_h = args.start_h
        if start_h is None:
            start_h = now.hour
        else:
            start_h = max(start_h ,now.hour)

        start_m = args.start_m
        if start_m is None:
            start_m = now.minute
        else:
            start_m = max(start_m ,now.minute)

        step = args.step
        if step is None:
            step = 15

        days = args.days
        if days is None:
            days = 1

        N_streamers = args.n
        if N_streamers is None:
            N_streamers = 100
        elif N_streamers>100:
            raise NotImplementedError

        N_times = args.n_times
        if N_times is None:
            duration = args.duration
            if duration is None:
                duration = 24*60
            for j in range(days):
                for i in range(duration//step):           
                    pause.until(datetime(int(year), int(month), int(day)+j+(start_h+(start_m+i*step)//60)//24, (start_h+(start_m+i*step)//60)%24, (start_m+i*step)%60))
                    file_dump = f"{year}-{month}-{int(day)+j+(start_h+(start_m+i*step)//60)//24}-{(start_h+(start_m+i*step)//60)%24:02d}-{(start_m+i*step)%60:02d}_dump.json"
                    try:
                        asyncio.run(get_streams(file_dump, file_subjects, base))
                    except:
                        try:
                            asyncio.run(get_streams(file_dump, file_subjects, base, N_streamers = 50))
                        except:
                            try:
                                asyncio.run(get_streams(file_dump, file_subjects, base, N_streamers = 20))
                            except:
                                continue
        else:
            for j in range(days):
                for i in range(N_times):
                    pause.until(datetime(int(year), int(month), int(day)+j+(start_h+(start_m+i*step)//60)//24, (start_h+(start_m+i*step)//60)%24, (start_m+i*step)%60))
                    file_dump = f"{year}-{month}-{int(day)+j+(start_h+(start_m+i*step)//60)//24}-{(start_h+(start_m+i*step)//60)%24:02d}-{(start_m+i*step)%60:02d}_dump.json"
                    try:
                        asyncio.run(get_streams(file_dump, file_subjects, base))
                    except:
                        try:
                            asyncio.run(get_streams(file_dump, file_subjects, base, N_streamers = 50))
                        except:
                            try:
                                asyncio.run(get_streams(file_dump, file_subjects, base, N_streamers = 20))
                            except:
                                continue