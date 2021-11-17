from ApiBattlefy.battlefyacess import BattlefyAcess


class BattlefyAPI:
    def __init__(self):
        self._api = BattlefyAcess()

    def save_tournament_participants(self, tournament_id: str):
        self._api.save_tournament_free_agents(tournament_id)
        self._api.save_tournament_teams(tournament_id)

    def get_free_agents_discord(self, tournament_id: str):
        saved_free_agents = self._api.load_tournament_free_agents()
        teams_on_bracket = self._api.get_tournament_teams(tournament_id)
        free_agents_on_team = self.get_free_agents_on_team(teams_on_bracket)
        free_agents_discord = self.filter_free_agents_discord(free_agents_on_team, saved_free_agents)
        return free_agents_discord

    @staticmethod
    def get_free_agents_on_team(teams_on_bracket: list):
        f_a_list = []
        for team in teams_on_bracket:
            for player in team['players']:
                if player['isFreeAgent'] and ('userID' in player.keys()):
                    f_a_list.append((player['userID'], team['name']))
        return f_a_list

    @staticmethod
    def filter_free_agents_discord(free_agents: tuple, saved_free_agents: list):
        agent_list = []
        for agent_id, agent_team in free_agents:
            for free_agent in saved_free_agents:
                if 'userID' in free_agent.keys():
                    if agent_id == free_agent['userID']:
                        agent_discord = free_agent['customFields'][0]['value']
                        agent_list.append((agent_discord, agent_team))
        return agent_list





# BattlefyAPI().save_tournament_teams('613414bc1bd6b9115464b3c6')
# BattlefyAPI().on_registrations_close('602c6ef8384ba37dec876ace')
# print(BattlefyAPI().on_brackets_release('602c6ef8384ba37dec876ace'))
# 5e581939424f96204e365c38


