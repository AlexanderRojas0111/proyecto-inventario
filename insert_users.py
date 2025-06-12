import sqlite3
import csv
from app.user_management import hash_password

DATABASE = "inventario.db"


def insert_users_from_csv(csv_file):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    with open(csv_file, mode="r", encoding="utf-8") as file:

        reader = csv.DictReader(file)
        for row in reader:
            print("Columnas disponibles:", row.keys())
            hashed_password = hash_password(row["Contraseña"].strip())

            cursor.execute(
                "INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)",
                (row["Correo"], hashed_password, row["Nombre"]),
            )
            print(f"Usuario insertado: {row['Correo']}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    insert_users_from_csv("data/users.csv")
