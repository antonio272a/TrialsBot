from ApiBattlefy.battlefyacess import *


def save_tournament_participants(tournament_id: str):
    save_tournament_free_agents(tournament_id)
    save_tournament_teams(tournament_id)


def get_free_agents_discord(tournament_id: str):
    saved_free_agents = load_tournament_free_agents()
    teams_on_bracket = get_tournament_teams(tournament_id)
    free_agents_on_team = get_free_agents_on_team(teams_on_bracket)
    free_agents_discord = filter_free_agents_discord(free_agents_on_team, saved_free_agents)
    return free_agents_discord


def get_free_agents_on_team(teams_on_bracket: list):
    f_a_list = []
    for team in teams_on_bracket:
        for player in team['players']:
            if player['isFreeAgent'] and ('userID' in player.keys()):
                f_a_list.append((player['userID'], team['name']))
    return f_a_list


def filter_free_agents_discord(free_agents: tuple, saved_free_agents: list):
    agent_list = []
    for agent_id, agent_team in free_agents:
        for free_agent in saved_free_agents:
            if 'userID' in free_agent.keys():
                if agent_id == free_agent['userID']:
                    agent_discord = free_agent['customFields'][0]['value']
                    agent_list.append((agent_discord, agent_team))
    return agent_list



