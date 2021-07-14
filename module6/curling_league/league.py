from module6.curling_league.identified_object import IdentifiedObject
from module6.curling_league.league_exceptions import DuplicateOid


class League(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        """SPEC: add team to teams"""
        if team.oid in [t.oid for t in self._teams]:
            raise DuplicateOid(team.oid)
        else:
            self._teams.append(team)

    def remove_team(self, team):
        """SPEC: remove team from teams"""
        if team in self._teams:
            self._teams.remove(team)

    def add_competition(self, competition):
        """SPEC: add competition to competitions"""
        if competition.oid in [c.oid for c in self._competitions]:
            raise DuplicateOid(competition.oid)
        else:
            self._competitions.append(competition)

    def teams_for_member(self, member):
        """SPEC: return a list of all teams for which member plays"""
        return [team for team in self._teams if member in team.members]

    def competitions_for_team(self, team):
        """SPEC: return a list of all competitions in which team is participating"""
        return [competition for competition in self.competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        """SPEC: return a list of all competitions for which member played on one of the competing teams"""
        return [competition for competition in self.competitions\
                for team in competition.teams_competing if member in team.members]

    def __str__(self):
        return f"{self.name}: {len(self._teams)} teams, {len(self._competitions)} competitions"
