import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
from main_ui_window import Ui_MainWindow
from currency_converter import CurrencyConverter
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QDoubleValidator, QValidator

class CurrencyCov(QtWidgets.QMainWindow):
    def __init__(self):
        super(CurrencyCov, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):

        self.ui.input_amount.setValidator(QtGui.QDoubleValidator())

        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(1068, 732)

        self.ui.convert_slide_btn.clicked.connect(self.convert_page_show)
        self.ui.history_slide_btn.clicked.connect(self.history_page_show)

        self.ui.pushButton.clicked.connect(self.slide_bar)

        self.ui.input_amount.setPlaceholderText("Cума:")
        self.ui.convert_button.clicked.connect(self.converter)


        with open("data.txt", "r") as data:
            for i in data:
                self.ui.history_listWidget.addItem(i)

    def slide_bar(self):
        width = self.ui.left_side_menu.width()

        if width == 70:
            newWidth = 220
            self.ui.convert_slide_btn.setStyleSheet("padding-left:0;")
            self.ui.history_slide_btn.setStyleSheet("padding-left:0;")
        else:
            newWidth = 70
            self.ui.convert_slide_btn.setStyleSheet("padding-left:110;")
            self.ui.history_slide_btn.setStyleSheet("padding-left:110;")

        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

        self.animation.start()

    def convert_page_show(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.convert_page)

    def history_page_show(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.history_page)

    def readFile(self):
        f = open("data.txt", "r")
        lineList=f.readlines()
        f.close()
        self.ui.history_listWidget.addItem(lineList[-1])

    def converter(self):

        c = CurrencyConverter()
        if self.ui.input_amount.text():
            input_amount = float(self.ui.input_amount.text())

            input_currency = self.ui.input_currency.currentText()
            output_currency = self.ui.output_currency.currentText()


            output_result = round(c.convert(input_amount, '%s' % (input_currency), '%s' % (output_currency)), 2)
            self.ui.result_label.setText(str(input_amount) + " " + str(input_currency) + " = " + str(output_result) + " " + str(output_currency))

            f = open("data.txt", "a")
            f.write(str(input_amount) + " " + str(input_currency) + " -> " + str(output_result) + " " + str(
                output_currency) + "\n")
            f.close()

        self.readFile()

app = QtWidgets.QApplication([])
application = CurrencyCov()
application.show()

sys.exit(app.exec())
