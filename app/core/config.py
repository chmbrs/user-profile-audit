import os

DATABASE_URL = os.getenv("DATABASE_URL")

class Settings:
    TITLE = "User Profile Audit System"
    DESCRIPTION = "An API for managing user profiles with audit logging and restoration."
    VERSION = "1.0.0"
    VALID_USER_NAME = os.getenv("USER_NAME", "admin") # TODO: WARNING! REMOVE THE DEFAULT VALUE IN PRODUCTION
    VALID_PASSWORD = os.getenv("PASSWORD", "admin") # TODO: WARNING! REMOVE THE DEFAULT VALUE IN PRODUCTION

settings = Settings()
