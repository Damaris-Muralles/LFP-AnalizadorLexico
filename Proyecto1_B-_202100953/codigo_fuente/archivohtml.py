import webbrowser

def constructorHTML(listaresultado,listaapariencia,titulop,descrip, archivo):
    print("imprimiendo archivo html")
    #print(listaresultado[1])
    if archivo=="R":
        titulopag="RESULTADOS"
    else:
        titulopag="ERRORES"

    file =open(f"{titulopag}"+"_202100953.html","w",encoding= "utf-8")
    contenido ="<!doctype html>\n" \
            "<html lang=\"es\">\n" \
            "\n" \
            "<head>\n" \
            "\n" \
            "  <meta charset=\"UTF-8\">\n" \
            "  <title> REPORTE DE "+f"{titulopag}"+"</title>\n" \
            "  <link rel=\"shortcut icon\" type=\"image/x-icon\" href=\"src/imagenes/icono1.jpg\" >\n" \
            "  <style>\n" \
            "    * {\n" \
            "      margin: 0;\n" \
            "      padding: 0;\n" \
            "      box-sizing: border-box;\n" \
            "      }\n" \
            "\n" \
            "      body{\n" \
            "      font-family: Arial;\n" \
            "      color:"+f"{listaapariencia[4]}" +";\n"\
            "      font-size: "+f"{listaapariencia[5]}" +"px;\n" \
            "      background: #f2f2f2;\n" \
            "      }\n" \
            "\n" \
            "      .contenedor{\n" \
            "      padding: 60px 0;\n" \
            "      width: 95%\n" \
            "      max-width: 1000px\n" \
            "      margin: auto;\n" \
            "      overflow: hidden;\n" \
            "      }    \n" \
            "\n" \
            "      .titulo{\n" \
            "      color: "+f"{listaapariencia[0]}" +";\n" \
            "      font-size: "+f"{listaapariencia[1]}" +"px;\n" \
            "      text-align: center;\n" \
            "      margin-bottom: 50px;\n" \
            "      } \n" \
            "      .descripcion{\n" \
            "      color: "+f"{listaapariencia[2]}" +";\n" \
            "      font-size: "+f"{listaapariencia[3]}" +"px;\n" \
            "      text-align: justify;\n" \
            "      margin-left: 50px;\n" \
            "      margin-right: 50px;\n"\
            "      } \n" \
            "      .contenidotxt{\n"\
            "       color: "+f"{listaapariencia[4]}" +";\n"\
            "       font-size: "+f"{listaapariencia[5]}" +"px;\n"\
            "       text-align: left;\n"\
            "       margin-top: 30px;\n"\
            "       margin-left: 50px;\n"\
            "       margin-right: 50px;\n"\
            "       }\n"\
            "  \n" \
            "      header{\n" \
            "      width:100%;\n" \
            "      height: 250px;\n" \
            "      background: rgb(0,153,210);\n"\
            "      background: linear-gradient(90deg, rgba(0,153,210,1) 7%, rgba(65,54,88,1) 53%);\n"\
            "      background-size: cover;\n" \
            "      background-attachment: fixed;\n" \
            "      position: relative;\n" \
            "      }  \n" \
            "     \n" \
            "      header .textos-header{\n" \
            "      display: flex;\n" \
            "      height: 430px;\n" \
            "      width: 100%;\n" \
            "      align-items: center;\n" \
            "      flex-direction: column;\n" \
            "      text-align: center;\n" \
            "      }\n" \
            "      \n" \
            "      .textos-header h1 {\n" \
            "         font-size: 50px;\n" \
            "         color: WHITE;\n" \
            "      }\n" \
            "\n" \
            "      .textos-header h2 {\n" \
            "         font-size: 30px;\n" \
            "         font-weight:300;\n" \
            "         color:WHITE;\n" \
            "      }\n" \
            "\n" \
            "      .wave{\n" \
            "      position: absolute;\n" \
            "      bottom: 0;\n" \
            "      width: 100%;\n" \
            "      }\n" \
            "\n" \
            "      #main-container{\n" \
            "      margin:60px auto;\n" \
            "      width:900px;\n" \
            "      } \n" \
            "\n" \
            "  </style>\n" \
            "\n" \
            "</head>\n" \
            "\n" \
            "<body> \n" \
            "\n" \
            " <header>\n" \
            "    <section class=\"textos-header\">\n" \
            "       <br>\n" \
            "       <br>\n" \
            "       <h1>"+f"{titulopag}"+"</h1>\n" \
            "       <h2> Analizador </h2>\n" \
            "       <div class=\"wave\" style=\"height: 150px; overflow: hidden;\" ><svg viewBox=\"0 0 500 150\" preserveAspectRatio=\"none\" style=\"height: 100%; width: 100%;\"><path            d=\"M-11.00,130.77 C207.38,132.73 264.95,80.44 499.15,126.81 L500.00,150.00 L0.00,150.00 Z\" style=\"stroke: none; fill: #f2f2f2;\"></path></svg></div>\n" \
            "    </section>\n" \
            "  </header>\n" \
            "<br>\n" \
            "  <main>\n" \
            "    <section>\n" \
            "      <div class=\"contenedor pagina\">\n" 
    if  archivo=="R":

        contenido+="           <h2 class=\"titulo\">"+f"{titulop}"+"</h2>\n" \
            "        <div class=\"curso\" id=\"main-container-descrip\">\n"\
            "           <h3 class=\"descripcion\">"+f"{descrip}" +"</h3>\n"
        for i in range(len(listaresultado)):
            resu=listaresultado[i]
            if i ==0 :
                contenido+="           <pre class=\"contenidotxt\">"+f"Operacion {i+1}: {resu['op']}" +"\n"\
                "      "+f"{resu['proceso']}={resu['res']}"+"\n"
            else:
                contenido=contenido+""+f"Operacion {i+1}: {resu['op']}" +"\n"\
                "      "+f"{resu['proceso']}={resu['res']}"+"\n"    

        contenido+="           </pre>\n"
    else:
        contenido+="            <p style=\"text-align:center;\">\n"\
            "                     <img src=\"errores.png\">\n"\
            "                   </p>\n"   
    contenido+="        </div>\n"\
            "       </div>\n"\
            "    </section>\n" \
            "  </main>\n" \
            "\n" \
            "</body>\n" \
            "\n" \
            "</html>"
    #"+f"{listaapariencia[1]}" +"
    file.write(contenido)
    file.close()
    webbrowser.open_new_tab(f"{titulopag}"+"_202100953.html")