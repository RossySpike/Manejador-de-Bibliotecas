import time
from enum import Enum
import re
import pickle

separador = "-" * 30


class Libro_attrib(Enum):
    TITULO, AUTOR, CATEGORIA, ISBN, ESTADO = range(5)


class Estado(Enum):
    DISPONIBLE, NO_DISPONIBLE = range(2)

class Registro_atrib(Enum):
    FECHA, USUARIO, ACCION, ISBN = range(4)

# Donde cada fila es un libro mientras que una columna contiene sus atributos
Matriz_Biblioteca = []

# Contiene un registro de todos los libros prestados/devueltos, donde cada fila es un evento y cada columna contiene los datos de dicho evento 
Matriz_Registro = []

# Contiene una lista de todos las personas que han egresado libros, cada fila es un egreso, donde la columna contiene los datos de dicho egreso
# los cuales son: para columna 0 -> el nombre del usuario; para columna 1->el isbn del libro
patron_isbn = re.compile(r"\d{3}-\d{2}-\d{3}-\d{4}-\d{1}")

patron_nombre = r"^[A-Za-z]+,\s[A-Za-z]+$"

def validar_entrada_numero(entrada):
    patron = re.compile(r"[-+]?\d+$")
    return patron.match(entrada) is not None


def pedir_opcion(mensaje):
    while True:
        print(mensaje)
        entrada = input("->: ")
        if validar_entrada_numero(entrada):
            return int(entrada)
        print("\n\nPOR FAVOR INGRESA UNA OPCION VALIDA\n\n")


def ord_por_titulo():
    for i in range(1, len(Matriz_Biblioteca)):
        key = Matriz_Biblioteca[i]
        j = i - 1
        while (
            j >= 0
            and Matriz_Biblioteca[j][Libro_attrib.TITULO.value]
            > key[Libro_attrib.TITULO.value]
        ):
            Matriz_Biblioteca[j + 1] = Matriz_Biblioteca[j]
            j -= 1
        Matriz_Biblioteca[j + 1] = key


def ord_por_autor():
    for i in range(1, len(Matriz_Biblioteca)):
        key = Matriz_Biblioteca[i]
        j = i - 1
        while (
            j >= 0
            and Matriz_Biblioteca[j][Libro_attrib.AUTOR.value] > key[Libro_attrib.AUTOR.value]
        ):
            Matriz_Biblioteca[j + 1] = Matriz_Biblioteca[j]
            j -= 1
        Matriz_Biblioteca[j + 1] = key

def mostrar_libros():
    for libro in Matriz_Biblioteca:
        print(
            f"\n{separador}\nTitulo: {libro[Libro_attrib.TITULO.value]}\nAutor: {libro[Libro_attrib.AUTOR.value]}\nCategoria: {libro[Libro_attrib.CATEGORIA.value]}\nISBN: {libro[Libro_attrib.ISBN.value]}\nEstado: {libro[Libro_attrib.ESTADO.value].name}\n{separador}\n"
        )


def validar_nombre_autor(nombre):
    # El patrón regex verifica que la entrada tenga el formato 'Apellido, Nombre'
    if re.match(patron_nombre, nombre):
        print(f"\n'{nombre}' ingresado correctamente!\n")
        return True
    else:
        print(
            f"\nError! '{nombre}' no esta ingresado con el formato correcto. Asegurate que sea en este formato 'Apellido, Nombre' (sin las comillas)\n\n."
        )
        return False


def pedir_nombre_autor():
    salir = False
    while not salir:
        nombre = str(
            input(
                "\nPor favor ingresa el nombre del autor. Asegurate de que sea en este formato 'Apellido, Nombre' (sin las comillas)\n\n->: "
            )
        )
        salir = validar_nombre_autor(nombre)
    return nombre


def validar_isbn(isbn):
    if re.match(patron_isbn, isbn):
        print("\nISBN ingresado valido!\n")
        return True
    else:
        print(
            f'\nError! {isbn} ISBN incorrecto. Asegurate de usar "-" al momento de separar los elementos del ISBN\n\n'
        )
        return False


def pedir_isbn():
    salir = False
    while not salir:
        isbn = str(input("\nPor favor ingresa el ISBN\n\n->: "))
        salir = validar_isbn(isbn)

    return isbn


def buscar_por_autor(autor):
    patron = re.compile(autor, re.IGNORECASE)
    libros_pos = []
    for i in range(len(Matriz_Biblioteca)):
        if re.match(patron, Matriz_Biblioteca[i][Libro_attrib.AUTOR.value]):
            libros_pos.append(i)
            print(
                f"\n\n{separador}\nDatos del libro con autor = {autor}\nTitulo: { Matriz_Biblioteca[i][Libro_attrib.TITULO.value]}\nCategoria: {Matriz_Biblioteca[i][Libro_attrib.CATEGORIA.value]}\nISBN: {Matriz_Biblioteca[i][Libro_attrib.ISBN.value]}\nEstado: {Matriz_Biblioteca[i][Libro_attrib.ESTADO.value].name}\n"
            )
    if len(libros_pos) != 0:
        return libros_pos
    print("Libro no encontrado")
    return -1


def buscar_por_isbn(isbn):
    for i in range(len(Matriz_Biblioteca)):
        if isbn in Matriz_Biblioteca[i]:
            print(
                f"\n\n{separador}Datos del libro con ISBN = {isbn}\nTitulo: {Matriz_Biblioteca[i][Libro_attrib.TITULO.value]}\nAutor: {Matriz_Biblioteca[i][Libro_attrib.AUTOR.value]}\nCategoria: {Matriz_Biblioteca[i][Libro_attrib.CATEGORIA.value]}\nEstado: {Matriz_Biblioteca[i][Libro_attrib.ESTADO.value].name}\n"
            )
            return i
    print("Libro no encontrado")
    return -1


