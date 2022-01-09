# Url providing informations

## Getting the most viewed users

https://api.twitch.tv/kraken/streams/
https://api.twitch.tv/helix/streams?first=20

## To have the user list of a stream

https://tmi.twitch.tv/group/user/USERNAMEHERE/chatters

## With curl

curl -X GET 'https://api.twitch.tv/helix/users?login=twitchdev' \
-H 'Authorization: Bearer td2g1ga0w8s9hcfq101oidtkr71ftv' \
-H 'Client-Id: 04xcfxwj2b2fv5oh359p4fh827g31p'

## List of streamers live

https://twitchtracker.com/channels/live/french?page=1

## List of best streamers

https://twitchtracker.com/channels/viewership/french?page=2 (Last 30 days)
https://twitchtracker.com/channels/hours-watched/french (Last 30 days)
