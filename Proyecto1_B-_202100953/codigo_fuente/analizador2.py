from email.mime import image
from enum import Enum
import math
import re
from archivohtml import constructorHTML

class token(Enum):
    # tokens usados
    t_menor = "<"
    t_mayor = ">"
    t_slash = "/"
    t_igual = "="
    t_e_tipo ="Tipo"
    t_e_operacion ="Operacion"
    t_e_num = "Numero"
    t_e_texto ="Texto"
    t_e_funcion ="Funcion"
    t_e_titulo ="Titulo"
    t_e_Descrip ="Descripcion"
    t_e_contenido ="Contenido"
    t_e_estilo ="Estilo"
    t_a_color ="Color"
    t_a_tam ="Tamanio"
    t_o_suma ="SUMA"
    t_o_resta = "RESTA"
    t_o_multiplicacion = "MULTIPLICACION"
    t_o_division = "DIVISION"
    t_o_potencia = "POTENCIA"
    t_o_raiz = "RAIZ"
    t_o_inverso = "INVERSO"
    t_o_seno = "SENO"
    t_o_coseno = "COSENO"
    t_o_tangente = "TANGENTE"
    t_o_mod = "MOD"
    t_num = "([0-9]+)(.[0-9]+)?"#"[0-9]+ [.[0-9]+]?"
    t_text = "[A-Za-z0-9\[\]_.,]*"
   

