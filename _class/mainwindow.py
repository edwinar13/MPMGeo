from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from _func import database
from _class import dialogperforaciones
from time import strftime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from _class import zoom


class MplCanvas(FigureCanvasQTAgg):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		fig.tight_layout(pad=0.0)
		super(MplCanvas, self).__init__(fig)



class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi('_ui/mainwindow.ui', self)

		with open("_css/stylesClaro.css") as f:
			self.setStyleSheet(f.read())

	
		# ::::::::::::::::::::::::::::::   INSTANCIAR UIs   ::::::::::::::::::::::::::::::			
		self.frame_Graficar= uic.loadUi('_ui/frameGraficar.ui')
		self.verticalLayout_principal.addWidget(self.frame_Inicio)
		self.verticalLayout_principal.addWidget(self.frame_Graficar)

		self.areaDraw = MplCanvas(self.frame_Graficar, width=5, height=4, dpi=100)
		self.verticalLayout_principal.addWidget(self.areaDraw)

		self.toolbarDraw = NavigationToolbar(self.areaDraw, self)
		self.verticalLayout_principal.addWidget(self.toolbarDraw)

		

		self.areaDraw.axes.cla()
		self.areaDraw.axes.plot([0], [0])
		
		scale = 1.1
		zp = zoom.ZoomPan()
		figZoom = zp.zoom_factory(self.areaDraw.axes, base_scale = scale)
		figPan = zp.pan_factory(self.areaDraw.axes)

		self.show()


	
	
		
			

		# ::::::::::::::::::::::::::::::   CONFIGURACÓN UIs   ::::::::::::::::::::::::::::::		
		self.functionStyleButtonPanel(0)
		self.setWindowIcon(QIcon('Images/Icono_2_PNG.png'))
		self.setWindowTitle("InSituGeo - Sistema de perforaciones")
		self.setMinimumSize(800, 600)
		self.textEdit_Console.setReadOnly(1)
		
		self.tabWidget.setTabEnabled(1,False)
		self.tabWidget.setTabEnabled(2,False)
		self.tabWidget.setTabEnabled(3,False)
		self.tabWidget.setTabEnabled(0,False)

		self.statusbar.showMessage('MPMGeo')
	
		

		# GUARDAR INFORMACIÓN EN EL PORTAPAPELES
		self.copiarInformacion = QApplication.clipboard()
		

		# VARIABLES GENERALES
		self.CommandSelect = None

		# ::::::::::::::::::::::::::::::   EVENTOS   ::::::::::::::::::::::::::::::
		self.checkBox_malla_coorIni.stateChanged.connect(self.stateChangedcheckBox_malla_coorIni)
		self.pushButton_malla_agregar.clicked.connect(self.onClickedpushButton_malla_agregar)

		# ::::::::::::::::::::::::::::::   TECLADO   ::::::::::::::::::::::::::::::
		self.actionNuevo.setShortcut('Ctrl+n')
		self.actionNuevo.setStatusTip('Nuevo')
		self.actionNuevo.triggered.connect(self.onTriggeredactionNuevo)

		"""
		self.toolButton_Rectangle.clicked.connect(self.onClickedToolButton_Rectangle)
		self.toolButton_Circle.clicked.connect(self.onClickedToolButton_Circle)
		self.toolButton_Line.clicked.connect(self.onClickedToolButton_Line)
		self.toolButton_Polyline.clicked.connect(self.onClickedToolButton_Polyline)

		self.lineEdit_Console_Command.returnPressed.connect(self.editingFinishedLineEdit_Console_Command)

		
		editingFinished
		inputRejected
		returnPressed 
		selectionChanged 
		textChanged (arg__1)
		textEdited (arg__1)
		"""

		#					_ _ _ _ _ _ FRAME MAINWINDOW _ _ _ _ _ 
		"""
		self.toolButtonInicio.clicked.connect(self.onClickedToolButtonInicio)
		self.listWidgetProyectos.doubleClicked.connect(self.onDoubleClickedlistWidgetProyectos)
		menuMostrarOcultar.triggered.connect(self.onTriggeredmenuMostrarOcultar)
		self.frameBDPerforaciones.tableWidgetPerforaciones.customContextMenuRequested.connect(self.customContextMenuRequestedtableWidgetPerforaciones)
		self.frameBDPerforaciones.lineEditNombrePerforacion.textEdited.connect(self.onEditlineEditNombrePerforacion)
		self.frameBDPerforaciones.tableWidgetPerforaciones.cellDoubleClicked.connect(self.onDoubleClickedtableWidgetPerforaciones)
		"""


		# ::::::::::::::::::::::::::::::   OTROS   ::::::::::::::::::::::::::::::

		#self.functionUpdateListProject(database.getListProjects(self))



	#************************************************************************************************
	# :::::::::::::::::::::::::::::::::::::   FUNCIONES EVENTOS :::::::::::::::::::::::::::::::::::::
	#************************************************************************************************

	def stateChangedcheckBox_malla_coorIni(self):
	
		if self.checkBox_malla_coorIni.isChecked():
			self.lineEdit_malla_xi.setEnabled(True)
			self.lineEdit_malla_xi.clear()
			self.lineEdit_malla_yi.setEnabled(True)	
			self.lineEdit_malla_yi.clear()		
		else:
			self.lineEdit_malla_xi.setEnabled(False)
			self.lineEdit_malla_xi.clear()
			self.lineEdit_malla_yi.setEnabled(False)
			self.lineEdit_malla_yi.clear()
		
	def onClickedpushButton_malla_agregar(self):

		var_ancho = self.lineEdit_malla_ancho.text()
		var_alto = self.lineEdit_malla_alto.text()		
		var_xi = self.lineEdit_malla_xi.text()
		var_yi = self.lineEdit_malla_yi.text()		
		coordenada_incio = self.checkBox_malla_coorIni.isChecked()
		print(coordenada_incio)

		if var_ancho != '' and var_alto != '':

			if coordenada_incio == True and (var_xi == '' or var_yi == ''):

				buttonReply = QMessageBox.question(self, 'Mensaje PyQt5', "Campos vacios en coordendas", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				self.tabWidget.setTabEnabled(1,False)

			else:

				# aca falta validar que sean nuemeros 
				if  coordenada_incio == False:
					var_xi = 0
					var_yi = 0
				else:
					var_xi = float(self.lineEdit_malla_xi.text())
					var_yi = float(self.lineEdit_malla_yi.text())

				var_ancho = float(self.lineEdit_malla_ancho.text())
				var_alto = float(self.lineEdit_malla_alto.text())

	
				lista_puntos=[(var_xi,var_yi),
							(var_xi+var_ancho,var_yi),
							(var_xi+var_ancho,var_yi+var_alto),
							(var_xi,var_yi+var_alto)]

				fila = 0
				self.tableWidget_malla_coordenadas.clearContents()
				self.tableWidget_malla_coordenadas.setRowCount(0)
				coordenadasx=[0,0,0,0]
				coordenadasy=[0,0,0,0]
				for x, y in lista_puntos:
					coordenadasx[fila]=x
					coordenadasy[fila]=y
					self.tableWidget_malla_coordenadas.setRowCount(fila + 1)			
					self.tableWidget_malla_coordenadas.setItem(fila, 0, QTableWidgetItem(str(fila+1)))
					self.tableWidget_malla_coordenadas.setItem(fila, 1, QTableWidgetItem(str(x)))
					self.tableWidget_malla_coordenadas.setItem(fila, 2, QTableWidgetItem(str(y)))
					fila += 1
		
				self.tabWidget.setTabEnabled(1,True)
				if self.pushButton_malla_agregar.text()=='Agregar':
					self.pushButton_malla_agregar.setText('Actualizar')

				
				self.areaDraw.axes.cla()
				self.areaDraw.axes.plot(coordenadasx, coordenadasy,'bo')				
				self.areaDraw.draw()
					
		
		else:
			buttonReply = QMessageBox.question(self, 'Mensaje MPMGeo', "Campos vacios")
			self.tabWidget.setTabEnabled(1,True)
		
	def onTriggeredactionNuevo(self):
		self.functionStyleButtonPanel(2)
		self.tabWidget.setTabEnabled(0,True)

		


		
	#************************************************************************************************
	# :::::::::::::::::::::::::::::::::::::   FUNCIONES GENERALES :::::::::::::::::::::::::::::::::::::
	#************************************************************************************************

	def functionIsInteger(self,value):
		pass

	def functionIsInteger(self,value):
		pass



	# ::::::::::::::::::::::::::::::   DRAW   :::::::::::::::::::::::::::::: 
	
			
	def editingFinishedLineEdit_Console_Command(self):
		Commandtext = self.lineEdit_Console_Command.text()

		if self.CommandSelect == "Line":
			data=Commandtext.split(":")
			data=data[1].split(",")
			if len(data)==4:
				xi, yi=float(data[0]),float(data[1])
				xj, yj=float(data[2]), float(data[3])
				self.drawLine(xi, yi, xj, yj)

		if self.CommandSelect == "Rectangle":
			data=Commandtext.split(":")
			data=data[1].split(",")
			if len(data)==4:
				xi, yi=float(data[0]),float(data[1])
				xj, yj=float(data[2]), float(data[3])
				self.drawRectangle(xi, yi, xj, yj)

		if self.CommandSelect == "Circle":
			data=Commandtext.split(":")
			data=data[1].split(",")
			if len(data)==3:
				xi, yi=float(data[0]),float(data[1])
				d=float(data[2])
				self.drawCircle(xi, yi, d)
		print('5555555555555555')
		if self.CommandSelect == "Polyline":
				self.drawPolyLine()
		

		'''

		if self.CommandSelect=="Rectangle":
			self.drawRectangle(Commandtext)
		'''	
		self.textEdit_Console_Command.append(Commandtext)
		self.lineEdit_Console_Command.clear()
		self.CommandSelect = None
		
	def drawCircle(self, xi, yi, d):

		whitebrus =QBrush(Qt.white)
		blapen = QPen(Qt.black)
		elipse=self.scena.addEllipse(xi,yi,d,d,blapen,whitebrus)
		elipse.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(self.scena)

	def drawRectangle(self, xi, yi, xj, yj):

		#scena = QGraphicsScene()
		whitebrus =QBrush(Qt.white)
		blapen = QPen(Qt.black)
		cuadro =self.scena.addRect(xi,yi,xj-xi,yj-yi,blapen,whitebrus)
		cuadro.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(self.scena)

	def drawLine(self, xi, yi, xj, yj):

		#scena = QGraphicsScene()
		blapen = QPen(Qt.black)
		cuadro =self.scena.addLine(xi,yi,xj,yj,blapen)
		cuadro.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(self.scena)

	def drawPolyLine(self):


		polygon = QPolygonF()
		polygon << QPointF(10.4, 20.5) 
		polygon << QPointF(20.2, 30.2)
		polygon << QPointF(0,100)
		#scena = QGraphicsScene()
		blapen = QPen(Qt.black)
		cuadro =self.scena.addPolygon(polygon,blapen)
		cuadro.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(self.scena)

	
	def mousePressEvent(self, event):
		print('--un click {}'.format(event.pos()))

	def QGraphicsSceneMouseEvent(self, event):
		print('--un click {}'.format(event.pos()))

		'''
	def mouseMoveEvent(scena, event: 'QGraphicsSceneMouseEvent'):
		new_cursor_position   = event.scenePos()
		old_cursor_position   = event.lastScenePos()
		old_top_left_corner   = self.scenePos()
		print(698)

	def mousePressEvent(scena, event: 'QGraphicsSceneMouseEvent'):
		print('click {}'.format(event.scenePos()))

		'''

	'''
		poscicion=QGraphicsSceneMouseEvent.pos()
		print(poscicion)
		#https://stackoverflow.com/questions/40955902/how-to-get-mouse-release-coordinates-in-qgraphicsview
		#https://www.walletfox.com/course/qgraphicsitemruntimedrawing.php
	'''
	def mouseMoveEvent(self, event):
		print('--Move click {}'.format(event.pos()))
		punto=event.pos()
		print(punto.x())

	def mouseRelaseEvent(self, event):
		print('--eRelase click {}'.format(event.pos()))

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			#self.close()
			self.lineEdit_Console_Command.clear()
			self.textEdit_Console_Command.append("→→ Cancel ←←")
			self.CommandSelect = None
			print(self.CommandSelect)

	def mouseDoubleClickEvent(self, event):
		print('Doble click x:{}'.format(event.x()))
		print('Doble click y:{}'.format(event.y()))
		print('--Doble click {}'.format(event.pos()))

		#self.close()

	def resizeEvent(self, event):
		self.label.setText("Window Resized to QSize(%d, %d)" %
		(event.size().width(), event.size().height()))
		
		"""
		#scena = QGraphicsScene()
		redbrus =QBrush(Qt.yellow)
		blapen = QPen(Qt.black)
		cuadro =self.scena.addRect(0,0,200,200,blapen,redbrus)
		cuadro.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(self.scena)
		"""
		






	#					_ _ _ _ _ _ FRAME PROYECTO _ _ _ _ _ 
	
	def onClickedtoolButtonStartProject(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"New Project","","Database Files (*.db)", options=options)
		if fileName:
			if database.newProject(fileName):			
				#self.botonOrdenCampo.setEnabled(True)
				#self.botonProyecto.setEnabled(True)
				self.labelProyecto.setText(fileName)
				hora = QTime.currentTime().toString("hh:mm:ss A ")
				fecha = strftime("%d/%m/%y")
				database.addListProjects(self,fileName.split('/')[-1],fecha,hora,fileName)
				self.functionUpdateListProject(database.getListProjects(self))
				self.functionStyleButtonPanel(1)
				self.functionSetDataProject(fileName)

	def onClickedtoolButtonOpenProject(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"Open Project", "","Database Files (*.db)", options=options)
		if fileName:
			self.labelProyecto.setText(fileName)
			hora = QTime.currentTime().toString("hh:mm:ss A ")
			fecha = strftime("%d/%m/%y")
			database.addListProjects(self,fileName.split('/')[-1],fecha,hora,fileName)
			self.functionUpdateListProject(database.getListProjects(self))
			self.functionStyleButtonPanel(1)
			self.functionSetDataProject(fileName)

	def onDoubleClickedlistWidgetProyectos(self):
		proyectoSeleccionado=([item.text() for item in self.listWidgetProyectos.selectedItems()])
		nombreP=(proyectoSeleccionado[0].split('\n')[0])
		rutaP=(proyectoSeleccionado[0].split('\n')[3])

		if proyectoSeleccionado:
			self.labelProyecto.setText(rutaP)
			hora = QTime.currentTime().toString("hh:mm:ss A ")
			fecha = strftime("%d/%m/%y")
			database.addListProjects(self,nombreP,fecha,hora,rutaP)
			self.functionUpdateListProject(database.getListProjects(self))
			self.functionStyleButtonPanel(1)
			self.functionSetDataProject(rutaP)

	def onClickedpushButtonActualizar(self):
		ruta = self.labelProyecto.text()
		data0 = self.frameProyecto.lineEditCodigo.text()
		data1 = self.frameProyecto.lineEditNombreInt.text()
		data2 = self.frameProyecto.lineEditContrato.text()
		data3 = self.frameProyecto.textEditDescripcion.toPlainText()
		database.updateDataProject(self,ruta,data0,data1,data2,data3)



	#					_ _ _ _ _ _ FRAME PERFORACIONES _ _ _ _ _ 


	def onTriggeredmenuMostrarOcultar(self, accion):
		columna = accion.data() + 2

		if accion.isChecked():
			self.frameBDPerforaciones.tableWidgetPerforaciones.setColumnHidden(columna, False)
		else:
			self.frameBDPerforaciones.tableWidgetPerforaciones.setColumnHidden(columna, True)

	def onClickedpushButtonBuscarTodasPerforaciones(self):
		ruta = self.labelProyecto.text()
		self.frameBDPerforaciones.tableWidgetPerforaciones.clearContents()
		self.frameBDPerforaciones.tableWidgetPerforaciones.setRowCount(0)
		datosDevueltos = database.getAllDBBorehole(self,ruta)

		if datosDevueltos:
			fila = 0
			for datos in datosDevueltos:
				self.frameBDPerforaciones.tableWidgetPerforaciones.setRowCount(fila + 1)
	
				idDato = QTableWidgetItem(str(datos[0]))
				idDato.setTextAlignment(Qt.AlignCenter)
				
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 0, idDato)
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 1, QTableWidgetItem(datos[1]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 2, QTableWidgetItem(datos[2]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 3, QTableWidgetItem(datos[3]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 4, QTableWidgetItem(str(datos[4])))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 5, QTableWidgetItem(str(datos[5])))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 6, QTableWidgetItem(datos[6]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 7, QTableWidgetItem(datos[7]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 8, QTableWidgetItem(datos[8]))

				fila += 1

		self.frameBDPerforaciones.lineEditNombreBuscarPerforacion.setText('')

	def onEditlineEditNombreBuscarPerforacion(self):
		ruta = self.labelProyecto.text()
		perforacion = self.frameBDPerforaciones.lineEditNombreBuscarPerforacion.text()
		datosDevueltos = ((database.getSearchDBBorehole(self,ruta,perforacion)))
		if datosDevueltos:
			fila = 0
			for datos in datosDevueltos:
				self.frameBDPerforaciones.tableWidgetPerforaciones.setRowCount(fila + 1)
	
				idDato = QTableWidgetItem(str(datos[0]))
				idDato.setTextAlignment(Qt.AlignCenter)
				
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 0, idDato)
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 1, QTableWidgetItem(datos[1]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 2, QTableWidgetItem(datos[2]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 3, QTableWidgetItem(datos[3]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 4, QTableWidgetItem(str(datos[4])))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 5, QTableWidgetItem(str(datos[5])))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 6, QTableWidgetItem(datos[6]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 7, QTableWidgetItem(datos[7]))
				self.frameBDPerforaciones.tableWidgetPerforaciones.setItem(fila, 8, QTableWidgetItem(datos[8]))

				fila += 1
		else:
			self.frameBDPerforaciones.tableWidgetPerforaciones.setRowCount(0)
	
	def onClickedpushButtonLimpiarTablaPerforacion(self):
		self.frameBDPerforaciones.tableWidgetPerforaciones.setRowCount(0)
		self.frameBDPerforaciones.lineEditNombreBuscarPerforacion.setText('')

	def onDoubleClickedtableWidgetPerforaciones(self, fila, columna):
		varPerforacion = self.frameBDPerforaciones.tableWidgetPerforaciones.item(fila,1).text()
		self.labelPerforacion.setText(varPerforacion)
	
	def customContextMenuRequestedtableWidgetPerforaciones(self, posicion):
			indices = self.frameBDPerforaciones.tableWidgetPerforaciones.selectedIndexes()

			if indices:
				menu = QMenu()

				itemsGrupo = QActionGroup(self)
				itemsGrupo.setExclusive(True)
				
				menu.addAction(QAction("Copiar todo", itemsGrupo))

				columnas = [self.frameBDPerforaciones.tableWidgetPerforaciones.horizontalHeaderItem(columna).text()
							for columna in range(self.frameBDPerforaciones.tableWidgetPerforaciones.columnCount())
							if not self.frameBDPerforaciones.tableWidgetPerforaciones.isColumnHidden(columna)]

				copiarIndividual = menu.addMenu("Copiar individual") 
				for indice, item in enumerate(columnas, start=0):
					accion = QAction(item, itemsGrupo)
					accion.setData(indice)
					
					copiarIndividual.addAction(accion)

				itemsGrupo.triggered.connect(self.copiarTableWidgetItem)
				
				menu.exec(self.frameBDPerforaciones.tableWidgetPerforaciones.viewport().mapToGlobal(posicion))

	def onClickedpushButtonAgergarPerforacion(self):
		ruta = self.labelProyecto.text()
		perforacion = self.frameBDPerforaciones.lineEditNombrePerforacion.text()
		localizacion = self.frameBDPerforaciones.lineEdiLocalizacionPerforacion.text()
		profundidad = float(self.frameBDPerforaciones.lineEditProfundidadPerforacion.text())
		coorE = self.frameBDPerforaciones.lineEditCoorEstePerforacion.text()
		coorN = self.frameBDPerforaciones.lineEditCorrNortePerforacion.text()
		elevacion = float(self.frameBDPerforaciones.lineEditElevacionPerforacion.text())
		dataInicial = self.frameBDPerforaciones.dateEditFechaInicioPerforacion.date()
		dataInicialString = dataInicial.toString( self.frameBDPerforaciones.dateEditFechaInicioPerforacion.displayFormat())
		dataFinal = self.frameBDPerforaciones.dateEditFechaFinalPerforacion.date()
		dataFinalString = dataFinal.toString( self.frameBDPerforaciones.dateEditFechaFinalPerforacion.displayFormat())

		
		database.addDBBorehole(self,ruta,perforacion,localizacion, profundidad,coorE,coorN,elevacion,dataInicialString,dataFinalString)
		self.functionClearBorehole()

	def onClickedpushButtonActualizarPerforacion(self):
		ruta = self.labelProyecto.text()
		perforacion = self.frameBDPerforaciones.lineEditNombrePerforacion.text()
		localizacion = self.frameBDPerforaciones.lineEdiLocalizacionPerforacion.text()
		profundidad = float(self.frameBDPerforaciones.lineEditProfundidadPerforacion.text())
		coorE = self.frameBDPerforaciones.lineEditCoorEstePerforacion.text()
		coorN = self.frameBDPerforaciones.lineEditCorrNortePerforacion.text()
		elevacion = float(self.frameBDPerforaciones.lineEditElevacionPerforacion.text())
		dataInicial = self.frameBDPerforaciones.dateEditFechaInicioPerforacion.date()
		dataInicialString = dataInicial.toString( self.frameBDPerforaciones.dateEditFechaInicioPerforacion.displayFormat())
		dataFinal = self.frameBDPerforaciones.dateEditFechaFinalPerforacion.date()
		dataFinalString = dataFinal.toString( self.frameBDPerforaciones.dateEditFechaFinalPerforacion.displayFormat())

		
		database.updateDBBorehole(self,ruta,perforacion,localizacion, profundidad,coorE,coorN,elevacion,dataInicialString,dataFinalString)
		self.functionClearBorehole()

	def onClickedpushButtonEliminarPerforacion(self):
		ruta = self.labelProyecto.text()
		perforacion = self.frameBDPerforaciones.lineEditNombrePerforacion.text()
		database.deleteDBBorehole(self,ruta,perforacion)
		self.functionClearBorehole()

	def onClickedpushButtonLimpiarPerforacion(self):

		self.functionClearBorehole()

	def onEditlineEditNombrePerforacion(self):
		ruta = self.labelProyecto.text()
		perforacion = self.frameBDPerforaciones.lineEditNombrePerforacion.text()
		result = ((database.getDBBorehole(self,ruta,perforacion)))
		if result:
			self.frameBDPerforaciones.lineEdiLocalizacionPerforacion.setText((result[0])[8])
			self.frameBDPerforaciones.lineEditProfundidadPerforacion.setText(str((result[0])[5]))
			self.frameBDPerforaciones.lineEditCoorEstePerforacion.setText((result[0])[2])
			self.frameBDPerforaciones.lineEditCorrNortePerforacion.setText((result[0])[3])
			self.frameBDPerforaciones.lineEditElevacionPerforacion.setText(str((result[0])[4]))			
			dateIni = QDate(int(((result[0])[6]).split('/')[2]),int(((result[0])[6]).split('/')[1]),int(((result[0])[6]).split('/')[0]))	
			self.frameBDPerforaciones.dateEditFechaInicioPerforacion.setDate(dateIni)
			dateFin = QDate(int(((result[0])[7]).split('/')[2]),int(((result[0])[7]).split('/')[1]),int(((result[0])[7]).split('/')[0]))
			self.frameBDPerforaciones.dateEditFechaFinalPerforacion.setDate(dateFin)

		else:
			self.functionClearBorehole(1)
	
	def onClickedtoolButtonMasOrdenPerforacion(self):
		texto = self.frameBDPerforaciones.labelVentanaAux.text()
		ventanaAuxiliar = dialogperforaciones.DialogPerforaciones(texto,self).exec_()
		print(ventanaAuxiliar)

		
	#************************************************************************************************
	# :::::::::::::::::::::::::::::::::::::   FUNCIONES GENERALES :::::::::::::::::::::::::::::::::::::
	#************************************************************************************************

	def functionStyleButtonPanel(self,frameNo):
		listSetVisible = [False,False,False]
		listSetVisible[frameNo]=True
		self.frame_Inicio.setVisible(listSetVisible[0])
		self.frame_Graficar.setVisible(listSetVisible[1])
		self.areaDraw.setVisible(listSetVisible[2])

		

	def functionUpdateListProject(self,dataProjects):
		self.listWidgetProyectos.clear()
		contador=0
		if dataProjects:
			for id_, proyecto_, fecha_, hora_, ruta_ in reversed(dataProjects):
				if contador<30:
					item = QListWidgetItem()
					item.setText('{}\n{}\n{}\n{}'.format(proyecto_, fecha_, hora_, ruta_))
					self.listWidgetProyectos.addItem(item)
				contador +=1

	def functionSetDataProject(self,fileName):		
		self.frameProyecto.lineEditCodigo.clear()
		self.frameProyecto.lineEditNombreInt.clear()
		self.frameProyecto.lineEditContrato.clear()
		self.frameProyecto.textEditDescripcion.clear()
		datos = database.getDataProject(self,fileName)
		if datos:
			self.frameProyecto.lineEditCodigo.setText(datos[0][1])
			self.frameProyecto.lineEditNombreInt.setText(datos[0][2])
			self.frameProyecto.lineEditContrato.setText(datos[0][3])
			self.frameProyecto.textEditDescripcion.setText(datos[0][4])
				
	def functionClearBorehole(self,tipo=0):
		if tipo == 0:
			self.frameBDPerforaciones.lineEditNombrePerforacion.clear()		
		
		self.frameBDPerforaciones.lineEdiLocalizacionPerforacion.clear()
		self.frameBDPerforaciones.lineEditProfundidadPerforacion.clear()
		self.frameBDPerforaciones.lineEditCoorEstePerforacion.clear()
		self.frameBDPerforaciones.lineEditCorrNortePerforacion.clear()
		self.frameBDPerforaciones.lineEditElevacionPerforacion.clear()
		dateIni = QDate(2000,1,1)
		self.frameBDPerforaciones.dateEditFechaInicioPerforacion.setDate(dateIni)
		self.frameBDPerforaciones.dateEditFechaFinalPerforacion.setDate(dateIni)			



	def copiarTableWidgetItem(self, accion):
			filaSeleccionada = [dato.text() for dato in self.frameBDPerforaciones.tableWidgetPerforaciones.selectedItems()]
				
			if accion.text() == "Copiar todo":
				filaSeleccionada = tuple(filaSeleccionada)
			else:
				filaSeleccionada = filaSeleccionada[accion.data()]

			self.copiarInformacion.clear(mode = QClipboard.Clipboard)
			self.copiarInformacion.setText(str(filaSeleccionada), QClipboard.Clipboard)