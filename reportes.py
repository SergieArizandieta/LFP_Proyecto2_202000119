
import Operaciones


ReportTokens = ""
ReportErrores = ""

#Contruye el reporte para ascendentes
def ReporteTokens():
    global ReportTokens
    ReportTokens=""
    num = 0
    #print(Operaciones.Tokens)
    ReportTokens+='<table class="steelBlueCols"><thead> <tr> <th>no.</th>  <th>Token</th> <th>Lexema</th> <th>Fila</th>  <th>Columna</th> </tr></thead><tbody>\n<tr>'

    for Tokens in Operaciones.Token:
        
        num += 1
        ReportTokens += "<td>" + str(num) + "</td>"
        ReportTokens += "<td>" + str(Tokens[0]) + "</td>"
        ReportTokens += "<td>" + str(Tokens[1])  + "</td>"
        ReportTokens += "<td>" + str(Tokens[2]) + "</td>"
        ReportTokens += "<td>" + str(Tokens[3])  + "</td></tr>"
        #print(Tokens[0])
    
    ReportTokens += "</tbody></table><br>" 
    ReportTokens +="\n"
    GenerarReportesToken()

def ReporteTErrores():
    global ReportErrores
    ReportErrores=""
    #print(Operaciones.Errores)
    ReportErrores+='<table class="steelBlueCols"><thead><tr> <th>no.</th>  <th>Contenido</th> <th>................................................Mensaje................................................</th> <th>Fila</th>  <th>Columna</th> </tr></thead><tbody>\n<tr>'
    num = 0
    for Errores in Operaciones.Errores:
        num += 1
        ReportErrores += "<td>" + str(num) + "</td>"
        ReportErrores += "<td>" + str(Errores[0]) + "</td>"
        ReportErrores += "<td>" + str(Errores[1])  + "</td>"
        ReportErrores += "<td>" + str(Errores[2]) + "</td>"
        ReportErrores += "<td>" + str(Errores[3])  + "</td></tr>"
        #print(Errores)
    
    ReportErrores += "</tbody></table><br>" 
    ReportErrores +="\n"
    GenerarReportesErrores()

#Contruye el reporte final  
def ReportesSolicitadosTokens():
    
    htmlcompleto = htmlInicial + ReportTokens + htmlFinal
    return htmlcompleto

def ReportesSolicitadosErrores():
    
    htmlcompleto = htmlInicial + ReportErrores + htmlFinal
    return htmlcompleto
import webbrowser
#Genera el Reporte

def GenerarReportesToken():
    try: 
        
        FileHTML=open("./Tokens.HTML","w") 
        FileHTML.write(ReportesSolicitadosTokens()) 
        FileHTML.close() 
        path = 'Tokens.HTML'
        webbrowser.open_new(path)
        #webbrowser.open("C:/Users/sergi/3D Objects/GitHub/LFP_Proyecto1_202000119/Reportes")
      

    except:
        print("La creación del Reporte falló")
    else:
         print("Se ha creado el Reporte Token" )

def GenerarReportesErrores():
    try: 
        

        FileHTML=open("./Errores.HTML","w") 
        FileHTML.write(ReportesSolicitadosErrores()) 
        FileHTML.close()
        path = 'Errores.HTML'
        webbrowser.open_new(path)
    except:
        print("La creación del Reporte falló")
    else:
         print("Se ha creado el Reporte Errores" )
htmlContenido = ""

htmlInicial = """<!DOCTYPE html>
<html>

<!--Encabezado-->
<head>
<meta charset="UTF-8">
<meta name="name" content="Reporte">
<meta name="description" content="name">
<meta name="keywods" content="python,dos,tres">
<meta name="robots" content="Index, Follow">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="css/styles.css"/>
<title>Reporte</title>
</head>
<!----Curerpo--->
<body>
   <center><h6 class=\"titulos\" ><b> Reportes </b></h6>"""

htmlFinal = """<br><footer style="background-color:white;">Creado por: Sergie Daniel Arizandieta Yol - 202000119</footer>
</center></body>
</html>"""

htmlcompleto = ""


css = """body{
background-image: url(https://fondosmil.com/fondo/9859.jpg);
background-attachment:fixed;
background-repeat:no-repeat;
background-size:cover;
background-position: center center;
background-color:white;}	
table.steelBlueCols {
  border: 4px solid #555555;
  background-color: #555555;
  width: 400px;
  text-align: center;
  border-collapse: collapse;
}
table.steelBlueCols td, table.steelBlueCols th {
  border: 1px solid #000000;
  padding: 5px 10px;
}
table.steelBlueCols tbody td {
  font-size: 20px;
  font-weight: bold;
  color: #FFFFFF;
}
table.steelBlueCols td:nth-child(even) {
  background: #398AA4;
}
table.steelBlueCols thead {
  background: #1693A4;
  background: -moz-linear-gradient(top, #50aebb 0%, #2d9dad 66%, #1693A4 100%);
  background: -webkit-linear-gradient(top, #50aebb 0%, #2d9dad 66%, #1693A4 100%);
  background: linear-gradient(to bottom, #50aebb 0%, #2d9dad 66%, #1693A4 100%);
}
table.steelBlueCols thead th {
  font-size: 15px;
  font-weight: bold;
  color: #FFFFFF;
  text-align: center;
  border-left: 2px solid #398AA4;
}
table.steelBlueCols thead th:first-child {
  border-left: none;
}
table.steelBlueCols tfoot td {
  font-size: 13px;
}
table.steelBlueCols tfoot .links {
  text-align: right;
}
table.steelBlueCols tfoot .links a{
  display: inline-block;
  background: #FFFFFF;
  color: #398AA4;
  padding: 2px 8px;
  border-radius: 5px;
}
/*Textos*/
.titulos{
color: white;
background:black;
width:40%;} 
.SUBtitulos{
color: black;
background:white;
text-align:center; 
width:80%;} 
.text{text-align:justify;
background-color:yellow;
color:black; }
.tipos{
	background-color:purple;
	color:white;	
}
h6{
  border: red 2px solid;
  margin: 20px;
font-weight: none;
 font-size:30px;
}
h2{
  border: white 2px solid;
  margin: 20px;
font-weight: none;
 font-size:50px;
}
div{
  background-color: #FFFFFF;
  }
"""