# -*- coding: utf-8 -*-
"""
Date     : 2016/10/04 16:52:07
FileName : DBLPA.py
Author   : septicmk
"""

import urllib, urllib2
import os, sys
import json, re
import numpy as np
from optparse import OptionParser

url_base='http://dblp.uni-trier.de/db/conf/'
conf_lists = ['usenix', 'eurosys', 'osdi', 'sosp', 'ics', 'spaa', 'ppopp', 'ipps', 'sc']
years = [ '2010', '2011', '2012', '2013', '2014', '2015', '2016']
query_conf_lists = conf_lists
key_words_include = [ 'GPU' ]
key_words_exclude = []

anslist = {}
infos = {}

def dump():
    with open('infos.json', 'w') as f:
        json.dump(infos, f)

def load():
    global infos 
    with open('infos.json', 'r') as f:
       infos = json.load(f)

def is_fetched():
    return os.path.isfile('infos.json')

def clean():
    if is_fetched():
        os.remove('infos.json')

def find_all_anchor_of_year( year, html):
    pat = r'<span class="title" itemprop="name">.*?</span> .*?<span itemprop="datePublished">%s</span>.*?<a href="(.*?)">' % (year)
    ret = re.findall(pat, html);
    return ret;

def find_all_title_of_anchor( html ):
    pat = r'<span class="title" itemprop="name">(.*?)</span>'
    ret = re.findall( pat, html )
    return ret[1:]

def fetch( conf_lists, years ):
    for year in years:
        year_conf = {}
        for conf in conf_lists:
            url = url_base + conf
            print url
            html = urllib2.urlopen(url).read()
            procs = find_all_anchor_of_year( year, html );
            tmp = []
            for p in procs:
                print "pro:" + p
                html_ = urllib2.urlopen(p).read()
                tmp += find_all_title_of_anchor( html_ )
            year_conf[conf] = tmp
        infos[year] = year_conf
    dump()

def check( kws, s ):
    for kw in kws:
        if re.search(kw, s):
            return True
    return False


def count_list(key_words_include, key_words_exclude, lists, year):
    global anslist
    cnt = 0
    for title in lists:
        if check(key_words_include, title) and not check(key_words_exclude, title):
            cnt +=1
            anslist[year].append(title)
    return cnt

def query( key_words_include, key_words_exclude):
    global anslist
    data = {}
    anslist = {}
    for (year, year_conf_lists) in infos.items():
        total = 0
        anslist[year] = []
        for (conf, lists) in year_conf_lists.items():
            total += count_list(key_words_include, key_words_exclude, lists, year)
        data[year] = total

    return data

def draw_trend ( topic, data ):
    indexs = []
    cnts = []
    for (k,v) in data.items():
        indexs.append(k)
        cnts.append(v)
    indexs = map(lambda x: int(x), indexs)
    ln = np.arange(len(indexs))
    print ln
    fx = zip(indexs, cnts)
    fx = sorted(fx, cmp=lambda x,y: cmp(x[0], y[0]))
    indexs, cnts = zip(*fx)


    print indexs
    print cnts
    import matplotlib.pyplot as plt
    with plt.style.context('fivethirtyeight'):
        plt.plot(ln, cnts)
        plt.xticks(ln,indexs)
        plt.ylim (0, max(cnts) + 1)
        plt.show()


if __name__=='__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fetch", action="store_true",  help="fetch info to local.", default=False)
    parser.add_option("-q", "--query", action="store_true", help="query key words.", default=False)
    parser.add_option("-d", "--delete", action="store_true", help="query key words.", default=False)
    (options, args) = parser.parse_args()
    ops = options.__dict__
    if ops['fetch'] == True:
        if not is_fetched():
            fetch(conf_lists, years)

    if ops['query'] == True:
        load()
        data = query( key_words_include, key_words_exclude )
        with open('ans.json', 'w') as f:
            json.dump(anslist, f)
        draw_trend( '', data )

    if ops['delete'] == True:
        pass
