"""
Δημιουργία εφαρμογής backend για το E-learning platform.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="E-Learning Platform API",
    description="Online courses platform",
    version="1.0.0"
)

def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
