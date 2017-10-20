from PyQt5 import QtWidgets, QtCore, QtGui
from FilmEditorUi import Ui_FilmDialog
import datetime

class FilmDialog(QtWidgets.QDialog,Ui_FilmDialog):
    def __init__(self, date, parent=None):
        super(FilmDialog, self).__init__(parent)
        self.setupUi(self)
        self.date = date
        self.setWindowTitle("Date: %d/%d/%d" % (self.date.day, self.date.month, self.date.year))

        self.newFilm.clicked.connect(self.new_film)
        self.deleteFilm.clicked.connect(self.delete_film)
        self.filmList.currentChanged.connect(self.current_changed)

        self.film_model = None

    def new_film(self):
        if self.film_model is not None:
            self.film_model.appendRow(Film(date=selected_date, title='<Title>').standard_item())

    def delete_film(self):
        if self.film_model is not None:
            index = self.filmList.currentIndex()
            self.film_model.removeRow(index.row())

    def current_changed(self):
        index = self.film_model.currentIndex()
        self.film_model

    def set_films_model(self, model):
        self.film_model = model
        self.filmList.setModel(model)

class Film:
    def __init__(self, date=None, title=None):
        self.title = title
        self.date = date
        self.dirty = False

    def standard_item(self):
        item = QtGui.QStandardItem(self.title)
        item.setData(self, role=QtCore.Qt.UserRole)
        return item

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    selected_date = datetime.date(day=20, month=8, year=2017)
    films_model = QtGui.QStandardItemModel()

    films_model.appendRow(Film(date=selected_date, title='Jaws').standard_item())

    a = FilmDialog(selected_date)
    a.set_films_model(films_model)
    a.show()
    sys.exit(app.exec_())