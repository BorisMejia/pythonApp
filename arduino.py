import serial

from tkinter import ttk
from tkinter import *

import sqlite3



class Aplicacion:
    
    db_proyecto = 'database.db'


    def __init__(self, window):
      self.wind = window
      self.wind.title('Aplicacion peso')
    #Creamos un recuadro contenedor 
      frame = LabelFrame(self.wind, text= 'Registrar Peso y Altura')
      frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    #Creamos label para identificar texto
      """ Label(frame, text = 'Nombre: ').grid(row=1, column=0)
      self.name = Entry(frame)
      self.name.grid(row = 1,column = 1) """
    #Creamos input para el peso 
      Label(frame, text = 'Peso: ').grid(row=2, column=0)
      self.peso =Entry(frame)
      self.peso.grid(row=2, column=1)
    #Creamos input para la estatura
      Label(frame, text='Estatura: ').grid(row=3, column=0)
      self.estatura = Entry(frame)
      self.estatura.grid(row=3, column=1)
    #Boton para funciones de la aplicacion
      ttk.Button(frame, text= 'Guardar peso', command=self.add_peso).grid(row=4, columnspan=2, sticky= W + E)
    #Mensaje de notificacion
      self.mensaje = Label(text='', fg='red')
      self.mensaje.grid(row=3, column=0, columnspan=3, sticky= W + E)
    #Tabla para visualizar todos los datos  
      self.tree = ttk.Treeview(height=10, columns=4)
      self.tree.grid(row=5, column=0, columnspan=3)
      self.tree.heading('#0', text='Peso', anchor= CENTER)
      self.tree.heading('#1', text='Altura', anchor= CENTER)
      self.get_pesos()
    #Configuración de la conexión serial
      self.serial_port = serial.Serial('COMX', 9600)  # Reemplaza 'COMX' con el puerto correcto
    
    def recibir_datos_arduino(self):
        # Lee datos desde Arduino
        try:
            datos = self.serial_port.readline().decode().strip()
            return datos
        except Exception as e:
            print(f"Error al recibir datos desde Arduino: {e}")
            return None

    def run_query(self, query, parameters = ()):
       with sqlite3.connect(self.db_proyecto) as conn:
          cursor = conn.cursor()
          resultado = cursor.execute(query, parameters)
          conn.commit()
          return resultado    
    
    def get_pesos(self):
       #Limpiar tabla
       registros = self.tree.get_children()
       for element in registros:
          self.tree.delete(element)
      #Consultando los datos
       query = 'SELECT * FROM peso ORDER BY peso DESC'
       db_row = self.run_query(query)
      #Rellenar datos
       for row in db_row:
        self.tree.insert('', 0, text=row[1], values=row[2])

    #Validar que los input tengan contenido
    def validar(self):
       return len(self.peso.get()) != 0 and len(self.estatura.get()) != 0
    #Agregar peso y estatura a la tabla
    def add_peso(self):
      datos_arduino = self.recibir_datos_arduino()
      if datos_arduino:
            self.guardar_en_archivo(datos_arduino)
      if self.validar():
          query = 'INSERT INTO peso VALUES(NULL, ?, ?)'
          parametros = (self.peso.get(), self.estatura.get())
          self.run_query(query, parametros)
          self.mensaje['text'] = 'El peso {} se guardo correctamente'.format(self.peso.get())
          self.peso.delete(0, END)
          self.estatura.delete(0, END)
      else:  
          self.mensaje['text'] = 'El peso y la estatura es requerido'       
      self.get_pesos()

    def guardar_en_archivo(self, datos):
        # Guardar datos en un archivo de texto
        try:
            with open('datos_arduino.txt', 'a') as archivo:
                archivo.write(datos + '\n')
        except Exception as e:
            print(f"Error al guardar en el archivo: {e}")

if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()