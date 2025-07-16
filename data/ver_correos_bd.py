import psycopg2
import json
from data.email_db import get_conn

# Script para mostrar los correos y el campo raw_message directamente desde la base de datos

def mostrar_correos():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, sender, recipients, subject, status, timestamp, raw_message FROM emails ORDER BY timestamp DESC')
        correos = cursor.fetchall()
        for correo in correos:
            print('='*60)
            print(f"ID:        {correo[0]}")
            print(f"De:        {correo[1]}")
            print(f"Para:      {json.loads(correo[2])}")
            print(f"Asunto:    {correo[3]}")
            print(f"Estado:    {correo[4]}")
            print(f"Fecha:     {correo[5]}")
            print('-'*60)
            print("RAW MESSAGE:")
            print(correo[6])
            print('='*60)

if __name__ == "__main__":
    mostrar_correos()
