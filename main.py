import uvicorn
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from typing import List
from fastapi.encoders import jsonable_encoder


app = FastAPI()
dict_id = {}


class User(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    recomendations: List[str]


@app.post('/create_user/')
def create_user(user: User):
    id = user.user_id
    if id in dict_id.keys():
        return f'User {id} creado. {user.user_name} User en la base de datos.'
    else:
        return f'{user.user_name} ya existe crear otro.'


@app.put('/update_user/{user_id}')
def update_user(user_id: str, user: User):
    user_id = int(user_id)
    if user_id not in dict_id.keys():
        return f'{user_id} no existe.'
    
    updated_user = jsonable_encoder(user)
    dict_id[user_id] = updated_user
    return f'actualizado {user_id}.'


@app.get('/get_user/{user_id}')
def get_user_info(user_id: str):
    
    user_id = int(user_id)
    if user_id not in dict_id.keys():
        return f'{user_id} no existe.'

    return dict_id[user_id]


@app.delete('/delete_user/{user_id}')
def delete_user(user_id: str):
    user_id = int(user_id)
    if user_id not in dict_id.keys():
        return f'{user_id} no existe.'
    
    popped = dict_id.pop(user_id)
    return f'Fue elimiado: \n {popped}'


if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=5001, log_level='info', reload=False)
