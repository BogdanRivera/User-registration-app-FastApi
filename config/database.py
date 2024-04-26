import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



file_data = "../data.sqlite"
# Read directory from the actual file
directory = os.path.dirname(os.path.realpath(__file__))
# DB Direction
route = f"sqlite:///{os.path.join(directory,file_data)}"
# Creating motor
motor = create_engine(route,echo=True)
# Creating session
session = sessionmaker(bind=motor)
# creating base for the manipulation of tables from BD
base = declarative_base()
