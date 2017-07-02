# -*- coding:utf-8 -*-
 
from tkinter import *
from tkinter import messagebox
import sqlite3
 
class Main:
    def __init__(self,master):
        self.frame = Frame(master)
        self.frame.pack()

        Label(self.frame,text="Nome do Produto").pack()
        self.nome = Entry(self.frame,width=35)
        self.nome.pack()

        Label(self.frame,text="Data").pack()
        self.data = Entry(self.frame,width=35)
        self.data.pack()

        Label(self.frame,text="Quantidade").pack()
        self.qnt = Entry(self.frame,width=35)
        self.qnt.pack()

        Label(self.frame,text="Unidade de Medida").pack()
        self.und = Entry(self.frame,width=35)
        self.und.pack()

        Label(self.frame,text="Valor").pack()
        self.valor = Entry(self.frame,width=35)
        self.valor.pack()
        
        Frame(height=2,bd=3,width=100,relief=SUNKEN).pack(fill=X,padx=5,pady=5)
        self.frame3 = Frame()
        self.frame3.pack()
        self.add = Button(self.frame3,text="Adicionar Compras",command=self.adicionar)
        self.add.pack(side=LEFT)
        self.apagar = Button(self.frame3,text="Apagar Compras",command=self.apagar)
        self.apagar.pack(side=LEFT)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        self.listbox = Listbox(master,height=20,width=50)
        self.listbox.pack()
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
         
        #criar banco
        self.conectar = sqlite3.connect("dados.db")
        self.cur = self.conectar.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS compras(nome TEXT, data TEXT, qnt TEXT, und TEXT, valor REAL)")
        self.conectar.commit()
        lista = self.cur.execute("SELECT * FROM compras")
        for i in lista:
            self.listbox.insert(END,i)

        
    def adicionar(self):
        nomes   = self.nome.get()
        datas   = self.data.get()
        qnts    = self.qnt.get()
        unds    = self.und.get()
        valores = self.valor.get()
        if nomes == "":
            messagebox.showinfo("Warning", "Dados Inválidos")
        else:
            self.cur.execute("insert into compras values (?,?,?,?,?)",(nomes, datas, qnts, unds, valores))
            self.conectar.commit()
            self.listbox.insert(END,nomes)
            self.listbox.insert(END,datas)
            self.listbox.insert(END,qnts)
            self.listbox.insert(END,unds)
            self.listbox.insert(END,valores)
    def apagar(self):
        nomex = str(self.listbox.get(ACTIVE))[3:-3]
        self.cur.execute("DELETE FROM compras WHERE nome=?",(nomex,))
        self.conectar.commit()
        self.listbox.delete(ANCHOR)
 
def fechar():
    if messagebox.showinfo("Fechar","Deseja realmente fechar esta aplicação?"):
        exit()
    else:
        pass
root = Tk()
root.protocol("WM_DELETE_WINDOW",fechar)
root.title("Inserir Compra")
root.geometry("300x400")
Main(root)
root.mainloop()
