from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 614)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(710, 50, 97, 33))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(710, 160, 150, 17))
        self.label.setObjectName("label")
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setGeometry(QtCore.QRect(55, 50, 651, 431))
        self.treeView.setObjectName("treeView")
        self.pushButton.clicked.connect(self.klik)
        self.treeView.clicked.connect(self.kohde)
        self.treeView.activated.connect(self.kohde)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Listaa Tiedostot"))
        self.label.setText(_translate("Form", "TextLabel"))
        
    def klik(self):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setNameFilters(("*.py", "*.txt"))
        self.model.setNameFilterDisables(0)
        self.model.setRootPath("/home/jani")
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index("/home/jani"))
    
    def kohde(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)
        if os.path.isfile(filePath):
            tyyppi="Tiedosto"
        else:
            tyyppi="Hakemisto"
        isDirectory = os.path.isdir(filePath)
        print("valittu", filePath, ">>>", fileName, tyyppi)
        self.label.setText(filePath)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
