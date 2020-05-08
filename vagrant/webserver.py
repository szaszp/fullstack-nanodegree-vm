
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import urllib
import urlparse
import re
import database_query
from database_setup import Base, Restaurant, MenuItem

mySession=database_query.initSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                print("Try to query db.")
                output = ""
                output += "<html><body>"
                output += "<h1>List of restaurants</h1>"
                #output += "<ul style='list-style-type:none'>"
                restaurants = database_query.getRestaurants(mySession)
                for r in restaurants:
                    print("Next one found: " + str(r.name))
                    output += "<h3>%s</h3>" % str(r.name)
                    output += "<a href='/restaurant/{0}/edit'><b>Edit</b></a>".format(r.id)
                    output += "&nbsp &nbsp"
                    params = {'id': r.id, 'name' : r.name.strip()}
                    params = urllib.urlencode(params)
                    print("Params:" + str(params))
                    output += "<a href='/restaurant/delete?{0}'><b>Delete</b></a>".format(str(params))
                #output += "</ul>"
                output += "</body></html>"
                print(output)
                self.wfile.write(output)
                return
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()             
                output = ""
                output += "<html><body>"
                output += "<h1>Add new restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h3>What is the name of the new restaurant?</h3><input name='name' type='text' ><input type='submit' value='Add'> </form>"
                output += "</body></html>"
                print(output)
                self.wfile.write(output)
            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()  
                
                output = ""
                output += "<html><body>"     
                
                findId = re.search("\d+(?=\/edit)", self.path)
                if findId:
                    id = int(findId.group())
                    r = database_query.getRestaurant(mySession, id)
                    if r:
                        output += "<html><body>"   
                        output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/edit'><h3>Rename the restaurant {1}:</h3><input name='name' type='text' placeholder='{1}'><input type='submit' value='Rename'> </form>".format(r.id, r.name)
                        output += "</body></html>"

                if len(output)==0:
                    output += "<html><body>"   
                    output += "No restaurant found with this id"
                    output += "</body></html>"

                print(output)
                self.wfile.write(output)
            elif re.search("\/delete(?=\?)", self.path):
                #print("URL:" + self.url)
                print("Path:" + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()  
                
                o = urlparse.urlparse(self.path)
                print("Query:" + o.query)
                params = urlparse.parse_qs(o.query)
                id = int(params.get("id",["-1"])[0])
                name = params.get("name", "")[0]

                output = ""
                if id>=0:
                    output += "<html><body>"   
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{0}/delete'><h3>Are you sure you want to delete {1}?</h3><input type='submit' value='Delete'> </form>".format(id, name)
                    output += "</body></html>"

                if len(output)==0:
                    output += "<html><body>"   
                    output += "No restaurant found with this id"
                    output += "</body></html>"

                print(output)
                self.wfile.write(output)


        except:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
            elif self.path.endswith("/restaurants/new"):
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newName = fields.get('name',[""])[0]          
                print("New resti:" + newName)     
                database_query.addRestaurant(mySession, newName)
                self.wfile.write("<html><body>New restaurant added</body></html>")
            elif self.path.endswith("/edit"):
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                findId = re.search("\d+(?=\/edit)", self.path)
                if findId:
                    id = int(findId.group()) 
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        newName = fields.get('name', [""])[0] 
                        print("New name of resti:" + newName)     
                        database_query.editName(mySession, id, newName)
                self.wfile.write("<html><body>Restaurant renamed</body></html>")
            elif self.path.endswith("/delete"):
                self.send_response(303)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                findId = re.search("\d+(?=\/delete)", self.path)
                if findId:
                    id = int(findId.group()) 
                    print("Delete " + str(id))
                    database_query.deleteRestaurant(mySession, id)

                self.wfile.write("<html><body>Restaurant deleted</body></html>")

        except:
            pass

def main():
    try:
        port=8080
        server = HTTPServer(('', port), WebServerHandler)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
    except Exception as ex:
        print(ex.message)


if __name__ == "__main__":
    main()