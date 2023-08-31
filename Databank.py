from sqlite3 import connect

class DB():
    def __init__(self):
        self.connection = connect('databank.db')
        self.cursor = self.connection.cursor()

    def create_product(self, *produto):
        sql = "INSERT INTO produtos VALUES(?,?,?,?,?,?)"
        self.cursor.execute(sql, produto)
        self.connection.commit()
    
    def read_products(self, campos='*', filtro=None, ordem=None):
        sql = f"SELECT {campos} FROM produtos"
        if filtro:
            sql += f" WHERE codigo LIKE '{filtro}%' OR nome LIKE '%{filtro}%'"
        if ordem:
            sql += f" ORDER BY {ordem}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def consultar_produto(self, codigo, campos='*'):
        sql = f"SELECT {campos} FROM produtos WHERE codigo = '{codigo}'"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def update_protuct(self, id, produto):
        updates = []
        keys = produto.keys()
        for key in keys:
            updates.append(f"{key} = '{produto[key]}'")
        updates = str(updates)[1:-1].replace('"', '')
        sql = f"UPDATE produtos SET {updates} WHERE codigo = '{id}'"
        self.cursor.execute(sql)
        self.connection.commit()

    def delete_product(self, codigo):
        sql = f"DELETE FROM produtos WHERE codigo='{codigo}'"
        self.cursor.execute(sql)
        self.connection.commit()

    def cadastrar_venda(self, produto):
        sql = f"INSERT INTO vendas VALUES(?,?,?,?)"
        self.cursor.execute(sql, produto)
        self.connection.commit()

if __name__ == '__main__':
    db = DB()
    