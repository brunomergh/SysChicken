import sqlite3
def create_bd(conn, c):
    #conn = sqlite3.connect('example.db')

    #c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS produto
                 (id INTEGER, nome text)''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS itemcardapio
                 (id INTEGER, nomeFicticio text, date text, valor real)''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS venda
                 (id INTEGER, quantidade real)''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS compra
                 (id INTEGER,valor real)''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS produtocompra
                 (id INTEGER, idProduto INTEGER, idCompra INTEGER, data text, quantidade real,unidadeMedida text)''')

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS gastoextra
                 (id INTEGER, nome text, valor real, data text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS itemcardapioproduto
                 (id INTEGER, idItemCardapio INTEGER, idProduto INTEGER, peso real)''')

    
    
    
    conn.commit()
    
def inserir_compra(c, conn, nomeProduto, valor, data, quantidade, unidadeMedida):

    
    flag = False
    for row in c.execute("SELECT * FROM produto"):
        #print(row)
        if row[1] == nomeProduto:
            #print (row)
            flag = True
            break
        else:
            #print("else")
            flag = False

    if not flag:
        c.execute("SELECT * FROM produto ORDER BY id desc")
        lastidProduto = c.fetchone()
        if (lastidProduto == None):
            lastidProduto = [0]
        #print(lastidProduto[0])
        c.execute("INSERT INTO produto VALUES (?, ?)", [int(lastidProduto[0]) + 1, nomeProduto])
        conn.commit()

    c.execute("SELECT * FROM compra ORDER BY id desc")
    #print(c.fetchone())
    lastidCompra = c.fetchone()
    if (lastidCompra == None):
        lastidCompra = [0]
    c.execute("INSERT INTO compra VALUES (?, ?)", [lastidCompra[0]+1, valor])
    
    c.execute("SELECT * FROM produto WHERE nome = :nome", {"nome": nomeProduto} )
    produto = c.fetchone()

    c.execute("SELECT * FROM produtocompra")
    lastidProdutoCompra = c.fetchone()
    
    if (lastidProdutoCompra == None):
        lastidProdutoCompra = [0]
    c.execute("INSERT INTO produtocompra VALUES (?, ?, ?, ?, ?, ?)", [lastidProdutoCompra[0] +1, produto[0], lastidCompra[0]+1, data, quantidade, unidadeMedida])

    #for row in c.execute("SELECT * FROM produto"):
        #print(row)

    #for row in c.execute("SELECT * FROM compra order by id desc"):
        #print(row)
    
   
    conn.commit()

def inserir_item_cardapio(c, conn, nomeFicticio, lstNomeProduto, valor, lstpeso, data):

    c.execute("SELECT * FROM itemCardapio ORDER BY id desc")
    lastidItemCardapio = c.fetchone()
    if (lastidItemCardapio == None):
        lastidItemCardapio = [0]

    c.execute("INSERT INTO itemCardapio VALUES (?, ?, ?, ?)", [int(lastidItemCardapio[0]) + 1, nomeFicticio, data, valor])
    idItemCardapio = lastidItemCardapio[0] + 1
    conn.commit()
    for nomeProduto in lstNomeProduto:
        c.execute("SELECT * FROM produto WHERE nome = :nome", {"nome": nomeProduto} )
        produto = c.fetchone()
        
        c.execute("SELECT * FROM itemCardapioProduto ORDER BY id desc")
        lastidItemCardapioProduto = c.fetchone()
        if (lastidItemCardapioProduto == None):
            lastidItemCardapioProduto = [0]

        c.execute("INSERT INTO itemCardapioProduto VALUES (?, ?, ?, ?)", [int(lastidItemCardapioProduto[0]) + 1, produto[0], idItemCardapio, lstpeso[0]])

        conn.commit()
    
    

conn = sqlite3.connect('example10.db')

c = conn.cursor()

create_bd(conn, c)
#inserir_compra(c, conn,"Batata", 10.0, "12/04/2017", 1000, "gramas")

ans=True
while ans:
    print("""
    1.Inserir uma compra(add no estoque)
    2.Inserir um item no cardápio
    3.Visualizar Cardapio
    4.Exit/Quit
    """)
    ans=input("O que gostaria de fazer? ")
    if ans=="1":
        nomeProduto = input("Nome do Produto: ")
        valor = input("Valor do Produto: ")
        quantidade = input("Peso do produto em gramas:")
        unidadeMedida = "gramas"
        data = "07052017"

        inserir_compra(c, conn, nomeProduto, valor, data, quantidade, unidadeMedida)

        #simounao = input("Compra inserida com sucesso, deseja visualiza-lá?(s/n)")
        print("Compra inserida com sucesso")
        
    elif ans=="2":
        nomeFicticio = input("Nome Ficticio: ")
        lstprodutos = input("Lista de Produto(s) separados por ESPAÇO: ")
        quantidade = input("Peso total do(s) iten(s) em gramas: ")
        unidadeMedida = "gramas"
        valor = input("Valor do item: ")
        data = "07052017"

        lstprodutos = lstprodutos.split()

        inserir_item_cardapio(c, conn, nomeFicticio, lstprodutos, valor, quantidade, data)
        
    elif ans=="3":
        lstIds = []
        lstprodutos = []
        lstnomeficticio = []
        lstvalores = []
        dic = {}
        lstidsprodutos = []
        #for row in c.execute("select * from itemCardapioProduto"):
        #    print(row)
        cont = 0
        #for i in c.execute("SELECT * " +
        #                     "FROM itemCardapio "):
        #    print(i)
        for row2 in c.execute("SELECT * " +
                             "FROM itemCardapio "):
                             #"WHERE itemCardapio.id = itemCardapioProduto.idItemCardapio"):
            print(row2)
            lstIds.append(row2[0])
            lstnomeficticio.append(row2[1])
            lstvalores.append(row2[3])
            
        for i in lstIds:    
            for row in c.execute("select * from itemCardapioProduto where idItemCardapio = :idp", {"idp" : i}):
                print(row)
                lstidsprodutos.append(row[1])
                for j in lstidsprodutos:
                    for row3 in c.execute("select * from produto where id = :id", {"id" : j}):
                        if row3[1] not in lstprodutos:
                            lstprodutos.append(row3[1])     
                        
                print("\nNome Ficticio:", lstnomeficticio[cont], "Itens Contido(s):", lstprodutos, "Valor:", lstvalores[cont] )
                lstprodutos = []
                cont+=1
            
        #lstIds = []
        #lstprodutos = []
        #lstnomeficticio = []
        #lstvalores = []
            
        '''cont = 0
        for identificador in lstIds:
            
            for row2 in c.execute("SELECT * FROM itemCardapioProduto WHERE idItemCardapio = :id", {"id": identificador}):
                print("p", row2)
                for row in c.execute("SELECT * FROM produto WHERE id = :id", {"id": row2[1]} ):
                    produto = row
                    
                    lstprodutos.append(produto[1])
                print("lstprodutos", lstprodutos)
            print("Nome Ficticio:", lstnomeficticio[cont], "Itens Contido(s):", lstprodutos, "Valor:", lstvalores[cont] )
            cont += 1;
            lstprodutos = []'''
            
            
  
    elif ans=="4":
      print("\n Goodbye") 
      ans = None
    else:
       print("\n Not Valid Choice Try again")
