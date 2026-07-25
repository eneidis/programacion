from abc import ABC, abstractmethod
from datetime import datetime


# REGISTRO DE LOGS


class Logger:

    ARCHIVO="logs.txt"

    @staticmethod
    def registrar(mensaje):

        with open(Logger.ARCHIVO,"a",encoding="utf8") as archivo:

            archivo.write(f"{datetime.now()} -> {mensaje}\n")


# EXCEPCIONES PERSONALIZADAS


class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass


# CLASE ABSTRACTA PERSONA


class Persona(ABC):

    def __init__(self,nombre,identificacion):

        self.nombre=nombre
        self.identificacion=identificacion

    @abstractmethod
    def mostrar(self):
        pass


# CLIENTE


class Cliente(Persona):

    def __init__(self,nombre,identificacion,email):

        if len(nombre)<3:
            raise ClienteError("Nombre inválido")

        if "@" not in email:
            raise ClienteError("Correo inválido")

        super().__init__(nombre,identificacion)

        self.__email=email

    @property
    def email(self):
        return self.__email

    def mostrar(self):
        return f"{self.nombre} - {self.identificacion}"


# SERVICIO ABSTRACTO


class Servicio(ABC):

    def __init__(self,nombre):

        self.nombre=nombre

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# RESERVA DE SALA


class ReservaSala(Servicio):

    def __init__(self,horas):

        super().__init__("Reserva Sala")

        if horas<=0:
            raise ServicioError("Horas inválidas")

        self.horas=horas

    def calcular_costo(self,iva=False,descuento=0):

        costo=self.horas*50000

        if descuento>0:
            costo-=costo*descuento

        if iva:
            costo*=1.19

        return costo

    def descripcion(self):

        return "Servicio de reserva de sala."


# ALQUILER DE EQUIPOS


class AlquilerEquipo(Servicio):

    def __init__(self,dias):

        super().__init__("Alquiler Equipo")

        if dias<=0:
            raise ServicioError("Cantidad de días inválida")

        self.dias=dias

    def calcular_costo(self,iva=False,descuento=0):

        costo=self.dias*80000

        if descuento>0:
            costo-=costo*descuento

        if iva:
            costo*=1.19

        return costo

    def descripcion(self):

        return "Alquiler de equipos tecnológicos."


# ASESORÍA


class AsesoriaEspecializada(Servicio):

    def __init__(self,horas):

        super().__init__("Asesoría")

        if horas<=0:
            raise ServicioError("Horas incorrectas")

        self.horas=horas

    def calcular_costo(self,iva=False,descuento=0):

        costo=self.horas*120000

        if descuento>0:
            costo-=costo*descuento

        if iva:
            costo*=1.19

        return costo

    def descripcion(self):

        return "Servicio de asesoría."


# RESERVA


class Reserva:

    def __init__(self,cliente,servicio):

        if not isinstance(cliente,Cliente):
            raise ReservaError("Cliente inválido")

        if not isinstance(servicio,Servicio):
            raise ReservaError("Servicio inválido")

        self.cliente=cliente
        self.servicio=servicio
        self.estado="Pendiente"

    def confirmar(self):

        self.estado="Confirmada"

        Logger.registrar(f"Reserva confirmada para {self.cliente.nombre}")

    def cancelar(self):

        self.estado="Cancelada"

        Logger.registrar(f"Reserva cancelada para {self.cliente.nombre}")

    def procesar(self):

        try:

            costo=self.servicio.calcular_costo(True)

        except Exception as e:

            raise ReservaError("No fue posible procesar la reserva") from e

        else:

            print("------------------------------------")
            print("Cliente:",self.cliente.nombre)
            print("Servicio:",self.servicio.nombre)
            print("Costo:",costo)
            print("Estado:",self.estado)

        finally:

            Logger.registrar("Proceso finalizado.")


# LISTAS


clientes=[]
reservas=[]

# FUNCION REGISTRO CLIENTE


def registrar_cliente(nombre,id,email):

    try:

        cliente=Cliente(nombre,id,email)

        clientes.append(cliente)

        Logger.registrar(f"Cliente registrado {nombre}")

    except ClienteError as e:

        Logger.registrar(str(e))

        print(e)


# SIMULACIÓN
==

print("SIMULACIÓN DEL SISTEMA\n")

#1 Registro válido
registrar_cliente("Carlos","1001","carlos@gmail.com")

#2 Registro válido 
registrar_cliente("Ana","1002","ana@gmail.com")

#3 Registro fallido (Correo inválido) -> NO se agrega a la lista
registrar_cliente("Lu","1003","correo")

#4 Registro válido
registrar_cliente("Pedro","1004","pedro@gmail.com")

#5 Registro válido
registrar_cliente("Maria","1005","maria@gmail.com")

#6 Reserva de sala exitosa 
try:

    servicio1=ReservaSala(5)

    reserva1=Reserva(clientes[0],servicio1)

    reserva1.confirmar()

    reserva1.procesar()

except Exception as e:

    Logger.registrar(str(e))

#7 Creación de Servicio Fallido (Horas Negativas)
try:

    servicio2=ReservaSala(-4)

except Exception as e:

    Logger.registrar(str(e))

#8 Alquiler de equipo exitoso 
try:

    servicio3=AlquilerEquipo(3)

    reserva2=Reserva(clientes[1],servicio3)

    reserva2.confirmar()

    reserva2.procesar()

except Exception as e:

    Logger.registrar(str(e))

#9 Asesoría exitosa 
try:

    servicio4=AsesoriaEspecializada(2)

    reserva3=Reserva(clientes[2],servicio4)

    reserva3.confirmar()

    reserva3.procesar()

except Exception as e:

    Logger.registrar(str(e))

#10 Reserva fallida por tipo de cliente inválido
try:

    servicio_temp=AsesoriaEspecializada(1)
    
    reserva4=Reserva("Cliente_Invalido_String",servicio4)

except Exception as e:

    Logger.registrar(str(e))

print("\nSistema ejecutado correctamente.")



