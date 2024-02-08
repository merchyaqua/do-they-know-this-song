import pylast
def setup():
    API_KEY = ""
    API_SECRET = ""
    # when I host this you'll see
    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return network
