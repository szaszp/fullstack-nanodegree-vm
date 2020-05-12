from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database_query

app = Flask(__name__)
mySession = database_query.initSession()


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    return render_template("menu.html", restaurant = database_query.getRestaurant(mySession, restaurant_id), items = database_query.getMenuItems(mySession, restaurant_id))
       
    
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    return jsonify(MenuItems=[i.serialize for i in database_query.getMenuItems(mySession, restaurant_id)])
       
    
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    return jsonify(MenuItem=database_query.getMenuItem(mySession, menu_id).serialize)
       


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    output = ""
    r = database_query.getRestaurant(mySession, restaurant_id)
    if r:
        if request.method == 'GET':
            output += "<html><body>"
            output += "<h2>Add new menu item for %s</h2>" % r.name
            output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/new'><h3>Enter new menu item</h3>" % str(restaurant_id)
            output += "<input name='name' type='text' placeholder='Name' ><br/><input name='price' type='text' placeholder='Price'><br/><input name='desc' type='text' placeholder='Description' ><br/>"
            output += "<input type='submit' value='Add'> </form>"
            output += "</body></html>"        
            return output
        elif request.method == 'POST':
            if database_query.addNewMenuItem(mySession, restaurant_id, request.form["name"], request.form["price"], request.form["desc"]):
                flash("new menu item created!")
                return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
            output = "Menu item cannot be added."
         
    return output 

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        print("hoho GET")
        return render_template("editmenuitem.html", restaurant_id=restaurant_id, menu_id=menu_id, menu_name=database_query.getMenuItem(mySession, menu_id).name)
    elif request.method == 'POST':
            if database_query.editMenuItem(mySession, menu_id, request.form["name"]):
                flash("menu item %s is edited!" % request.form["name"])
                return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    return "Menu item cannot be added."

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = database_query.getMenuItem(mySession, menu_id)
    if item:
        if request.method == 'GET':
            return render_template("deletemenuitem.html", item = item)
        elif request.method == 'POST':
            database_query.deleteMenuItem(mySession, menu_id)
            flash("menu item is deleted!")
            return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    return "cannot find item to delete"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)