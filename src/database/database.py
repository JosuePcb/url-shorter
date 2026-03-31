from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
import certifi
import os
import string
import random

# Cargar las variables de entorno ANTES de usarlas
load_dotenv()

URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Crear el cliente asíncrono de MongoDB con certificados raíz
client = AsyncMongoClient(URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())

# Acceder a la base de datos y colección
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


# Caracteres base62: a-z, A-Z, 0-9
BASE62_CHARS = string.ascii_letters + string.digits


async def generate_unique_id(length: int = 8) -> str:
    while True:
        short_id = ''.join(random.choices(BASE62_CHARS, k=length))

        # Verificar si ya existe en la colección
        exists = await collection.find_one({"_id": short_id})

        if not exists:
            return short_id


async def save_url(original_url: str) -> str:
    """Genera un ID corto, guarda el mapeo en MongoDB y retorna el short_id."""
    short_id = await generate_unique_id()
    await collection.insert_one({"_id": short_id, "url": original_url})
    return short_id


async def get_url(short_id: str) -> str | None:
    """Busca un short_id en MongoDB y retorna la URL original o None."""
    doc = await collection.find_one({"_id": short_id})
    return doc["url"] if doc else None