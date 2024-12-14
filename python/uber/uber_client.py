import grpc
import random
import math
import time
import uber_pb2
import uber_pb2_grpc

def calcular_distancia(posicion_inicial, posicion_final):
    """Calcula la distancia euclidiana entre dos puntos."""
    return math.sqrt((posicion_final.X - posicion_inicial.X) ** 2 + 
                     (posicion_final.Y - posicion_inicial.Y) ** 2)

def main():
    # Dirección del servidor gRPC
    server_address = "localhost:50051"

    # Crear un canal y un cliente stub
    with grpc.insecure_channel(server_address) as channel:
        stub = uber_pb2_grpc.UberStub(channel)

        # Generar posición inicial del cliente
        posicion_cliente = uber_pb2.Posicion(
            X=random.randint(0, 50), 
            Y=random.randint(0, 50)
        )

        print(f"Solicitando viaje desde posición: ({posicion_cliente.X}, {posicion_cliente.Y})")

        try:
            # Llamar al servicio solicitarViaje
            vehiculo = stub.solicitarViaje(posicion_cliente)
            print(f"Se encontró vehículo:\nPlacas: {vehiculo.placa}\nTipo: {vehiculo.tipo}\n")

            # Simular tiempo del viaje
            time.sleep(5)

            # Generar posición final del viaje
            posicion_final = uber_pb2.Posicion(
                X=random.randint(0, 50), 
                Y=random.randint(0, 50)
            )

            print(f"Posición final del viaje: ({posicion_final.X}, {posicion_final.Y})")

            # Calcular distancia y costo del viaje
            distancia = calcular_distancia(posicion_cliente, posicion_final)
            if vehiculo.tipo == uber_pb2.UBER_PLANET:
                tipo = "UberPlanet"
                costo = distancia * 10
            elif vehiculo.tipo == uber_pb2.UBER_XL:
                tipo = "UberXL"
                costo = distancia * 15
            else:  # UBER_BLACK
                tipo = "UberBlack"
                costo = distancia * 25

            print(f"Tipo de vehículo: {tipo}\nDistancia: {distancia:.2f}\nCosto: ${costo:.2f}")

            # Terminar el viaje
            terminar_viaje_request = uber_pb2.TerminarViajeRequest(
                posicion=posicion_final, 
                costo=costo, 
                placa=vehiculo.placa
            )
            stub.terminarViaje(terminar_viaje_request)
            print("\n¡Viaje concluido con éxito!")

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                print("No se encontró vehículo disponible.")
            else:
                print(f"Error: {e.details()}")

if __name__ == "__main__":
    main()
