from Model import Model


def mainC():

    m = Model()
    op = 0
    while(op != 3):
        print("\n-----------------------\n")
        print("Parking Agente P \n")
        print("1.Ingreso Vehiculo\n")
        print("2.Salida de Vehiculo\n")
        print("3.Desconectar\n")
        op = int(input("Ingrese opcion: "))

        print('\n')
        if op == 1:
            Placa = str(input("Ingrese la placa...\n")).upper()
            m.ingresoVehiculo(Placa)
        elif op == 2:
            Placa = str(input("Ingrese la placa...\n")).upper()
            m.salidaVehiculo(Placa)
        elif op == 3:
            break
        _ = input("presione cualquier tecla para continuar")


mainC()
