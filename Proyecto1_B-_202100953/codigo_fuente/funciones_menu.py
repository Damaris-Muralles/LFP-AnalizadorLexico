
from tkinter import  filedialog as FileDialog
from tkinter import Frame
from tkPDFViewer import tkPDFViewer 
from analizador2 import analizador
class funciones:
    def __init__(self):
        self.ruta=""

        
    def pdfviwer(self,menuop):
        #Frame para visor de pdf
        frame2 = Frame()
        frame2.place(x = 600, y = 250)
        frame2.config(width = "50", height = "300")
        v1 = tkPDFViewer.ShowPdf()
        v1.img_object_li.clear()
        if menuop==0:
            v2 = v1.pdf_view(frame2, pdf_location = r"../archivos/Vista_previa.pdf",width = 70, height = 27.2, bar=False)
        elif menuop==1:
            v2 = v1.pdf_view(frame2, pdf_location = r"../Documentacion/Manual_usuario.pdf",width = 70, height = 27.2,bar=False)
        else:
            v2 = v1.pdf_view(frame2, pdf_location = r"../Documentacion/Manual_tecnico.pdf",width = 70, height = 27.2,bar=False)
        
        v2.pack()

    def viewer(self):

        self.ruta = FileDialog.askopenfilename(initialdir='.',filetypes=( ("Ficheros de texto", "*.txt"),),  title="Abrir un fichero.")

        # Si la ruta es válida abrimos el contenido en lectura
        if self.ruta != "":  
            archivo  = open(self.ruta, 'r',encoding= "utf-8")
            contenido =  archivo.read()
            archivo.close()
            return contenido
    def salve(self, contenido):
        op=0
        if self.ruta != "":
            op=1
            archivo  = open(self.ruta, 'w+',encoding= "utf-8")
            archivo.write(contenido)
            archivo.close()
        else:
            self.salve_c(contenido)
        return op

    def salve_c(self,contenido):
        archivo = None
        archivo = FileDialog.asksaveasfile(title="Guardar como", mode="w", defaultextension=".txt")

        if  archivo  is not None:
            self.ruta =  archivo.name
            archivo  = open(self.ruta, 'w+',encoding= "utf-8")
            archivo.write(contenido)
            archivo.close()
        else:
            self.ruta = ""   

    def run(self):
        print("ruta",self.ruta)
        analizador().compilador(self.ruta)
    #l1=Label(q,text='ADD TEXT HERE ',fg='grey',bg=None)
    #l=('Calibri (Body)',24,'bold')
    #l1.config(font=l)
    #l1.place(x=80,y=100)
    """
    # en este fragmento de codigo se utiliza la libreria os para abrirlo con un 
    #lector de pdf en nuestra computadora por medio de cmd
    separador = os.path.sep
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    dir = separador.join(dir_actual.split(separador)[:-1])
    path = f"{dir}/Documentacion/Manual_usuario.pdf"
    os.system(path)
    """                           