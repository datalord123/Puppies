from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy, Adopter_Puppy,Adopter,PuppyProfile
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine 

DBSession = sessionmaker(bind = engine)

session = DBSession()

def diff_month(d1, d2):
    """calculate number of months by counting day from today"""
    delta = d1 - d2
    return delta.days / 30
    
def puppy_names():
	"""Query all the puppies and return the results in alphabetical order"""
	for puppy in session.query(Puppy).order_by(Puppy.name.asc()).all():
		print puppy.name

def puppy_ages():
	"""Query all of the puppies that are less than 6 months old organized by the youngest first"""
	threshold = datetime.date.today() - datetime.timedelta(6 * 365/12)
	for puppy in session.query(Puppy).filter(Puppy.dateOfBirth>threshold).order_by(Puppy.dateOfBirth.desc()).all():
		puppy_months = diff_month(datetime.date.today(), puppy.dateOfBirth)
		print "{name}: {months}".format(name = puppy.name, months = puppy_months)

def puppy_weights():
	"""Query all puppies by ascending weight"""
	for puppy in session.query(Puppy).order_by(Puppy.weight.asc()).all():
		print puppy.name, puppy.weight

def check_max_capacity(shelter_name):
	"""Query the maximum capacity for a shelter"""
	result = session.query(Shelter).filter_by(name = shelter_name).one()
	print "Max Capacity - {sname}: {smax}".format(sname = shelter_name, smax = result.max_occ)

#Also, please tell me how I can write this as a LEFT outerjoin, is what I did below correct?
def check_occupancy(shelter_name):
	"""Query the current occupancy for a shelter"""
	result = session.query(Shelter.name,func.count(Puppy.id).label('puppy_count'),Shelter.max_occ)\
	.outerjoin(Shelter.name).group_by(Shelter.name).filter(Shelter.name==shelter_name).one()
	num_left = result.max_occ-result.puppy_count
	print "Cur Occupancy - {sname}: {pcount}, {remaining} openings remaining".format(sname = shelter_name, pcount = result.puppy_count, remaining = num_left)

def show_puppies(shelter_name):
	pup_shelter = session.query(Shelter).filter_by(name=shelter_name).one()
	puppies = session.query(Puppy).filter_by(shelter=pup_shelter).all()
	for puppy in puppies:
	    print puppy.id,puppy.name

def Adopt_Puppy(puppy_id,adopter):
	"""Not sure how I got away with not using 'append' here"""
	adopterlist=[]
	i = 0
	while i < len(adopter):
		adopterlist.append(Adopter(name=adopter[i]))
		print adopterlist
		i +=1
	puppy = session.query(Puppy).filter_by(id = puppy_id).one()
	puppy.status = "Adopted"
	puppy.adopter = adopterlist
	session.add(puppy)
	session.commit()

def Check_Status(puppy_id = 98):
	result = session.query(Puppy).filter_by(id = puppy_id).one()
	print "Puppy Name: " + result.name
	print "Puppy Status: " + result.status
	for i in result.adopter:
		print "Adopter:"+ i.name

#This works
#How can I write it as a left outer join?
def shelter_puppy_count():
    """Query all puppies grouped by the shelter in which they are staying"""
    for shelter in session.query(Shelter.id, Shelter.name,func.count(Puppy.id).label('puppy_count'))\
    .join(Puppy).group_by(Shelter.name).order_by(func.count(Puppy.id).desc()):
        print shelter.id, shelter.name, shelter.puppy_count

#This isn't working
def empty_shelter(shelter_name):
	remPuppies = session.query(Puppy).join(Shelter).filter(Shelter.name==shelter_name).all()
	[session.delete(x) for x in remPuppies]
	session.commit()

#puppy_names()
#puppy_ages()
#puppy_weights()
#show_puppies("Oakland Animal Services")
#check_max_capacity("Oakland Animal Services")
#empty_shelter("Wonder Dog Rescue")

## This isn't working
check_occupancy("Oakland Animal Services")
#AttributeError: 'ColumnProperty' object has no attribute 'mapper'

#I want there to a "Wonder Dog Rescue" should show up as a Shelter
# that has a puppy count of 0 following the running of empty_shelter("Wonder Dog Rescue")
# This seems a classic fix for a left join(unless I am running into a cascade issue in the schema)
shelter_puppy_count()
# Please show me how to update my shelter_puppy_count() query so that it 
# is refactored as a left join from the Shelter Class(table).


#Adopt_Puppy(puppy_id = "98",adopter = ["Elliot Alderson","Tyrell Wellick"])
##Explain why I don't need to use append here(inside the adopt_puppy function)
#This is how docs did it, I just did an add and got it to work.

#How can I write this so that print 
## "result.adopter.puppy" outputs as a list. Is that a thing?
#Check_Status()

