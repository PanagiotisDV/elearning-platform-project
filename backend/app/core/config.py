
"""

Διαβάζει το .env και φορτώνει τις ρυθμίσεις

"""


from pydantic_settings import BaseSettings
from typing import Optional
  


class Settings(BaseSettings):
    """
    Όλες τις ρυθμίσεις της εφαρμογής
    Κάθε ιδιότητα διαβάζεται από το .env
    """
    
   
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

       
   
    class Config:
        env_file = ".env"
        case_sensitive = True
       


settings = Settings()
