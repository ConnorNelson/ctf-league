import collections
import datetime

import requests


def ctftime_get(endpoint, params=None):
    return requests.get(
        "https://ctftime.org/api/v1" + endpoint,
        params=params,
        headers={"User-Agent": "definitely-not-requests"},
    ).json()


def ctftime_year_events(year):
    return ctftime_get(
        "/events/",
        params={
            "limit": 1024,
            "start": int(datetime.datetime(year, 1, 1).timestamp()),
            "finish": int(datetime.datetime(year + 1, 1, 1).timestamp()),
        },
    )


def ctftime_year_results(year):
    return ctftime_get(f"/results/{year}/")


def ctftime_team(team_id):
    return ctftime_get(f"/teams/{team_id}/")


def linear_leaderboard(year, num_events, num_teams):
    events = ctftime_year_events(year)
    results = ctftime_year_results(year)

    team_scores = collections.defaultdict(int)

    def cmp_event(event):
        return str(event["id"]) not in results, -event["weight"]

    print("=== Events ===")
    top_events = sorted(events, key=cmp_event)[:num_events]
    for event in top_events:
        print(event["title"])
        top_teams = results[str(event["id"])]["scores"][:num_teams]
        for i, team in enumerate(top_teams):
            assert team["place"] == i + 1
            team_id = team["team_id"]
            value = num_events - i
            tie_breaker_value = pow(num_events + 1, -(i + 1))
            team_scores[team_id] += value + tie_breaker_value

    print()

    print("=== Rankings ===")
    print("Place", "\t", "Score", "\t", "Name")
    rankings = sorted(team_scores.items(), key=lambda k: -k[1])
    for i, (team_id, score) in enumerate(rankings):
        rank = i + 1
        name = ctftime_team(team_id)["name"]
        print(rank, "\t", int(score), "\t", name)


if __name__ == "__main__":
    linear_leaderboard(2020, 10, 10)
