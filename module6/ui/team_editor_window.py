import os
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from module6.curling_league.league_database import LeagueDatabase
from module6.curling_league.team import Team
from module6.curling_league.team_member import TeamMember

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "team_editor_window.ui"))


class TeamEditorWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, database, team, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonDeleteMember.clicked.connect(self.buttonDeleteMember_clicked)
        self.buttonAddMember.clicked.connect(self.buttonAddMember_clicked)
        self.buttonUpdateMember.clicked.connect(self.buttonUpdateMember_clicked)
        self.listMember.itemClicked.connect(self.itemClicked)
        self.team = team
        self._db = database

    def update_ui(self):
        """updates list items and line edits"""
        self.listMember.clear()
        self.lineMemberName.clear()
        self.lineEmail.clear()
        for member in self.team.members:
            self.listMember.addItem(str(member))

    def get_current_selected_member(self):
        """unpack selection for use"""
        if len(self.listMember.selectedItems()) > 0:
            selection_text = self.listMember.currentItem().text()
            name, email = selection_text.split('<')
            for member in self.team.members:
                if member.name == name and member.email == email[:-1]:
                    return member

    def itemClicked(self):
        """updates line edit fields when list items are clicked"""
        member_selected = self.get_current_selected_member()
        self.lineMemberName.setText(member_selected.name)
        self.lineEmail.setText(member_selected.email)

    def warn(self, title, message):
        """warning message"""
        mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def buttonDeleteMember_clicked(self):
        """Delete the selected member"""
        member_to_remove = self.get_current_selected_member()
        if member_to_remove:
            self.team.remove_member(member_to_remove)
            self.update_ui()
        else:
            self.warn("No Member Selected", "You must select a member before removing it.")

    def buttonAddMember_clicked(self):
        """add member to list"""
        member_name = self.lineMemberName.text()
        member_email = self.lineEmail.text()
        if member_name != "":
            new_member = TeamMember(self._db.instance().next_oid(), member_name, member_email)
            self.team.add_member(new_member)
            self.update_ui()
        else:
            self.warn("No Name or Email Entered", "You must enter a member name and email before adding it.")

    def buttonUpdateMember_clicked(self):
        """updates current selected member"""
        member_to_update = self.get_current_selected_member()
        member_to_update.name = self.lineMemberName.text()
        member_to_update.email = self.lineEmail.text()
        self.update_ui()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamEditorWindow(LeagueDatabase(), Team(0, "Team Example"))
    window.show()
    sys.exit(app.exec_())
