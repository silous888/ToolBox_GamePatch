# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\Documents\Programmation\PublicProject\ToolBox_GamePatch\image_table_process\window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(737, 248)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_startProcess = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_startProcess.setGeometry(QtCore.QRect(260, 150, 75, 23))
        self.pushButton_startProcess.setObjectName("pushButton_startProcess")
        self.checkBox_subSubFolderChoice = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_subSubFolderChoice.setGeometry(QtCore.QRect(410, 150, 301, 21))
        self.checkBox_subSubFolderChoice.setObjectName("checkBox_subSubFolderChoice")
        self.lineEdit_sheetName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_sheetName.setGeometry(QtCore.QRect(120, 20, 351, 20))
        self.lineEdit_sheetName.setObjectName("lineEdit_sheetName")
        self.label_sheetNameQuery = QtWidgets.QLabel(self.centralwidget)
        self.label_sheetNameQuery.setGeometry(QtCore.QRect(20, 20, 151, 21))
        self.label_sheetNameQuery.setObjectName("label_sheetNameQuery")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(17, 80, 501, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_progressInfo = QtWidgets.QLabel(self.centralwidget)
        self.label_progressInfo.setGeometry(QtCore.QRect(20, 110, 461, 16))
        self.label_progressInfo.setObjectName("label_progressInfo")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_startProcess.setText(_translate("MainWindow", "Start"))
        self.checkBox_subSubFolderChoice.setText(_translate("MainWindow", "Only one image in sheet for subsubfolder"))
        self.label_sheetNameQuery.setText(_translate("MainWindow", "Name of the sheet:"))
        self.label_progressInfo.setText(_translate("MainWindow", "Processing this thing..."))