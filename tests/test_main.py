import os
import pytest
import requests
from hypothesis import given, example
import hypothesis.strategies as st

from TiddlPy import loadtiddlers, searchtiddlers, findtiddlers, wikiedit


@pytest.fixture(scope='session')
def tiddlywikidotcom():
    filename = 'tempfile.html'
    r = requests.get('http://tiddlywiki.com')
    file = open(filename, 'wb')
    file.write(r.content)
    yield(filename)
#    os.remove(filename)


# @given(txt=st.text())
# def test_reading1(tiddlywikidotcom, txt):
#     t=loadtiddlers(tiddlywikidotcom, ['HelloThere'])
#     print(t[0]['title'])
#     assert t[0]['title'] == 'HelloThere'

def test_reading1(tiddlywikidotcom):
    t=loadtiddlers(tiddlywikidotcom, ['HelloThere'])
    print(t[0]['title'])
    assert t[0]['title'] == 'HelloThere'
    pass


# def test_reading2(tiddlywikidotcom):
#     pass

# def test_writing1(tiddlywikidotcom):
#     pass
# def test_writing2(tiddlywikidotcom):
#     pass

# def test_integrity1(tiddlywikidotcom):
#     pass
# def test_integrity2(tiddlywikidotcom):
#     pass


    