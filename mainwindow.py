from PyQt5.QtWidgets import *
from PyQt5 import uic

from popup_wnd import AddEditWnd
from download import Download
import ui_mainwindow


# noinspection PyArgumentList
class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.initUi()

    def initUi(self):
        self.btn_event()
        self.progressbar.setValue(0)

    def btn_event(self):
        self.btn_addLink.clicked.connect(self.btn_addLink_clicked)
        self.btn_editLink.clicked.connect(self.btn_editLink_clicked)
        self.btn_deleteLink.clicked.connect(self.btn_deleteLink_clicked)
        self.btn_start.clicked.connect(self.btn_start_clicked)

    def btn_addLink_clicked(self):
        popup = AddEditWnd(editmode=False)
        popup.exec_()

        if popup.returnvalue is not False:
            popup_return = popup.returnvalue
            self.add_linkobj(popup_return)

    def btn_editLink_clicked(self):
        self.selected = self.tw_monitor.currentRow()

        if self.selected is not -1:
            self.selected_rowdata = [self.tw_monitor.item(self.selected, data) for data in range(0, 6)]
            self.args = {'link': self.selected_rowdata[0].text(),
                         'format': self.selected_rowdata[1].text(),
                         'path': self.selected_rowdata[2].text(),

                         'filename': self.selected_rowdata[3].text(),

                         'is_thumbnail': self.selected_rowdata[4].text(),
                         'is_subtitle': self.selected_rowdata[5].text()
                         }

            popup = AddEditWnd(editmode=True, args=self.args)
            popup.exec_()

            if popup.returnvalue is not False:
                popup_return = popup.returnvalue
                self.set_linkobj(self.selected, popup_return)

    def btn_deleteLink_clicked(self):
        self.delete_range = self.tw_monitor.selectedRanges()

        self.to_delete = set()
        for select in self.delete_range:
            if select.bottomRow() > select.topRow():
                self.to_delete.update(range(select.topRow(), select.bottomRow() + 1))
            else:
                self.to_delete.update(range(select.bottomRow(), select.topRow() + 1))

        self.to_delete = list(self.to_delete)
        self.to_delete.reverse()

        if self.to_delete is not []:
            reply = QMessageBox.question(
                self,
                'Delete links',
                f'Are you sure you want to delete {len(self.to_delete)} ' +
                f'link{"s" if len(self.to_delete) == 1 else ""}?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)

            if reply == QMessageBox.Yes:
                for select in self.to_delete:
                    print(select)
                    self.tw_monitor.removeRow(select)

    def btn_start_clicked(self):
        # TODO: popup start processing
        self.progressbar.setValue(0)
        self.data = []
        for row in range(0, self.tw_monitor.rowCount()):
            self.coloum_data = []
            if self.tw_monitor.item(row, 6).text() == "False":
                self.coloum_data.append(row)
                for column in range(0, self.tw_monitor.columnCount() - 1):
                    self.coloum_data.append(self.tw_monitor.item(row, column).text())
                self.data.append(self.coloum_data)

        print(self.data)

        if self.data == []:
            pass
        else:
            self.progress = 0
            for row in self.data:

                dl = Download()

                dl.link = row[1]
                if row[2] == "mp3":
                    dl.format = "bestaudio/best"
                elif row[2] == "mp4":
                    dl.format = "best/best"
                dl.output_path = row[3]
                if row[4] == "":
                    dl.is_custom_name = False
                    dl.custom_name = ""
                else:
                    dl.is_custom_name = True
                    dl.custom_name = row[4]
                dl.thumbnail = row[5]
                dl.subtitle = row[6]

                dl.download()

                self.tw_monitor.takeItem(row[0], 6)
                self.tw_monitor.setItem(row[0], 6, QTableWidgetItem("True"))

                print(int(100 * (self.progress / len(self.data))))
                self.progressbar.setValue(int(100 * (self.progress / len(self.data))))
                self.progress += 1

            self.progressbar.setValue(100)

    def add_linkobj(self, popup_return):
        rowPosition = self.tw_monitor.rowCount()
        self.tw_monitor.insertRow(rowPosition)
        self.set_linkobj(rowPosition, popup_return)

    def set_linkobj(self, rowPosition, value):
        self.tw_monitor.setItem(rowPosition, 0, QTableWidgetItem(value['link']))
        self.tw_monitor.setItem(rowPosition, 1, QTableWidgetItem(value['format']))
        self.tw_monitor.setItem(rowPosition, 2, QTableWidgetItem(value['path']))

        if value['is_customname']:
            self.tw_monitor.setItem(rowPosition, 3, QTableWidgetItem(value['filename']))
        else:
            self.tw_monitor.setItem(rowPosition, 3, QTableWidgetItem(''))

        self.tw_monitor.setItem(rowPosition, 4, QTableWidgetItem(str(value['is_thumbnail'])))
        self.tw_monitor.setItem(rowPosition, 5, QTableWidgetItem(str(value['is_subtitle'])))

        self.tw_monitor.setItem(rowPosition, 6, QTableWidgetItem("False"))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
