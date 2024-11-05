import os

VERSION = os.getenv("VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", 0)  # 0 is False, 1 is True
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", 8000)

# Set up database connection details
POSTGRES_USER = os.getenv("POSTGRES_USER")  # required
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # required
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "kbaseball")
DMOTION_APP_ID = os.getenv("DMOTION_APP_ID")  # required
DMOTION_API_KEY = os.getenv("DMOTION_API_KEY")  # required
SECRET_KEY = os.getenv("SECRET_KEY", "254bcd5390c2749197742e649f77")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "be85a59019e1e6ec6be3113")

# PASSWORD hashing configuration
ARGON2_MEMORY_COST = int(
    os.getenv("ARGON2_MEMORY_COST", 65536)
)  # Memory cost (in kibibytes)
ARGON2_TIME_COST = int(os.getenv("ARGON2_TIME_COST", 3))  # Number of iterations
ARGON2_PARALLELISM = int(os.getenv("ARGON2_PARALLELISM", 4))  # Number of threads
ARGON2_SALT_SIZE = int(
    os.getenv("ARGON2_SALT_SIZE", 16)
)  # Salt size (in bytes, default is 16)

__all__ = [
    "VERSION",
    "DEBUG",
    "SERVER_HOST",
    "SERVER_PORT",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "SECRET_KEY",
    "REFRESH_SECRET_KEY",
    "ARGON2_MEMORY_COST",
    "ARGON2_TIME_COST",
    "ARGON2_PARALLELISM",
    "ARGON2_SALT_SIZE",
    "DMOTION_APP_ID",
    "DMOTION_API_KEY",
]
