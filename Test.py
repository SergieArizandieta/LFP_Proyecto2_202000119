class Humano:
    def __init__(self,edad,correlativo):
        self.edad = edad
        self.correlativo = correlativo

    def hablar(self,mensaje):
        print("soy un humano de:" , self.edad , " Y ",mensaje )

    def AcrualizarEdad(self,edad):
       self.edad = edad

if __name__ == "__main__":
    
    #try: 
        print("Intento")
        huma1= Humano(25,25)
        huma1.hablar("Hola")

        humno = []

        for i in range(0,10):
            humno.append(Humano(i,i))

        for i in humno:
            #print(i)
            #i.hablar(" Edad actual")
            print("Humano:",i.correlativo, "de edad",i.edad  )

        contador = 0
        print("\n")

        for i in humno:
            contador +=1
            i.AcrualizarEdad(100-contador)

        for i in humno:
            print("Humano:",i.correlativo, "de edad",i.edad  )

        print("\n")

        #Eliminiar correlativo 5    
        for i in humno:
            if i.correlativo == 5:
                humno.remove(i)
               
        for i in humno:
            print("Humano:",i.correlativo, "de edad",i.edad  )

        print("\n")
        #Arreglar correaltivos
        auxcontador = 0
        for i in humno:
            i.correlativo = auxcontador
            auxcontador += 1

        for i in humno:
            print("Humano:",i.correlativo, "de edad",i.edad  )

    #except Exception:
    #   pass
     
