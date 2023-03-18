from tkinter import messagebox, ttk
from tkinter.font import ITALIC
from tkinter.ttk import Progressbar
from tkinter import *
import os

from funcionesmenu import funciones
# SI NO FUNCIONA EL VISOR: pip install --upgrade pymupdf==1.18.17

def ventanaanalizador():
    #Creando y configurando ventana
    q = Tk()
    q.title('Analizador lexico')
    q.config(bg = "#413658") #181e36#413658
    q.geometry('1200x900+40+0')
    q.iconbitmap('logo.ico')

    #Frame para visor de pdf
    funcion.pdfviwer(0)
    #Frame de editor de texto
    frame3 = Frame()
    frame3.config(width = "550", height = "455", bg = "#140b1e")
    frame3.place(x = 20, y = 250)
    # Caja de texto 
    texto = Text(frame3)
    texto.place(x = 0, y = 0)
    texto.config(padx = 6, pady = 2, width="45", height = "19", bg = "#140b1e")
    texto.config( insertbackground = "white", foreground = "#45f9cf", font = ("Consolas", 16))

    #Frame para menu
    frame1 = Frame()
    frame1.pack(pady = 40, padx = 20)
    frame1.config(width = "1270", height = "180", bg = "#140b1e")
    #LABEL PARA MENU DE ARCHIVO
    l1 = Label(frame1, bg='#140b1e', text="ARCHIVO",fg="#45f9cf")
    l1.config(font= ("Roboto", 14, 'bold'), width=20)
    l1.place(x=175,y=5)
    #Botones menu de archivo
    b1 = Button(frame1, bg='white', text="Abrir",fg="#726881" )
    b1.config(width=60, activebackground='#24adbf', bd=0)
    b1.config(font=("Roboto",12,ITALIC), bg='#140b1e',command=lambda: abrir(texto))
    b1.place(x=10,y=30)

    b2 = Button(frame1, bg='white', text="Guardar",fg="#786292" )
    b2.config(width=60, activebackground='#24adbf', bd=0)
    b2.config(font=("Roboto",12,ITALIC),bg='#140b1e',command=lambda: guardar(texto))
    b2.place(x=10,y=55)

    b3 = Button(frame1, bg='white', text="Guardar como",fg="#786292" )
    b3.config(width=60, activebackground='#24adbf', bd=0)
    b3.config(font=("Roboto",12,ITALIC),bg='#140b1e',command=lambda: guardar_como(texto))
    b3.place(x=10,y=80)

    b4 = Button(frame1, bg='white', text="Ejecutar",fg="#786292" )
    b4.config(width=60, activebackground='#24adbf', bd=0)
    b4.config(font=("Roboto",12,ITALIC),bg='#140b1e',command=lambda: ejecutar(texto))
    b4.place(x=10,y=105)

    b5 = Button(frame1, bg='white', text="Salir",fg="#786292" )
    b5.config(width=60, activebackground='#24adbf', bd=0)
    b5.config(font=("Roboto",12,ITALIC),bg='#140b1e',command=lambda: salir(q))
    b5.place(x=10,y=130)

     #LABEL PARA MENU DE AYUDA
    l2 = Label(frame1, bg='#140b1e', text="AYUDA",fg="#45f9cf")
    l2.config(font= ("Roboto", 14, 'bold'), width=20)
    l2.place(x=750,y=5)
    #Botones manual usuario
    b6 = Button(frame1, bg='white', text="Manual de usuario",fg="#726881" )
    b6.config(width=62, activebackground='#24adbf', bd=0)
    b6.config(font=("Roboto",12,ITALIC), bg='#140b1e', command=manualu)
    b6.place(x=580,y=30)
    #Botones manual tecnico
    b7 = Button(frame1, bg='white', text="Manual tecnico",fg="#786292" )
    b7.config(width=62, activebackground='#24adbf', bd=0)
    b7.config(font=("Roboto",12,ITALIC),bg='#140b1e', command=manualt)
    b7.place(x=580,y=55)
    #boton de ayuda
    b8 = Button(frame1, bg='white', text="Temas de ayuda",fg="#786292" )
    b8.config(width=62, activebackground='#24adbf', bd=0)
    b8.config(font=("Roboto",12,ITALIC),bg='#140b1e',command =info)
    b8.place(x=580,y=80)
   
    q.mainloop()

def abrir(texto):
    contenido=funcion.viewer()
    texto.delete(1.0, 'end')           # Nos aseguramos de que esté vacío
    texto.insert('insert', contenido)  # Le insertamos el contenido

def guardar(texto):
    contenido=contenido = texto.get(1.0,'end-1c')
    op=funcion.salve(contenido)
    if op==1:
        messagebox.showinfo(message="Se guardaron los cambios correctamente",title="Guardar")
    else:
        messagebox.showinfo(message="El archivo se guardo correctamente",title="Guardar")

def guardar_como(texto):
    contenido = texto.get(1.0,'end-1c')
    funcion.salve_c(contenido)
    messagebox.showinfo(message="El archivo se guardo correctamente",title="Guardar como")

def ejecutar(texto):
    contenido = texto.get(1.0,'end-1c')
    op=funcion.salve(contenido)
    funcion.run()

def salir(q):
    q.destroy()

def manualu():
    funcion.pdfviwer(1)
 
def manualt():
    funcion.pdfviwer(2)

def info():
    messagebox.showinfo(message= f"Informacion del desarollador:\nDamaris Julizza Muralles Veliz\nCarnet: 202100953\nCurso: LFP\nSeccion: B-",title="Temas de ayuda")
    funcion.pdfviwer(0)


if __name__ == "__main__":
    funcion=funciones()
    #ventanaanalizador()
    w = Tk()
    width_of_window = 427
    height_of_window = 250
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    x_coordinate = (screen_width/2)-(width_of_window/2)
    y_coordinate = (screen_height/2)-(height_of_window/2)
    w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))

    w.overrideredirect(1)

    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='red', background='#249794')
    progress=Progressbar(w,style = "red.Horizontal.TProgressbar",orient = HORIZONTAL)
    progress.config(length = 500,mode='determinate')

   #PANTALLA FLOTANTE PARA INICIO DE PROGRAMA
    def bar():
        l4=Label(w,text='Espere...',fg='white',bg=a)
        lst4=('Calibri (Body)',10)
        l4.config(font=lst4)
        l4.place(x=18,y=210)
        
        import time
        r = 0
        for i in range(100):
            progress['value'] = r
            w.update_idletasks()
            time.sleep(0.03)
            r = r+1
        
        w.destroy()
        ventanaanalizador()
               
    progress.place(x = -10,y = 235)

    # frame 
    a='#140b1e'#249794=celeste
    Frame(w,width=427,height=241,bg=a).place(x=0,y=0)  
    b1=Button(w,width=10,height=1,text='Comenzar',command=bar)
    b1.config(border="0", fg = "white", bg ="#249794")
    b1.place(x=170,y=200)

    ######## Label
    l1=Label(w,text='ANALIZADOR',fg='#45f9cf',bg=a)
    lst1=('Calibri (Body)',18,'bold')
    l1.config(font=lst1)
    l1.place(x=50,y=80)

    l2=Label(w,text='LEXICO',fg='#45f9cf',bg=a)
    lst2=('Calibri (Body)',18)
    l2.config(font=lst2)
    l2.place(x=210,y=82)

    l3=Label(w,text='PROYECTO 1',fg='#45f9cf',bg=a)
    lst3=('Calibri (Body)',13)
    l3.config(font=lst3)
    l3.place(x=50,y=110)

    w.mainloop()
    """  
   
    """
    
   
    


   
	