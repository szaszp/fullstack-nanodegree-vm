from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def initSession():
    engine = create_engine('sqlite:///restaurantMenu.db')
    Base.metadata.bind=engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()
    return session


def getRestaurants(session):
    return session.query(Restaurant).all()

def addRestaurant(session, name):
    new = Restaurant(name = name)
    session.add(new)
    session.commit()
    return new

def getRestaurant(session, id):
    r = session.query(Restaurant).filter_by(id=id).one()
    return r

def editName(session, id, newName):
    r = session.query(Restaurant).filter_by(id=id).one()
    if r:
        r.name = newName
        session.add(r)
        session.commit()
    return r

def deleteRestaurant(session, id):
    r = session.query(Restaurant).filter_by(id=id).one()
    if r:
        session.delete(r)
        session.commit()
    return r    


def getMenuItems(session, restaurantId):
    return session.query(MenuItem).filter_by(restaurant_id = restaurantId).all()

def getMenuItem(session, menuItemId):
    return session.query(MenuItem).filter_by(id = menuItemId).one()



def addNewMenuItem(session, restaurant_id, name, price, description):
    i = MenuItem(name = name, restaurant_id = restaurant_id)
    i.price = price
    i.description = description
    session.add(i)
    session.commit()
    return i

def editMenuItem(session, menu_id, name):
    i = session.query(MenuItem).filter_by(id = menu_id).one()
    print("Change name from {0} to {1}".format(i.name, name))
    i.name = name 
    session.add(i)
    session.commit()
    return i


def deleteMenuItem(session, menu_id):
    i = session.query(MenuItem).filter_by(id = menu_id).one()
    session.delete(i)
    session.commit()
    return i


'''
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()


#read
firstResult = session.query(Restaurant).first()
firstResult.name

items = session.query(MenuItem).all()
for item in items:
    print item.name


veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name    


#update
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit() 

#delete
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit() 

'''
