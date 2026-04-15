#importa biblioteca os para el comando (os.system("cls") que sirve para limpiar la consola;) y para el analisis de archivos
import os

import csv

#Biblioteca para manejar archivos .json
import json
#Biblioteca para pedir y analizar fechas
from datetime import datetime,timedelta

#Crea el archivo si no existe
if not os.path.exists("Contratos.json"):
    with open("Contratos.json", "w") as archivo:
        json.dump({}, archivo)

#Funcion poner titulo
def titulo():
    print("-----------------------------------")
    print("\t     Contratos")
    with open("Contratos.json", "r") as archivo:
        Contenido=json.load(archivo)
        Contratos=len(Contenido) 
    print(f"      Cantidad de contratos: {Contratos}")      
    print("-----------------------------------")

#Funcion salir del programa
def salir():
    while True:
        try:
            Seguir=str(input("Desea salir del programa? digita si/no\n")).lower()
            if Seguir in ("si","no"):
                break
            else:
                print("Ingrese si/no")
        except Exception:
            print("Error al digitar")
    return Seguir

#Funcion salir en cualquier momento
def input_seguro(mensaje=""):
    dato = input(mensaje)
    if dato.lower() == "salir":
        return None
    return dato

#Funcion para pedir numero de contrato y validar
def numero_contrato():
    Numero_Contrato=(input_seguro("Ingrese su numero de contrato:\n"))
    if Numero_Contrato is None:
        return None
    while (Numero_Contrato.isdigit()==False):
        Numero_Contrato=(input_seguro("Ingrese su numero de contrato:\n"))
        if Numero_Contrato is None:
            return None
    Numero_Contrato=int(Numero_Contrato)
    while Numero_Contrato<=0:
        Numero_Contrato=(input_seguro("Ingrese su numero de contrato:\n"))
        if Numero_Contrato is None:
            return None
    Numero_Contrato=str(Numero_Contrato)
    return Numero_Contrato

#Funcion para pedir el valor del contrato y verificar
def valor_Contrato():
    while True:
        try:
            Valor_Contrato=(input_seguro("Engrese el valor del contrato"))
            if Valor_Contrato is None:
                return None    
            Valor_Contrato=float(Valor_Contrato)

            if Valor_Contrato>0:
                        return Valor_Contrato
            else:
                print("El valor debe ser mayor que 0.")
        except ValueError:
            print("Ingrese un número válido.")
        
#Funcion para pedir fecha de inicio y final de contrato y verificar que sean validas
def pedir_Fechas():
    while True:
        dato_inicio = input_seguro("Ingrese la fecha de inicio (dd mm aaaa): ")
        if dato_inicio is None:
            return None

        try:
            Fecha_inicio = datetime.strptime(dato_inicio, "%d %m %Y")
            break
        except ValueError:
            print("Formato inválido. Use: dd mm aaaa")

    while True:
        dato_fin = input_seguro("Ingrese la fecha de terminación (dd mm aaaa): ")
        if dato_fin is None:
            return None

        try:
            Fecha_term = datetime.strptime(dato_fin, "%d %m %Y")
            break
        except ValueError:
            print("Formato inválido. Use: dd mm aaaa")

    return Fecha_inicio, Fecha_term

#Compara las fechas pedidas anteriormente con la fecha actual para determinar el estado
def estado_contrato(fecha_inicio, fecha_term):
    fecha_hoy = datetime.today()
    if fecha_inicio <= fecha_hoy < fecha_term:
        return "ACTIVO"
    elif fecha_hoy >= fecha_term:
        return "TERMINADO"
    else:
        return "SUSPENDIDO"

#Pide el correo y lo verifica
def pedir_correo():
    while True:
        correo = input_seguro("Ingrese su correo electrónico:\n")
        if correo is None:
            return None 
        if "@" in correo and "." in correo:
            return correo
        else:
            print("Correo inválido. Intente de nuevo.")

