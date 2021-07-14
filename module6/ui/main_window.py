import os
import sys
import copy

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox

from module6.curling_league.league_database import LeagueDatabase
from module6.curling_league.league import League
from module6.ui.league_editor_window import LeagueEditorWindow

ui_path = os.path.dirname(os.path.abspath(__file__))
Ui_MainWindow, QtBaseWindow = uic.loadUiType(os.path.join(ui_path, "main_window.ui"))


class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonDeleteLeague.clicked.connect(self.buttonDeleteLeague_clicked)
        self.buttonAddLeague.clicked.connect(self.buttonAddLeague_clicked)
        self.buttonEditLeague.clicked.connect(self.buttonEditLeague_clicked)
        self.actionLoad.triggered.connect(self.actionLoad_triggered)
        self.actionSave.triggered.connect(self.actionSave_triggered)
        self.actionQuit.triggered.connect(self.actionQuit_triggered)
        self.leagues = []
        self._db = LeagueDatabase()

    def update_ui(self):
        """updates list ui"""
        self.listLeague.clear()
        for league in self.leagues:
            self.listLeague.addItem(str(league))

    def warn(self, title, message):
        """warning message"""
        mb = QMessageBox(QMessageBox.Icon.Warning, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def get_current_selected_league(self):
        """unpack selection for use"""
        if len(self.listLeague.selectedItems()) > 0:
            selection_text = self.listLeague.currentItem().text()
            league_name, rest = selection_text.split(':')
            for league in self.leagues:
                if league.name == league_name:
                    return league

    def buttonDeleteLeague_clicked(self):
        """Delete league from list and database"""
        league_to_remove = self.get_current_selected_league()
        if league_to_remove:
            self.leagues.remove(league_to_remove)
            self.update_ui()
        else:
            self.warn("No League Selected", "You must select a league before removing it.")

    def buttonAddLeague_clicked(self):
        """Add league directly from window input"""
        league_name = self.lineLeagueName.text()
        if league_name != "":
            new_league = League(self._db.instance().next_oid(), league_name)
            self.leagues.append(new_league)
            self.update_ui()
            self.lineLeagueName.clear()
        else:
            self.warn("No Name Entered", "You must enter a league name before adding it.")

    def buttonEditLeague_clicked(self):
        """Edit the league by opening league editor window"""
        league_to_edit = copy.deepcopy(self.get_current_selected_league())
        current_index = self.listLeague.currentRow()
        if league_to_edit:
            edit_league_window = LeagueEditorWindow(self._db, league_to_edit)
            # updates ui prior to opening
            edit_league_window.update_ui()
            if edit_league_window.exec_() == QDialog.DialogCode.Accepted:
                # Remove instance of league, add league back with team info, update ui
                self.leagues.remove(league_to_edit)
                self.leagues.insert(current_index, edit_league_window.league)
                self.update_ui()
                #print("League Editor Saved")
            else:
                #print("League Editor Cancelled")
                self.update_ui()
        else:
            self.warn("No League Selected", "You must select a league before editing it.")



    def actionLoad_triggered(self):
        """Load previously saved database"""
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(["All files (*.*)", "DAT (*.dat)"])
        dialog.selectNameFilter("DAT (*.dat)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._db.instance().leagues = [] # CLEAR DB BEFORE LOAD
            self.leagues = []
            filepath = dialog.selectedFiles()[0]
            self._db.instance().load(filepath)
            # load league from DB into list
            for league in self._db.instance().leagues:
                self.leagues.append(league)
            self.update_ui()
        else:
            self.warn("File Load Cancelled", "Unable to load the specified file.")

    def actionSave_triggered(self):
        """Save database for later use"""
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["All files (*.*)", "DAT (*.dat)"])
        dialog.selectNameFilter("DAT (*.dat)")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self._db.instance().leagues = []  # CLEAR DB BEFORE SAVE
            filepath = dialog.selectedFiles()[0]
            # send league from list to DB
            for league in self.leagues:
                self._db.instance().add_league(league)
            self._db.instance().save(filepath)
            self.update_ui()
        else:
            self.warn("File Save Cancelled", "Unable to save the specified file.")

    def actionQuit_triggered(self):
        """QUIT"""
        sys.exit(QtWidgets.QApplication(sys.argv).exec_())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()