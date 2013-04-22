#!/usr/bin/env python
import os
import datanommer.models as m
import sqlalchemy
import oculum
import requests
import shelve
import urllib
import time
import sh

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
def good_gravatars(N=12 * 5):
    count = 0
    results = []
    checked = []
    while True:
        try:
            all_users = m.session.query(m.User)\
                .order_by(sqlalchemy.func.random())\
                .limit(500)\
                .all()
        except UnicodeDecodeError:
            print " * crap"
            all_users = []

        for user in all_users:
            if user.name in checked:
                continue
            checked.append(user.name)
            gravatar_url = oculum.make_gravatar(user.name)
            response = requests.get(gravatar_url, params={'d': 404})

            if response.status_code == 200:
                if (user.name, gravatar_url) not in results:
                    results.append((user.name, gravatar_url))
                    print len(results), "of", N, "good ones found so far."

            if len(results) >= N:
                return results


def refresh_cache():
    candidates = good_gravatars()

    import shelve
    d = shelve.open(os.path.join(datadir, "candidates.shelve"))
    d['candidates'] = candidates
    d.close()


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
    # This takes a long time
    #refresh_cache()

    import shelve
    d = shelve.open(os.path.join(datadir, "candidates.shelve"))
    candidates = d['candidates']
    d.close()

    make_montage(candidates)

if __name__ == '__main__':
    main()