#Funcion secundaria para registrar contratos
def registrar_contrato():
    os.system("cls")
    titulo()
    #Usa la funcion para pedir el numero de contrato
    Numero_Contrato=numero_contrato()
    if Numero_Contrato is None:
        return "no" 
    #Abre el archivo "contratos.json" y saca su contenido a la variable contenido
    with open("Contratos.json", "r") as archivo:
        contenido = json.load(archivo)  

    #Verifica que el numero de contrato no este ya en el archivo
    while Numero_Contrato in contenido:
        print("El numero de contrato ya esta en el sistema, ingresa otro número")
        Numero_Contrato=numero_contrato()
        if Numero_Contrato is None:
            return "no" 
    #Pide el nombre del contratista
    Nombre_Contratista=str(input_seguro("Ingrese su nombre"))
    if Nombre_Contratista is None:
        return "no" 
        
    #Pide el objetivo del contrato
    obj_contrato=str(input_seguro("¿Cuál es el objetivo de su contrato?"))
    if obj_contrato is None:
        return "no" 

    #Usa la funcion pedir_Fechas para su respectivo uso

    fechas=pedir_Fechas()
    if fechas is None:
        return "no" 
    fecha_inicio,fecha_term=fechas
    while fecha_inicio>=fecha_term:
        print("ingrese una fecha valida")
        fechas=pedir_Fechas()
        if fechas is None:
            return "no" 
        fecha_inicio,fecha_term=fechas    
    fecha_inicio_str = fecha_inicio.strftime("%d/%m/%Y")
    fecha_term_str = fecha_term.strftime("%d/%m/%Y")
        
    #Pide el Valor del contrato
    Valor_Contrato=valor_Contrato()
    if Valor_Contrato is None:
        return "no" 
    #Pide el nombre del supervisor
    Nombre_Supervisor=str(input_seguro("Ingrese el nombre del supervisor"))
    if Nombre_Supervisor is None:
        return "no" 

    #Verifica estado del contrato
    Estado_Contrato=estado_contrato(fecha_inicio=fecha_inicio,fecha_term=fecha_term)

    Correo=pedir_correo()
    if Correo is None:
        return "no" 

    #Agrega los valores pedidos anteriormente al archivo "Contratos.json"
    contenido[Numero_Contrato]=(Nombre_Contratista),(obj_contrato),(fecha_inicio_str),(fecha_term_str),(Valor_Contrato),(Nombre_Supervisor),(Estado_Contrato),(Correo),[]
    with open("Contratos.json", "w") as archivo:
        json.dump(contenido,archivo)
    Seguir=salir()
    return Seguir
        
def listar_contratos():
    os.system("cls")
    titulo()

    with open("Contratos.json", "r") as archivo:
        contratos = json.load(archivo)

    lista = []

    for num in contratos:
        nombre = contratos[num][0]
        lista.append([nombre.lower(), num, contratos[num]])

    # Ordena por el PRIMER dato → el nombre
    lista.sort()

    print(" LISTA DE CONTRATOS (A-Z)")

    for item in lista:
        _, num, datos = item  # _ porque no necesitamos el nombre en minúscula
        print(f"Número: {num}")
        print(f"Contratista: {datos[0]}")
        print("-" * 30)

    Seguir=salir()
    return Seguir       
        
def busqueda():
    os.system("cls")
    titulo()
    with open("Contratos.json","r") as archivo:
        contratos=json.load(archivo)
        num=numero_contrato()
        if num is None:
            return "no"
    if num in contratos:
        print("numero de contrato encontrado")
       
        datos=contratos[num]

        print(f"Número: {num}")
        print(f"Contratista: {datos[0]}")
        print(f"Objetivo: {datos[1]}")
        print(f"Fecha inicio: {datos[2]}")
        print(f"Fecha fin: {datos[3]}")
        print(f"Valor: {datos[4]}")
        print(f"Supervisor: {datos[5]}")
        print(f"Estado: {datos[6]}")
        print(f"Correo: {datos[7]}")
    else:
        print("Numero de contrato no encontrado")
    Seguir=salir()
    return Seguir
        
#Funcion secundaria para mostrar las estadisticas rapidas
def estadisticas_rapidas():
    os.system("cls")
    titulo()
    with open("Contratos.json","r") as archivo:
        Contenido=json.load(archivo)
    Activo=0
    Terminado=0
    Suspendido=0
    Valor_total=0
    #Cuenta cuantos contratos hay en cada estado
    for i in (Contenido):
        contrato=Contenido[i][6]
        if contrato=="ACTIVO":
            Activo+=1
        elif contrato=="TERMINADO":
            Terminado+=1
        else:
            Suspendido+=1
    print("Total contratos por estado:\n"
        f"\tTerminados: {Terminado}\n"
        f"\tActivos: {Activo}\n"
        f"\tSuspendidos: {Suspendido}")
    
    #Valor todal contratado
    for i in Contenido:
        Valor_total+=Contenido[i][4]
    print(f"El valor total contratado es de: {Valor_total}")
    
    #Promedio del valor de los contratos
    Valor_promedio=Valor_total/len(Contenido)
    print(f"El valor promedio contratado es de: {Valor_promedio}")
    
    valores = [Contenido[i][4] for i in Contenido]
    mayor = max(valores)
    menor = min(valores)
    print(f"El valor maximo contratado es de: {mayor}")
    print(f"El valor minimo contratado es de: {menor}")
    
    hoy = datetime.today()
    limite = hoy + timedelta(days=30)

    for i in Contenido:
        fecha_fin_str = Contenido[i][3]
        fecha_fin = datetime.strptime(fecha_fin_str, "%d/%m/%Y")

        if hoy <= fecha_fin <= limite:
            print("Contrato:", i)
            print("Fecha fin:", fecha_fin_str)
            print("----------------------")
            
    Seguir=salir()
    return Seguir
        
