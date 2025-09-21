# simulador_cardo_puntos.py
# Autor: Zaira
# Simulador de Cardo con puntos y registro completo en MongoDB

from pymongo import MongoClient
from datetime import datetime
import random
import time

# 1. Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client["cardo"]
coleccion = db["situaciones"]
print("✅ Conexión exitosa a la base de datos 'cardo'\n")

# 2. Solicitar nombre y mostrar bienvenida
jugador = input("Ingresa tu nombre: ")
print("\n🎴 Bienvenida al juego CARDО 🎴")
print("En cada ronda se presentará una situación aleatoria. Reflexiona y acumula puntos.\n")
input("Presiona Enter para comenzar el juego...")

# 3. Lógica del juego
rondas = 5
situaciones_jugadas = []
total_puntos = 0

for i in range(rondas):
    print(f"\n🔁 Ronda {i+1}/{rondas}")
    carta = coleccion.aggregate([{"$sample": {"size": 1}}])
    for c in carta:
        descripcion = c["descripcion"]
        puntos = random.randint(1, 3)  # Asignación aleatoria de puntos por carta
        print(f"🃏 Situación: {descripcion} (Puntos: {puntos})")
        situaciones_jugadas.append(descripcion)
        total_puntos += puntos
    if i < rondas - 1:
        input("Presiona Enter para continuar a la siguiente ronda...")

# 4. Registro en MongoDB con puntos
partida = {
    "jugador": jugador,
    "rondas": rondas,
    "situaciones": situaciones_jugadas,
    "puntos": total_puntos,
    "fecha": datetime.now()
}
resultado = db.partidas.insert_one(partida)

# 5. Mostrar resultados
print(f"\n🎯 Puntos totales: {total_puntos}")
print(f"📦 Partida registrada con ID: {resultado.inserted_id}")
print("✅ Puedes verificar la partida en Studio 3T.")

# 6. Final
print("\n🎉 ¡Gracias por jugar CARDО! Reflexiona sobre lo vivido. Hasta pronto.")
