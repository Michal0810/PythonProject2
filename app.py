def hello():
    return "Hello, world!"

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

import os
from dotenv import load_dotenv

# Wczytanie zmiennych z pliku .env
load_dotenv()

# Dostęp do zmiennych środowiskowych
mongo_uri = os.getenv("MONGO_URI")
debug_mode = os.getenv("DEBUG")

print("URI:", mongo_uri)
