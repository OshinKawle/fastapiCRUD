from fastapi import FastAPI,Depends
from database import Base,SessionLocal,engine
from models import Users
from typing import List
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserSchema(BaseModel):
    name:str
    co_ordinates:str
    class Config:
        orm_mode=True

class UserCreateSchema(UserSchema):
    password:str

@app.get('/status',response_model=List[UserCreateSchema])
def get_users(db:Session=Depends(get_db)):
    return db.query(Users).all()

@app.post('/status',response_model=UserSchema)
def get_users(user:UserCreateSchema, db:Session=Depends(get_db)):
    u=Users(name=user.name,co_ordinates=user.co_ordinates,password=user.password)
    db.add(u)
    db.commit()
    return u

@app.put('/status/{user_id}',response_model=UserSchema)
def update_user(user_id:int,user:UserSchema,db:Session=Depends(get_db)):
    try:
        u=db.query(Users).filter(Users.id==user_id).first()
        u.name=user.name
        u.co_ordinates=user.co_ordinates
        db.add(u)
        db.commit()
        return u

    except:
        return HttpException(status_code=404,details='user not found')


@app.delete("/status/{user_id}",response_class=JSONResponse)
def delete_user(user_id:int,db:Session=Depends(get_db)):
    try:
        u=db.query(Users).filter(Users.id==user_id).first()
        db.delete(u)
        db.commit()
        return{f"user of id {user_id} has been deleted":True}
    except:
        return HttpException(status_code=404,details='user not found')
