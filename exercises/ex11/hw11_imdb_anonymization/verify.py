import os
import csv
import random
import traceback
import warnings

import numpy as np

from scipy import stats
from termcolor import colored

import dp # the script must be in the same directory as the verifier!

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(CURRENT_DIR, "imdb-dp.csv")
movie_name = "Pulp Fiction"
rating_threshold = 4
epsilon = 10


def test_basic_budget_accounting():
    querier = dp.DpQuerySession(db_path, privacy_budget=10 * epsilon)
    assert (
        querier.remaining_budget == 10 * epsilon
    ), "Remaining budget is computed incorrectly"
    querier.get_count(movie_name, rating_threshold, epsilon)
    assert (
        querier.remaining_budget == 9 * epsilon
    ), "Remaining budget is computed incorrectly"


def test_budget_depleted():
    querier = dp.DpQuerySession(db_path, privacy_budget=2 * epsilon)
    querier.get_count(movie_name, 1, epsilon)
    querier.get_count(movie_name, 2, epsilon)

    # Budget is fully spent by now. The next query should raise BudgetDepletedError.
    raised = False
    try:
        querier.get_count(movie_name, 3, epsilon)
    except Exception as e:
        raised = True
        assert isinstance(
            e, dp.BudgetDepletedError
        ), f"Expected BudgetDepletedError exception, got {type(e)}"

    assert raised, "Does not raise an error when privacy budget is depleted."


def test_noise_distribution():
    num_trials = 300
    values = np.zeros(num_trials)
    for i in range(num_trials):
        querier = dp.DpQuerySession(db_path, privacy_budget=10 * epsilon)
        noisy_count = querier.get_count(movie_name, rating_threshold, epsilon=epsilon)
        values[i] = noisy_count

    noise = values - _get_real_count(db_path, movie_name, rating_threshold)

    # Check that the noise follows Laplace distribution with scale 1/epsilon
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _, p_value = stats.kstest(noise, "laplace", (0, 1. / epsilon))
    p_value_thresh = 0.005
    assert (
        not np.isnan(p_value) and p_value > p_value_thresh
    ), "The added noise does not seem to result in the required level of privacy."


def test_multiple_queries_1():
    num_trials = 30
    querier = dp.DpQuerySession(db_path, privacy_budget=2 * epsilon)
    values = np.zeros(num_trials)
    for i in range(num_trials):
        noisy_count = querier.get_count(movie_name, rating_threshold, epsilon=epsilon)
        values[i] = noisy_count

    # Responses to identical queries should have the same noise. Otherwise, the attacker can
    # retrieve the real value from multiple repetitions of the same query.
    assert np.all(values == values[0]), (
        "The attacker might be able to retrieve the exact value of a given query because the "
        "noise is freshly drawn for every response."
    )

    assert querier.remaining_budget == epsilon, (
        "Remaining budget is incorrectly computed when " "queries are repeated."
    )


def test_multiple_queries_2():
    querier = dp.DpQuerySession(db_path, privacy_budget=5 * epsilon)
    values = np.zeros(5)
    for i, stars in enumerate(range(1, 6)):
        noisy_count = querier.get_count(
            movie_name, rating_threshold=stars, epsilon=epsilon
        )
        values[i] = noisy_count

    # Same noise should be returned for the identical queries, which are defined by the values of
    # both movie_name and rating_threshold.
    assert np.all(
        values[1:] != values[0]
    ), "Got the exact same response to different queries."


def _load_db(db_path):
    entries = []
    with open(db_path) as f:
        reader = csv.reader(f, quotechar='"', delimiter=",")
        for email, movie, date, stars in reader:
            entries.append(
                dp.Rating(user=email, movie=movie, date=date, stars=int(stars))
            )
    return entries


def _get_real_count(db_path, movie_name, rating_threshold):
    entries = _load_db(db_path)
    count = 0
    for entry in entries:
        if entry.movie == movie_name and entry.stars >= rating_threshold:
            count += 1
    return count


def _run_tests(tests):
    print("Running tests...")
    print()
    for test_name, test_func in tests:
        print(f"> {test_name}")
        try:
            test_func()
            print(colored("PASSED 👌 ", "green"))
        except AssertionError as e:
            print(colored("FAIL 💔 :", "red"), e)
        except Exception as e:
            exception_data = traceback.format_exc().splitlines()
            relevant_lines = "\n".join([exception_data[-1]] + exception_data[-3:-1])
            print(colored("ERROR 💥 :", "yellow"), relevant_lines)
        print()


def main():
    _run_tests(
        [
            ("Basic privacy budget accounting", test_basic_budget_accounting),
            ("Privacy budget depletion control", test_budget_depleted),
            ("DP noise distribution", test_noise_distribution),
            ("Multiple query behavior (I)", test_multiple_queries_1),
            ("Multiple query behavior (II)", test_multiple_queries_2),
        ]
    )


if __name__ == "__main__":
    main()
