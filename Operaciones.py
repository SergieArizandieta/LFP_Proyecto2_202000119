import easygui
import copy

Token = []
Errores = []
pila = []
Claves = []
cantidad_claves = 0
Registros = []
AllData = []

#analizador lexico  
def Analisis_Lexico(texto):
    global Token
    global Errores
    Token[:] = []
    Errores[:] = []

    print("Analisis Lexico")
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
                    
                    estado = 3
                    txtTemp += txt
                    multilinea = False
                elif isSimbolo(txt):
                    simbolo = True
                    estado = 2
                    txtTemp += txt
                    multilinea = False
                elif ord(txt) == 35: # #
                    estado = 5
                    txtTemp += txt
                    multilinea = True
                    filamulti = fila
                    columnamulti = columna
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
                        ErrorTemp= []
                        ErrorTemp.append(txt)
                        ErrorTemp.append("Error Lexico, caracter irreconocible")
                        ErrorTemp.append(fila)
                        ErrorTemp.append(columna)
                        Errores.append(ErrorTemp)
            
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
                    else:
                        guardarToken("Registro",fila,columna - len(txtTemp),txtTemp)
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
                    guardarToken("Digito",fila,columna - len(txtTemp),txtTemp)
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
                    guardarToken("Digito",fila,columna - len(txtTemp),txtTemp)
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
    print(len(Errores))
    redefinirTokens()
    Analisis_Sintactico()
    #for tet in Token:
      #  print(tet)

#analizador sintactico  
def Analisis_Sintactico():
    print("Analisis Sintactico")
    global Token
    global Errores
    global pila
    pila[:] = []
    pila = copy.deepcopy(Token)
    #print(Token)
    print("")
    #print(Errores) 
    print("")
    print(pila) 
    print("")

    if len(Errores) >0 :
        popupmsg("Hubieron errores en la lectura de caracteres, se omitieron dichos caracteres","Errores")

    inicio_gramar()   
    

def inicio_gramar():
    global Registros
    global Claves
    Registros[:] = []
    Claves[:] = []

    claves_gramar()
    registros_gramar()
    registrar_alldata()
    intrucciones_gramar()

def claves_gramar():
    global pila
 

    if pila[0][0] == "tk_key":
        pila.pop(0) 
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_key",pila[0][1] ,pila[0][2] ,pila[0][0])

    if pila[0][0] == "tk_igual":
        pila.pop(0)
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_igual",pila[0][1] ,pila[0][2] ,pila[0][0])

    if pila[0][0] == "tk_CA":
        pila.pop(0)
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_CA",pila[0][1] ,pila[0][2] ,pila[0][0])
   
    AsignacionC_gramar()

    global cantidad_claves
    cantidad_claves = len(Claves)

def AsignacionC_gramar():
    global pila
    global Claves
    while(True):

        if pila[0][0] == "Registro":
            Claves.append(pila[0][3])
            pila.pop(0)
            #print(pila) 
            #print("")
            
        else:
            ErrrorSintactico("Registro",pila[0][1] ,pila[0][2] ,pila[0][0])
        
        if pila[0][0] == "tk_CC":
            pila.pop(0)
            #print(pila) 
            #print("")
            break
        
        if pila[0][0] == "tk_Coma":
            pila.pop(0)
            #print(pila) 
            #print("")
        else:
            ErrrorSintactico("tk_Coma",pila[0][1] ,pila[0][2] ,pila[0][0])

        if pila[0][0] != "Registro" and pila[0][0] != "tk_CC" and pila[0][0] != "tk_Coma":
            ErrrorSintactico("tk_Coma|tk_CC|Registro",pila[0][1] ,pila[0][2] ,pila[0][0])
            break

def registros_gramar():
    global pila
    global Registros

    if pila[0][0] == "tk_logs":
        pila.pop(0) 
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_logs",pila[0][1] ,pila[0][2] ,pila[0][0])

    if pila[0][0] == "tk_igual":
        pila.pop(0)
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_igual",pila[0][1] ,pila[0][2] ,pila[0][0])

    if pila[0][0] == "tk_CA":
        pila.pop(0)
        #print(pila) 
        #print("")
    else:
        ErrrorSintactico("tk_CA",pila[0][1] ,pila[0][2] ,pila[0][0])

    AsignacionR_gramar()
                  
