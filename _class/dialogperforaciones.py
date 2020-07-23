from PyQt5 import uic
from PyQt5.QtCore import (Qt, QFile, QDate,QTime, QSize, QTimer, QRect, 
						QRegExp, QTranslator, QLocale, QLibraryInfo)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,QRegExpValidator)

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog, QTableWidget, QMenu,
							 QTableWidgetItem, QAbstractItemView, QLineEdit, QPushButton,
							 QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
							 QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox,
							 QDateEdit, QComboBox)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#-------------------------- CLASE DE VENTANA ACERCA DE  ---------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class DialogPerforaciones(QDialog):
	"""docstring for DialogPerforaciones"""
	def __init__(self, texto, parent=None):
		super(DialogPerforaciones, self).__init__()
		
		self.parent = parent
		self.texto = texto		
		uic.loadUi('_ui/dialogPerforaciones.ui', self)
		self.setWindowTitle(texto)
		self.iniciarUI()

	def iniciarUI(self):
		self.spinBoxNoPerforaciones.setEnabled(False)
		self.textEditPreview.setEnabled(False)
		self.spinBoxNoPerforaciones.setMinimum(1)
		self.spinBoxNoPerforaciones.setMaximum(100)


		self.lineEditNuevaPerforacion.textEdited.connect(self.onEditlineEditNuevaPerforacion)
		self.pushButtonOK.clicked.connect(self.onClickedpushButtonOK)
		self.checkBoxMultiPeroraciones.clicked.connect(self.onClickedcheckBoxMultiPeroraciones)
		self.spinBoxNoPerforaciones.valueChanged.connect(self.onvalueChangedspinBoxNoPerforaciones)
		self.pushButtonCancelar.clicked.connect(self.close)

	def onEditlineEditNuevaPerforacion(self):
		if self.checkBoxMultiPeroraciones.isChecked():
			self.onvalueChangedspinBoxNoPerforaciones()
		else:
			self.textEditPreview.setText('{}'.format(self.lineEditNuevaPerforacion.text()))

	def onClickedpushButtonOK(self):
		
		self.parent.frameBDPerforaciones.labelVentanaAux.setText(self.textEditPreview.toPlainText())
		self.close()

	def onClickedcheckBoxMultiPeroraciones(self):
		if self.checkBoxMultiPeroraciones.isChecked():
			self.spinBoxNoPerforaciones.setEnabled(True)
			self.textEditPreview.setText('{}{}'.format(self.lineEditNuevaPerforacion.text(),1))

		else:
			self.spinBoxNoPerforaciones.setEnabled(False)
			self.spinBoxNoPerforaciones.setValue(1)
			self.textEditPreview.clear()
			self.textEditPreview.setText('{}'.format(self.lineEditNuevaPerforacion.text()))
			

	def onvalueChangedspinBoxNoPerforaciones(self):
		string = ''
		nombre = self.lineEditNuevaPerforacion.text()
		NoPerforaciones = self.spinBoxNoPerforaciones.value() + 1

		for i in range(1,NoPerforaciones):
			if i == 1:
				string = '{}{}'.format(nombre,i)
			else:
				string = '{}\n{}{}'.format(string,nombre,i)
		self.textEditPreview.setText(string)

