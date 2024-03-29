from tkinter import * 
from tkinter import ttk
from tkinter import filedialog, Tk
import tkinter.scrolledtext as scrolledtext
import Operaciones as op
from reportes import ReporteTokens, ReporteTErrores
Nombre = ""

opcion = ["No data"]
def ventanas():
    try:
        linea = "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
        global opcion
        
        ventana = Tk()
        ventana.title('Proyecto 1')
        ventana.geometry("1500x800")
        


        def cerrar():
            exit()

        def OptenerTextoArxhivo():
            Editor.delete("1.0", END)
            texto = AbrirArchivo()
            Editor.insert("1.0", texto)
            

        def mostrarConsola():
            consola.config(state="normal")
            consola.delete("1.0", END)
            #print("Masivo")
      
            print(op.textConsola) 
            if op.llenarclaves == False or op.llenarclaves == False:
                op.textConsola = "Hay errores sintacticos, resviasar reporte de Errores"
                
            
            consola.insert("1.0", op.textConsola)
            consola.config(state="disabled")

        def Analizar():
            TextoEditor = Editor.get("1.0", END)
            op.Analisis_Lexico(TextoEditor)
            mostrarConsola()
           
        def GeneraraRequerido():
            data = ComboReportes.get()
            if data == "Reporte Token":
                print("Reporte token")
                op.popupmsg("Se genero reporte Token","Reporte")
                ReporteTokens()  
        
            elif data ==  "Reporte Error":
                print("Reportye Errores")
                op.popupmsg("Se genero reporte Errores","Reporte")
                ReporteTErrores()
            elif data == "Arbol de derivacion":
                if op.llenarclaves == False or op.llenarclaves == False:
                    op.popupmsg("No se pudo genrar ya que hay errores sintacticos",'Error')
                else:
                    op.popupmsg("Se genero Arbol de derivacion","Reporte")
                    print("Arbol de derivacion")


        #Ventana-----------------------------------------------------------------------------------
     
        #Encabezado--------------------------------------------------------------------------------
        Button(ventana,text="Salir",command= cerrar).place(x=1400, y =0)
        
        Label(ventana,text = "Proyecto 2 - 202000119",fg="Gray",font=("Popins",12)).place(x=10, y =25)
        Button(ventana,text="Abrir",command= OptenerTextoArxhivo).place(x=1000, y =25)
        Button(ventana,text="Analizar",command= Analizar).place(x=1050, y =25)
        Button(ventana,text="Generar",command= GeneraraRequerido).place(x=1300, y =25)
        Label(ventana,text = linea,fg="Gray",font=("Popins",12)).place(x=15, y= 50)
        #Terminar Encabezado ------------------------------------------------------------------------------------
        ComboReportes =  ttk.Combobox(ventana, 
                            values=[
                                    "Reporte Token", 
                                    "Reporte Error",
                                    "Arbol de derivacion"],state="readonly")
        ComboReportes.place(x=1120, y= 25)  
        #ImagenesCombo.pack( pady=200,)
        ComboReportes.current()

       
        #Cuerpo-----------------------------------------------------------------------------------
        Label(ventana,text = "Editor:",fg="Gray",font=("Popins",12)).place(x=50, y= 75)
        Label(ventana,text = "Consola:",fg="Gray",font=("Popins",12)).place(x=890, y= 80)

        Editor = scrolledtext.ScrolledText(ventana, undo=True, width=70,height=34,bg = "#B8B8B8",fg= "#000000")
        Editor['font'] = ('consolas', '12')
        Editor.place(x=50, y= 115)

        consola = scrolledtext.ScrolledText(ventana, undo=True, width=60,height=34,bg = "#FFF5D4",fg= "#000000")
        consola.configure(state="disabled")
        consola['font'] = ('consolas', '12')
        consola.place(x=890, y= 115)

        ventana.mainloop() 
      
    except Exception:
       
        print("Error, v")


def AbrirArchivo():
    
  
        Tk().withdraw()

        archivo = filedialog.askopenfilename(
            
            title = "Seleccionar un archivo LFP",
            initialdir = "./",
            filetypes = (
                ("archivos pxla", "*.lfp"),
                ("todos los archivos",  "*.*")
            )
        )
        
        if archivo is None or archivo == "" or archivo == " ":
            print('\nNo se seleccionó ningun archivo')
            return None
        else:
            print(archivo, "dsa")
            texto = open(archivo, 'r',encoding="utf8" ).read()
            
            print('\n"Lectura exitosa"\n')
            texto += "~"
            return texto