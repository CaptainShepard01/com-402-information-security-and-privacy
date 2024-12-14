#!/usr/bin/env python3

import collections
from dataclasses import dataclass
import csv
import itertools

@dataclass
class Rating:
    user: str
    movie: str
    date: str
    stars: int

    def __str__(self):
        return f'{self.user},"{self.movie}",{self.date},{self.stars}'

def load_files(exercise):
    anon = []
    with open(f"com402-{exercise}.csv") as f:
        for email, movie, date, stars in csv.reader(f, skipinitialspace=True):
            anon.append(Rating(user=email, movie=movie, date=date, stars=stars))
    public = []

    with open(f"imdb-{exercise}.csv") as f:
        for email, movie, date, stars in csv.reader(f, skipinitialspace=True):
            public.append(Rating(user=email, movie=movie, date=date, stars=stars))

    user = []
    with open(f"user-{exercise}.csv") as f:
        user = set(f.read().rstrip().split("\n"))

    return anon, public, user


def get_most_common(items):
    """
    >>> get_most_common(["a", "a", "a", "b", "b"])
    'a'
    """
    most_common = collections.Counter(items).most_common()[0]
    item, count = most_common
    return item


def sort_by_freq(entries):
    """
    >>> sort_by_freq(["a", "a", "a", "b", "b"])
    ['a', 'b']
    """
    counter = collections.Counter(entries)
    return [item for item, count in counter.most_common()]


def filter_ratings_by_user(ratings, user):
    """
    >>> ratings = [Rating(user="a", movie="b", date=None, stars=5), Rating(user="b", movie="b", date=None, stars=5)]
    >>> list(filter_ratings_by_user(ratings, "b"))
    [Rating(user='b', movie='b', date=None, stars=5)]
    """
    for rating in ratings:
        if rating.user == user:
            yield rating
            
######## PART 3 HELPERS ########

import numpy as np
import datetime

def get_date_maps(ratings):
    """Map users to dates, movie to dates mappings."""
    user2dates = collections.defaultdict(list)
    movie2dates = collections.defaultdict(list)
    for rating in ratings:
        user2dates[rating.user].append(rating.date)
        movie2dates[rating.movie].append(rating.date)
    return user2dates, movie2dates


def get_one_hot_from_dates(dates, start=None, end=None):
    """List of dates to their one-hot representation."""
    start = start or datetime.date(1999, 1, 1)
    end = end or datetime.date(2017, 3, 3)
    one_hot = np.zeros((end - start).days)
    for date in dates:
        pos = (datetime.datetime.strptime(date, "%d/%m/%y").date() - start).days
        one_hot[pos] = 1.0

    return one_hot


def get_best_matching_item(target_dates, items2dates, kernel, n=1):
    """Get best matching item based on the convolution score."""
    if n <= 0:
        return 
    
    conv = np.convolve(kernel, get_one_hot_from_dates(target_dates), mode="same")
    item2score = {}
    for item, dates in items2dates.items():
        item2score[item] = np.dot(conv, get_one_hot_from_dates(dates))

    if n == 1:
        return max(item2score, key=item2score.get)

    sorted_item2score = {k: v for k, v in sorted(item2score.items(), key=lambda item: item[1], reverse=True)}

    return (set(itertools.islice(sorted_item2score.keys(), 0, n)))
