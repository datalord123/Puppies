from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#Please go over this schema with me so I can be sure that it is optimized.
#Keep getting this error when trying cascades
"""delete-orphan cascade is not supported on a many-to-many or many-to-one 
relationship when single_parent is not set. Set single_parent=True on the relationship()."""

#There is also some confusion from my end as to whether the referenced class objects in relationship()
# should be in quotes or not. Queries seem to work if they ARE in quotes.
# But all of the lesson video's show outside of quotes.
# If I do not use quotes, I get a reference error.

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False, unique = True)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    puppies = relationship('Puppy',cascade = 'all, delete, delete-orphan', back_populates = 'shelter')
    max_occ = Column(Integer,default=25)

#How can I test to see if orphans are removed from the association table?
Adopter_Puppy=Table('association',Base.metadata,
    Column('puppy_id',Integer,ForeignKey('puppy.id'),primary_key = True),
    Column('adopter_id',Integer,ForeignKey('adopter.id'), primary_key = True)
    )

class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship('Shelter',back_populates = 'puppies')
    adopter = relationship('Adopter',secondary = Adopter_Puppy,back_populates = 'puppies')
    profile = relationship('PuppyProfile',uselist=False, cascade = 'all, delete, delete-orphan', back_populates = 'puppy')
    weight = Column(Numeric(10,2))
    status = Column(String(20),default='available') #added for adoption function

class Adopter(Base):
   __tablename__ = 'adopter'

   id  = Column(Integer, primary_key = True)
   name = Column(String(100))
   puppies = relationship('Puppy',secondary = Adopter_Puppy,back_populates = 'adopter')

class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'

    id = Column(Integer, primary_key=True)
    picture = Column(String(250))
    puppy_id = Column(Integer,ForeignKey('puppy.id'))
    puppy = relationship(Puppy,back_populates = 'profile')
    desc = Column(Text)
    needs = Column(Text)

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
