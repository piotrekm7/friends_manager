import os

os.environ['DB_URL']='sqlite:///./dev.db'
os.system('uvicorn main:app')