def AsignacionR_gramar():
    global pila
    global Registros
    guaradar = True
    
    while(True):
        if guaradar:
            if pila[0][0] == "tk_LA" or pila[0][0] == "tk_CC":   
                if pila[0][0] == "tk_CC":
                    pila.pop(0)
                    break
                if pila[0][0] == "tk_LA":
                    registrosTemp = []
                guaradar = False
                pila.pop(0)
                #print(pila) 
                #print("")
            else:
                ErrrorSintactico("tk_LA",pila[0][1] ,pila[0][2] ,pila[0][0])
        

        if pila[0][0] == "Digito" or pila[0][0] == "Registro":
            registrosTemp.append(pila[0][3])
            pila.pop(0)
            #print(pila) 
            #print("")
            
        else:
            ErrrorSintactico("Digito | Registro",pila[0][1] ,pila[0][2] ,pila[0][0])

        if pila[0][0] == "tk_LC" or  pila[0][0] == "tk_Coma":
            if pila[0][0] == "tk_LC":
                guaradar = True
                Registros.append(registrosTemp)
            pila.pop(0)
            #print(pila) 
            #print("")

        else:
            ErrrorSintactico("tk_LC | tk_Coma",pila[0][1] ,pila[0][2] ,pila[0][0])


        if pila[0][0] != "tk_LA" and pila[0][0] != "Digito"   and pila[0][0] != "Registro" and pila[0][0] != "tk_CC" and pila[0][0] != "tk_LC" and pila[0][0] != "tk_Coma":
            ErrrorSintactico("tk_Coma|tk_CC|Registro",pila[0][1] ,pila[0][2] ,pila[0][0])
            break  

def registrar_alldata():
    global Registros
    global Claves
    global AllData
    global cantidad_claves
    AllData[:] = []

    #print(cantidad_claves)
    #print("")
    print(Registros)
    print("")

    print(Claves)
    print("")

    for i in range(0,cantidad_claves):
        AllData.append(Claves[i])
        for k in Registros:
            AllData.append(k[i])

    print(AllData)
    print("")

def  intrucciones_gramar():
    global pila
    print(pila) 
    print("")

def imprimir_gramar():
    pass
def imprimirln_gramar():
    pass
def conteo_gramar():
    pass
def promedio_gramar():
    pass
def contarsi_gramar():
    pass
def datos_gramar():
    pass
def max_gramar():
    pass
def min_gramar():
    pass
def expReport_gramar():
    pass

#error sintactico
def ErrrorSintactico(tipo,fila,columna,data):
    global Errores
    ErrorTemp= []
    ErrorTemp.append(data)
    ErrorTemp.append(("Error sintactico, se esperaba token: " + tipo))

    ErrorTemp.append(fila)
    ErrorTemp.append(columna)
    Errores.append(ErrorTemp)
    print( Errores)
    
#dar nombres a los tokensa reservados
def redefinirTokens():
    PalabrasReservadas = [["Claves","tk_key"],["Registros","tk_logs"],["imprimir","tk_print"],["imprimirln","tk_println"],["conteo","tk_count"],["promedio","tk_avg"],["contarsi","tk_contif"],["datos","tk_dat"],["max","tk_max"],["min","tk_min"],["exportarReporte","tk_export"]]
    SimbolosReservadas = [["=","tk_igual"],[";","tk_PtoComa"],["{","tk_LA"],["}","tk_LC"],["[","tk_CA"],["]","tk_CC"],[",","tk_Coma"],["(","tk_PA"],[")","PC"]]                                                                    
    global Token
    for tk in Token:
        txtTemp = str(tk[3])
        for reservadas in PalabrasReservadas:
            if txtTemp.__eq__(reservadas[0]):
                tk[0] = reservadas[1]
                break 
        for reservadas in SimbolosReservadas:
            if txtTemp.__eq__(reservadas[0]):
                tk[0] = reservadas[1]
                break 
    
#mensaje emegente   
def popupmsg(msg, title):
    easygui.msgbox(msg, title=title)

#Guaradar mi token 
def guardarToken(tipo,fila,columna,temp):
    texttemp = []
    texttemp.append(tipo)
    texttemp.append(fila)
    texttemp.append(columna)
    texttemp.append(temp)
    global Token
    Token.append(texttemp)

#si es letra  
def isLetra(txt):
    if((ord(txt) >= 65 and ord(txt) <= 90) or (ord(txt) >= 97 and ord(txt) <= 122) or ord(txt) == 164 or ord(txt) == 165):
        return True
    else:
        return False

#si es simbolo  
def isSimbolo(txt):
    #           =                    ;              {                   }                   [               ]                   ,               (                   )
    if(ord(txt) == 61 or ord(txt) == 59 or ord(txt) == 123 or ord(txt) == 125  or ord(txt) == 91 or ord(txt) == 93 or ord(txt) == 44 or ord(txt) == 40 or ord(txt) == 41):
        return True
    else:
        return False

#si es numero  
def isNumero(txt):
    if ((ord(txt) >= 48 and ord(txt) <= 57)):
        return True
    else:
        return False
