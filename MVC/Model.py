import sqlite3
from tools import *

from datetime import datetime as dt
# En el modelo, definimos el manejo de las transacciones sys-bd

RUTA_DB = 'D:\\Escritorio\\Teo\\ParkingTeo.db'


class Model:

    def __init__(self):

        self.dbCon = sqlite3.connect(RUTA_DB, check_same_thread=False)

    def ingresoVehiculo(self, Placa):

        # capturo los datos y lanzo la Query para almacenar el ingreso
        self.vehiculoExiste(Placa)
        dbCur = self.dbCon.cursor()  # Instanciar el cursor para hacer consultas

        query = 'SELECT TIPO FROM VEHICULO WHERE PLACA = {}'.format(
            '"'+Placa+'"')
        dbCur.execute(query)
        Tipo = dbCur.fetchone()[0]

        disponible, cupo = self.cupoDisponible(Tipo)
        #print("El cupo es ", cupo, disponible)
        if disponible:
            string0 = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            # string0 = "2021-05-23 09:10:33"
            string1 = 'Insert into Ingreso values({},{})'.format(
                '"'+Placa+'"', '"'+string0+'"')

            try:
                dbCur.execute(string1)
                dbCur.execute('UPDATE PARQUEADERO SET LIBRE ={} WHERE TIPO = {}'.format(
                    cupo-1, '"'+Tipo+'"'))
                dbCur.execute("commit")
                print(
                    "El ingreso del vehiculo fue exitoso\n...Generando ticket de ingreso...")

            except Exception as ex:
                if type(ex) == sqlite3.IntegrityError:
                    print(
                        "El vehiculo ya figura como ingresado.....\n Verifique la placa a ingresar e intente nuevamente ")
                else:
                    print(ex, type(ex))

            finally:
                dbCur.close()
        else:
            print("No hay lugar de parqueo disponible en el momento...")

    def salidaVehiculo(self, Placa):
        # capturo los datos  y lanzo la Query para hacer la operacion de salida
        Tipo = self.getTipo(Placa)
        # print(" el tipo es ", Tipo)

        dbCur = self.dbCon.cursor()  # Instanciar el cursor para hacer consultas

        string1 = 'select HoraIngreso from Ingreso where Placa = {}'.format(
            '"'+Placa+'"')
        string2 = 'select ValorHora from Tarifa where Tipo = {}'.format(
            '"'+Tipo+'"')
        string3 = 'delete from Ingreso where Placa ="'+Placa+'"'

        dbCur.execute(string1)
        try:
            fechaIngreso = dbCur.fetchone()[0]
            dbCur.execute(string2)
            valor = dbCur.fetchone()[0]
            print("Valor a pagar $" + str(calcularCobro(fechaIngreso, valor)))

            # Una vez calculado el valor a pagar, se debe eliminar ese registro de la tabla de ingreso
            _, cupo = self.cupoDisponible(Tipo)
            try:
                dbCur.execute(string3)
                dbCur.execute('UPDATE PARQUEADERO SET LIBRE ={} WHERE TIPO = {}'.format(
                    cupo+1, '"'+Tipo+'"'))
                dbCur.execute("commit")
            except Exception as ex:
                print("No se pudo ejecutar la eliminacion del regitro"+ex+type(ex))

        except:
            print("El vehiculo a consultar no figura como ingresado,\npor favor rectifique la placa e intente nuevamente")
        finally:
            dbCur.close()

    def editarCliente(self):
        pass

    def getTipo(self, Placa):
        Tipo = ""
        dbCur = self.dbCon.cursor()  # Instanciar el cursor para hacer consultas
        string1 = 'select Tipo from Vehiculo where Placa = {}'.format(
            '"'+Placa+'"')

        dbCur.execute(string1)
        try:
            Tipo = dbCur.fetchone()[0]
        except:
            print("El vehiculo en consulta no se encuentra registrado...")

        finally:
            dbCur.close()
            return Tipo

    def vehiculoExiste(self, Placa):
        # Recibo una placa y valido si ya está registrado, sino se procede a guardar el vehiculo
        dbCur = self.dbCon.cursor()  # Instanciar el cursor para hacer consultas
        string1 = 'Select * from Vehiculo where  Placa = {}'.format(
            '"'+Placa+'"')
        dbCur.execute(string1)
        try:
            vehiculo = dbCur.fetchone()[0]

        except:
            print(
                "El vehiculo aún no se encuentra registrado...\nIniciando proceso de registro...")
            self.registrarVehiculo(Placa)
        finally:
            dbCur.close()

    def clienteExiste(self, Placa, Cedula):

        # Recibo una cedula  y valido si ya está  el cliente, sino se procede a guardar el cliente
        dbCur = self.dbCon.cursor()  # Instanciar el cursor para hacer consultas
        string1 = 'SELECT NOMBRE,TELEFONO FROM CLIENTE WHERE ID = {}'.format(
            '"'+Cedula+'"')
        dbCur.execute(string1)

        try:
            Nombre, Telefono = dbCur.fetchone()
            query = 'INSERT INTO CLIENTE VALUES({},{},{},{})'.format(
                '"'+Cedula+'"', '"' + Placa+'"', '"'+Nombre+'"', str(Telefono))
            print("my query is : ", query)

            try:
                dbCur.execute(query)
                print("El vehiculo fue agregado al cliente existente...")
                dbCur.execute("commit")
            except:
                print("No se pudo agregar el Vehiculo al cliente existente...")

        except:
            print(
                "El cliente aún no se encuentra registrado...\nIniciando proceso de registro...")
            self.registrarCliente(Placa, Cedula)
        finally:
            dbCur.close()

    def registrarVehiculo(self, Placa):
        dbCur = self.dbCon.cursor()
        Marca = str(input("Ingrese la Marca...\n")).upper()
        Color = str(input("Ingrese el Color...\n")).upper()
        Tipo = str(input("Ingrese el Tipo...\n")).upper()
        Cedula = str(input("Ingrese la cedula del cliente...\n"))

        string2 = 'INSERT INTO VEHICULO VALUES({},{},{},{})'.format(
            '"'+Placa+'"', '"' + Marca+'"', '"'+Color+'"', '"'+Tipo+'"')

        try:
            dbCur.execute(string2)
            dbCur.execute("commit")
            print("Vehiculo registrado satisfactoriamente\n")
            # Se debe validar si el cliente ya existe, para no solicitar los datos nuevamente
            self.clienteExiste(Placa, Cedula)

        except Exception as ex:
            print("No se pudo agregar el vehiculo a la BD...", ex, type(ex))
        finally:
            dbCur.close()

    def registrarCliente(self, Placa, Cedula):

        dbCur = self.dbCon.cursor()
        Nombre = str(input("Ingrese el Nombre del cliente...\n")).upper()
        Telefono = int(input("Ingrese el teléfono...\n"))
        string3 = 'INSERT INTO CLIENTE VALUES({},{},{},{})'.format(
            '"'+Cedula+'"', '"' + Placa+'"', '"'+Nombre+'"', str(Telefono))
        if Nombre != "":
            try:
                dbCur.execute(string3)
                dbCur.execute("commit")
                print("Cliente agregado correctamente")
            except:
                print("No se pudo agregar el Cliente")
            finally:
                dbCur.close()
        else:
            dbCur.close()

    def cupoDisponible(self, Tipo):
        # Recibe un tipo de vehiculo y valida si hay disponibilidad del total
        dbCur = self.dbCon.cursor()
        flag = False
        string1 = 'SELECT LIBRE FROM PARQUEADERO WHERE TIPO = {}'.format(
            '"'+Tipo+'"')
        try:
            dbCur.execute(string1)
            libre = dbCur.fetchone()[0]
            if libre > 0:
                flag = True
        except:
            print("Falló la consulta de espacios libres")
        finally:
            dbCur.close()
            return (flag, libre)


# a = Model()
# a.ingresoVehiculo("VWV50D")
