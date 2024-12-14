import grpc
import random
import math
import time
import uber_pb2
import uber_pb2_grpc
import time

def main():
    # Dirección del servidor gRPC
    server_address = "localhost:50051"

    # Crear un canal y un cliente stub
    with grpc.insecure_channel(server_address) as channel:
        stub = uber_pb2_grpc.UberStub(channel)

        vacio = uber_pb2.Vacio()

        while(True):
            estado = stub.estadoServicio(vacio)
            print(f"Viajes: {estado.viajes}\nAutos disponibles: {estado.autosLibres}\nGanancia total: {estado.ganancia}\n")
            time.sleep(2)
            

if __name__ == "__main__":
    main()
