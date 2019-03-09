import sqlite3

class Base_db:
    """Contiene los metodos basicos para interactuar con la base de datos."""

    def __init__(self):
        self.status_db = False
        try:
            self.db = sqlite3.connect(r"BackEnd\\database\\database.db")
        except:
            raise Exception(ConnectionError("error connecting with the database"))

        try:
            self.create_tables()
        except:
            raise Exception(FileNotFoundError("cant create the database tables"))

        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()

    def close_db(self):
        self.cursor.close()
        self.commit()
        self.db.close()

    def create_tables(self):
        """Crea las tables "tiendas" y "productos" si no existen, agrega claves primarias a
        cada registro """

        tables = \
            ['''
                CREATE TABLE IF NOT EXISTS tiendas(
                    id_tienda INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE,
                    direccion TEXT NOT NULL ,
                    categoria TEXT NOT NULL,
                    ruta_imagen TEXT NOT NULL,
                    contacto TEXT NOT NULL)
            ''',

            '''
                CREATE TABLE IF NOT EXISTS productos
                (
            
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL ,
                    ruta_imagen TEXT NOT NULL,
                    precio TEXT NOT NULL,
                    id_tienda_madre INTEGER,
                
                    CONSTRAINT prod_unico UNIQUE
                    (
                        nombre,descripcion,ruta_imagen,
                        id_tienda_madre
                    )
                        
                    FOREIGN KEY (id_tienda_madre) REFERENCES tiendas(id_tienda)
                );
            ''']

        for table in tables:
            self.cursor.execute(table)
            self.commit()  # se deja abierto para uso por otras clases, mientras el objecto exista

    def __del__(self):
        self.close_db()
