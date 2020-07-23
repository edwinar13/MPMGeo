from PyQt5.QtCore import (QFile)
from PyQt5.QtWidgets import (QMessageBox)
import sqlite3
import sys



#*************************************************************************************************
# ::::::::::::::::::::::::::::::   BASE DE DATOS DEL SOFWARE  ::::::::::::::::::::::::::::::
#*************************************************************************************************


def newApp():
	"""CREA DBASE DE DATOS DE SOFWARE, AL INCIAR SI NO EXISTE"""
	conexion=sqlite3.connect('_DB_InSituGeo/DB_InSituGeo.db')
	cursor=conexion.cursor()
	try:
		cursor.execute('CREATE TABLE IF NOT EXISTS ULTIMOSPROYECTOS (ID INTEGER PRIMARY KEY, PROYECTO TEXT,'
						'FECHA TEXT, HORA TEXT,RUTA TEXT)')
		conexion.commit()
		print('Base de datos creada con exito')

	except sqlite3.Error as e:
		print('EL ERROR ES: {}'.format(e))
	conexion.close()

def getListProjects(objeto):
	"""CONSULTA LOS PROYECTOS EN LA BASE DE DATOS Y LOS DEVUELVE TODOS"""
		
	if QFile.exists("_DB_InSituGeo/BD_Config.db"):
		conexion = sqlite3.connect("_DB_InSituGeo/BD_Config.db")
		cursor = conexion.cursor()
			
		try:
			sql = "SELECT * FROM ULTIMOSPROYECTOS"
			cursor.execute(sql)						
			datosDevueltos = cursor.fetchall()
			conexion.close()

		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)
	return datosDevueltos


def addListProjects(objeto,proyecto, fecha, hora, ruta):
	"""AGREGA UN NUEVO PROYECTO"""
	if QFile.exists('_DB_InSituGeo/BD_Config.db'):
		conexion = sqlite3.connect('_DB_InSituGeo/BD_Config.db')
		cursor = conexion.cursor()			  
		try:

			cursor.execute("DELETE FROM ULTIMOSPROYECTOS WHERE PROYECTO = ?", (proyecto,))
			conexion.commit()

			datos = [proyecto, fecha, hora, ruta]
			cursor.execute("INSERT INTO ULTIMOSPROYECTOS (PROYECTO, FECHA, HORA, RUTA) "
						   "VALUES (?,?,?,?)", datos)

			conexion.commit()
			conexion.close()
			validacion=True

		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
			validacion=False
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo"
							 "   ", QMessageBox.Ok)


#*************************************************************************************************
# ::::::::::::::::::::::::::::::   BASE DE DATOS PROYECTO's   ::::::::::::::::::::::::::::::
#*************************************************************************************************

def newProject(fileName):
	"""CREA LA BASE DER DATOS DE CADA PROYECTO NUEVO"""
		
	fileName='{}.db'.format(fileName)
	conexion=sqlite3.connect(fileName)
	cursor=conexion.cursor()
	print(fileName)
	try:
		cursor.execute('CREATE TABLE IF NOT EXISTS DATAPROJECT (ID INTEGER PRIMARY KEY,'
						'CODIGO TEXT,'
						'NOMBREPROJECTO TEXT,'
						'CONTRATO TEXT,'
						'DESCRIPCION TEXT)')
		conexion.commit()
		datos = ['', '', '', '']
		cursor.execute("INSERT INTO DATAPROJECT (CODIGO, NOMBREPROJECTO, CONTRATO, DESCRIPCION) "
					   "VALUES (?,?,?,?)", datos)

		conexion.commit()
		cursor.execute('CREATE TABLE IF NOT EXISTS BOREHOLE (ID INTEGER PRIMARY KEY, '
						'PERFORACION TEXT,'
						'COORE TEXT,'
						'COORN TEXT,'
						'ELEVACION FLOAT,'
						'PROFUNDIDAD FLOAT,'
						'FECHAINICIO DATE,'
						'FECHAFINAL DATE,'
						'LOCALIZACION TEXT)')
		conexion.commit()
		cursor.execute('CREATE TABLE IF NOT EXISTS WATERLEVEL (ID INTEGER PRIMARY KEY, '
						'PERFORACION TEXT,'
						'PROFUNDIDAD FLOAT,'
						'FECHA DATE,'
						'HORA DATE)')						  
		conexion.commit()
		cursor.execute('CREATE TABLE IF NOT EXISTS SAMPLES (ID INTEGER PRIMARY KEY, '
						'PERFORACION TEXT,'
						'MUESTRANO FLOAT,'
						'MUESTRATIPO FLOAT,'
						'PROFINICIAL FLOAT,'
						'PROFFINAL FLOAT,'
						'USC FLOAT,'
						'HUMEDADNATURAL FLOAT,'
						'LILITELIQUIDO FLOAT,'
						'LIMITEPLASTICO FLOAT,'
						'INDICEPLASTICIDAD FLOAT,'
						'FINOS FLOAT,'
						'ARENAS FLOAT,'
						'GRAVAS FLOAT,'
						'GAMAHUMEDO FLOAT,'
						'GAMASECO FLOAT,'
						'MATERIAORGANICA FLOAT,'
						'NSPT1 FLOAT,'
						'NSPT2 FLOAT,'
						'NSPT3 FLOAT,'
						'RQD FLOAT,'
						'I50 FLOAT,'
						'COMPRESIONROCA FLOAT,'
						'CDCOHESION FLOAT,'
						'CDFRICCION FLOAT,'
						'COMPRESIONINCOFINADA FLOAT,'
						'VELETAPICO FLOAT,'
						'VELETARESIDUAL FLOAT,'
						'MODULOELASTICIDAD FLOAT)')						  
		conexion.commit()
		validacion=True

	except sqlite3.Error as e:
		print('EL ERROR ES: {}'.format(e))
		validacion=False
	conexion.close()
	return validacion


