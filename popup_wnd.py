from PyQt5.QtWidgets import *
from PyQt5 import uic


from exceptions import *


addform = uic.loadUiType("addwindow.ui")[0]


# noinspection PyArgumentList
class AddEditWnd(QDialog, addform):
    def __init__(self, editmode, args=None):
        super().__init__()
        self.setupUi(self)

        self.initUi()
        self.returnvalue = False

        if editmode:
            self.le_link.setText(args['link'])
            self.cb_format.setCurrentText(args['format'])
            self.le_path.setText(args['path'])

            if args['filename'] is "":
                self.cb_custom_file_name.setChecked(False)
                self.le_filename.setText("")
            else:
                self.cb_custom_file_name.setChecked(True)
                self.le_filename.setText(args['filename'])

            if args['is_thumbnail'] == "False":
                self.cb_thumbnail.setChecked(False)
            else:
                self.cb_thumbnail.setChecked(True)

            if args['is_subtitle'] == "False":
                self.cb_subtitle.setChecked(False)
            else:
                self.cb_subtitle.setChecked(True)

    def initUi(self):
        self.btn_event()

        self.cb_custom_file_name.stateChanged.connect(self.cb_custom_file_name_changed)

    def btn_event(self):
        self.btn_pathfinder.clicked.connect(self.btn_pathfinder_clicked)

        self.btn_exit.accepted.connect(self.btn_exit_accepted)
        self.btn_exit.rejected.connect(self.btn_exit_rejected)

    def btn_pathfinder_clicked(self):
        # noinspection PyCallByClass
        self.le_path.setText(str(
            QFileDialog.getExistingDirectory(
                self, "Select Directory")
        ))

    def btn_exit_accepted(self):
        try:
            self.checkvalid()
        except BlankLinkException:
            # TODO: raise Exception
            print("Invalid link exception")
        except BlankFilenameException:
            # TODO: raise Exception
            print("Invalid filename exception")

        else:
            self.returnvalue = {'link': self.le_link.text(),
                                'format': self.cb_format.currentText(),
                                'path': self.le_path.text(),

                                'is_customname': self.cb_custom_file_name.isChecked(),
                                'filename': self.le_filename.text(),

                                'is_thumbnail': self.cb_thumbnail.isChecked(),
                                'is_subtitle': self.cb_subtitle.isChecked()
                                }

            self.close()

    def btn_exit_rejected(self):
        self.returnvalue = False

        self.close()

    def cb_custom_file_name_changed(self):
        if self.cb_custom_file_name.isChecked():
            self.le_filename.setEnabled(True)
        else:
            self.le_filename.setEnabled(False)

    def closeEvent(self, event):
        if self.returnvalue is not False:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.returnvalue = False
                event.accept()
            else:
                event.ignore()

    def checkvalid(self):
        if self.le_link.text() == "":
            raise BlankLinkException

        if self.cb_custom_file_name.isChecked():
            if self.le_filename.text() == "":
                raise BlankFilenameException
