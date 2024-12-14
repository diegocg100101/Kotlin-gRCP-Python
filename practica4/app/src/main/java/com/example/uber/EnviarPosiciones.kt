package com.example.uber

import android.content.Context
import android.widget.Toast
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import uber.UberOuterClass
import uber.UberOuterClass.Posicion
import uber.UberOuterClass.TerminarViajeRequest
import kotlin.math.cos
import kotlin.math.sqrt

@Composable
fun EnviarPosicion(modifier: Modifier = Modifier) {

    val client = UberClient("192.168.100.21", 50051)
    val context = LocalContext.current
    var vehiculo by remember { mutableStateOf<UberOuterClass.infoAuto?>(null) }

    if (client.testConnection()){
        Toast.makeText(context, "Conectado correctamente al servidor", Toast.LENGTH_SHORT).show()
    } else {
        Toast.makeText(context, "Error de conexión al servidor", Toast.LENGTH_SHORT).show()
    }

    val focusY = remember {
        FocusRequester()
    }

    val focusEnviar = remember {
        FocusRequester()
    }

    var posX by remember {
        mutableStateOf("")
    }

    var posY by remember {
        mutableStateOf("")
    }

    Box (
        Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center) {
        Column (horizontalAlignment = Alignment.CenterHorizontally){
            Text(text = "Uber")
            OutlinedTextField(value = posX,
                onValueChange = {posX = it},
                label = { Text(text = "X") },
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Number,
                    imeAction = ImeAction.Next,
                ),
                keyboardActions = KeyboardActions(
                    onNext = {focusY.requestFocus()}
                )
            )

            Spacer(modifier = Modifier.size(30.dp))

            OutlinedTextField(value = posY,
                onValueChange = {posY = it},
                label = { Text(text = "Y") },
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Number,
                    imeAction = ImeAction.Done
                ),
                keyboardActions = KeyboardActions(
                    onDone = {focusEnviar.requestFocus()}
                ),
                modifier = Modifier.focusRequester(focusY)
            )

            Spacer(modifier = Modifier.size(30.dp))

            OutlinedButton(
                onClick = { vehiculo = solicitarViaje(client, context, posX, posY)},
                modifier = Modifier.focusRequester(focusEnviar)
            ) {
                Text(text = "Enviar")
            }

            Spacer(modifier = Modifier.size(30.dp))

            if(vehiculo != null) {

            }
            vehiculo?.let {
                Viaje(vehiculo = it)
                Thread.sleep(7000)
                val costo = terminarViaje(context, client, it, posX.toFloat(), posY.toFloat())
                Text(text = "El costo del viaje es: $costo")
            }
        }
    }
}

fun solicitarViaje(client: UberClient, context : Context, x : String, y : String): UberOuterClass.infoAuto? {
    if (client.testConnection()){
        if(x.isEmpty() || y.isEmpty()) {
            Toast.makeText(context, "Ingresa los valores de X y Y", Toast.LENGTH_SHORT).show()
            return null
        } else {
            val respuesta = client.solicitarViaje(x.toFloat(), y.toFloat())
            if (respuesta != null) {
                Toast.makeText(context, "Viaje en proceso", Toast.LENGTH_SHORT).show()
                return respuesta
            } else {
                Toast.makeText(context, "No hay autos disponibles", Toast.LENGTH_SHORT).show()
                return null
            }
        }
    } else {
        Toast.makeText(context, "No hay conexión con el servidor", Toast.LENGTH_SHORT).show()
        return null
    }
}

fun terminarViaje(context: Context, client: UberClient, vehiculo : UberOuterClass.infoAuto, x1: Float, y1: Float) : Float{

    var posXFinal = (0..50).random().toFloat()
    var posYFinal = (0..50).random().toFloat()

    val posicionFinal = Posicion.newBuilder().setX(posXFinal).setY(posYFinal).build()

    var distancia = calcularDistancia(x1, posXFinal, y1, posYFinal)

    val tipo = vehiculo.tipo

    if (tipo.toString() == "UBER_PLANET") {
        distancia *= 10
    } else if (tipo.toString() == "UBER_XL") {
        distancia *= 15
    } else if (tipo.toString() == "UBER_BLACK"){
        distancia *= 25
    }
    val request = TerminarViajeRequest.newBuilder()
        .setPlaca(vehiculo.placa)
        .setPosicion(posicionFinal)
        .setCosto(distancia.toDouble())
        .build()

    Toast.makeText(context, "Viaje concluido con éxito", Toast.LENGTH_SHORT).show()

    client.terminarViaje(request)
    return distancia
}

fun calcularDistancia(x1 : Float, x2 : Float, y1 : Float, y2: Float) : Float {
    return sqrt(Math.pow((x2 - x1).toDouble(), 2.0) + Math.pow((y2 - y1).toDouble(), 2.0)).toFloat()
}