from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database_query

app = Flask(__name__)
mySession = database_query.initSession()

@app.route('/')
@app.route('/restaurants')
def getRestaurants():
    return render_template("restaurants.html", items=database_query.getRestaurants(mySession))

@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        if database_query.addRestaurant(mySession, request.form["name"]):
            return redirect(url_for("getRestaurants"))
    else:
        return render_template("newRestaurant.html")


@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        if database_query.editName(mySession, restaurant_id, request.form["name"]):
            return redirect(url_for("getRestaurants"))
    else:
        return render_template("editrestaurant.html", restaurant = database_query.getRestaurant(mySession, restaurant_id) )


@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        if database_query.deleteRestaurant(mySession, restaurant_id):
            return redirect(url_for("getRestaurants"))
    else:
        return render_template("deleteRestaurant.html", restaurant = database_query.getRestaurant(mySession, restaurant_id) )

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    return render_template("menu.html", restaurant = database_query.getRestaurant(mySession, restaurant_id), items = database_query.getMenuItems(mySession, restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/new',  methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        if database_query.addNewMenuItem(mySession, restaurant_id, request.form["name"], request.form["price"], request.form["description"]):
            return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    else:
        return render_template("addmenuitem.html", restaurant = database_query.getRestaurant(mySession, restaurant_id))
    return "Menu item cannot be found"



@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',  methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        if database_query.editMenuItem(mySession, menu_id, request.form["name"]):
            return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    else:
        i = database_query.getMenuItem(mySession, menu_id)
        if i:
            return render_template("editmenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, menu_name = i.name)
    return "Menu item cannot be found"



@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        if database_query.deleteMenuItem(mySession, menu_id):
            return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    else:
        item = database_query.getMenuItem(mySession, menu_id)
        if item:
            return render_template("deletemenuitem.html", item = item )
    return "Menu item cannot be found"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