class analizador:
    def __init__(self):
        self.cadena = ""
        self.fila = 0
        self.columna = 0
        self.listacadena = []
        self.listaoperacion =[]
        self.resultado =[]
        self.listaerror = []
        self.temporal_c = ""
        self.resulttxt=""
        self.listaapariencia= []
        self.cont = 1
        self.tipe = 0
        self.conte = 0
    
    def compilador(self):
        archivo = open("../archivos/prueba3.txt", "r")
        contenido = archivo.readlines()
        archivo.close()
        #print(contenido)

        #quitando espacios y saltos
        cadena_n = ""
        lista_c = []

        for i in contenido:

            i = i.replace(" ", "")
            i = i.replace("\n", "")
            if i != "":
                cadena_n += i
                lista_c.append(i)
        print(cadena_n)
        print(lista_c)
        print("")
        self.listacadena = lista_c
        result=self.tipo(cadena_n)
        print("")
        print(result)  
        print(self.listaoperacion)
        print("")
        print(self.resultado)
        self.resulttxt=self.texto_f(result["cadena"])
        print("")
        print(self.resulttxt)  
        result1=self.funcion(self.resulttxt["cadena"])
        print("")
        print(result1) 
        result2=self.estilo(result1["cadena"])
        print("")
        print(result2)   
        print("")
        #if self.resultado:
        #    constructorHTML(self.resultado,"RESULTADOS_202100953",None)  
        if self.listaerror:
            for i in self.listaerror:
               print( i["No"]," | ", i["token"]," | ", i["tipo"]," | ", i["fila"]," | ", i["columna"]," | ", i["descrip"]) 
         #   constructorHTML(None,"ERRORES_202100953","cop")

    def numero (self,cadena:str):
        tokens = [
            token.t_menor.value,
            token.t_e_num.value,
            token.t_mayor.value,
            token.t_num.value,
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_num.value,
            token.t_mayor.value,
        ]

        numero =""
        
        for i in tokens:
            try:
                #print(i)
                patron = re.compile(f"^{i}")
                s = patron.search(cadena)
                self.columna += int(s.end())
                print("| ",self.fila," | ",self.columna," | ", s.group())
                #guardar token
                
                # lista,clase, diccionario, linea columna, simbolo, nombre token
                if i == token.t_num.value:
                    numero = s.group()
                cadena = self.quitar_L(cadena,s.end())
                self.lineas()
            except:
                self.conte+=1
                #guardar error
                if i==token.t_num.value:
                    self.tipe = 1
                    print("Ocurrio un error #1: ", self.tipe)
                    e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Numeros invalidos"}
                else:
                    self.tipe =2
                    print("Ocurrio un error #2: ", self.tipe)
                    e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Caracteres omitidos, adicionales,\nincorrectos o mezclados"}
                # linea, columna, error,simbolo, token donde ocurre error
                self.listaerror.append(e)
                self.listaoperacion=[]
                patron = re.compile(f"</Operacion>")
                s = patron.search(cadena)
                self.columna = int(s.end())
                cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                return {"tipoerror": i, "cadena":cadena, "error": True}
        #print(numero)
        return {"resultado": numero, "cadena":cadena, "error": False}
    
    def operador(self, cadena:str):
        tokens = [
            token.t_menor.value,
            token.t_e_operacion.value,
            token.t_igual.value,
            "OPERADOR",
            token.t_mayor.value,
            "NUMERO",
            "NUMERO",
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_operacion.value,
            token.t_mayor.value,
        ]
        numero = ""
        _operador = None
        for i in tokens:
            #print(i)
            try:
                #print("token; "+ i)
                if "NUMERO"== i:
                    #print("cadena: "+cadena)
                    if self.etiqueta(cadena, "<Numero>"):
                        result =self.numero(cadena)
                        cadena =result["cadena"]
                        if result["error"]:
                             #guardar error
                            if self.tipe !=1 and self.tipe !=2:
                                self.conte+=1
                                self.tipe = 3
                                print("Ocurrio un error #3: ", self.tipe)
                                e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Caract"}
                                self.listaerror.append(e)
                                self.listaoperacion=[""]
                                patron = re.compile(f"</Operacion>")
                                s = patron.search(cadena)
                                self.columna = int(s.end())
                                cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                            return {"tipoerror": i, "cadena":cadena, "error": True}
                        else:
                            print("Numero a guradar ",result["resultado"])
                            self.listaoperacion.append(result["resultado"])
                            #print(self.listaoperacion)
                    elif self.etiqueta(cadena,"<Operacion="):
                        self.cont+=1
                        result =self.operador(cadena)
                        cadena =result["cadena"]
                        if result["error"]:
                            #guardar error
                            if self.tipe!=5:
                                self.conte+=1
                                self.tipe = 4
                                print("Ocurrio un error #4: ", self.tipe)
                                e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Numeros invalidos"}
                                # linea, columna, error,simbolo, token donde ocurre error
                                self.listaerror.append(e)
                                self.listaoperacion=[]
                                patron = re.compile(f"</Operacion>")
                                s = patron.search(cadena)
                                self.columna = int(s.end())
                                cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                            return {"resultado": numero, "cadena":cadena, "error": True}
                    else:
                        self.conte+=1
                        self.tipe = 5
                        print("Ocurrio un error #5: ", self.tipe)
                        e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Caracteres omitidos, adicionales,\nincorrectos o mezclados"}
                        # linea, columna, error,simbolo, token donde ocurre error
                        self.listaerror.append(e)
                        self.listaoperacion=[]
                        patron = re.compile(f"</Operacion>")
                        s = patron.search(cadena)
                        self.columna = int(s.end())
                        cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                        return {"resultado": numero, "cadena":cadena, "error": True, "token": i}
                else:
                    oper=""
                    if "OPERADOR"== i:
                        #suma
                        opatron =re.compile(f"^SUMA")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="SUMA"
                            #print("entron a operador")
                            _operador = token.t_o_suma
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)

                         #Resta
                        opatron =re.compile(f"^RESTA")
                        #print("entra a res")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="RESTA"
                            _operador = token.t_o_resta
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                        
                         #multiplicacion
                        opatron =re.compile(f"^MULTIPLICACION")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="MULTIPLICACION"
                            _operador = token.t_o_multiplicacion
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                         #DIVISION
                        opatron =re.compile(f"^DIVISION")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="DIVISION"
                            _operador = token.t_o_division
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                         #potencia
                        opatron =re.compile(f"^POTENCIA")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="POTENCIA"
                            _operador = token.t_o_potencia
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                         #RAIZ
                        opatron =re.compile(f"^RAIZ")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="RAIZ"
                            _operador = token.t_o_raiz
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                         #INVERSO
                        opatron =re.compile(f"^INVERSO")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="INVERSO"
                            _operador = token.t_o_inverso
                            tokens.pop(6)
                         #SENO
                        opatron =re.compile(f"^SENO")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="SENO"
                            _operador = token.t_o_seno
                            tokens.pop(6)
                         #COSENO
                        opatron =re.compile(f"^COSENO")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="COSENO"
                            _operador = token.t_o_coseno
                            tokens.pop(6)
                         #TANGENTE
                        opatron =re.compile(f"^TANGENTE")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="TANGENTE"
                            _operador = token.t_o_tangente
                            tokens.pop(6)
                            #print(tokens)
                         #MOD
                        opatron =re.compile(f"^MOD")
                        t =opatron.search(cadena)
                        if t!=None:
                            i="MOD"
                            _operador = token.t_o_mod
                            if tokens[6]!="NUMERO":
                                tokens.insert(6, "NUMERO")
                                #print(tokens)
                        
                         #ninguno
                        if _operador==None:
                            #guardar error
                            # linea, columna, error,simbolo, token donde ocurre error
                            print("Ocurrio un error operacion")
                            self.tipe = 9
                            self.conte+=1
                            print("Ocurrio un error #9: ", self.tipe)
                            e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Operacion no definida"}
                            # linea, columna, error,simbolo, token donde ocurre error
                            self.listaerror.append(e)
                            self.listaoperacion=[]
                            patron = re.compile(f"</Operacion>")
                            s = patron.search(cadena)
                            self.columna = int(s.end())
                            cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                            return {"resultado": numero, "cadena":cadena, "error": True}
                        
                        self.listaoperacion.append(_operador.value)

                    elif "/"== i and self.listaoperacion!=[]:
                       # print("entra")
                        #print(self.cont)
                        for j in range(self.cont):
                            
                            if self.cont>1:
                                ini="("
                                fin=")"
                            else:
                                ini=""
                                fin=""
                            #print(ini)

                            op=0
                            
                            posicion =len(self.listaoperacion)-2
                            #print(posicion)
                            if posicion>=0:
                                #print(self.listaoperacion[posicion-1])
                                if posicion>0:
                                    if self.listaoperacion[posicion-1]=="SUMA":
                                        #print("sum")
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}+{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}+{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}+{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])+float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="RESTA":
                                        #print("res")
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}-{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}-{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}-{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])-float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="MULTIPLICACION":
                                        #print("multi")
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}*{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}*{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}*{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])*float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="DIVISION":
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}/{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}/{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}/{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])/float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="POTENCIA":
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}^{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}^{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}^{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])**float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="MOD":
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}%{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}%{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}%{oper}"
                                        resultadoop=float(self.listaoperacion[posicion])%float(self.listaoperacion[posicion+1])
                                    if self.listaoperacion[posicion-1]=="RAIZ":
                                        if j==0:
                                            oper=oper+ini+f"{float(self.listaoperacion[posicion])}&radic{float(self.listaoperacion[posicion+1])}"+fin
                                        elif j>0 and j<self.cont-1:
                                            oper=ini+f"{float(self.listaoperacion[posicion])}&radic{oper}"+fin
                                        else:
                                            oper=f"{float(self.listaoperacion[posicion])}&radic{oper}"
                                        resultadoop=float(self.listaoperacion[posicion+1])**(1/float(self.listaoperacion[posicion]))
                                if self.listaoperacion[posicion]=="SENO":
                                    op=1
                                    if j==0:
                                        oper=oper+ini+f"SEN({float(self.listaoperacion[posicion+1])})"+fin
                                    elif j>0 and j<self.cont-1:
                                        oper=ini+f"SEN({oper})"+fin
                                    else:
                                        oper=f"SEN({oper})"
                                    resultadoop=math.sin(float(self.listaoperacion[posicion+1]))
                                if self.listaoperacion[posicion]=="COSENO":
                                    op=1
                                    if j==0:
                                        oper=oper+ini+f"COS({float(self.listaoperacion[posicion+1])})"+fin
                                    elif j>0 and j<self.cont-1:
                                        oper=ini+f"COS({oper})"+fin
                                    else:
                                        oper=f"COS({oper})"
                                    resultadoop=math.cos(float(self.listaoperacion[posicion+1]))
                                if self.listaoperacion[posicion]=="TANGENTE":
                                    
                                    op=1
                                    if j==0:
                                        oper=oper+ini+f"TAN({float(self.listaoperacion[posicion+1])})"+fin
                                    elif j>0 and j<self.cont-1:    
                                        oper=ini+f"TAN({oper})"+fin
                                    else:
                                        oper=f"TAN({oper})"+fin
                                    resultadoop=math.tan(float(self.listaoperacion[posicion+1]))
                                   # print(resultadoop)
                                if self.listaoperacion[posicion]=="INVERSO":
                                    op=1
                                    if j==0:
                                        oper=oper+ini+f"1/{float(self.listaoperacion[posicion+1])}"+fin
                                    elif j>0 and j<self.cont-1:
                                        oper=ini+f"1/"+oper+fin
                                    else:
                                        oper=f"1/"+oper
                                    resultadoop=1/(float(self.listaoperacion[posicion+1]))   
                                
                                #print("llega")
                                self.listaoperacion.pop(posicion+1)
                                #print("hace")
                                self.listaoperacion.pop(posicion)
                                #print("hace")
                                if posicion-1>=0 and op==0:
                                    self.listaoperacion.pop(posicion-1)
                                    #print("hace")
                                if j!=self.cont-1:
                                  #  print("hace primera")
                                    #print(resultadoop)
                                    #print(self.listaoperacion)
                                    self.listaoperacion.append(resultadoop)
                                    #print("llega")
                                   # print(self.listaoperacion)
                                else:
                                    if self.cont>1:
                                        self.resultado.append({"op":"COMPLEJA","proceso":oper,"res":resultadoop})
                                    else:
                                        self.resultado.append({"op":_operador.value,"proceso":oper,"res":resultadoop})
                                    #print(self.listaoperacion)
                                    self.cont=1            
                    #print(i)                            
                    
                   

                    patron = re.compile(f"^{i}")
                    s = patron.search(cadena)
                    self.columna += int(s.end())
                    print("| ",self.fila," | ",self.columna," | ", s.group() )
                    #guardar token
                    # lista,clase, diccionario, linea columna, simbolo, nombre token
                    cadena = self.quitar_L(cadena,s.end())
                self.lineas()
            except:
                #guardar error
                # linea, columna, error,simbolo, token donde ocurre error
                if self.tipe!=1 and self.tipe !=2:
                    if self.tipe==5:
                        self.tipe=10
                        print("Ocurrio un error #10: No se puede operar debido al error anterior")

                        self.listaoperacion=[]
                        pato = re.compile(f"/Operacion>")
                       # print(cadena)
                        k = pato.search(cadena)
                        self.columna = int(k.end())
                        #print(k.end())
                        cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                    else:
                        anterior=self.tipe
                        self.tipe=6
                        self.conte+=1
                        print("Ocurrio un error #6: ", self.tipe )
                        e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Caracteres omitidos, adicionales,\nincorrectos o mezclados"}
                        # linea, columna, error,simbolo, token donde ocurre error
                        self.listaerror.append(e)
                       # print("rompe123")
                        self.listaoperacion=[]
                        patro = re.compile(f"</Operacion>")
                       # print(patro)
                       # print("rompeq3eq")
                        #print(cadena)
                        r = patro.search(cadena)
                        #print(r)
                        #print(anterior)
                        self.columna = int(r.end())
                        
                        #print(r.start()+1)
                        #print(self.columna)
                        cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                       # print("rompe3")   
                if self.tipe==1 or self.tipe==2:
                    if i== token.t_e_operacion.value:
                        patron = re.compile(f"^{i}")
                        s = patron.search(cadena)
                        if s==None:
                            pt= re.compile(f"/Operacion>")
                            r = pt.search(cadena)
                            self.columna = int(r.end())
                            cadena =self.quitar_E(cadena,"/Operacion>",self.columna)
                
                 #   self.operador(cadena)
                #print("rompe4")
                return {"resultado": numero, "cadena":cadena, "error": True}

        return {"resultado": numero, "cadena":cadena, "error": False}

    def tipo(self,cadena:str):
        tokens = [
            token.t_menor.value,
            token.t_e_tipo.value,
            token.t_mayor.value,
            "OPERACIONES",
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_tipo.value,
            token.t_mayor.value,
        ]
        numero = ""
        for i in tokens:
           
            try:
                if "OPERACIONES"==i:
                    salida =True
                    while salida:
                        print("________________________________")
                        result =self.operador(cadena)
                        cadena = result["cadena"]
                        if result["error"]:
                            #guardar error
                            if  self.tipe!=1 and self.tipe!=2 and self.tipe !=5 and self.tipe !=6 and self.tipe !=9 and self.tipe !=10:
                                self.tipe=7
                                self.conte+=1
                                print("ocurrio un error #7: ", self.tipe)
                                e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Operacion no valida"}
                                # linea, columna, error,simbolo, token donde ocurre error
                                self.listaerror.append(e)
                                self.listaoperacion=[]
                                patron = re.compile(f"</Operacion>")
                                s = patron.search(cadena)
                                self.columna = int(s.end())
                                cadena =self.quitar_E(cadena,"/Operacion>",self.columna)
                            if self.tipe==6:
                                #print("rom2")
                                self.tipe==0
                            if self.tipe ==1 or self.tipe ==2:
                                
                                salida=True
                            #print("rompe2")
                        elif self.etiqueta(cadena,"</Tipo>"):
                            salida=False
                        
                else:
                   # print("rompe 1")
                    patron = re.compile(f"^{i}")
                    s = patron.search(cadena)
                    self.columna += int(s.end())
                    print("| ",self.fila," | ",self.columna," | ", s.group() )
                    #guardar token
                    # lista,clase, diccionario, linea columna, simbolo, nombre token
                    cadena = self.quitar_L(cadena,s.end())
                    self.lineas()
            except:
                #guardar error
                # linea, columna, error,simbolo, token donde ocurre error
                if i!="OPERACIONES":
                    self.conte+=1
                    self.tipe=8
                    #print("Ocurrio un error #8: ", self.tipe)
                    e={"No":self.conte,"token":i,"tipo":"ERROR","fila":self.fila,"columna":self.columna, "descrip":"Numeros invalidos"}
                    if int(tokens.index(i))<int(tokens.index("OPERACIONES")):
                        patron = re.compile(f"</Tipo>")
                        s = patron.search(cadena)
                        self.columna = int(s.end())
                        cadena =self.quitar_E(cadena,"</Tipo>",self.columna)
                        
                if self.tipe==1 or self.tipe==2:
                    pt= re.compile(f"/Operacion>")
                    r = pt.search(cadena)
                    if r!=None:
                        self.columna = int(r.end())
                        cadena =self.quitar_E(cadena,"</Operacion>",self.columna)
                    # linea, columna, error,simbolo, token donde ocurre error
                #print("rompe")
                return {"resultado": numero, "cadena":cadena, "error": True}
        print("no ocurrio ningun error")
        return {"resultado": numero, "cadena":cadena, "error": False}

    def texto_f(self,cadena:str):
        tokens = [
            token.t_menor.value,
            token.t_e_texto.value,
            token.t_mayor.value,
            token.t_text.value,
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_texto.value,
            token.t_mayor.value,
        ]
        descr =""
        
        for i in tokens:
            try:
                #print(i)
                patron = re.compile(f"^{i}")
                s = patron.search(cadena)
                self.columna += int(s.end())
                print("| ",self.fila," | ",self.columna," | ", s.group())
                
                cadena = self.quitar_L(cadena,s.end())
                self.lineas()
            except:
                #guardar error
                # linea, columna, error,simbolo, token donde ocurre error
                print("Ocurrio un errror 8")
                return {"resultado": "", "cadena":cadena, "error": True}
        #print(numero)
        return {"resultado": descr, "cadena":cadena, "error": False}

    def funcion(self,cadena:str):
        tokens = [
            token.t_menor.value,
            token.t_e_funcion.value,
            token.t_igual.value,
            "ESCRIBIR",
            token.t_mayor.value,
            token.t_menor.value,
            token.t_e_titulo.value,
            token.t_mayor.value,
            token.t_text.value,
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_titulo.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_e_Descrip.value,
            token.t_mayor.value,
            "\[TEXTO\]",
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_Descrip.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_e_contenido.value,
            token.t_mayor.value,
            "\[TIPO\]",
            token.t_menor.value,
            token.t_slash.value,
            token.t_e_contenido.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_slash.value,
            token.t_e_funcion.value,
            token.t_mayor.value,
        ]
        numero =""
        
        for i in tokens:
            try:

                #print(i)
                patron = re.compile(f"^{i}")
                s = patron.search(cadena)
                self.columna += int(s.end())
                print("| ",self.fila," | ",self.columna," | ", s.group())
                if i==token.t_text.value:
                    numero= s.group()
                cadena = self.quitar_L(cadena,s.end())
                self.lineas()
            except:
                #guardar error
                # linea, columna, error,simbolo, token donde ocurre error
                print("Ocurrio un errror 9")
                return {"resultado": numero, "cadena":cadena, "error": True}
        #print(numero)
        return {"resultado": numero, "cadena":cadena, "error": False}

    def estilo(self,cadena:str):
        colores = [
            "NEGRO",
            "AZUL",
            "AMARILLO",
            "ROJO",
            "VERDE",
            "MORADO",
            "ANARANJADO"
            ]
        tokens = [
            token.t_menor.value,
            token.t_e_estilo.value,
            token.t_mayor.value,
            token.t_menor.value,
            token.t_e_titulo.value,
            token.t_a_color.value,
            token.t_igual.value,
            "COLOR",
            token.t_a_tam.value,
            token.t_igual.value,
            token.t_num.value,
            token.t_slash.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_e_Descrip.value,
            token.t_a_color.value,
            token.t_igual.value,
            "COLOR",
            token.t_a_tam.value,
            token.t_igual.value,
            token.t_num.value,
            token.t_slash.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_e_contenido.value,
            token.t_a_color.value,
            token.t_igual.value,
            "COLOR",
            token.t_a_tam.value,
            token.t_igual.value,
            token.t_num.value,
            token.t_slash.value,
            token.t_mayor.value,

            token.t_menor.value,
            token.t_slash.value,
            token.t_e_estilo.value,
            token.t_mayor.value,
        ]
        numero =""
        _color =None
        for i in tokens:
            #print(i)
            try:
                #print("token; "+ i)
                if "COLOR"== i:
                    #print("cadena: "+cadena)
                    for j in colores:
                        opatron =re.compile(f"^{j}")
                        t =opatron.search(cadena)
                        if t!=None:
                            i=j
                            #print("entron a operador")
                            _color = j
                            self.listaapariencia.append(_color)

                    if _color==None:
                            #guardar error
                            # linea, columna, error,simbolo, token donde ocurre error
                            print("Ocurrio un errror operacion 10")
                            return {"resultado": numero, "cadena":cadena, "error": True}  
                    if i== token.t_num.value:
                        self.listaapariencia.append(s.group)

                #print(i)    
                patron = re.compile(f"^{i}")
                s = patron.search(cadena)
                self.columna += int(s.end())
                print("| ",self.fila," | ",self.columna," | ", s.group() )
                if i== token.t_num.value:
                    self.listaapariencia.append(s.group)
                #guardar token
                # lista,clase, diccionario, linea columna, simbolo, nombre token
                cadena = self.quitar_L(cadena,s.end())
                self.lineas()
            except:
                #guardar error
                # linea, columna, error,simbolo, token donde ocurre error
                print("Ocurrio un errror 11")
                return {"resultado": numero, "cadena":cadena, "error": True}

        return {"resultado": numero, "cadena":cadena, "error": False}
              
    def lineas(self):
        
        tmp =self.listacadena[self.fila]
        #print(self.fila)
        if tmp ==self.temporal_c:
            #print("entra a lineas")
            self.fila += 1
            self.temporal_c = ""
            self.columna = 0

    def quitar_L (self,cadena:str,column:int):
        #print("quitando")
        tmp =""
        cont = 0
        for i in cadena:
            if cont >= column:
                tmp += i
            else:
                self.temporal_c += i
            cont += 1
        
        #print(self.temporal_c)
        #print("")
        #print(tmp)
        return tmp

    def quitar_E (self,cadena:str,etiqueta:str,column:int):
        #print("quitando E")
        tmp =""
        cont = 0
        #print(len(self.listacadena))
        pos = int(self.listacadena.index(etiqueta))
        for k in range(len(self.listacadena)):
            #print("entron a cambio")
            if k<= pos:
                #print("entrando")
                #print(self.listacadena[k])
                cambio=self.listacadena[k]
                self.listacadena[k]=f"{cambio}{k}"

        #print(self.listacadena[pos])
        self.fila=pos+1
       # print(self.fila)
        self.columna=0
        for i in cadena:
            if cont >= column:
                tmp += i  
            cont += 1
        self.temporal_c = ""
        #print("")
        #print(tmp)
        return tmp

    def etiqueta(self, cadena:str,etiquet:str):
        tmp = ""
        cont = 0
        for i in cadena:
            if cont < len(etiquet):
                tmp += i
                cont += 1
        if tmp == etiquet:
            #print(tmp +" _______"+ etiquet)
            return True
        else: 
           # print(tmp+" _______"+etiquet)
            return False
    

analizador().compilador()