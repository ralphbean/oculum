#!/usr/bin/env python
import os
import sqlalchemy
import oculum
import shelve
import time
import sh
import bs4
import urllib
import hashlib
import requests

# For development purposes
datadir = oculum.datadir
gravatar_dir = oculum.gravatar_dir
montage_dir = oculum.montage_dir

try:
    os.makedirs(datadir)
except OSError:
    pass

try:
    os.makedirs(gravatar_dir)
except OSError:
    pass

try:
    os.makedirs(montage_dir)
except OSError:
    pass


# We need 12*5==60 images to do this right.
def avatars(N=12 * 5):

    count = 0

    url = 'https://badges.fedoraproject.org/badge/mugshot/full'

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    last_pane = soup.findAll(attrs={'class': 'grid-100'})[-1]
    persons = last_pane.findAll('a')
    for person in persons:
        count = count + 1
        if count >= N:
            break

        name = person.text.strip()
        openid = 'http://%s.id.fedoraproject.org/' % name
        hash = hashlib.sha256(openid).hexdigest()
        url = "https://seccdn.libravatar.org/avatar/%s" % hash
        yield (name, url)


def make_montage(candidates):
    """ Pull down gravatars to disk and stich with imagemagick """

    filenames = []
    for name, url in candidates:
        print "Grabbing", name, "at", url
        filename = os.path.join(gravatar_dir, name)
        urllib.urlretrieve(url, filename=filename)
        filenames.append(filename)

    args = filenames + [montage_dir + '/montage.png']
    sh.montage('-tile', '12x5', '-geometry', '+0+0', *args)


def main():
    candidates = avatars()

    make_montage(candidates)

if __name__ == '__main__':
    main()
