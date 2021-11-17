import httpx
import json


class BattlefyAcess:

    def __init__(self):
        self._tournament_api = 'https://dtmwra1jsgyb0.cloudfront.net/tournaments/'
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    def save_tournament_teams(self, tournament_id):
        url = f'{self._tournament_api}{tournament_id}/teams'
        response = httpx.request(url=url, method='GET', headers=self._headers)
        data = response.json()
        self.save_on_json_file('teams', data)

    def save_tournament_free_agents(self, tournament_id):
        url = f'{self._tournament_api}{tournament_id}/free-agents'
        response = httpx.request(url=url, method='GET', headers=self._headers)
        data = response.json()
        self.save_on_json_file('free-agents', data)

    def get_tournament_free_agents(self, tournament_id):
        url = f'{self._tournament_api}{tournament_id}/free-agents'
        response = httpx.request(url=url, method='GET', headers=self._headers)
        data = response.json()
        return data

    def get_tournament_teams(self, tournament_id):
        url = f'{self._tournament_api}{tournament_id}/teams'
        response = httpx.request(url=url, method='GET', headers=self._headers)
        data = response.json()
        return data

    @staticmethod
    def load_tournament_teams():
        with open('./Docs/DocsBattlefy/teams.json', 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def load_tournament_free_agents():
        with open('./Docs/DocsBattlefy/free-agents.json', 'r') as f:
            data = json.load(f)
        return data

    @staticmethod
    def save_on_json_file(file, data):
        with open(f'./Docs/DocsBattlefy/{file}.json', 'w') as f:
            json.dump(data, f)

# class BattlefyApi {
#
#   constructor() {
#     this.searchApi = axios.create({
#       baseURL: 'https://search.battlefy.com/',
#     });
#     this.tournamentApi = axios.create({
#       baseURL: 'https://dtmwra1jsgyb0.cloudfront.net/',
#     });
#     this.userApi = axios.create({
#       baseURL: 'https://battlefy.com/users/'
#     });
#   }
#   async getPopularGames() {
#     const response = await this.searchApi.get('game/popular');
#     return response.data;
#   }
#   async getGameTournaments(gameId) {
#     const response = await this.searchApi.get(`tournament/browse/${gameId}`);
#     return response.data.tournaments;
#   }
#   async getStaffPicks() {
#     const response = await this.searchApi.get(`spotlight?type=discovery`);
#     return response.data;
#   }
#   async getTournamentData(id) {
#     const response = await this.tournamentApi.get(`tournaments/${id}`);
#     return response.data;
#   }
#   async getTournamentStageData(stage) {
#     const response = await this.tournamentApi.get(`stages/${stage}`);
#     return response.data;
#   }
#   async getTournamentStageMatches(stage) {
#     const response = await this.tournamentApi.get(`stages/${stage}/matches`);
#     for (match in response.data) {
#       var winner = response.data[match].top.winner ? 'top' : 'bottom'
#       response.data[match].winner = winner;
#     }
#     return response.data;
#   }
#   async getTournamentTeams(id) {
#     const response = await this.tournamentApi.get(`tournaments/${id}/teams`);
#     return response.data;
#   }
#
#   async getTournamentFreeAgents(id) {
#     const response = await this.tournamentApi.get(`tournaments/${id}/free-agents`);
#     return response.data
#   }
# }
