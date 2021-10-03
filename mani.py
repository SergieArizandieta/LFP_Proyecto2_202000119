import Grafica 
import Operaciones as op
import Grafica as g

if __name__ == "__main__":
    
    try: 
       #Grafica.ventanas()
        op.ObtencionTokens(g.AbrirArchivo())

    except Exception:
        
        print("Error, main")
