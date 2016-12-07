import pytest
import requests

from TiddlPy import loadtiddlers, searchtiddlers, findtiddlers, wikiedit


@pytest.fixture(scope=session)
def tiddlywikidotcom():
    filename = 'tempfile.html'
    r = requests.get('http://tiddlywiki.com')
    file = open(filename, 'wb')
    file.write(r.content)
    yield(filename)
    # remove file

@pytest.fixture(scope=class)
def dummywiki():
    pass

class TestReading():
    def test_reading1(tiddlywikidotcom):
        pass
    def test_reading2(tiddlywikidotcom):
        pass

class TestWriting():
    def test_writing1(tiddlywikidotcom):
        pass
    def test_writing2(tiddlywikidotcom):
        pass

class TestIntegrity():
    def test_integrity1(tiddlywikidotcom):
        pass
    def test_integrity2(tiddlywikidotcom):
        pass


    