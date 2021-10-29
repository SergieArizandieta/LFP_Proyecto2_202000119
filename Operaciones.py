import easygui
import copy
from fpdf import FPDF
from tabla import tablas

Token = []
Errores = []
pila = []
Claves = []
cantidad_claves = 0
cantidad_registro =0 
Registros = []
AllData = []
textConsola = ""

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
    #print(len(Errores))
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
    global textConsola
    if len(Errores) >0 :
        popupmsg("Hubieron errores en la lectura de caracteres, se omitieron dichos caracteres","Errores")
        print(Errores)
    else:
        inicio_gramar() 
        print(textConsola) 


#gramatica-------------------------------------------------------   
def inicio_gramar():
    global Registros
    global Claves
    Registros[:] = []
    Claves[:] = []

    claves_gramar()
    registros_gramar()
    registrar_alldata()
    intrucciones_gramar()

llenarclaves = True
def claves_gramar():
    global pila
    global llenarclaves
    llenarclaves = True

    if pila[0][0] == "tk_key":
        pila.pop(0) 
        #print(pila) 
        #print("")
    else:
        llenarclaves = False
        ErrrorSintactico("tk_key, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    if llenarclaves:
        if pila[0][0] == "tk_igual":
            pila.pop(0)
            #print(pila) 
            #print("")
        else:
            ErrrorSintactico("tk_igual, se remplazo el token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)

        if pila[0][0] == "tk_CA":
            pila.pop(0)
            #print(pila) 
            #print("")
        else:
            ErrrorSintactico("tk_CA, se remplazo el token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)
    
    
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
           
            ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)
            continue

        if pila[0][0] != "Registro" and pila[0][0] != "tk_CC" and pila[0][0] != "tk_Coma":
            ErrrorSintactico("tk_Coma|tk_CC|Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)
            break
        
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
            ErrrorSintactico("tk_Coma, se rempazo token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)
            continue

llenarregistro = True
def registros_gramar():
    global pila
    global Registros
    global Claves
    global cantidad_registro
    cantidad_registro = 0
    global llenarregistro
    llenarregistro = True
    

    if pila[0][0] == "tk_logs":
        pila.pop(0) 
        #print(pila) 
        #print("")
    else:
        llenarregistro = False
        ErrrorSintactico("tk_logs, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
    if llenarregistro:
        if pila[0][0] == "tk_igual":
            pila.pop(0)
            #print(pila) 
            #print("")
        else:
            ErrrorSintactico("tk_igual, se remplzo token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)

        if pila[0][0] == "tk_CA":
            pila.pop(0)
            #print(pila) 
            #print("")
        else:
            ErrrorSintactico("tk_CA, se remplzo token",pila[0][1] ,pila[0][2] ,pila[0][0])
            pila.pop(0)

        
        AsignacionR_gramar()

        if malosRegistro:
            Registros = []

        
        registrosTempP = []
        
        for x in Registros:
            registrosTemp = []
            for i in range(0,len(Claves)):
                try:
                    registrosTemp.append(x[i])
                except Exception:
                    registrosTemp.append('')
    
            registrosTempP.append(registrosTemp)

        print(registrosTempP)

        Registros = copy.deepcopy(registrosTempP)
        for x in Registros:
            cantidad_registro += len(x)

malosRegistro = False     
def AsignacionR_gramar():
    global pila
    global Registros
    global malosRegistro 
    guaradar = True
    resguardar = False


    while(True):
        if guaradar:
            if pila[0][0] == "tk_LA" or pila[0][0] == "tk_CC":   
                if pila[0][0] == "tk_CC":
                    pila.pop(0)
                    break
                if pila[0][0] == "tk_LA":
                    registrosTemp = []
                    resguardar = True
                
                guaradar = False
                pila.pop(0)
                #print(pila) 
                #print("")
            else:
               
                ErrrorSintactico("tk_LA|tk_CC, se omition token",pila[0][1] ,pila[0][2] ,pila[0][0])
                pila.pop(0)
                continue
        

        if pila[0][0] == "Digito" or pila[0][0] == "Registro":
            if resguardar:
                resguardar
                registrosTemp.append(pila[0][3])
                pila.pop(0)
                #print(pila) 
                #print("")
            
        else:
            ErrrorSintactico("Digito | Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
           
            malosRegistro = True

        if pila[0][0] == "tk_LC" or  pila[0][0] == "tk_Coma":
            if pila[0][0] == "tk_LC":
                guaradar = True 
                Registros.append(registrosTemp)
            pila.pop(0)
            #print(pila) 
            #print("")

        else:
            ErrrorSintactico("tk_LC | tk_Coma, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
            malosRegistro = True

        if pila[0][0] != "tk_LA" and pila[0][0] != "Digito"   and pila[0][0] != "Registro" and pila[0][0] != "tk_CC" and pila[0][0] != "tk_LC" and pila[0][0] != "tk_Coma":
            ErrrorSintactico("tk_Coma|tk_CC|Registro",pila[0][1] ,pila[0][2] ,pila[0][0])
            malosRegistro = True
            pila.pop(0)
            break  

def registrar_alldata():
    global Registros
    global Claves
    global AllData
    global cantidad_claves
    AllData[:] = []

    #print(cantidad_claves)
    #print("")
    print(Claves)
    print("")
    print(Registros)
    print("")

  

    for i in range(0,cantidad_claves):
        temp= []
        temp.append(Claves[i])
        
        for k in Registros:
            temp.append(k[i])
        AllData.append(temp)

    print(AllData)
    print("")

def  intrucciones_gramar():
    global textConsola
    textConsola = ""

    #validar = true
    while(True):
        try:
            if pila[0][0] == "tk_print":
                pila.pop(0)
                imprimir_gramar()
                
            elif pila[0][0] == "tk_println":
                pila.pop(0)
                imprimirln_gramar()
                
            elif pila[0][0] == "tk_count":
                pila.pop(0)
                conteo_gramar()
                
            elif pila[0][0] == "tk_avg":
                pila.pop(0)
                promedio_gramar()
                         
            elif pila[0][0] == "tk_contif":
                pila.pop(0)
                contarsi_gramar()
                
            elif pila[0][0] == "tk_suma":
                pila.pop(0)
                sumar_gramar()
                
            elif pila[0][0] == "tk_dat":
                pila.pop(0)
                datos_gramar()
                

            elif pila[0][0] == "tk_max":
                pila.pop(0)
                max_gramar()
                
            elif pila[0][0] == "tk_min":
                pila.pop(0)
                min_gramar()
                
            elif pila[0][0] == "tk_export":
                pila.pop(0)
                expReport_gramar()
                break
            else:
                print("Error")
                #print(pila) 
                print("")
                #print(textConsola) 
                print("")
                ErrrorSintactico("intruccion, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
                pila.pop(0)
                
        except Exception:
            print("no hya mas datos")
            #print(textConsola) 
            #print("Error, main")
            break

def imprimir_gramar():
    global textConsola
    global pila

    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola +=   pila[0][3].replace('"',"") 
        pila.pop(0) 
    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)
        

    validar_PC_gramar()

    validar_ptocoma_gramar()

def imprimirln_gramar():
    global textConsola
    global pila

    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola +=  "\n"+  pila[0][3].replace('"',"") 
        pila.pop(0) 
    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    validar_PC_gramar()

    validar_ptocoma_gramar()
    
def conteo_gramar():
    global textConsola
    global pila
    global cantidad_registro


    validar_PA_gramar()

    validar_PC_gramar()

    validar_ptocoma_gramar()

    textConsola += "\n" + str(cantidad_registro)

def promedio_gramar():
    global textConsola
    global pila

    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola += "\n" + str(hacer_promedio(pila[0][3]))
        pila.pop(0) 

    else:
         
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    validar_PC_gramar()

    validar_ptocoma_gramar()

import pandas as pd

def hacer_promedio(data):
    global AllData
    prom = 0
    contador = 0
    for i in AllData:
        if i[0] == data:
            for x in i:
                if is_integer(x):
                    contador += 1
                    prom += float(x)
                else:
                    if x != data:
                        return "No todos los registros son numericos" 
            promedio = prom / contador
            return promedio
    return "No se encontro registro "     

def contarsi_gramar():
    global textConsola
    global pila
    registro= ""
    validar_PA_gramar()

    if pila[0][0] == "Registro":
        registro = pila[0][3]
        pila.pop(0) 

    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    if pila[0][0] == "tk_Coma":
        pila.pop(0) 
    else:
        ErrrorSintactico("tk_Coma",pila[0][1] ,pila[0][2] ,pila[0][0])

    if pila[0][0] == "Digito" or  pila[0][0] == "Registro":
        valor = pila[0][3]
        textConsola += "\n" + str(hacer_conteo(registro,valor))
        pila.pop(0) 

    else:
        ErrrorSintactico("Registro | Digito, se omitio ttoken",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0) 

    validar_PC_gramar()

    validar_ptocoma_gramar()

def hacer_conteo(data,valor):
    global AllData
    contador = 0
    for i in AllData:
        if i[0] == data:
            for x in i:
                if valor == x:
                    contador += 1
            return contador
    return "No se encontro registro"     

def sumar_gramar():
    global textConsola
    global pila

    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola += "\n" + str(hacer_suma(pila[0][3]))
        pila.pop(0) 

    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    validar_PC_gramar()

    validar_ptocoma_gramar()
  
def hacer_suma(data):
    global AllData
    suma = 0
    for i in AllData:
        if i[0] == data:
            for x in i:
                if is_integer(x):
                    suma += float(x)
                else:
                    if x != data:
                        return "No todos los registros son numericos"
            return suma
    return "No se encontro registro"     

def datos_gramar():
    global AllData
    global Claves
    global Registros
    global textConsola
    
    validar_PA_gramar()
    
    textConsolas = textConsola
    textConsolas += "\n"
    for i in Claves:
        textConsolas += i.replace('"',"")  + "\t"
  


    for x in Registros:
        textConsolas += "\n"
        for i in range (0,len(x)):
            if is_integer( x[i]):
                textConsolas += str(x[i].replace('"',"")) +  "\t"
            else:
                textConsolas += x[i].replace('"',"")  + "\t"
    
    
    data = []
    
    for x in Registros:
        temp = []
        for i in x:
            if is_integer(i):
                temp.append(str(i))
            else:
                temp.append(i.replace('"',""))
           
        data.append(temp)
   
    keys = []
    for x in Claves:
        keys.append(x.replace('"',""))

    
    if data != None  and keys != None:
        df = pd.DataFrame(data, columns = keys)
        textConsola += "\n" + str(df) + "\n"
    else:
        textConsola += "\n" + str("No data") + "\n"

       
    validar_PC_gramar()
    validar_ptocoma_gramar()

def max_gramar():
    global textConsola
    global pila
    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola += "\n" + str(hacer_max(pila[0][3]))
        pila.pop(0) 

    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    validar_PC_gramar()

    validar_ptocoma_gramar()

def hacer_max(dato):
    global AllData
    mayor = 0
    for i in AllData:
        if i[0] == dato:
            for x in i:
   
                if is_integer(x):
                    if mayor<float(x):
                        mayor = float(x)
                else:
                    if x != dato:
                        return "No todos los registros son numericos" 
            return mayor
    return "No se encontro registro" 

def min_gramar():
    global textConsola
    global pila
    validar_PA_gramar()

    if pila[0][0] == "Registro":
        textConsola += "\n" + str(hacer_min(pila[0][3]))
        pila.pop(0) 

    else:
        
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

    validar_PC_gramar()

    validar_ptocoma_gramar()

def hacer_min(dato):
    global AllData
    menor = 99999999999999999999999
    for i in AllData:
        if i[0] == dato:
            for x in i:
   
                if is_integer(x):
                    if menor>float(x):
                        menor = float(x)
                else:
                    if x != dato:
                        return "No todos los registros son numericos" 
            return menor
    return "No se encontro registro" 

import webbrowser

def expReport_gramar():
    global Claves
    global Registros
    global textConsola
    data = []
    validar_PA_gramar()
    if pila[0][0] == "Registro":
        temp = []
        temp.append(pila[0][3].replace('"',""))
        data.append(temp)
        datatemp = []

        for x in Registros:
            temporal = []
            for i in x:
                if is_integer(i):
                    temporal.append(str(i))
                else:
                    temporal.append(i.replace('"',""))
            
            datatemp.append(temporal)
       
        keys = []
        for x in Claves:
            keys.append(x.replace('"',""))
        data.append(keys)
        for x in datatemp:
            data.append(x) 
        textConsola += "\n" + "Se genero la exportacion del Reporte"
        path = 'ExporteReporte.pdf'
        
        tablas(data,'ExporteReporte.pdf')
        webbrowser.open_new(path)
        pila.pop(0) 

    else:
        ErrrorSintactico("Registro, se omitio token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)


    validar_PC_gramar()
    validar_ptocoma_gramar()

    
    #print(pila) 
    print("")
    #print(textConsola) 
    print("")

def validar_ptocoma_gramar():
    global pila
    if pila[0][0] == "tk_PtoComa":
        pila.pop(0) 
    else:
        ErrrorSintactico("tk_PtoComa, se remplazo el token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0) 

def validar_PA_gramar():
    global pila
    if pila[0][0] == "tk_PA":
        pila.pop(0) 
    else:
        ErrrorSintactico("tk_PA, se remplazo el token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)

def validar_PC_gramar():
    global pila
    if pila[0][0] == "tk_PC":
        pila.pop(0) 
    else:
        ErrrorSintactico("tk_PC, se remplazo el token",pila[0][1] ,pila[0][2] ,pila[0][0])
        pila.pop(0)
#temina gramatica-------------------------------------------------------          

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
    PalabrasReservadas = [["Claves","tk_key"],["Registros","tk_logs"],["imprimir","tk_print"],["imprimirln","tk_println"],["conteo","tk_count"],["promedio","tk_avg"],["contarsi","tk_contif"],["datos","tk_dat"],["max","tk_max"],["min","tk_min"],["exportarReporte","tk_export"],["sumar","tk_suma"]]
    SimbolosReservadas = [["=","tk_igual"],[";","tk_PtoComa"],["{","tk_LA"],["}","tk_LC"],["[","tk_CA"],["]","tk_CC"],[",","tk_Coma"],["(","tk_PA"],[")","tk_PC"]]                                                                    
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

#numero entero
def is_integer(string):
    try: 
        float(string)
        return True
    except ValueError:
        return False
        