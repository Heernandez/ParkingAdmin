from datetime import datetime as dt


def calcularDiferenciaHoras(horaEntrada):
    # Calcular, dada dos fechas (fecha y hora), la diferencia y decir cuantas horas transcurrieron
    # (hh:mm:ss) 00:00:01 y 00:59:59 cuentan como 1 hora, para efectos del cobro por hora

    string0 = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    horaSalida = dt.strptime(string0, "%Y-%m-%d %H:%M:%S")

    # Convertir a datetime
    horaEntrada = dt.strptime(horaEntrada, "%Y-%m-%d %H:%M:%S")

    tiempo = (horaSalida - horaEntrada)
    # print(type(tiempo))
    #print("Tiempo: {}".format(tiempo))
    diaEstadia = tiempo.days*86400
    horaEstadia = int(diaEstadia//3600 + tiempo.seconds//3600)
    horaAdicional = tiempo.seconds % 3600
    #print(horaEntrada, horaSalida)
    #print(horaEstadia, horaAdicional)
    if horaAdicional > 0:
        horaEstadia += 1

    print("Hora Entrada : {}\nHora Salida : {}\n".format(
        horaEntrada, horaSalida))
    return horaEstadia


def calcularCobro(horaEntrada, valor):
    # Se recibe el tiempo en horas de estadía de un vehiculo y el valor de la hora y retorna el valor a pagar
    tiempo = calcularDiferenciaHoras(horaEntrada)
    return tiempo*valor


#prueba1 = "2021-05-23 09:10:33"
# prueba2 = "2021-5-23 22:15:00"
# prueba3 = "2021-5-23 22:59:00"
# calcularDiferenciaHoras(prueba1)
# calcularDiferenciaHoras(prueba2)
# calcularDiferenciaHoras(prueba3)
#print(calcularCobro(prueba1, 1000))
