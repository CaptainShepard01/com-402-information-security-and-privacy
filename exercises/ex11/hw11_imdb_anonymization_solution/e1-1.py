#!/usr/bin/env python3
import itertools
import collections
from helpers import *

victim_email = "donald.trump@whitehouse.gov"

anonymized, public, true_movies = load_files(1)

hash2movie = collections.defaultdict(list)
user2hash = collections.defaultdict(list)

submission_dates = []

for anon_entry, pub_entry in itertools.product(anonymized, public):
    # If the date and stars match record the candidate plaintext email and movie.
    if anon_entry.date == pub_entry.date and anon_entry.stars == pub_entry.stars:
        hash2movie[anon_entry.movie].append(pub_entry.movie)
        user2hash[pub_entry.user].append(anon_entry.user)

# Guess the victim's email hash as the most common candidate.
victim_hash_guess = get_most_common(user2hash[victim_email])
movie_guesses = set()
for anon_entry in filter_ratings_by_user(anonymized, victim_hash_guess):
    # Guess the movie name as most common candidate for this hash.
    movie_guess = get_most_common(hash2movie[anon_entry.movie])
    movie_guesses.add(movie_guess)
    
assert movie_guesses == true_movies

print(movie_guesses)