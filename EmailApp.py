import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSlot
import os
import openai
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel("Email:", self)
        self.label.move(15, 20)

        self.textbox = QTextEdit(self)
        self.textbox.move(80, 20)
        self.textbox.resize(1000, 300)
        self.textbox.setPlaceholderText("Paste your email here...")
        
        self.label2 = QLabel("Parameters:", self)
        self.label2.move(15, 335)
        
        self.textbox2 = QTextEdit(self)
        self.textbox2.move(80, 540)
        self.textbox2.resize(700, 200)
        self.textbox2.setReadOnly(1)
        self.textbox2.setPlaceholderText("Press submit for a response...")
        
        self.label3 = QLabel("Response:", self)
        self.label3.move(15, 650)
        
        self.responseParamsBox = QTextEdit(self)
        self.responseParamsBox.move(80, 330)
        self.responseParamsBox.resize(700, 200)
        self.responseParamsBox.setPlaceholderText("Write a short sentence saying how to respond. For example, you could say \" Respond saying that I am not interested.\" ")

        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["Business", "Casual", "Business-Casual", "2nd-grade level", "5th-grade level"])
        self.dropdown.move(80, 760)
        
        self.submitButton = QPushButton(self)
        self.submitButton.setText("Submit")
        self.submitButton.move(190,760)
        self.submitButton.clicked.connect(self.submitClick)
        
        self.clearButton = QPushButton(self)
        self.clearButton.setText("Clear")
        self.clearButton.move(300,760)
        self.clearButton.clicked.connect(self.clearClick)

        self.setGeometry(300, 300, 1200, 900)
        self.setWindowTitle("Field Bros Email App v0.9")
        self.show()
        
    def queryChatGPT(self, email, params, style):
        openai.api_key = "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"
        prompt1=  "I reveived the following email, " + email +". "  + params + " Respond in a " + style + " style."
        print(prompt1)
        
        res = openai.Completion.create(
          model="text-davinci-003",
          prompt =  prompt1,
          max_tokens=2100,
          temperature=0
        )
        r = str(res)
        resTemp = json.loads(r)
        response = resTemp['choices'][0]['text']
        print(response)
        return response
        
        
    @pyqtSlot()
    def submitClick(self):
        email = self.textbox.toPlainText()
        params = self.responseParamsBox.toPlainText()
        style = self.dropdown.currentText()
        result = self.queryChatGPT(email, params, style)
        self.textbox2.setPlainText(result)
        
    @pyqtSlot()
    def clearClick(self):
        self.textbox.clear()
        self.textbox2.clear()
        self.responseParamsBox.clear()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
