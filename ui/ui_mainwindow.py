# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.0.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1059, 656)
        self.actionOpen_File = QAction(MainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionExport_SD = QAction(MainWindow)
        self.actionExport_SD.setObjectName(u"actionExport_SD")
        self.actionExport_Cybercard = QAction(MainWindow)
        self.actionExport_Cybercard.setObjectName(u"actionExport_Cybercard")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.productTab = QWidget()
        self.productTab.setObjectName(u"productTab")
        self.horizontalLayout_2 = QHBoxLayout(self.productTab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.productTreeView = QTreeView(self.productTab)
        self.productTreeView.setObjectName(u"productTreeView")

        self.horizontalLayout_2.addWidget(self.productTreeView)

        self.tabWidget.addTab(self.productTab, "")
        self.taxTab = QWidget()
        self.taxTab.setObjectName(u"taxTab")
        self.horizontalLayout_3 = QHBoxLayout(self.taxTab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.taxTableView = QTableView(self.taxTab)
        self.taxTableView.setObjectName(u"taxTableView")
        self.taxTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.taxTableView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.taxTableView.setAlternatingRowColors(True)
        self.taxTableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.taxTableView.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout_3.addWidget(self.taxTableView)

        self.tabWidget.addTab(self.taxTab, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1059, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_SD)
        self.menuFile.addAction(self.actionExport_Cybercard)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MIDCOM 8000 Tax Editor - Standard Format (20,20,100)", None))
        self.actionOpen_File.setText(QCoreApplication.translate("MainWindow", u"Open File... (.dat, .str)", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.actionExport_SD.setText(QCoreApplication.translate("MainWindow", u"Export SD Card Format (*.str) ...", None))
        self.actionExport_Cybercard.setText(QCoreApplication.translate("MainWindow", u"Export Cybercard Format (*.dat) ...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.productTab), QCoreApplication.translate("MainWindow", u"Products (100)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.taxTab), QCoreApplication.translate("MainWindow", u"Taxes && Labels (20,20)", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

