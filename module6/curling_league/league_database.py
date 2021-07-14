import pickle
import csv
from module6.curling_league.league import League
from module6.curling_league.team import Team
from module6.curling_league.team_member import TeamMember
import os.path


class LeagueDatabase():
    """SINGLETON"""
    _sole_instance = None

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        """Loads LeagueDatabase from specified file, stores in _sole_instance"""
        # Attempting to Load
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
        except FileExistsError:
            print("File does not exist")
        except:
            # Attempting to load from backup
            try:
                with open(file_name+".backup", mode="rb") as f:
                    cls._sole_instance = pickle.load(f)
            except FileExistsError:
                print("Backup file does not exist")
            except:
                print("Failed to Load")

    def __init__(self):
        self._last_oid = 0
        self.leagues = []

    @property
    def last_oid(self):
        return self._last_oid

    def add_league(self, league):
        """add specified league to leagues list"""
        self.leagues.append(league)

    def remove_league(self, league):
        """removes specified league from leagues list"""
        if league in self.leagues:
            self.leagues.remove(league)

    def next_oid(self):
        """increment last_id and return value"""
        self._last_oid = self._last_oid + 1
        return self._last_oid

    def save(self, file_name):
        """save DB on specified file"""
        # If File exists, create backup
        if os.path.exists(file_name):
            file_name = file_name + ".backup"
        # Save File
        with open(file_name, mode="wb") as f:
            pickle.dump(self._sole_instance, f)

    def import_league(self, league_name, file_name):
        """load league from a CSV"""
        league = League(self.instance().next_oid(), league_name)
        team_name = ""
        try:
            with open(file_name, 'r', encoding="utf-8", newline="\n") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if team_name != row["Team name"]:
                        if team_name != "":
                            league.add_team(team)
                        team_name = row["Team name"]
                        team = Team(self.instance().next_oid(), row["Team name"])
                    member = TeamMember(self.instance().next_oid(), row["Member name"], row["Member email"])
                    team.add_member(member)
            league.add_team(team)
            self.instance().add_league(league)
        except:
            print("There was a problem importing the league")

    def export_league(self, league, file_name):
        """write league to CSV"""
        if league not in self.leagues:
            print("There was a problem exporting the league")
        else:
            try:
                with open(file_name, 'w', encoding="utf-8", newline="\n") as csvfile:
                    fieldnames = ['Team name', 'Member name', 'Member email']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for team in league.teams:
                        for member in team.members:
                            writer.writerow({'Team name': team.name, 'Member name': member.name, 'Member email': member.email})
            except:
                print("There was a problem exporting the league")