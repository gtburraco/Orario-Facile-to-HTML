# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_html.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QHBoxLayout, QPushButton,
                               QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout)


class Ui_Show_Html(object):
    def setupUi(self, Show_Html):
        if not Show_Html.objectName():
            Show_Html.setObjectName(u"Show_Html")
        Show_Html.resize(700, 500)
        self.verticalLayout = QVBoxLayout(Show_Html)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stampa_btn = QPushButton(Show_Html)
        self.stampa_btn.setObjectName(u"stampa_btn")

        self.horizontalLayout.addWidget(self.stampa_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.html_text = QTextBrowser(Show_Html)
        self.html_text.setObjectName(u"html_text")

        self.verticalLayout.addWidget(self.html_text)

        self.retranslateUi(Show_Html)

        QMetaObject.connectSlotsByName(Show_Html)

    # setupUi

    def retranslateUi(self, Show_Html):
        Show_Html.setWindowTitle(QCoreApplication.translate("Show_Html", u"Orario", None))
        self.stampa_btn.setText(QCoreApplication.translate("Show_Html", u"Stampa", None))
    # retranslateUi
