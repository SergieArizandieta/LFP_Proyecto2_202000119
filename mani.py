import Grafica 
import Operaciones as op
import Grafica as g

if __name__ == "__main__":
    
    try: 
        Grafica.ventanas()
        #texto = open("C:/Users/sergi/3D Objects/GitHub/LFP_Proyecto2_202000119/Prueba.lfp", 'r',encoding="utf8" ).read()
       # texto = open("C:/Users/sergi/3D Objects/GitHub/LFP_Proyecto2_202000119/z/PruebaTemp.lfp", 'r',encoding="utf8" ).read()
        print('\n"Lectura exitosa"\n')
        #texto += "~" 
        #op.Analisis_Lexico(texto)

    except Exception:
        
        print("Error, main")
