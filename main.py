import os.path as path
import funcionesydeclaraciones as func
"""
HECHO POR:
PEDRO,REYMAR,MARTIN,JOHNNY
"""
if path.exists("BIBLIOTECA.bin"):
    func.Matriz_Biblioteca = func.cargar_archivo("BIBLIOTECA.bin")
if path.exists("REGISTRO.bin"):
    func.Matriz_Registro = func.cargar_archivo("REGISTRO.bin")

if path.exists("EGRESOS.bin"):
    func.Matriz_Egresos = func.cargar_archivo("EGRESOS.bin")

salir = False
print(f"\n{func.separador}\n\n         BIENVENIDO!\n")
while not salir:
    entrada = func.pedir_opcion(
        f"\n{func.separador}\nOpciones (ej: presiona '1' para mostrar los libros disponibles):\n1) Para mostrar todos los libros disponibles.\n2) Para buscar un libro por su titulo.\n3) Para buscar libros por su autor.\n4) Para buscar libros por su ISBN.\n5) Para pedir un libro.\n6) Para devolver un libro.\n7) Para salir.\n\n"
    )
    match entrada:
        case 1:  # Mostrar libros
            func.mostrar_libros()
        case 2:  # Buscar por titulo
            titulo_libro = input(
                "\nPor favor ingresa el titulo del libro que deseas buscar\n\n->: "
            )
            func.ord_por_titulo()
            libro_pos = func.buscar_por_titulo(titulo_libro)
            func.ejecutar_opcion(libro_pos )
        case 3:  # Buscar por autor
            func.ord_por_autor()
            libros = func.buscar_por_autor(func.pedir_nombre_autor())
            if libros != -1:
                func.ejecutar_opcion(func.elegir_libro(libros))
            #
        case 4:  # Buscar por ISBN
            libro_pos = func.buscar_por_isbn(func.pedir_isbn())
            func.ejecutar_opcion(libro_pos)
        case 5:  # Pedir libro
            buscar_libro = 0
            while (buscar_libro < 1 or buscar_libro > 3):
                buscar_libro = func.pedir_opcion("Como deseas buscar el libro?\n1) Por titulo.\n2) Por autor.\n3) Por ISBN.\n4) Para salir.\n\n")
                match buscar_libro:
                    case 1:
                        func.ord_por_titulo()
                        libro_pos = func.buscar_por_titulo(input("\nPor favor ingresa el titulo del libro que deseas buscar\n\n->: "))
                        func.prestar_libro(libro_pos)

                    case 2:
                        func.ord_por_autor()
                        libros = func.buscar_por_autor(func.pedir_nombre_autor())
                        if libros != -1:
                            func.prestar_libro(func.elegir_libro(libros))
                    case 3:
                        libro_pos = func.buscar_por_isbn(func.pedir_isbn())
                        
                        func.prestar_libro(libro_pos)
                    case 4:
                        break
                    case _:
                        print(f"\n\n{func.separador}\n\nPor favor selecciona una opción valida.\n\n{func.separador}\n\n")
        case 6:  # Devolver libro
            opcion = 0
            while (opcion < 1 or opcion > 3):
                opcion = func.pedir_opcion("Como deseas buscar el libro?\n1) Por titulo.\n2) Por ISBN.\n3) Para salir.\n\n")
                match opcion:
                    case 1: # Por titulo
                        func.ord_por_titulo()
                        libro_pos = func.buscar_por_titulo(input("\nPor favor ingresa el titulo del libro que deseas buscar\n\n->: "))
                        func.devolver_libro(libro_pos)
                    case 2: # Por ISBN
                        libro_pos = func.buscar_por_isbn(func.pedir_isbn())
                        func.devolver_libro(libro_pos)
                    case 3:
                        break
                    case _:
                        print(f"\n\n{func.separador}\n\nPor favor selecciona una opción valida.\n\n{func.separador}\n\n")

        case 7:  # Salir
            salir = True
            func.guardar_archivo("BIBLIOTECA.bin",func.Matriz_Biblioteca)
            func.guardar_archivo("REGISTRO.bin",func.Matriz_Registro)
            func.guardar_archivo("EGRESOS.bin",func.Matriz_Egresos)
            print("\nGracias por usar la biblioteca! Hasta luego!")
        case _:
            print("\nPor favor selecciona una opción valida.\n\n")
