import httpx
import json


tournament_api = 'https://dtmwra1jsgyb0.cloudfront.net/tournaments/'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    }


def save_tournament_teams(tournament_id):
    url = f'{tournament_api}{tournament_id}/teams'
    response = httpx.request(url=url, method='GET', headers=headers)
    data = response.json()
    save_on_json_file('teams', data)


def save_tournament_free_agents(tournament_id):
    url = f'{tournament_api}{tournament_id}/free-agents'
    response = httpx.request(url=url, method='GET', headers=headers)
    data = response.json()
    save_on_json_file('free-agents', data)


def get_tournament_free_agents(tournament_id):
    url = f'{tournament_api}{tournament_id}/free-agents'
    response = httpx.request(url=url, method='GET', headers=headers)
    data = response.json()
    return data


def get_tournament_teams(tournament_id):
    url = f'{tournament_api}{tournament_id}/teams'
    response = httpx.request(url=url, method='GET', headers=headers)
    data = response.json()
    return data


def load_tournament_teams():
    with open('./Docs/DocsBattlefy/teams.json', 'r') as f:
        data = json.load(f)
    return data


def load_tournament_free_agents():
    with open('./Docs/DocsBattlefy/free-agents.json', 'r') as f:
        data = json.load(f)
    return data


def save_on_json_file(file, data):
    with open(f'./Docs/DocsBattlefy/{file}.json', 'w') as f:
        json.dump(data, f)
