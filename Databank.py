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

if __name__ == '__main__':
    db = DB()
    