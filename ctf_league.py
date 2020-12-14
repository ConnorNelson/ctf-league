import collections

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


def linear_leaderboard(year, num_events):
    events = ctftime_year_events(year)
    results = ctftime_year_results(year)

    team_scores = collections.defaultdict(int)

    print("=== Events ===")
    count = 0
    for event in sorted(events_2020, key=lambda k: -k["weight"]):
        event_id = str(event["id"])
        if event_id in results:
            count += 1
            print(event["title"])
            value = num_events
            for i, team in enumerate(results_data[event_id]["scores"][:10]):
                assert team["place"] == i + 1
                team_id = team["team_id"]
                team_scores[team_id] += value
                value -= 1

        if count >= num_events:
            break

    print()

    print("=== Rankings ===")
    print("Place", "\t", "Score", "\t", "Name")
    rankings = sorted(team_scores.items(), key=lambda k: -k[1])
    for i, (team_id, score) in enumerate(rankings):
        rank = i + 1
        name = ctftime_team(team_id)["name"]
        print(rank, "\t", score, "\t", name)


if __name__ == "__main__":
    linear_leaderboard(2020, 10)
