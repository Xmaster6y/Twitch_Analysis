# Twitch Analysis

This Analysis has the ambition to study the Twitch network.
This repository was refactorized to be lighter (with compressed files).

## Read Before Using

For all the files (python and notebook) to run properly you should first unzip
the files `graphs.zip` and `Streamers_fr_1D.zip` see git-lfs for `Streamers_fr_1W.zip`

## Gathering the Network Information

### Twitch API

Getting the information through the Twitxh API really is the way to go! Yet it suffer from a
major disadvantage: you can only get the top 100 streamers for your request.

### [Twitchtracker](https://twitchtracker.com/channels/live/french?page=1)

Scraping the awesome Twitchtracker website is simple but not "cool". Since this website tracks
Twitch it must possible to do it ourselves, surely by scraping the home page of twitch.tv.

## Link Between Channels

- Two channels will be consider linked if a viewer has watched both of them over
a given amount of time. The more viewers the more stronger the links.

- The precedent formulation is, in a sense, equivalent to keeping the viewers. Yet keeping the viewers is
memory costly.


## Flow Over Time

Another study could be on the time point of view and the flow of viewers. We try
to give some insight for channel recommendation at the end of the notebook.

## File description

### [API Request](./api_req_streams.py)

The file `api_req_streams.py` is meant to order streamer request.
By default it runs for a complete day and store the results in the folder `Streamers_fr/`.

### [Twitchtracker Scraping](./scrape_streams.py)

The file `scrape_streams.py` is used to scrape the Twitchtracker website.
- :warning: modularity is not guaranteed.

## [Data Gathered](./Streamer_fr_1D.zip)

Contains the data of streamers for one given day. See the notebook for more
inforamation.

### [Building the Network](./build_network.py)

The file `build_network.py` is used to build the network by default from the folder `Streamers_fr/`.
It can be slightly modified to keep the viewers.
It mainly use the librairy `networkx`.
- The variant serve different purposes but are alike.

### [Network](./graphs.zip)

Graph used for the notebook and obtain from the data above.


### [Analysis Notebook](./twitch_analysis.ipynb)

The file `twitch_analysis.ipynb` is a notebook to
analyse the Twitch network/data.

### [Requirement.txt](./requirements.txt)

Python librairies requirements


### [Visualisation Gephi File](./images)

Images of representation obtained with Gephi.
- :warning: it correspond to the filtered graphs (see the notebook).
