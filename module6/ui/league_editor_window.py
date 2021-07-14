import os
import sys
import copy

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog

from module6.curling_league.league import League
from module6.curling_league.league_database import LeagueDatabase
from module6.curling_league.team import Team
from module6.ui.team_editor_window import TeamEditorWindow

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "league_editor_window.ui"))


class LeagueEditorWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, database, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonDeleteTeam.clicked.connect(self.buttonDeleteTeam_clicked)
        self.buttonAddTeam.clicked.connect(self.buttonAddTeam_clicked)
        self.buttonEditTeam.clicked.connect(self.buttonEditTeam_clicked)
        self.buttonImportLeague.clicked.connect(self.buttonImportLeague_clicked)
        self.buttonExportLeague.clicked.connect(self.buttonExportLeague_clicked)
        self.league = league
        self._db = database

    def update_ui(self):
        """updates list items and line edits"""
        self.listTeam.clear()
        self.lineTeamName.clear()
        for team in self.league.teams:
            self.listTeam.addItem(str(team))

    def get_current_selected_team(self):
        """unpack selection for use"""
        if len(self.listTeam.selectedItems()) > 0:
            selection_text = self.listTeam.currentItem().text()
            team_name, rest = selection_text.split(':')
            for team in self.league.teams:
                if team.name == team_name:
                    return team

    def warn(self, title, message):
        """warning message"""
        mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def buttonDeleteTeam_clicked(self):
        """Delete the selected team"""
        team_to_remove = self.get_current_selected_team()
        if team_to_remove:
            self.league.remove_team(team_to_remove)
            self.update_ui()
        else:
            self.warn("No Member Selected", "You must select a member before removing it.")

    def buttonAddTeam_clicked(self):
        """add team to list"""
        team_name = self.lineTeamName.text()
        if team_name != "":
            new_team = Team(self._db.instance().next_oid(), team_name)
            self.league.add_team(new_team)
            self.update_ui()
        else:
            self.warn("No Name or Email Entered", "You must enter a member name and email before adding it.")

    def buttonEditTeam_clicked(self):
        """Edit the team by opening team editor window"""
        team_to_edit = copy.deepcopy(self.get_current_selected_team())
        current_index = self.listTeam.currentRow()
        if team_to_edit:
            edit_team_window = TeamEditorWindow(self._db, team_to_edit)
            # updates ui prior to opening
            edit_team_window.update_ui()
            if edit_team_window.exec_() == QDialog.DialogCode.Accepted:
                # Remove instance of team, add team back with member info, update ui
                self.league.teams.remove(team_to_edit)
                self.league.teams.insert(current_index, edit_team_window.team)
                self.update_ui()
                #print("Team Editor Saved")
            else:
                #print("Team Editor Cancelled")
                self.update_ui()
        else:
            self.warn("No League Selected", "You must select a league before editing it.")

    def buttonExportLeague_clicked(self):
        """EXPORTS TEAM INTO CSV FILE"""
        #print("Export Team")
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["All files (*.*)", "CSV (*.csv)"])
        dialog.selectNameFilter("CSV (*.csv)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            self._db.instance().add_league(self.league)
            self._db.instance().export_league(self.league, filepath)
            #print("Successful Export")
        else:
            self.warn("File Export Cancelled", "Unable to export the specified file.")

    def buttonImportLeague_clicked(self):
        """IMPORTS TEAM FROM CSV FILE"""
        #print("Import Team")
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(["All files (*.*)", "CSV (*.csv)"])
        dialog.selectNameFilter("CSV (*.csv)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filepath = dialog.selectedFiles()[0]
            self._db.instance().import_league(self.league.name, filepath) # league name comes from previous screen
            self.league = self._db.instance().leagues[len(self._db.instance().leagues)-1] # most recent added league
            self.update_ui()
            #print("Successful Import")
        else:
            self.warn("File Import Cancelled", "Unable to import the specified file.")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeagueEditorWindow(LeagueDatabase(), League(0, "League Example"))
    window.show()
    sys.exit(app.exec_())
