from concurrent import futures
import logging

import grpc
import uber_pb2
import uber_pb2_grpc
import numpy as np
import random

class Uber(uber_pb2_grpc.UberServicer):
    
    def __init__(self):
        # Variables globales 
        self.AUTOS = 1
        self.viajes = 0
        self.ganancia = 0
        self.vehiculo = self.inicializarAutos()
        
        
    def distancia(self, x1, y1, x2, y2):
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) **2)
        
    def generarPlaca(self):
        numeros = ''.join(random.choices("0123456789", k=3))
        letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        return numeros + letras
        
    def inicializarAutos(self):
        return [uber_pb2.infoAuto(disponibilidad=True, 
                                           posXY=uber_pb2.Posicion(X=random.randint(0,50), Y=random.randint(0,50)),
                                           tipo=random.randint(0, 2),
                                           placa=self.generarPlaca()) for _ in range(self.AUTOS)]
        
    def solicitarViaje(self, request, context):
        posX = request.X
        posY = request.Y
        
        distanciaMin = np.inf
        uberSeleccionado = None
        
        for uber in self.vehiculo:
            if(uber.disponibilidad):
                distancia = self.distancia(uber.posXY.X, uber.posXY.Y, posX, posY)
                
                if(distancia < distanciaMin):
                    distanciaMin = distancia
                    uberSeleccionado = uber
                    
        if(uberSeleccionado):
            for uber in self.vehiculo:
                if uber.placa == uberSeleccionado.placa:
                    uber.disponibilidad = False
                    break
            return uberSeleccionado                   
        else:
            print("No hay autos disponibles.")
        return uber_pb2.infoAuto()

    def terminarViaje(self, request, context):
        posicion = request.posicion
        costo = request.costo
        placa = request.placa
        
        for uber in self.vehiculo:
            if uber.placa == placa:
                uber.disponibilidad = True
                uber.posXY.CopyFrom(posicion)
                self.ganancia = self.ganancia + costo
                self.viajes = self.viajes + 1
                
                print(f"Auto con placas {uber.placa} está disponible\n")
                break
        
        return uber_pb2.Vacio()
    
    def estadoServicio(self, request, context):
        libres = 0
        for uber in self.vehiculo:
            if(uber.disponibilidad):
                libres = libres + 1
        return uber_pb2.infoServicio(viajes=self.viajes, autosLibres=libres, ganancia=self.ganancia)
    
    

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    uber_pb2_grpc.add_UberServicer_to_server(Uber(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()