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
      self.mensaje.grid(row=3, column=0, columnspan=2, sticky= W + E)
    #Tabla para visualizar todos los datos  
      self.tree = ttk.Treeview(height=10, columns=4)
      self.tree.grid(row=5, column=0, columnspan=2)
      self.tree.heading('#0', text='Peso', anchor= CENTER)
      self.tree.heading('#1', text='Altura', anchor= CENTER)
      self.get_pesos()

    #Botones 
      ttk.Button(text= 'Exportar', command = self.exportar).grid(row=6, column=0, sticky= W + E) 
      ttk.Button(text= 'Eliminar', command = self.eliminar_peso).grid(row=6, column=1, sticky= W + E) 
    def exportar(self):
        self.mensaje['text'] = ''
        try:
          #Obtener los valores de peso y estatura del elemento seleccionado
          seleccion = self.tree.selection()
          if seleccion:
          #Utilizar índices específicos que correspondan a peso y estatura en el Treeview
            peso = self.tree.item(seleccion, 'values')[0]
            estatura = self.tree.item(seleccion, 'values')[1]
          else:
            raise IndexError("No hay elementos seleccionados")  

        except (IndexError, TypeError) as e:
           self.mensaje['text'] = 'Por favor selecione peso y estatura'
           return
        self.mensaje['text'] = ''

        if peso and estatura:
        # Si hay valores de peso y estatura válidos, procede con la exportación
          try:
              with open("PesoEstatura.txt", "w") as archivo:
                archivo.write(f"{peso}, {estatura}\n")
              self.mensaje['text'] = 'Peso y estatura exportados correctamente.'
              self.get_pesos()
          except Exception as e:
            self.mensaje['text'] = f"Error al exportar peso y estatura: {e}"
        else:
          self.mensaje['text'] = 'No se han seleccionado peso y estatura válidos.'
    
    def eliminar_peso(self):
       self.mensaje['text'] = ''
       try:
          self.tree.item(self.tree.selection())['text']
       except IndexError as e:
          self.mensaje['text'] = 'Por favor selecione peso y estatura'  
          return
       self.mensaje['text'] = ''

       peso = self.tree.item(self.tree.selection())['text']
       query = 'DELETE FROM peso WHERE peso = ?' 
       self.run_query(query, (peso, ))
       self.mensaje['text'] = 'Peso {} eliminado correctamente'.format(peso)
       self.get_pesos()   
        
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
       """ for row in db_row:
        self.tree.insert('', 0, text=row[1], values=row[2]) """
       for row in db_row:
          self.tree.insert('', 0, text=row[1], values=row[2])

    #Validar que los input tengan contenido
    def validar(self):
       return len(self.peso.get()) != 0 and len(self.estatura.get()) != 0
    #Agregar peso y estatura a la tabla
    def add_peso(self):
      if self.validar():
          query = 'INSERT INTO peso VALUES(NULL, ?, ?)'
          parametros = (self.peso.get(), self.estatura.get())
          self.run_query(query, parametros)
          self.mensaje['text'] = 'El peso {} y la estatura {} se guardo correctamente'.format(self.peso.get(), self.estatura.get())
          self.peso.delete(0, END)
          self.estatura.delete(0, END)
      else:  
          self.mensaje['text'] = 'El peso y la estatura es requerido'       
      self.get_pesos()


if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()
