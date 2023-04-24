from lastfm import y_n, result, get_user, select_similar, generate_question
import pylast
from setup import setup

def test_get_user():

    network = setup()
    assert get_user('kjfdlasfjdfda', network) == None
    assert get_user('iohcareh', network)
    assert get_user('', network) == None


def test_y_n():
    assert y_n('y') == True
    assert y_n('Y') == True
    assert y_n('YES') == True
    assert y_n('Yeah of course') == True

    assert y_n('n') == False
    assert y_n('N') == False
    assert y_n('No') == False
    assert y_n('No of course not') == False

    assert y_n('hahaha') == None

def test_result():
    assert result(True) == 'Yay! You are right.'
    assert result(False) == 'Nope'


def test_select_similar():
    network = setup()
    t = [pylast.Track('Wallows','Remember When',network)]
    assert select_similar(t[0], t) != None

def test_generate_question():

    network = setup()
    t = [pylast.Track('Wallows','Remember When',network)]
    assert generate_question(t, True) == t[0]
    assert generate_question(t, False) != t[0]
    assert generate_question([], True) == None