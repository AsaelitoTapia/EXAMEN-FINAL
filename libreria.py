# Clase Cliente
# Por default el cliente inicia con 0 penalizaciones
class Cliente:
    def __init__(self, id_usuario, nombre, apellidos, penalizaciones=0):
        # Encapsulamiento: atributos privados
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__penalizaciones = penalizaciones

    # Métodos para acceder a los atributos privados (encapsulamiento)
    def get_id_usuario(self):
        return self.__id_usuario

    def get_nombre(self):
        return self.__nombre

    def get_apellidos(self):
        return self.__apellidos

    def get_penalizaciones(self):
        return self.__penalizaciones

    def actualizar_penalizacion(self, cantidad):
        self.__penalizaciones += cantidad


# Clase Libros
class Libro:
    def __init__(self, id_libro, unidades, nombre, autor, editorial):
        # Encapsulamiento: atributos privados
        self.__id_libro = id_libro
        self.__unidades = unidades
        self.__nombre = nombre
        self.__autor = autor
        self.__editorial = editorial

    # Métodos para acceder a los atributos privados (encapsulamiento)
    def get_id_libro(self):
        return self.__id_libro

    def get_unidades(self):
        return self.__unidades

    def get_nombre(self):
        return self.__nombre

    def get_autor(self):
        return self.__autor

    def get_editorial(self):
        return self.__editorial

    def actualizar_catalogo(self, nuevas_unidades):
        self.__unidades += nuevas_unidades


# Clase LibrosDisponibles (Herencia de Libro)
class LibrosDisponibles(Libro):  # Utilización de herencia
    def __init__(self, id_libro, unidades, nombre, autor, editorial):
        super().__init__(id_libro, unidades, nombre, autor, editorial)

    # Polimorfismo: redefinición de método
    def actualizar_catalogo(self, nuevas_unidades):
        super().actualizar_catalogo(nuevas_unidades)
        if nuevas_unidades < 0:
            print(f"El catálogo ha sido actualizado. Se prestaron {-nuevas_unidades} unidades.")
        else:
            print(f"El catálogo ha sido actualizado. Se devolvieron {nuevas_unidades} unidades.")

    # Método para buscar un libro en una lista de libros disponibles
    @staticmethod
    def buscar_libro(libros, criterio):
        for libro in libros:
            if libro.get_nombre().lower() == criterio.lower() or str(libro.get_id_libro()) == criterio:
                return libro
        return None


# Clase Catalogo
class Catalogo:
    def __init__(self):
        # Encapsulamiento: atributo privado
        self.__libros = []
        self.__prestamos = {}

    def agregar_libro(self, libro):
        self.__libros.append(libro)

    def checar_libros(self):
        for libro in self.__libros:
            print(f"{libro.get_nombre()} - {libro.get_unidades()} unidades disponibles")

    def mostrar_info(self):
        for libro in self.__libros:
            print(f"ID: {libro.get_id_libro()}, Nombre: {libro.get_nombre()}, Autor: {libro.get_autor()}, Editorial: {libro.get_editorial()}")

    def recibo(self, cliente, libro):
        print(f"Recibo:\nCliente: {cliente.get_nombre()} {cliente.get_apellidos()}\nLibro: {libro.get_nombre()}")
        self.__prestamos[cliente.get_id_usuario()] = libro.get_nombre()

    def actualizar_cuenta(self, cliente_id):
        if cliente_id in self.__prestamos:
            print(f"Cliente con ID {cliente_id} tiene en préstamo: {self.__prestamos[cliente_id]}")
        else:
            print(f"Cliente con ID {cliente_id} no tiene libros en préstamo.")


# Clase Permisos
class Permisos:
    def __init__(self, id_cliente, penalizaciones=0):
        # Encapsulamiento: atributos privados
        self.__id_cliente = id_cliente
        self.__penalizaciones = penalizaciones

    def get_id_cliente(self):
        return self.__id_cliente

    def get_penalizaciones(self):
        return self.__penalizaciones

    def actualizar_cuenta(self):
        if self.__penalizaciones > 3:
            print(f"El cliente con ID {self.__id_cliente} tiene demasiadas penalizaciones y no puede realizar préstamos.")
            return False
        print(f"El cliente con ID {self.__id_cliente} puede realizar préstamos.")
        return True


# Caso de usos

if __name__ == "__main__":
    try:
        # Crear cliente
        cliente1 = Cliente(1, "Juan", "Pérez")
        permisos_cliente1 = Permisos(cliente1.get_id_usuario(), penalizaciones=2)

        # Verificar si el cliente puede realizar préstamos
        if not permisos_cliente1.actualizar_cuenta():
            raise PermissionError("No se puede realizar el préstamo debido a penalizaciones.")  # Manejo de errores

        # Crear libros y catálogo
        libro1 = LibrosDisponibles(101, 3, "Cien Años de Soledad", "Gabriel García Márquez", "Editorial X")
        libro2 = LibrosDisponibles(102, 5, "Don Quijote de la Mancha", "Miguel de Cervantes", "Editorial Y")

        catalogo = Catalogo()
        catalogo.agregar_libro(libro1)
        catalogo.agregar_libro(libro2)

        # Buscar un libro
        criterio = "Cien Años de Soledad"
        libro_buscado = LibrosDisponibles.buscar_libro([libro1, libro2], criterio)

        if libro_buscado:
            print(f"\nSe encontró el libro: {libro_buscado.get_nombre()} con {libro_buscado.get_unidades()} unidades disponibles.")
            catalogo.recibo(cliente1, libro_buscado)
            libro_buscado.actualizar_catalogo(-1)
            catalogo.actualizar_cuenta(cliente1.get_id_usuario())
        else:
            print(f"\nEl libro '{criterio}' no se encuentra disponible en el catálogo.")

        # Mostrar catálogo actualizado
        print("\nCatálogo actualizado:")
        catalogo.checar_libros()

    except (ValueError, PermissionError) as e:
        print(f"Error: {e}")  # Manejo de errores

