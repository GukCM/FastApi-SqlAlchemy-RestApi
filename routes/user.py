from fastapi import APIRouter, Response, status
#APIRouter Permite definir rutas por separado #Response devuelve un codigo de respuesta
from starlette.status import HTTP_204_NO_CONTENT
#Devuelve un código en especifico
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet 
#Permite cifrar contraseñas

#Inicializa el cifrador
key = Fernet.generate_key()
#Arroja una función para cifrar lo que quieras
f = Fernet(key)
user = APIRouter()

@user.get("/users", response_model=list[User], tags=["users"])
def get_user():
    return conn.execute(users.select()).fetchall()

@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    #Se necesita transformar a codificación utf-8
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result.lastrowid)
    #Consulta el id del ultimo usuario agregado y arroja solo el primer resultado de la lista 
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

@user.get("/users/{id}", response_model= User, tags=["users"])
def get_user_id(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
        conn.execute(users.delete().where(users.c.id == id))
        return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(name = user.name, email = user.email, password = f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

