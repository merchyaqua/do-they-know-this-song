import pylast
import random
import re
import time
import datetime
from setup import setup


def main():
    network = setup()
    user = None
    while not user:
        username = input("Person's username: ")
        user = get_user(username, network)

    ago = datetime.datetime.timestamp(datetime.datetime.today() - datetime.timedelta(days=7))

    tops = user.get_top_tracks(limit=200)

    print('Loading listening history...')
    recents = user.get_recent_tracks(limit=None,time_from=int(ago),time_to=int(time.time()))
    while True:

        print()

        again = game(user, tops=tops, recents=recents)

        if not again:
            break
        print()

def game(user, tops, recents):
    r_copy = recents
    # print(len(tops), len(recents))
    # remove duplicates
    tops = list(set([t.item for t in tops]))
    recents = list(set([t.track for t in recents]))
    # notimplemented # if stranger, show top artists to infer
    score = 0
    for i in range(5):
        print(f'======= Round {i+1} =======')
        if len(recents) ==0:
            t_or_f = False
            question = generate_question(tops, r_copy, False)

        else:
            t_or_f = bool(random.randint(0,1))
            question = generate_question(tops, recents, t_or_f)
        if t_or_f:
            recents.remove(question) # stop repeats
        print('-',question,'- \n')
        # let user guess
        correct = guess(f'Do you think {user.name} has played this track in the past week? y/n ', t_or_f)
        # output result
        if correct:
            score += 1
        print(result(correct))
        print('Score:', score)
        time.sleep(1)
    print('============\nYou got', score, 'out of 5. \n')
    time.sleep(1)
    return play_again()

def get_user(username, network):
    user = network.get_user(username)
    try:
        if user.get_recent_tracks(limit=1):
            return user # user exists
    except pylast.PyLastError:
        print('User not found/they have no played tracks')
        return None

def generate_question(t, r, t_or_f):
    try:
        rando = random.choice(t)
    except IndexError:
        return None

    if t_or_f == True:
        # select one of their listened tracks
        return random.choice(r)
    else:
        #depending on difficulty selected (randomly), choose
        return select_similar(rando, t, r)

def select_similar(rando, t, r):
    def tag_similar(track):
        # print('Trying similar tags...')
        # too obscure so we have to generate through selecting a tag
        tags = track.get_top_tags()
        if not tags:
            return None
        tag = random.choice(tags).item
        return tag.get_top_tracks(10)

    def artist_similar(track):
        # returns a list of artist top tracks
        # print('Trying similar artists...')
        artists = track.get_artist().get_similar(5)
        if not artists:
            return None
        a = random.choice(artists).item
        return a.get_top_tracks(10)

    def track_similar(track):
        # print('Trying similar tracks...')
        t = track.get_similar(10)
        return None if not t else t

    # print(rando)
    functions = [track_similar,artist_similar, tag_similar]
    while True:
        t.remove(rando)
        # try out all functions
        for function in functions:

            try:
                similar_tracks = [t.item for t in function(rando)]
                for similar_track in similar_tracks:
                    st = similar_tracks.pop(random.randint(0,len(similar_tracks)))
                    if st not in r:
                        return st
                    # print('uhh')
            except IndexError:
                continue
            except TypeError:
                continue


        # # there are no similar tracks
        # print(f'{rando} is too indie. Retrying..')
        # both have been listened to - pick another 'base' track instead
        rando = random.choice(t)


def y_n(s):
    if matches := re.search(r'^([yY]|[nN])', s):
        g = matches.group(1).lower() == 'y'
        return g
    return None

def guess(prompt, t_or_f):
    while True:
        the_guess = input(prompt)
        g = y_n(the_guess)

        if g == t_or_f: # check correctness
            return True
        elif g == None:
            print('Type your answer properly') #invalid
        else:
            return False


def result(c):
    match c:
        case True:
            return('Yay! You are right.')
        case False:
            return('Nope')

def play_again():
    while True:
        again = y_n(input('Play again? y/n: '))
        if again == None:
            continue
        return again



if __name__ == '__main__':
    main()