 # Do They Know This Song?
    by Hera Choi, Oxford, UK
A guessing game for Last.fm users. How well do you know your friends' music tastes?

    Video Demo:  https://youtu.be/WaKf-cQRpN8
    PyLast https://github.com/pylast/pylast

## Overview:
Enter a last.fm username and generates a track for 5 rounds. Player has to then guess if the last.fm user has played the track recently (past 7 days).

## Why not Spotify?
Although Spotify is more widely used, its API does not allow access to listening history, whereas a main purpose of Last.fm is to collect a user's Spotify history.

# How it works
## Getting recent tracks
Using the PyLast library to use the Last.fm API, a network object is created. User enters a Last.fm username and a User object is returned by network.get_user(). The program then checks if the user exists by attempting to access their most recent track, which, if empty, means the user is invalid.

The user's recent tracks are accessed by user.get_recent_tracks(), for the last 7 days, returned as a list of PlayedTrack objects. Accessing the entire listening history takes way too long.

As the user could listen to the same track multiple times, the list of recent tracks are converted into a set so duplicates are removed (as they could bias the randomness) then back to a list so random.choice() can work.

## Generating a question
Firstly, it is randomly determined whether the question's answer will be True or False. If True, a track is simply selected from the list of recent tracks.

If False, similar tracks are generated through PyLast's track.get_similar() based on a track in recents. Tracks are randomly chosen and returned when checked that the similar track is not in the recents. If all happens to be in the recents, the same process is applied to getting top tracks from a similar artist, then if there are none, a tag ('rock', 'blues' etc). The tag condition used to be the only backup, but as many tracks have no tags, this is a reserve option for very rare occasions. Similar artist seems to work better than tags as well, with it actually generating artists I have listened to before.

On occasions where the 'base' track selected is so little known on Last.fm there is no sufficient information to find a similar track, another track from recents is chosen.

If the recent list is exhausted, it will default to False and

## The guess
The final selected track is then printed and the user inputs 'y' or 'n' to answer the question of whether the track has been listened to recently. The string inputted is converted into a Boolean value or None when the input was improper.
## Play again
The game for the same user continues with another 5 rounds. Last.fm user is not changed as it can be time consuming to retrieve tracks again. Exit the program and start again to play with the history of a different user.

# Files:
## project.py
Contains main code for the game.
## test_project.py
Ensure correct running of logic, correct user input and never returning None for users or tracks.
## setup.py
Initialising code to create a PyLast network object, which is then used in the game to get access to Last.fm's real data.