from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from _func import database
from _class import dialogperforaciones
from time import strftime


class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self):
		QMainWindow.__init__(self)
		uic.loadUi('_ui/mainwindow.ui', self)

		with open("_css/stylesOscuro.css") as f:
			self.setStyleSheet(f.read())


		
		# ::::::::::::::::::::::::::::::   INSTANCIAR UIs   ::::::::::::::::::::::::::::::
		
		self.frameProyecto = uic.loadUi('_ui/frameProyecto.ui')
		self.frameOrdenCampo = uic.loadUi('_ui/frameOrdenCampo.ui')
		self.frameOrdenLab= uic.loadUi('_ui/frameOrdenLab.ui')
		self.frameBDPerforaciones= uic.loadUi('_ui/frameBDPerforaciones.ui')
		self.frameBDEnsayos= uic.loadUi('_ui/frameBDEnsayos.ui')
		self.frameReportes= uic.loadUi('_ui/frameReportes.ui')
		self.frameGraficar= uic.loadUi('_ui/frameGraficar.ui')
		self.frameConfiguracion= uic.loadUi('_ui/frameConfiguracion.ui')


		self.verticalLayoutModel.addWidget(self.frameInicio)
		self.verticalLayoutModel.addWidget(self.frameProyecto)
		self.verticalLayoutModel.addWidget(self.frameOrdenCampo)
		self.verticalLayoutModel.addWidget(self.frameOrdenLab)
		self.verticalLayoutModel.addWidget(self.frameBDPerforaciones)
		self.verticalLayoutModel.addWidget(self.frameBDEnsayos)
		self.verticalLayoutModel.addWidget(self.frameReportes)
		self.verticalLayoutModel.addWidget(self.frameGraficar)
		self.verticalLayoutModel.addWidget(self.frameConfiguracion)

		self.functionStyleButtonPanel(0)
		
		#self.frameBDPerforaciones.setStyleSheet('background-color: #1B7499;')
		#self.frameGraficar.setStyleSheet('background-color: #102D39;')

		scena = QGraphicsScene()
		redbrus =QBrush(Qt.blue)
		blapen = QPen(Qt.black)
		elipse=scena.addEllipse(10,.10,200,200,blapen,redbrus)
		cuadro =scena.addRect(-100,-100,200,200,blapen,redbrus)
		elipse.setFlag(QGraphicsItem.ItemIsMovable)
		cuadro.setFlag(QGraphicsItem.ItemIsMovable)
		self.frameGraficar.graphicsView.setScene(scena)

		# ::::::::::::::::::::::::::::::   CONFIGURACÓN UIs   ::::::::::::::::::::::::::::::
		
		self.setWindowIcon(QIcon('Images/Icono_2_PNG.png'))
		self.setWindowTitle("InSituGeo - Sistema de perforaciones")
		#self.setMinimumSize(800, 600)
		self.toolButtonStartProject.setCursor(Qt.PointingHandCursor)
		self.listWidgetProyectos.setSpacing(5)
		nombresColumnasPerforaciones = ('Coor Este', 'Coor Norte', 'Elevación', 'Profundidad',
						  'Fecha Inicio', 'Fecha Final', 'Localización')
		menuMostrarOcultar = QMenu()
		for indice, columna in enumerate(nombresColumnasPerforaciones, start=0):
			accion = QAction(columna, menuMostrarOcultar)
			accion.setCheckable(True)
			accion.setChecked(True)
			accion.setData(indice)

			menuMostrarOcultar.addAction(accion)
		self.frameBDPerforaciones.pushButtonMostrarOcultarPerforaciones.setCursor(Qt.PointingHandCursor)
		self.frameBDPerforaciones.pushButtonMostrarOcultarPerforaciones.setMenu(menuMostrarOcultar)
		self.frameBDPerforaciones.tableWidgetPerforaciones.setContextMenuPolicy(Qt.CustomContextMenu)

		# GUARDAR INFORMACIÓN EN EL PORTAPAPELES
		self.copiarInformacion = QApplication.clipboard()

		

		# ::::::::::::::::::::::::::::::   EVENTOS   ::::::::::::::::::::::::::::::

		#					_ _ _ _ _ _ FRAME MAINWINDOW _ _ _ _ _ 
		self.toolButtonInicio.clicked.connect(self.onClickedToolButtonInicio)
		self.toolButtonProyecto.clicked.connect(self.onClickedToolButtonProyecto)
		self.toolButtonOrdenCampo.clicked.connect(self.onClickedToolButtonOrdenCampo)
		self.toolButtonOrdenLab.clicked.connect(self.onClickedToolButtonOrdenLab)
		self.toolButtonBDPerforaciones.clicked.connect(self.onClickedToolButtonBDPerforaciones)
		self.toolButtonBDEnsayos.clicked.connect(self.onClickedToolButtonBDEnsayos)
		self.toolButtonReportes.clicked.connect(self.onClickedToolButtonReportes)
		self.toolButtonGraficar.clicked.connect(self.onClickedToolButtonGraficar)
		self.toolButtonConfiguracion.clicked.connect(self.onClickedToolButtonConfiguracion)

		#					_ _ _ _ _ _ FRAME INICIO _ _ _ _ _ 
		self.toolButtonStartProject.clicked.connect(self.onClickedtoolButtonStartProject)
		self.toolButtonOpenProject.clicked.connect(self.onClickedtoolButtonOpenProject)
		self.listWidgetProyectos.doubleClicked.connect(self.onDoubleClickedlistWidgetProyectos)

		#					_ _ _ _ _ _ FRAME PROYECTO _ _ _ _ _ 
		self.frameProyecto.pushButtonActualizar.clicked.connect(self.onClickedpushButtonActualizar)


		#					_ _ _ _ _ _ FRAME PERFORACIONES _ _ _ _ _ 
		menuMostrarOcultar.triggered.connect(self.onTriggeredmenuMostrarOcultar)
		self.frameBDPerforaciones.tableWidgetPerforaciones.customContextMenuRequested.connect(self.customContextMenuRequestedtableWidgetPerforaciones)

		self.frameBDPerforaciones.pushButtonBuscarTodasPerforaciones.clicked.connect(self.onClickedpushButtonBuscarTodasPerforaciones)
		self.frameBDPerforaciones.pushButtonAgergarPerforacion.clicked.connect(self.onClickedpushButtonAgergarPerforacion)
		self.frameBDPerforaciones.pushButtonActualizarPerforacion.clicked.connect(self.onClickedpushButtonActualizarPerforacion)
		self.frameBDPerforaciones.pushButtonEliminarPerforacion.clicked.connect(self.onClickedpushButtonEliminarPerforacion)
		self.frameBDPerforaciones.pushButtonLimpiarPerforacion.clicked.connect(self.onClickedpushButtonLimpiarPerforacion)
		self.frameBDPerforaciones.lineEditNombrePerforacion.textEdited.connect(self.onEditlineEditNombrePerforacion)
		self.frameBDPerforaciones.lineEditNombreBuscarPerforacion.textEdited.connect(self.onEditlineEditNombreBuscarPerforacion)
		self.frameBDPerforaciones.pushButtonLimpiarTablaPerforacion.clicked.connect(self.onClickedpushButtonLimpiarTablaPerforacion)
		self.frameBDPerforaciones.tableWidgetPerforaciones.cellDoubleClicked.connect(self.onDoubleClickedtableWidgetPerforaciones)
		self.frameBDPerforaciones.toolButtonMasOrdenPerforacion.clicked.connect(self.onClickedtoolButtonMasOrdenPerforacion)

		#					_ _ _ _ _ _ FRAME GRAFICAR _ _ _ _ _ 
		


		# ::::::::::::::::::::::::::::::   OTROS   ::::::::::::::::::::::::::::::

		self.functionUpdateListProject(database.getListProjects(self))



	#************************************************************************************************
	# :::::::::::::::::::::::::::::::::::::   FUNCIONES EVENTOS :::::::::::::::::::::::::::::::::::::
	#************************************************************************************************

	#					_ _ _ _ _ _ FRAME INICIO _ _ _ _ _ 
	def onClickedToolButtonInicio(self):
		self.functionStyleButtonPanel(0)

	def onClickedToolButtonProyecto(self):
		self.functionStyleButtonPanel(1)

	def onClickedToolButtonOrdenCampo(self):
		self.functionStyleButtonPanel(2)
		
	def onClickedToolButtonOrdenLab(self):
		self.functionStyleButtonPanel(3)

	def onClickedToolButtonBDPerforaciones(self):
		self.functionStyleButtonPanel(4)
		
	def onClickedToolButtonBDEnsayos(self):
		self.functionStyleButtonPanel(5)

	def onClickedToolButtonReportes(self):
		self.functionStyleButtonPanel(6)

	def onClickedToolButtonGraficar(self):
		self.functionStyleButtonPanel(7)
		
	def onClickedToolButtonConfiguracion(self):
		self.functionStyleButtonPanel(8)



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


	def functionStyleButtonPanel(self,buttonNo):
		listSetVisible = [False,False,False,False,False,False,False,False,False]
		listSetVisible[buttonNo]=True
		self.frameInicio.setVisible(listSetVisible[0])
		self.frameProyecto.setVisible(listSetVisible[1])
		self.frameOrdenCampo.setVisible(listSetVisible[2])
		self.frameOrdenLab.setVisible(listSetVisible[3])
		self.frameBDPerforaciones.setVisible(listSetVisible[4])
		self.frameBDEnsayos.setVisible(listSetVisible[5])
		self.frameReportes.setVisible(listSetVisible[6])
		self.frameGraficar.setVisible(listSetVisible[7])
		self.frameConfiguracion.setVisible(listSetVisible[8])
		'''
		itemSetStyleSheet = 'hover{background-color: #4087c9;font-size:16px;}'
		#itemSetStyleSheet = 'background-color: #19303d; color: gray;'
		listSetStyleSheet = [itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet,
							itemSetStyleSheet]

		listSetStyleSheet[buttonNo]='background-color: #102D39; color: gray;'
		self.toolButtonInicio.setStyleSheet(listSetStyleSheet[0])
		self.toolButtonProyecto.setStyleSheet(listSetStyleSheet[1])
		self.toolButtonOrdenCampo.setStyleSheet(listSetStyleSheet[2])
		self.toolButtonOrdenLab.setStyleSheet(listSetStyleSheet[3])
		self.toolButtonBDPerforaciones.setStyleSheet(listSetStyleSheet[4])
		self.toolButtonBDEnsayos.setStyleSheet(listSetStyleSheet[5])
		self.toolButtonReportes.setStyleSheet(listSetStyleSheet[6])
		self.toolButtonGraficar.setStyleSheet(listSetStyleSheet[7])
		self.toolButtonConfiguracion.setStyleSheet(listSetStyleSheet[8])
		'''

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