import pylast
def setup():
    API_KEY = "d0fdedba80f404a92cf3bb7dcda39230"
    API_SECRET = "9a15aac73a7776dcf8deee14d7a18f30"
    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return network