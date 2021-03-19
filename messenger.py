from PyQt5 import QtWidgets, QtCore
from clientui import Ui_Form
import requests
from datetime import datetime

class ExampleApp(QtWidgets.QMainWindow, Ui_Form):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.sendButton.pressed.connect(self.send_message)

		self.after = 0

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.get_messages)
		self.timer.start(1000)

	def print_message(self, message):
	    dt = datetime.fromtimestamp(message['time'])
	    dt_str = dt.strftime('%d %b %H:%M:%S')
	    self.textBrowser.append(dt_str + ' ' + message['name'])
	    self.textBrowser.append(message['text'])
	    self.textBrowser.append('')

	def get_messages(self):
		try:
			response = requests.get(
				'http://127.0.0.1:5000/messages',
				params={'after': self.after}
			)
		except:
			return

		messages = response.json()['messages']
		for message in messages:
			self.print_message(message)
			self.after = message['time']

	def send_message(self):
		text = self.textEdit.toPlainText()
		name = self.lineEdit.text()

		try:
			response = requests.post(
				'http://127.0.0.1:5000/send',
				json={'name': name, 'text': text}
			)
		except:
			self.textBrowser.append('Сервер недоступен')
			self.textBrowser.append('Попробуйте ещё раз')
			self.textBrowser.append('')
			return

		if response.status_code != 200:
			self.textBrowser.append('Имя и текст не должны быть пустыми. Текст <= 1000 символов.')
			self.textBrowser.append('')
			return

		self.textEdit.clear()

app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()