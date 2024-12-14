#!/usr/bin/env python3

from helpers import *

victim_email = "donald.trump@whitehouse.gov"

spread = 14
kernel = list(range(0, spread)) + list(range(spread, -1, -1))

anonymized, public, true_movies = load_files(3)

user_hash_2_dates, movie_hash_2_dates = get_date_maps(anonymized)
user2dates, movie2dates = get_date_maps(public)

# Guess the most likely victim's email hash.
victim_hash_guess = get_best_matching_item(
        target_dates=user2dates[victim_email],
        items2dates=user_hash_2_dates,
        kernel=kernel)

movie_guesses = set()

for victim_anon_entry in filter_ratings_by_user(anonymized, victim_hash_guess):
        movie_hash = victim_anon_entry.movie
        dates = []

        for any_anon_entry in anonymized:
                if any_anon_entry.movie == movie_hash:
                        dates.append(any_anon_entry.date)

        movie_guess = get_best_matching_item(
            target_dates=dates,
            items2dates=movie2dates,
            kernel=kernel)

        del movie2dates[movie_guess]

        movie_guesses.add(movie_guess)

assert movie_guesses == true_movies

print(movie_guesses)