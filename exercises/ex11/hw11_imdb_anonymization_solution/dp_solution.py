import csv
from dataclasses import dataclass
import numpy as np


class BudgetDepletedError(Exception):
    pass


@dataclass
class Rating:
    user: str
    movie: str
    date: str
    stars: int

    def __str__(self):
        return f'{self.user},"{self.movie}",{self.date},{self.stars}'


class DpQuerySession:
    """
    Respond to database queries with differential privacy.

    Args:
        db (str): Path to the ratings database csv-file.
        privacy_budget (float): Total differential privacy epsilon for the session.
    """

    def __init__(self, db, privacy_budget):
        self.db = db
        self.privacy_budget = privacy_budget
        self._spent_budget = 0                      # Adding a spent budget var
        self._cached_responses = {}                 # Cached responses for speed
        self.load_db()

    @property
    def remaining_budget(self):
        """
        Calculate the remaining privacy budget.

        Returns:
            float: The remaining privacy budget.
        """
        return self.privacy_budget - self._spent_budget     # Remaining budget as total - spent

    def load_db(self):
        """Load the rating database from a csv file."""
        self._entries = []
        with open(self.db) as f:
            reader = csv.reader(f, quotechar='"', delimiter=",")
            for email, movie, date, stars in reader:
                self._entries.append(
                    Rating(user=email, movie=movie, date=date, stars=int(stars))
                )

    def _get_real_count(self, movie_name, rating_threshold):
        count = 0
        for entry in self._entries:
            if entry.movie == movie_name and entry.stars >= rating_threshold:
                count += 1
        return count

    def get_count(self, movie_name, rating_threshold, epsilon):
        if (movie_name, rating_threshold) in self._cached_responses:
            return self._cached_responses[(movie_name, rating_threshold)]       # Let's not check budget for previous responses, just give them away
        if epsilon > self.remaining_budget:                                     # If the specified epsilon is too high, we raise an exception
            raise BudgetDepletedError

        count = self._get_real_count(movie_name, rating_threshold)
        noisy_count = count + np.random.laplace(loc=0, scale=1. / epsilon)      # Add laplacian noise as in the definition
        self._cached_responses[(movie_name, rating_threshold)] = noisy_count    # Add response to cache
        self._spent_budget += epsilon                                           # Update budget
        return noisy_count

