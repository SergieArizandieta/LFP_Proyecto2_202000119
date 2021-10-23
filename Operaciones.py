
Token = []
Errores = []

def Analisis_Lexico(texto):
    multilinea = False
    repetir = True
    estado = 0
    txtTemp = ""
    columna = 1
    fila = 1
    filamulti = 0
    columnamulti = 0
    simbolo = False;
    for txt in texto:
        repetir = True
        while repetir:
            if estado==0:
                if isLetra(txt):
                    estado = 1
                    txtTemp += txt
                    multilinea = False
                elif isNumero(txt):
                    estado = 4
                    txtTemp += txt
                    multilinea = False
                elif ord(txt) == 34: # "
                    simbolo = True
                    estado = 3
                    txtTemp += txt
                    multilinea = False
                elif isSimbolo(txt):
                    estado = 2
                    txtTemp += txt
                    multilinea = False
                elif ord(txt) == 35: # #
                    estado = 5
                    txtTemp += txt
                    multilinea = False
                elif ord(txt) == 39: # '
                    multilinea = True
                    txtTemp += txt
                    estado = 100
                    filamulti = fila
                    columnamulti = columna
                    
                else:

                    if ord(txt) == 32 or ord(txt) == 10 or ord(txt) == 9 or txt == '~':
                        pass
                    else: 
                        print("Error Lexico, se detecto " + txt + " en S0  F: " + str(fila) + ", C: " + str(columna))
                        errortipo= 'Caracter inesperado, esperaba L|D|#|S|"|@' 
            
            elif estado == 1:
                if (isLetra(txt)):
                    txtTemp += txt

                elif (ord(txt) == 95 ): # _
                    txtTemp += txt

                elif (isNumero(txt)):
                    txtTemp +=   txt

                else:
                    guardarToken("Identificador",fila,columna - len(txtTemp),txtTemp)
                    print("se reconocio en S1: '" + txtTemp + "' F: " + str(fila) + ", C: " + str(columna - len(txtTemp)))
                    txtTemp = ""
                    estado = 0
                    continue
           
            elif estado ==2:
                if multilinea == False:
                    if simbolo:
                        simbolo = False
                        guardarToken("Simbolo",fila,columna - len(txtTemp),txtTemp)
                    print("se reconocio en S2: '" + txtTemp + "' F: " + str(fila) + ", C: " + str(columna - len(txtTemp)))
                else:
                    print("se reconocio en S2: '" + txtTemp + "' F: " + str(filamulti) + ", C: " + str(columnamulti))
                txtTemp = ""
                estado = 0
                continue

            elif estado ==3:
                if ord(txt) != 34: # "
                    txtTemp += txt
                else:
                    txtTemp += txt
                    estado = 2         
                
            elif estado ==4:
                if isNumero(txt):
                    txtTemp += txt

                elif (ord(txt) == 46 ): # .
                    txtTemp += txt
                    estado = 7
                else:
                    guardarToken("Digito",fila,columna - len(txtTemp),columnamulti)
                    print("Se reconocio en S4: '" + txtTemp + "' F: " + str(fila) + ", C: " + str(columna - len(txtTemp)))
                    txtTemp = ""
                    estado = 0
                    continue

            elif estado ==5:
                if ord(txt) != 10: # "
                    txtTemp += txt
                else:
                    estado = 2 
                    continue 
            
            elif estado ==6:
                if ord(txt) != 39: # '
                    txtTemp += txt   
                else:
                    txtTemp += txt 
                    estado = 200
                     
            elif estado ==7:

                if isNumero(txt):
                    txtTemp += txt
                    estado = 8

            elif estado ==8:
                if isNumero(txt):
                    txtTemp += txt
                else:
                    guardarToken("Digito",fila,columna - len(txtTemp),columnamulti)
                    print("Se reconocio en S4: '" + txtTemp + "' F: " + str(fila) + ", C: " + str(columna - len(txtTemp)))
                    txtTemp = ""
                    estado = 0
                    continue        

            elif estado == 100:
                if ord(txt) == 39: # '
                    txtTemp += txt
                    estado = 101
           
            elif estado == 101:
                if ord(txt) == 39: # '
                    txtTemp += txt
                    estado = 6
         
            elif estado == 200:
                if ord(txt) == 39: # '
                    txtTemp += txt
                    estado = 201
           
            elif estado == 201:
                if ord(txt) == 39: # '
                    txtTemp += txt
                    estado = 2

            # Salto de Linea
            if (ord(txt) == 10):
                columna = 1
                fila += 1
                repetir = False
                continue
            # Tab Horizontal
            elif (ord(txt) == 9):
                columna += 4
                repetir = False
                continue
            # Espacio
            elif (ord(txt) == 32):
                columna += 1
                repetir = False
                continue
            repetir = False
            columna += 1               

    global Token
    print(Token)
    #for tet in Token:
      #  print(tet)
    

def Analisis_Sintactico():
    pass 


def guardarError():
    pass

def guardarToken(tipo,fila,columna,temp):
    texttemp = []
    texttemp.append(tipo)
    texttemp.append(fila)
    texttemp.append(columna)
    texttemp.append(temp)
    global Token
    Token.append(texttemp)


def isLetra(txt):
    if((ord(txt) >= 65 and ord(txt) <= 90) or (ord(txt) >= 97 and ord(txt) <= 122) or ord(txt) == 164 or ord(txt) == 165):
        return True
    else:
        return False

def isSimbolo(txt):
    #           =                    ;              {                   }                   [               ]                   ,               (                   )
    if(ord(txt) == 61 or ord(txt) == 59 or ord(txt) == 123 or ord(txt) == 125  or ord(txt) == 91 or ord(txt) == 93 or ord(txt) == 44 or ord(txt) == 40 or ord(txt) == 41):
        return True
    else:
        return False

def isNumero(txt):
    if ((ord(txt) >= 48 and ord(txt) <= 57)):
        return True
    else:
        return False
