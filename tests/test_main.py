import pytest
import requests

from TiddlPy import loadtiddlers, searchtiddlers, findtiddlers, wikiedit


@pytest.fixture(scope="session")
def tiddlywikidotcom():
    filename = 'tempfile.html'
    r = requests.get('http://tiddlywiki.com')
    file = open(filename, 'wb')
    file.write(r.content)
    yield filename
    # remove file


@pytest.fixture
def tempwifkifile(scope="class"):
    wikifilecopy = 'copyfilename.html'
    # copy example
    yield wikifilecopy
    #delete copy


class TestReading():
    def test_reading1(self, tiddlywikidotcom):
        pass
    def test_reading2(self, tiddlywikidotcom):
        pass
    def test_readtextfield(self):
        assert 1
    def test_readauthorfield(self):
        assert 1

class TestWriting():
    def test_writing1(self, tiddlywikidotcom):
        pass
    def test_writing2(self, tiddlywikidotcom):
        pass
    def test_readtextfield(self):
        assert 1
    def test_readauthorfield(self):
        assert 1
		
class TestIntegrity():
    def test_integrity1(self, tiddlywikidotcom):
        pass
    def test_integrity2(self, tiddlywikidotcom):
        pass


