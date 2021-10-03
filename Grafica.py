
from tkinter import * 
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
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

        def OperarMasivo():
            consola.delete("1.0", END)
            print("Masivo")
            TextoEditor = txt.get("1.0", END)
            for text in TextoEditor:
                if  text=="\n":
                    pass
                else:
                    print(text)
            consola.insert("1.0", TextoEditor)
            

        #Ventana-----------------------------------------------------------------------------------
     
        #Encabezado--------------------------------------------------------------------------------
        Button(ventana,text="Salir",command= cerrar).place(x=1400, y =0)
        
        Label(ventana,text = "Proyecto 2 - 202000119",fg="Gray",font=("Popins",12)).place(x=10, y =25)
        Button(ventana,text="Abrir",command= OperarMasivo).place(x=1000, y =25)
        Button(ventana,text="Analizar",command= OperarMasivo).place(x=1050, y =25)
        Button(ventana,text="Reportes",command= OperarMasivo).place(x=1120, y =25)
        Label(ventana,text = linea,fg="Gray",font=("Popins",12)).place(x=15, y= 50)
        #Terminar Encabezado ------------------------------------------------------------------------------------
        #Cuerpo-----------------------------------------------------------------------------------
        Label(ventana,text = "Editor:",fg="Gray",font=("Popins",12)).place(x=50, y= 75)
        Label(ventana,text = "Consola:",fg="Gray",font=("Popins",12)).place(x=890, y= 80)

        txt = scrolledtext.ScrolledText(ventana, undo=True, width=70,height=34,bg = "#B8B8B8",fg= "#000000")
        txt['font'] = ('consolas', '12')
        txt.place(x=50, y= 115)

        consola = scrolledtext.ScrolledText(ventana, undo=True, width=60,height=34,bg = "#FFF5D4",fg= "#000000")
        consola['font'] = ('consolas', '12')
        consola.place(x=890, y= 115)

        ventana.mainloop() 
      
    except Exception:
       
        print("Error, v")

def destruir():
     print("Error, v")

