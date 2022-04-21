from database import Base
from sqlalchemy import Column,Integer,String,Float

class Users(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50))
    co_ordinates=Column(String(100),unique=True)
    
