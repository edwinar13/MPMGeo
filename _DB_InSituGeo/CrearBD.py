import sqlite3

conexion=sqlite3.connect('BD_Config.db')
cursor=conexion.cursor()
try:
	cursor.execute('CREATE TABLE IF NOT EXISTS ULTIMOSPROYECTOS (ID INTEGER PRIMARY KEY, PROYECTO TEXT,'
					'FECHA TEXT, HORA TEXT,RUTA TEXT)')
	conexion.commit()
	print('Base de datos creada con exito')

except sqlite3.Error as e:
	print('EL ERROR ES: {}'.format(e))
conexion.close()




