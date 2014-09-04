#!/usr/bin/env python

import hashlib
import os
import random
import urllib

import sh
import bs4
import requests

dimensions = (12, 5)

datadir = './data'
avatar_dir = datadir + '/avatars'
montage_dir = datadir + '/montage'


def make_directories():
    try:
        os.makedirs(datadir)
    except OSError:
        pass

    try:
        os.makedirs(avatar_dir)
    except OSError:
        pass

    try:
        os.makedirs(montage_dir)
    except OSError:
        pass


def avatars(N):
    url = 'https://badges.fedoraproject.org/badge/mugshot/full'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    last_pane = soup.findAll(attrs={'class': 'grid-100'})[-1]
    persons = last_pane.findAll('a')

    persons = random.sample(persons, N)

    for person in persons:
        name = person.text.strip()
        openid = 'http://%s.id.fedoraproject.org/' % name
        hash = hashlib.sha256(openid).hexdigest()
        url = "https://seccdn.libravatar.org/avatar/%s" % hash
        yield (name, url)


def make_montage(candidates):
    """ Pull down avatars to disk and stich with imagemagick """

    filenames = []
    for name, url in candidates:
        filename = os.path.join(avatar_dir, name)
        if not os.path.exists(filename):
            print "Grabbing", name, "at", url
            urllib.urlretrieve(url, filename=filename)
        else:
            print "Already have", name, "at", filename
        filenames.append(filename)

    args = filenames + [montage_dir + '/montage.png']
    sh.montage('-tile', '%ix%i' % dimensions, '-geometry', '+0+0', *args)


def main():
    make_directories()
    N = dimensions[0] * dimensions[1]
    candidates = avatars(N)
    make_montage(candidates)

if __name__ == '__main__':
    main()
