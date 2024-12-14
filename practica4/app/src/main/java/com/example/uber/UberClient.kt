package com.example.uber

import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import uber.UberGrpc
import uber.UberOuterClass
import uber.UberOuterClass.Posicion
import uber.UberOuterClass.TerminarViajeRequest
import uber.UberOuterClass.Vacio

class UberClient(private val serverUrl: String, private val port : Int) {
    private val channel: ManagedChannel = ManagedChannelBuilder
        .forAddress(serverUrl, port)
        .usePlaintext()
        .build()
    private val stub: UberGrpc.UberBlockingStub = UberGrpc.newBlockingStub(channel)

    fun solicitarViaje(x: Float, y: Float): UberOuterClass.infoAuto? {
        return try {
            val posicion = Posicion.newBuilder().setX(x).setY(y).build()
            val response = stub.solicitarViaje(posicion)
            response
        } catch (e: io.grpc.StatusRuntimeException) {
            println("Error al solicitar viaje: ${e.status}")
            null
        }
    }

    fun testConnection(): Boolean {
        return try {
            UberGrpc.newBlockingStub(channel)
            val vacio = Vacio.newBuilder().build()
            stub.estadoServicio(vacio)
            true
        } catch (e: Exception) {
            println("Error al conectar: ${e.localizedMessage}")
            false
        }
    }


    fun terminarViaje(request : TerminarViajeRequest) {
        stub.terminarViaje(request)
    }
}