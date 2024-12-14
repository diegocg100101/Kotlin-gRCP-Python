package com.example.uber

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import uber.UberOuterClass

@Composable
fun Viaje(modifier: Modifier = Modifier, vehiculo :  UberOuterClass.infoAuto ) {
    Text(text = "Información del vehículo")
    Text(text = "Tipo: ${vehiculo.tipo}")
    Text(text = "Placa: ${vehiculo.placa}")
}