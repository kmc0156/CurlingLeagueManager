from module6.curling_league.identified_object import IdentifiedObject


class Competition(IdentifiedObject):
    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams_competing = teams # must be a list
        self.date_time = datetime
        self.location = location

    @property
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        """SPEC: send an email to all members of all teams in the competition"""
        recipients = []
        for team in self.teams_competing:
            for member in team.members:
                if member.email is not None:
                    recipients.append(member.email)
        return emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        if self.date_time is None:
            return f"Competition at {self.location} with " \
                    f"{len(self._teams_competing)} teams"
        return f"Competition at {self.location} on "\
                f"{self.date_time} with "\
                f"{len(self._teams_competing)} teams"