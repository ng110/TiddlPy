# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 15:05:36 2015
TiddlPy

@author: Neil Griffin
"""

import re
import shutil
from time import strftime, gmtime
from bs4 import BeautifulSoup

#validtypes = ['text/vnd.tiddlywiki', 'text/plain']


def tid2dict(tiddler):
    """
    tid2dict(tiddler)

    Converts tiddler as a BeautifulSoup object into a Python dictionary
    """

    tiddict = tiddler.attrs
    tiddict[u'text'] = tiddler.text
    return tiddict

def loadtiddlers(wiki, tidnames='_loadall'):
    """
    loadtiddlers(wikifilename, tiddlernames)

    Loads the specified tiddlers from the specified TiddlyWiki file and returns
    the successfully loaded tiddlers as a list of dictionarys.

    tiddlernames specified as a list of strings. If not supplied, load all
    ordinary tiddlers in storeArea.
    """
    twsoup = BeautifulSoup(open(wiki, mode='rb'), "html.parser")
    storearea = twsoup.find('div', id="storeArea")
    tiddlers = storearea('div')
    matchedtiddlers = []

    for tid in tiddlers:
        if (tid.has_attr(u'title') and tid[u'title'] in tidnames) or tidnames == '_loadall':
#        if (t['title'] in tidnames or tidnames == '_loadall') and t['type'] in validtypes:
            matchedtiddlers.append(tid2dict(tid))
    return matchedtiddlers

def findtiddlers(wiki, tidnames='_loadall'):
    """
    wiki is the wikifilename
    tidnames is a list of tiddler titles

    Search for the specified tiddlers in the specified TiddlyWiki file. Return
    the list of tiddler titles successfully matched.

    If tidnames not supplied, search all ordinary tiddlers in storeArea.
    """
    foundtiddlers = loadtiddlers(wiki, tidnames)
    foundlist = []
    for tid in foundtiddlers:
        foundlist.append(tid[u'title'])
    return foundlist

def searchtiddlers(wiki, srchtxt, fieldlist, caseinsensitive=True):
    """
    wiki is the wikifilename

    Search all tiddlers, returning a list of tiddler titles for those tiddlers
    that match the regexp search text in any of the specified fields.

    Case insensitive by default.  Specify False for case sensitive.
    """
    alltiddlers = loadtiddlers(wiki)
    matchlist = []
    for tid in alltiddlers:
        for field in fieldlist:
            if tid.has_key(field) and re.search(srchtxt, tid[field], re.I if caseinsensitive else 0):
                matchlist.append(tid[u'title'])
                break
    return matchlist


def wikiedit(wiki, tiddlers, deletelist, modi=u'python'):
    """
    wiki is the wikifilename.

    Deletes tiddlers in the deletelist and the tiddlers list, if they currently
    exist, then writes the tiddlers list, adding/replacing the modifier
    attribute with the specified or default value.  Timestamps modified and/or
    created dates in UTC.

    Returns (writtenlist, deletedlist) - list of tiddlers successfully deleted
    and written.
    """
    encoding = 'utf-8'
    savelist = []
    writtenlist = []
    deletedlist = []
    created = {}
    for tid in tiddlers:
        savelist.append(tid[u'title'])
    with open(wiki, 'br') as fhi, open('temp__.html', 'bw') as fho:
        for line in fhi:
            if re.search('^<div id="storeArea"', line.decode(encoding)):
                fho.write(line)
                break
            fho.write(line)
        else:
            print('Store area not found')
            raise SystemError
        enddiv = False

        for line in fhi:
            if re.search(b'^<div', line):
                enddiv = False
                if len(re.findall(b'title=".*?"', line)) < 1:
                    print('error - no title in line: ', line)
                    raise SystemError
                title = (re.findall(b'title=".*?"', line)[0][7:-1]).decode(encoding)
                if len(title) <= 0:
                    print('title not found in tiddler', line)
                    raise SystemError
                if title not in deletelist and title not in savelist:
                    fho.write(line)
                    continue
                deletedlist.append(title)
                if re.search(b'created=".*?"', line):
                    createddate = re.findall(b'created=".*?"', line)[0][9:-1]
                    created[title] = createddate
                for line2 in fhi:
                    if re.search(b'^</div>', line2):
                        enddiv = True
                        break
            elif re.search(b'^</div>', line):
                if enddiv:
                    break
                else:
                    fho.write(line)
                    enddiv = True
            else:
                fho.write(line)
        else:
            print('end of Store area not found')
            raise SystemExit

        for tiddler in tiddlers:
            tiddler['modifier'] = modi
            tiddler['modified'] = strftime('%Y%m%d%H%M%S', gmtime())
            if tiddler['title'] not in deletedlist:
                tiddler['created'] = tiddler['modified']
            elif tiddler['title'] in created:
                tiddler['created'] = created[tiddler['title']].decode(encoding)
            fho.write(b'<div')
            for key in tiddler:
                if key == 'text':
                    continue
                fho.write(b' ' + bytes(key, encoding)
                          + b'="' + bytes(tiddler[key], encoding) + b'"')
            fho.write('>\n<pre>{}</pre>\n</div>\n'.format(tiddler['text']).encode(encoding))
            writtenlist.append(tiddler['title'])

        fho.write(line)  # delayed write of </div> line at end of storearea
        for line in fhi:
            fho.write(line)
        # end 'with'

    shutil.copyfile('temp__.html', wiki)
    return (writtenlist, deletedlist)


if __name__ == "__main__":
    print('TiddlPy module for Python v3.x')

