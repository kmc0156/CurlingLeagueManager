from module6.curling_league.identified_object import IdentifiedObject
from module6.curling_league.league_exceptions import DuplicateOid
from module6.curling_league.league_exceptions import DuplicateEmail


class Team(IdentifiedObject):
    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        """SPEC: add member to members"""
        if member.oid in [mem.oid for mem in self._members]:
            raise DuplicateOid(member.oid)
        elif member.email in [mem.email for mem in self._members]:
            raise DuplicateEmail(member.email)
        else:
            self._members.append(member)

    def remove_member(self, member):
        """SPEC: remove member from members"""
        if member in self._members:
            self._members.remove(member)

    def send_email(self, emailer, subject, message):
        """SPEC: send email to all members of a team except those whose email address is None"""
        recipients = []
        for member in self.members:
            if member.email is not None:
                recipients.append(member.email)
        return emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        return f"{self.name}: {len(self._members)} members"