def registro_seguimiento():
    os.system("cls")
    titulo()
    with open("Contratos.json","r") as archivo:
        Contenido=json.load(archivo)
        while True:
            try:
                contrato=(input_seguro("Ingrese el contrato al que desea agregarle un seguimiento"))
                if contrato is None:
                    return "no"
                if contrato in Contenido:
                    break
                else:
                    print("Ingresa un contrato definido")
            except Exception:
                print("Error al digitar")
             
    while True:
        try:
            Opcion=int(input("Que desea hacer?\n1.Agregar seguimiento\n2.Listar seguimientos"))         
            if 0<Opcion<=2:
                break
            else:
                print("Digite un dato del 1 al 2")
        except Exception:
            print("Error al digitar")
            
    if Opcion==1:                    
        Fecha_hoy = datetime.today().strftime("%d/%m/%Y")    
        Descripcion=str(input("Escriba una descripcion corta del seguimiento: "))
        
        while True:
            try:
                Nivel_avance=int(input("Nivel de  avance 0-100%"))
                if 0<=Nivel_avance<=100:
                    break
                else:
                    print("Escriba el avance de 0 a 100")
            except Exception:
                print("Error al digitar") 
        Observacion=str(input("Escriba una observacion adicional: "))
        
        Contenido[contrato][8].append((Fecha_hoy,Descripcion,Nivel_avance,Observacion))               
                    
        with open("Contratos.json", "w") as archivo:
            json.dump(Contenido,archivo)
              
    if Opcion==2:
        Lista=[]
        suma=0
        for i in range(len(Contenido[contrato][8])):
            Seguimiento=Contenido[contrato][8][i]
            Lista.append(Seguimiento)   
        for i in Lista:
            suma+=i[2]
            print(i)
        Promedio=suma/(len(Contenido[contrato][8]))    
        print(f"El promedio de avance del contrato es de:{Promedio}")                            
                    
                    
    Seguir=salir()
    return Seguir
        
def exportar_contratos():
    with open("Contratos.json", "r") as archivo:
        contenido = json.load(archivo)

    with open("contratos.csv", "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)

        # Encabezados
        writer.writerow(["Numero", "Contratista", "Objeto", "Fecha Inicio","Fecha Fin", "Valor", "Supervisor", "Estado", "Correo"])

        for num in contenido:
            datos = contenido[num]

            writer.writerow([num,datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6],datos[7]])
            
def exportar_seguimientos():
    with open("Contratos.json", "r") as archivo:
        contenido = json.load(archivo)

    with open("seguimientos.csv", "w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)

        # Encabezados
        writer.writerow(["Numero Contrato", "Fecha", "Descripcion","Nivel Avance", "Observacion"])

        for num in contenido:
            seguimientos = contenido[num][8]

            for seg in seguimientos:
                writer.writerow([num,seg[0],seg[1],seg[2],seg[3]])
                
#Funcion principal
def main():
    os.system("cls")
    titulo()
    while True:
        try:
            Opcion = int(input("Ingrese la opcion que desea:\n"
                "1. Registrar Contrato\n"
                "2. Listar Contratos\n"
                "3. Buscar Contrato\n"
                "4. Registro de seguimiento\n"
                "5. Estadisticas Rapidas\n"
                "6. Exportar csv\n"
                "7. Salir del programa\n"
                "Opcion elegida:\t"))
            if 1 <= Opcion <= 7:
                break
            else:
                print("Ingrese una opción entre 1 y 7.")

        except ValueError:
            print("Ingrese un dato válido.")
    if Opcion==1:
        Seguir=registrar_contrato()
    elif Opcion==2:
        Seguir=listar_contratos()
    elif Opcion==3:
        Seguir=busqueda()
    elif Opcion==4:
        Seguir=registro_seguimiento()
    elif Opcion==5:
        Seguir=estadisticas_rapidas()
    elif Opcion == 6:
        exportar_contratos()
        exportar_seguimientos()
        print("Archivos CSV exportados ")
        Seguir = salir()
    else:
        Seguir="no"
    return Seguir,Opcion
        
#Variables que van a definir si el sistema sigue funcionando o no, estas seran cambiadas a lo largo del programa        
Seguir="no"
Opcion=0
while Seguir=="no" and Opcion!=7:
    Seguir,Opcion=main()
os.system("cls")