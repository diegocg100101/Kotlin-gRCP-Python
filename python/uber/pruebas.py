import random

def generarPlaca():
        numeros = ''.join(random.choices("0123456789", k=3))
        letras = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        return numeros + letras
    
placa = generarPlaca()

print(placa)