def getDataProject(objeto,ruta):
	""" CONSULTA LA INFORMACION DE LA TABLA DATAPROJECT Y DEVUELVE LOPS DATOS """
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		try:
			sql = "SELECT * FROM DATAPROJECT"
			cursor.execute(sql)					 
			datosDevueltos = cursor.fetchall()
			conexion.close()
			return datosDevueltos

		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)


def updateDataProject(objeto, ruta, Codigo, NombreInt, Contrato, Descripcion):
	""" ACTUALIZA DATAPROJECT"""
	datos = [Codigo, NombreInt, Contrato, Descripcion,1]

	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		try:
			cursor.execute("UPDATE DATAPROJECT SET CODIGO = ?, NOMBREPROJECTO = ?, "
								   "CONTRATO = ?, DESCRIPCION = ? "
								   "WHERE ID = ?", datos)

	   
			conexion.commit()
			conexion.close()
			QMessageBox.information(objeto, "InSituGeo", "Datos Actualizados", QMessageBox.Ok)


		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)


#*************************************************************************************************
# ::::::::::::::::::::::::::::::   BASE DE DATOS PERFORACION   ::::::::::::::::::::::::::::::
#*************************************************************************************************

def addDBBorehole(objeto, ruta, perforacion, localizacion, profundidad, coorE, coorN, elevacion, dataInicialString, dataFinalString):
	"""AGREGA UN NUEVO PROYECTO"""
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()			
		#try:

		#cursor.execute("DELETE FROM ULTIMOSPROYECTOS WHERE PROYECTO = ?", (proyecto,))
		#conexion.commit()

		datos = [perforacion, coorE, coorN, elevacion, profundidad, dataInicialString, dataFinalString , localizacion]

		cursor.execute("INSERT INTO BOREHOLE (PERFORACION, COORE, COORN, ELEVACION , PROFUNDIDAD, FECHAINICIO, FECHAFINAL, LOCALIZACION) "
					   "VALUES (?,?,?,?,?,?,?,?)", datos)

		conexion.commit()
		conexion.close()
		QMessageBox.information(objeto, "InSituGeo", "Datos Agregados", QMessageBox.Ok)

		"""
		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
		"""	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo"
							 "   ", QMessageBox.Ok)


def getDBBorehole(objeto,ruta,perforacion):
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		#try:
		sql = "SELECT * FROM BOREHOLE WHERE PERFORACION=?"
		cursor.execute(sql, (perforacion,))				  
		datosDevueltos = cursor.fetchall()
		conexion.close()
		return datosDevueltos
		"""
		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
		"""

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)


def deleteDBBorehole(objeto,ruta,perforacion):
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		try:
			sql = "DELETE FROM BOREHOLE WHERE PERFORACION=?"
			cursor.execute(sql, (perforacion,))	
			conexion.commit()
			conexion.close()
			QMessageBox.information(objeto, "InSituGeo", "Perforación Eliminada",
								 QMessageBox.Ok)
		
		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
		

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)

def updateDBBorehole(objeto, ruta, perforacion, localizacion, profundidad, coorE, coorN, elevacion, dataInicialString, dataFinalString):

	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		#try:
		datos = [coorE, coorN, elevacion, profundidad, dataInicialString, dataFinalString , localizacion, perforacion]
		cursor.execute("UPDATE BOREHOLE SET PERFORACION = ?, COORE = ?, "
							   "COORN = ?, ELEVACION = ?, "
							   "PROFUNDIDAD = ?, FECHAINICIO = ? "
							   "FECHAFINAL = ?, LOCALIZACION = ? "
							   "WHERE PERFORACION = ?", datos)


		conexion.commit()
		conexion.close()
		QMessageBox.information(objeto, "InSituGeo", "Datos Actualizados", QMessageBox.Ok)

		"""
		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
		"""
	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)

def getAllDBBorehole(objeto,ruta):
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		try:
			sql = "SELECT * FROM BOREHOLE"
			cursor.execute(sql)					 
			datosDevueltos = cursor.fetchall()
			conexion.close()
			return datosDevueltos

		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)

	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)
	

def getSearchDBBorehole(objeto,ruta,perforacion):
	fileName='{}.db'.format(ruta)
	if QFile.exists(fileName):
		conexion = sqlite3.connect(fileName)
		cursor = conexion.cursor()
			
		try:
			
			sql = "SELECT * FROM BOREHOLE WHERE PERFORACION LIKE ?", ("%"+perforacion+"%",)
			cursor.execute(sql[0], sql[1])			
			datosDevueltos = cursor.fetchall()
			conexion.close()
			return datosDevueltos
		
		except:
			conexion.close()
			QMessageBox.critical(objeto, "InSituGeo", "Error desconocido 2",
								 QMessageBox.Ok)
		
	
	else:
		QMessageBox.critical(objeto, "InSituGeo", "No se encontro la base de datos de InSituGeo   ",
							 QMessageBox.Ok)
