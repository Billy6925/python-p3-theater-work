from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role, Audition
import ipdb

engine = create_engine('sqlite:///auditions.db')
Session = sessionmaker(bind=engine)
session = Session()

def get_actor_for_role(role):
    return [audition.actor for audition in role.auditions]

def get_location_for_role(role):
    return [audition.location for audition in role.auditions]

#Delete existing data
session.query(Role).delete()
session.query(Audition).delete()
session.commit()

#Sample data for testing
def add_sample_data():
    print('Adding sample data...')
    role = Role(character_name = "Hamlet")
    session.add(role)
    session.commit()

    audition1 = Audition(actor = "Actor A", location = "Location A", phone = 1234567890, hired = False, role_id = role.id)
    audition2 = Audition(actor = "Actor B", location = "Location B", phone = 9087654321, hired = True, role_id = role.id)
    session.add(audition1)
    session.add(audition2)
    session.commit()
    print('Sample data added')

def query_data():
    print('Querying data...')
    role = session.query(Role).first()
    ipdb.set_trace()
    print(role)
    print(role.auditions)
    print('Querying completed')

if __name__ == "__main__":
    add_sample_data()
    query_data()
    