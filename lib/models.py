from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///auditions.db')
Session = sessionmaker(bind=engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    character_name = Column(String(), nullable=False)
    auditions = relationship('Audition', backref='role')

    def lead(self):
        hired_audition = next((audition for audition in self.auditions if audition.hired),None)
        if hired_audition:
            return hired_audition
        else:
            return "No actor has been hired for this role"
    
    def understudy(self):
        hired_audition = [audition for audition in self.auditions if audition.hired]
        if len(hired_audition) >=2:
            return hired_audition[1]
        else:
            return "No actor has been hired for understudy for this role"

    def __repr__(self):
        return f"Role (id {self.id}: character_name = {self.character_name})"
    

class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean, default=False)
    role_id = Column(Integer(), ForeignKey('roles.id')) 

    def call_back(self):
        self.hired = True
        session.commit()

    def __repr__(self):
        return f"Audition {self.id}: actor = {self.actor}, hired = {self.hired}"

def get_actor_for_role(role):
    return [audition.actor for audition in role.auditions]

def get_location_for_role(role):
    return [audition.location for audition in role.auditions]
