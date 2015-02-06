# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 15:05:36 2015
TiddlPy

@author: Neil Griffin
"""

from bs4 import BeautifulSoup
import re
import shutil


def tid2dict(tiddler):
    dict=tiddler.attrs
    dict['text']=tiddler.text
    return dict

def loadtiddlers(wiki, tidnames='_loadall'):
    """
    loadtiddlers(wikifilename, tiddlernames)

    Loads the specified tiddlers from the specified TiddlyWiki file and returns
    the successfully loaded tiddlers as a list of dictionarys.

    tiddlernames specified as a list of strings. If not supplied, load all
    ordinary tiddlers in storeArea.
    """
    twsoup = BeautifulSoup(open(wiki))
    store=twsoup.find('div', id="storeArea")
    tiddlers=store('div')
    matchedtiddlers=[]
    for t in tiddlers:
        if t['title'] in tidnames or tidnames=='_loadall':
            matchedtiddlers.append(tid2dict(t))
    return matchedtiddlers

def findtiddlers(wiki, tidnames='_loadall'):
    """
    wiki is the wikifilename
    tidnames is a list of tiddler titles)

    Search for the specified tiddlers in the specified TiddlyWiki file. Return
    the list of tiddler titles successfully matched.

    If tidnames not supplied, search all ordinary tiddlers in storeArea.
    """
    foundtiddlers = loadtiddlers(wiki, tidnames)
    foundlist=[]
    for t in foundtiddlers:
        foundlist.append(t['title'])
    return foundlist

def searchtiddlers(wiki, srchtxt, fieldlist, caseinsensitive=True):
    """
    wiki is the wikifilename

    Search all tiddlers, returning a list of tiddler titles for those tiddlers
    that match the regexp search text in any of the specified fields.

    Case insensitive by default.  Specify False for case sensitive.
    """
    alltiddlers = loadtiddlers(wiki)
    matchlist=[]
    for t in alltiddlers:
        for f in fieldlist:
            if t.has_key(f) and re.search(srchtxt, t[f], re.I if caseinsensitive else 0):
                matchlist.append(t['title'])
                break
    return matchlist


def wikiedit(wiki, tiddlers, deletelist, modi='python'):
    """
    wiki is the wikifilename

    Deletes tiddlers in the deletelist and the tiddlers list, if they currently
    exist, then writes the tiddlers list, adding/replacing the modifier
    attribute with the specified or default value.

    Returns (writtenlist, deletedlist) - list of tiddlers successfully deleted
    and written
    """
    savelist=[]
    writtenlist=[]
    deletedlist=[]
    for t in tiddlers:
        savelist.append(t['title'])
    with open(wiki) as fhi, open('temp__.html', 'w') as fho:
        for line in fhi:
            if re.search('^<div id="storeArea"', line):
                fho.write(line)
                break
            fho.write(line)
        else:
            print('Store area not found')
            raise SystemExit
        enddiv=False
        for line in fhi:
            if re.search('^<div', line):
                enddiv=False
                title = re.findall('title=".*?"',line)[0][7:-1]
                if len(title)<=0:
                    print('title not found')
                    raise SystemExit
                if title not in deletelist and title not in savelist:
                    fho.write(line)
                    continue
                deletedlist.append(title)
                for linex in fhi:
                    if re.search('^</div>', linex):
                        enddiv=True
                        break
            elif re.search('^</div>', line):
                if enddiv==True:
                    break
                else:
                    fho.write(line)
                    enddiv=True
            else:
                fho.write(line)
        else:
            print ('end of Store area not found')
            raise SystemExit

        for tiddler in tiddlers:
            tiddler['modifier'] = modi
            fho.write('<div')
            for key in tiddler:
                if key == 'text':
                    continue
                fho.write(' '+key+'="'+tiddler[key]+'"')
            fho.write('>\n<pre>{}</pre>\n</div>\n'.format(tiddler['text']))
            writtenlist.append(tiddler['title'])

        fho.write(line)  # delayed write of library modules line
        for line in fhi:
            fho.write(line)
        # end 'with'

    shutil.copyfile('temp__.html',wiki)
    return (writtenlist, deletedlist)





if __name__ == "__main__":
    print ('TiddlPy module')
