# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 15:05:36 2015
TiddlPy

@author: Neil Griffin
"""

from bs4 import BeautifulSoup
#import parsedatetime
#import datetime
import re
import shutil
from time import strftime

#validtypes = ['text/vnd.tiddlywiki', 'text/plain']


def tid2dict(tiddler):
    dict=tiddler.attrs
    dict[u'text']=tiddler.text
    return dict

def loadtiddlers(wiki, tidnames='_loadall'):
    """
    loadtiddlers(wikifilename, tiddlernames)

    Loads the specified tiddlers from the specified TiddlyWiki file and returns
    the successfully loaded tiddlers as a list of dictionarys.

    tiddlernames specified as a list of strings. If not supplied, load all
    ordinary tiddlers in storeArea.
    """
    twsoup = BeautifulSoup(open(wiki, mode='rb'), "html.parser")
    storearea=twsoup.find('div', id="storeArea")
    tiddlers=storearea('div')
    matchedtiddlers=[]

    for t in tiddlers:
#        print (len(t), t['title'], len(tiddlers))
        if (t.has_attr(u'title') and t[u'title'] in tidnames) or tidnames=='_loadall':
#        if (t['title'] in tidnames or tidnames=='_loadall') and t['type'] in validtypes:
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
        foundlist.append(t[u'title'])
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
                matchlist.append(t[u'title'])
                break
    return matchlist


def wikiedit(wiki, tiddlers, deletelist, modi=u'python'):
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
    created={}
    for t in tiddlers:
        savelist.append(t[u'title'])
    with open(wiki, 'br') as fhi, open('temp__.html', 'bw') as fho:
        for line in fhi:
            if re.search('^<div id="storeArea"', line.decode('utf-8')):
####            if re.search('^<div id="storeArea"', line):
                fho.write(line)
                break
            fho.write(line)
        else:
            print('Store area not found')
            raise SystemExit
        enddiv=False
#        print('xxxxxxx')
        for line in fhi:
            try:
                line.decode('utf-8')
            except:
                print (line)
        for line in [ll.decode('utf-8') for ll in fhi]:
            if re.search('^<div', line):
                enddiv=False
 #               title = re.split('title="',line)[1].split('"')[0]
                if len(re.findall('title=".*?"',line))<1:
                    print ('xx',line)
                title = re.findall('title=".*?"',line)[0][7:-1]
                if len(title)<=0:
                    print('title not found in tiddler', line)  ##############################
#                    continue
                    raise SystemExit

##                if 'Trinity' in title:
##                    ttt=title
##                if title not in savelist:
##                    fho.write(line)
##                    continue
##                if title not in deletelist:
##                    fho.write(line)
##                    continue
                if title not in deletelist and title not in savelist:   ### not recognising £, " in deletelist entries
                    fho.write(line)
                    continue
                deletedlist.append(title)
                if re.search('created=".*?"',line):
                    createddate = re.findall('created=".*?"',line)[0][9:-1]
                    created[title]=createddate
                for line2 in fhi:
#                    fho.write(line2)
                    if re.search('^</div>', line2):
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
            tiddler['modified'] = strftime('%Y%m%d%H%M%S')
            if tiddler['title'] not in deletedlist:
                tiddler['created'] = tiddler['modified']
            elif created.has_key(tiddler['title']):
                tiddler['created'] = created[tiddler['title']]
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


def try_utf8(data):
    "Returns a Unicode object on success, or None on failure"
    try:
       return data.decode('utf-8')
    except UnicodeDecodeError:
       return None



if __name__ == "__main__":
    print ('Test of TiddlPy module')

    wiki = r"C:\Users\Neil\Dropbox\TiddlyWiki\NewsReaderTW5.1.8pre.html"
    wiki = r"C:\Users\neil.griffin\Documents\Dropbox\TiddlyWiki\NewsReaderTW5.1.9x.html"
    wiki = r"C:\Users\Neil\Documents\test\NewsReaderTW5.1.9 test_2.html"
    modi = 'NeilPy'

    tidnames = ['Cambridge News Articles', 'Test1', 'update']

    tiddlers = loadtiddlers(wiki, tidnames)
#    tiddlers = loadtiddlers(wiki)
    print(len(tiddlers))

#    tlist = findtiddlers(wiki, tidnames)
#    tlist = findtiddlers(wiki)
#    print(len(tlist), tlist)

#    tlist = searchtiddlers(wiki, 'tpt', ['title', 'tags'], True)
#    print(len(tlist), tlist)

#    newtid=[]
#    newtid.append({'title':'newtid4','text':'newtid text\nhello world', 'tags':'newtidtag'})
#    a,b=wikiedit(wiki, newtid, ['newtid1'], modi)
#    print ("deleted:{}\nwritten:{}".format(b,a))



