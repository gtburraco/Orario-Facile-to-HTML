# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QAbstractItemView, QHBoxLayout, QLabel, QMenuBar, QPushButton,
                               QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
                               QTableView, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.load_btn = QPushButton(self.centralwidget)
        self.load_btn.setObjectName(u"load_btn")

        self.horizontalLayout.addWidget(self.load_btn)

        self.salva_html_btn = QPushButton(self.centralwidget)
        self.salva_html_btn.setObjectName(u"salva_html_btn")
        self.salva_html_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.salva_html_btn)

        self.salva_xlsx_btn = QPushButton(self.centralwidget)
        self.salva_xlsx_btn.setObjectName(u"salva_xlsx_btn")
        self.salva_xlsx_btn.setEnabled(False)

        self.horizontalLayout.addWidget(self.salva_xlsx_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_lezioni = QWidget()
        self.tab_lezioni.setObjectName(u"tab_lezioni")
        self.verticalLayout_2 = QVBoxLayout(self.tab_lezioni)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.table_view_lezioni = QTableView(self.tab_lezioni)
        self.table_view_lezioni.setObjectName(u"table_view_lezioni")
        self.table_view_lezioni.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view_lezioni.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view_lezioni.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view_lezioni.setSortingEnabled(True)

        self.verticalLayout_2.addWidget(self.table_view_lezioni)

        self.tabWidget.addTab(self.tab_lezioni, "")
        self.tab_docenti = QWidget()
        self.tab_docenti.setObjectName(u"tab_docenti")
        self.verticalLayout_4 = QVBoxLayout(self.tab_docenti)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.table_view_docenti = QTableView(self.tab_docenti)
        self.table_view_docenti.setObjectName(u"table_view_docenti")
        self.table_view_docenti.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view_docenti.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view_docenti.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view_docenti.setSortingEnabled(True)

        self.verticalLayout_4.addWidget(self.table_view_docenti)

        self.label_docenti = QLabel(self.tab_docenti)
        self.label_docenti.setObjectName(u"label_docenti")

        self.verticalLayout_4.addWidget(self.label_docenti)

        self.tabWidget.addTab(self.tab_docenti, "")
        self.tab_classi = QWidget()
        self.tab_classi.setObjectName(u"tab_classi")
        self.verticalLayout_5 = QVBoxLayout(self.tab_classi)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.table_view_classi = QTableView(self.tab_classi)
        self.table_view_classi.setObjectName(u"table_view_classi")
        self.table_view_classi.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view_classi.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view_classi.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view_classi.setSortingEnabled(True)

        self.verticalLayout_5.addWidget(self.table_view_classi)

        self.label_classi = QLabel(self.tab_classi)
        self.label_classi.setObjectName(u"label_classi")

        self.verticalLayout_5.addWidget(self.label_classi)

        self.tabWidget.addTab(self.tab_classi, "")
        self.tab_stanze = QWidget()
        self.tab_stanze.setObjectName(u"tab_stanze")
        self.verticalLayout_6 = QVBoxLayout(self.tab_stanze)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.table_view_stanze = QTableView(self.tab_stanze)
        self.table_view_stanze.setObjectName(u"table_view_stanze")
        self.table_view_stanze.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view_stanze.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_view_stanze.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view_stanze.setSortingEnabled(True)

        self.verticalLayout_6.addWidget(self.table_view_stanze)

        self.label_aule = QLabel(self.tab_stanze)
        self.label_aule.setObjectName(u"label_aule")

        self.verticalLayout_6.addWidget(self.label_aule)

        self.tabWidget.addTab(self.tab_stanze, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Carica XML", None))
        self.salva_html_btn.setText(QCoreApplication.translate("MainWindow", u"Salva HTML", None))
        self.salva_xlsx_btn.setText(QCoreApplication.translate("MainWindow", u"Salva XLSX", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lezioni),
                                  QCoreApplication.translate("MainWindow", u"Lezioni", None))
        self.label_docenti.setText(QCoreApplication.translate("MainWindow",
                                                              u"Doppio click del mouse per mostrare le lezioni associate al docente",
                                                              None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_docenti),
                                  QCoreApplication.translate("MainWindow", u"Docenti", None))
        self.label_classi.setText(QCoreApplication.translate("MainWindow",
                                                             u"Doppio click del mouse per mostrare le lezioni associate alla classe",
                                                             None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_classi),
                                  QCoreApplication.translate("MainWindow", u"Classi", None))
        self.label_aule.setText(QCoreApplication.translate("MainWindow",
                                                           u"Doppio click del mouse per mostrare le lezioni associate alle aule",
                                                           None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_stanze),
                                  QCoreApplication.translate("MainWindow", u"Aule", None))
    # retranslateUi
