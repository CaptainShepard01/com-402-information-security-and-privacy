#!/usr/bin/env python3
import itertools
import collections
from helpers import *

anonymized, public, true_movies = load_files(2)

victim_email = "donald.trump@whitehouse.gov"

hash2movie = {}
movie2hash = {}

# Match movie hashes to plaintexts by frequency.
sorted_movie_hashes = sort_by_freq(entry.movie for entry in anonymized)
sorted_movie_names = sort_by_freq(entry.movie for entry in public)
for movie_hash, movie_name in zip(sorted_movie_hashes, sorted_movie_names):
    movie2hash[movie_name] = movie_hash
    hash2movie[movie_hash] = movie_name

# Get the victim's movie hashes from the public data.
victim_movie_hashes = set()
for pub_entry in filter_ratings_by_user(public, victim_email):
    victim_movie_hashes.add(movie2hash[pub_entry.movie])

# At this point, we have deanonymized a subset of victim's movies.
# Now we need to deanonymize the rest.

# Identify the victim's email hash.
# First, map the email hashes to the corresponding movie hashes from the anonymized data.
user_hash_2_movie_hashes = collections.defaultdict(list)
for anon_entry in anonymized:
    user_hash_2_movie_hashes[anon_entry.user].append(anon_entry.movie)

# Second, find the hash that has all the movie hashes from above.
found_match = False
for user_hash, movie_hashes in user_hash_2_movie_hashes.items():
    victim_hash_guess = user_hash
    if victim_movie_hashes.issubset(movie_hashes) and not found_match:
        victim_movie_hashes.update(movie_hashes)
        found_match = True

    # If multiple possibilities, then the generated datasets are not good.
    elif victim_movie_hashes.issubset(movie_hashes):
        raise ValueError("Multiple possible user hashes.")

# Guess the victim's email hash from the frequency mapping.
movie_guesses = set()
for movie_hash in victim_movie_hashes:
    movie_guesses.add(hash2movie[movie_hash])

assert movie_guesses == true_movies

print(true_movies)
