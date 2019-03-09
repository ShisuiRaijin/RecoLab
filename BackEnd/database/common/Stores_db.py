import sqlite3

from BackEnd.resources.Tienda.Store import Store
from .Base_db import Base_db

class Stores_DB:

    """Permite interactuar con la talba tiedas"""

    def __init__(self, db):
        if not isinstance(db, Base_db):
            raise ValueError("supply a Base_db object")

        self.data_base = db
        self.cursor = db.cursor

    def commit(self):
        self.data_base.commit()

    def add_store(self, store):

        """Recibe un objeto de la clase Store y permite insertar sus datos en la
        tabla tiendas."""

        store_data = [store.nombre_tienda, store.direccion_tienda,
                      store.categoria, store.imagen_portada_tienda,
                      store.contacto]

        self.cursor.execute('''INSERT INTO tiendas(
                                    nombre, direccion, 
                                    categoria, ruta_imagen,
                                    contacto) 
                                    VALUES (?,?,?,?,?);
                            ''', store_data)
        self.commit()

    def update_store(self, id_tienda, nombre_columna, datos_nuevos):

        """Modifica los datos almacenados en la base de datos, correspondientes
        al id de la tienda, necesariamente se deben pasar los tres parámetros
        requeridos, id de la tienda, nombre de la columna a modificar y el dato nuevo."""

        try:
            self.cursor.execute("UPDATE tiendas SET {} = ? WHERE id_tienda = ?;"
                                .format(nombre_columna), [datos_nuevos, id_tienda])
            self.commit()
        except sqlite3.OperationalError:
            return False

    @staticmethod
    def stores_parser(stores):

        """Se utiliza internamente, toma una lista con los resultados de una consulta a
        la tabla tiendas y devuelve una lista de objetos Store"""

        store_list = []

        for records in stores:
            store = Store(records[0], records[1],
                          records[2], records[3],
                          records[4], records[5])

            store_list.append(store)

        return store_list

    @staticmethod
    def abort_if_empty(to_check):
        if to_check is None:
            raise Exception("aborting!")

        if to_check is int:
            if to_check == 0:
                raise Exception("aborting!")

        if to_check is str:
            if to_check == 'None':
                raise Exception("aborting!")

    def get_store(self, store_id):
        """Extrae los datos de la tabla tiendas referentes al parámetro id.

        El cual debe recibir necesariamente, retorna un objeto de clase Store
        generado a partir de los datos obtenidos, se puede almacenar en una variable
        que se debe asignar en la declaración
        Ej: tienda_recuperada=Base_db.extraer_tienda(id)
        Si la busqueda no obtiene resultados devuelve un objeto por Store por defecto
        """

        self.cursor.execute("SELECT * FROM tiendas WHERE id_tienda = ?;", [store_id])
        store_data = self.cursor.fetchone()

        # verifica que la consulta devuelva algun dato
        self.abort_if_empty(store_data)

        store = Store(store_data[1], store_data[2],
                      store_data[3], store_data[4],
                      store_data[5], store_data[6])
        return store

    def get_n_store_order(self, n=10, contiene ='', orden='desc',
                          columna='nombre||direccion||categoria||contacto'):

        """Devuelve 10 ultimas tiendas, puede buscar coincidencia en columnas y variar el orden.
        Acepta parametros: n, orden, contiene y columna.El parametro n debe ser un
        numero entero representa la cantidad maxima de objetos a devolver, orden puede ser
        'desc' (descendente),'asc'(ascendente) o 'aleatorio'; 'contiene' representa
        el contenido que se desea buscar y 'columna' el nombre de la columna en la tabla.
        Devuelve una lista de Tiendas ordenada segun el parametro 'orden'.
        """

        if (columna != 'nombre' and columna != 'direccion' and
            columna != 'categoria' and columna != 'contacto'):
            columna='nombre||direccion||categoria||contacto'

        if orden != 'desc' and orden != 'asc' and orden != 'aleatorio':
            orden = 'desc'

        if orden == "aleatorio":
            self.cursor.execute("SELECT * FROM tiendas WHERE {} LIKE '%{}%' ORDER BY random() LIMIT ?;"
                                .format(columna, contiene), [n])
        else:
            self.cursor.execute("SELECT * FROM tiendas WHERE {} LIKE '%{}%' ORDER BY id_tienda {} LIMIT ?;"
                                .format(columna, contiene, orden), [n])

        stores_data = self.cursor.fetchall()

        self.abort_if_empty(stores_data)
        return self.stores_parser(stores_data)

    def get_all_stores(self):
        """Devuelve una lista de objetos de todas las tiendas_data almacenadas en la base
        de datos"""

        self.cursor.execute("SELECT * FROM tiendas")
        stores_data = self.cursor.fetchall()
        self.abort_if_empty(stores_data)
        return self.stores_parser(stores_data)

    def delete_store(self, id_store):
        """Borra los datos almacenados en la base de datos, correspondientes al id de
        la tienda, necesariamente se debe pasar el parámetro requerido id de la tienda
        a borrar"""

        try:
            self.cursor.execute("DELET FROM productos WHERE id_tienda madre = ?", [id_store])
            self.cursor.execute("DELETE FROM tiendas WHERE id_tienda = ?;", [id_store])
            self.commit()
        except sqlite3.IntegrityError:
            raise Exception("error deleting store")