def buscar_por_titulo(titulo):
    patron = re.compile(titulo, re.IGNORECASE)
    for i in range(len(Matriz_Biblioteca)):
        if re.match(patron, Matriz_Biblioteca[i][Libro_attrib.TITULO.value]):
            print(
                f"\n\n{separador}Datos del libro con titulo = {titulo}\nAutor: {Matriz_Biblioteca[i][Libro_attrib.AUTOR.value]}\nCategoria: {Matriz_Biblioteca[i][Libro_attrib.CATEGORIA.value]}\nISBN: {Matriz_Biblioteca[i][Libro_attrib.ISBN.value]}\nEstado: {Matriz_Biblioteca[i][Libro_attrib.ESTADO.value].name}\n"
            )
            return i
    print("Libro no encontrado")
    return -1

def elim_egreso(isbn):
    for i in range(len(Matriz_Egresos)):
        if isbn in Matriz_Egresos[i]:
            Matriz_Egresos.pop(i)
            return 

def guardar_egreso(isbn, nombre):
    Matriz_Egresos.append([nombre,isbn])

def registrar(isbn,accion):
    print(f"\nRegistrando {accion}...")
    while True:
        usuario_nombre = input("\n\nIngresa tu nombre en el formato 'Apellido, Nombre' (sin las comillas)\n\n->: ")
        if validar_nombre_autor(usuario_nombre):
            break
    hora = time.strftime("%H:%M:%S")
    fecha = time.strftime("%d/%m/%y")
    Matriz_Registro.append([f"{fecha} {hora}",usuario_nombre,accion,isbn])
    if accion == "Egreso":
        guardar_egreso(isbn, usuario_nombre)
    if accion == "Ingreso":
        elim_egreso(isbn)


def prestar_libro(libro_pos):
    if Matriz_Biblioteca[libro_pos][Libro_attrib.ESTADO.value] == Estado.NO_DISPONIBLE:
        print("\n\nEl libro no esta disponible.")
        return
    registrar(Matriz_Biblioteca[libro_pos][Libro_attrib.ISBN.value],"Egreso")
    Matriz_Biblioteca[libro_pos][Libro_attrib.ESTADO.value] = Estado.NO_DISPONIBLE
    print("\n\nEl libro ha sido prestado.") 


def ingresar_libro():
    isbn = encontrar_mayor_isbn() + 1
    Matriz_Biblioteca.append([input("\nPor favor ingresa el titulo del libro\n\n->: ")
        ,pedir_nombre_autor(),pedir_categ(),isbn,Estado.DISPONIBLE])
    registrar(isbn,"Ingreso")

def devolver_libro(libro_pos):
    if Matriz_Biblioteca[libro_pos][Libro_attrib.ESTADO.value] == Estado.DISPONIBLE:
        print("\n\nEl libro seleccionado se encuentra disponible.")
        return
    if libro_pos == -1:
        print(
            "\n\nEl libro no se encuentra en la Matriz_Biblioteca. Ingrese sus datos para ingresar el libro a la Matriz_Biblioteca."
        )
        ingresar_libro()
        return
    registrar(Matriz_Biblioteca[libro_pos][Libro_attrib.ISBN.value],"Ingreso")
    Matriz_Biblioteca[libro_pos][Libro_attrib.ESTADO.value] = Estado.DISPONIBLE
    print("\n\nEl libro ha sido devuelto.")


def ejecutar_opcion(libro_pos):
    if libro_pos == -1:
        return
    salir = False
    while not salir:
        opcion = pedir_opcion(
            f"\n\n{separador}\n\nQue deseas hacer?\n1) Pedir libro.\n2) Devolver libro.\n3) No hacer nada.\n\n"
        )
        match opcion:
            case 1:  # Pedir libro
                prestar_libro(libro_pos)
                salir = True
            case 2:  # Devolver libro
                devolver_libro(libro_pos)
                salir = True
            case 3:  # No hacer nada
                salir = True
            case _:
                print("\nPor favor selecciona una opción valida.\n\n")


def elegir_libro(libros):
    if libros == -1:
        return
    opcion = 0
    tam_lista = len(libros)
    while opcion < 1 or opcion >= tam_lista:
        print(f"\n{separador}\nSelecciona un libro de la lista: ")
        for i in range(tam_lista):
            print(f"{i+1}) {Matriz_Biblioteca[i][Libro_attrib.TITULO.value]}")
        opcion = pedir_opcion("\nIngresa el numero del libro que deseas seleccionar\n")
    return libros[opcion - 1]

def validar_categoria(cadena):
    patron = '^[A-Z][^0-9]*$'
    
    if re.match(patron, cadena):
        return True
    else:
        print("\nError! Categoria Invalida. Asegurate de comenzar con mayusculas y que no contenga numeros\n\n")
        return False

def pedir_categ():
    while True:
        categoria = input("\nIngresa la categoria (Comienza con mayuscula y sin usar numeros)\n\n->: ")
        if validar_categoria(categoria):
            break

def obtener_digitos(isbn):
    return int("".join(re.findall(r"\d",isbn)))

def encontrar_mayor_isbn():
    mayor = 0
    for libro in Matriz_Biblioteca:
        actual = obtener_digitos(libro[Libro_attrib.ISBN.value])
        if actual > mayor:
            mayor = actual
    return mayor

def guardar_archivo(ruta,contenido):
    with open (ruta,"wb") as archivo:
        pickle.dump(contenido,archivo)

def cargar_archivo(ruta):
    with open (ruta,"rb") as archivo:
        return pickle.load(archivo)





