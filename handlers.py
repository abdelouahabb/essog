# this is to add unicode support to the application, since we will use tifinagh and arabic and french caracters
#coding: utf-8

from __future__ import division # go to future and bering that real division :D
import tornado.web, tornado.escape, tornado.gen, tornado.auth # tornado stuff ;)
import motor # this is the library that allows to do non-blocking I/O to mongodb ^_^
from pymongo.errors import DuplicateKeyError, AutoReconnect # catch database errors
from gridfs.errors import NoFile # catch the error tome 2 :D
from bson.errors import InvalidId # catch the error tome 3 ;)
import user_agents # this library to get the client's user agent (browser) version
#from os import path # uncomment this is you want not to use GridFS but the normal OS file system, check this for more informations http://en.wikipedia.org/wiki/Comparison_of_file_systems#Limits
import passlib.hash # this is the library used to hash passwords, if you want BCrypt or SCrypt you must install them separately, and it will be chance that will not install on windows :(
from PIL import Image # library to be used with image files.
import StringIO # the image uploaded is a stream, use this to read it, then PIL to manipulate it
#import imghdr # uncomment this if you want only read the header of the image without needing to manipulate the picture.
from bson import json_util, ObjectId # using python json will not manipulate ObjectId.
import time, datetime, string, random, re # various python libraries needed.
import amazon.api as amazon # amazon api to use amazon price compare system
#from apiclient.discovery import build # uncomment this if you want to use google shopping instead of amazon
from latlong import validatorE, validatorP, villes # import functions from an external file
import simpleencode # library to use a string to encode another string
from maill import send_email # sadly this is using smtp which is blocking, only for test, uncomment to try it


#this is only used for mongoHQ, remove the uri from the db to connect by default to your machine,
uri = "mongodb://alien:12345@kahana.mongohq.com:10067/essog"
db = motor.MotorClient(uri).essog #initialize the connection to the mongodb modif

hashh = passlib.hash.pbkdf2_sha512 # pbkdf2 is the one that worked here on windows, BCrypt and SCrypt uses C extension to speed up operation, which dident build on my pc, you can try them on your linux box, it will work

# this will help to show only n products by page and not all the results, we will see it later
spliter = re.compile("\?") # this will be our link splitter ;)
replace = re.compile("s=\d+") # and this one to replace values in te url

# get your 3 keys using this tutorial http://www.clickonf5.org/6932/amazon-developer-api-secret-access-key/
access_key_ID = ""
secret_key = ""
Associate_Tag = ""

#this is used to let only HTML5 browsers use your website
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        a = self.request.headers["User-Agent"]
        #name = user_agents.parse(a).browser.family
        name = user_agents.parse(a)
        if name.is_pc:
            if (name.browser.family == 'Chrome') and (name.browser.version[0]>=30):
                self.render("acc.html")
            elif (name.browser.family == 'Firefox') and (name.browser.version[0]>=30):
                self.render("acc.html")
            elif (name.browser.family == 'Opera') and (name.browser.version[0]>=12):
                self.render("acc.html")
            else:
                self.render("browser.html")
        else:
            self.write('mazal el hal chwyia 3la les portables ^_^')
        #version = int(user_agents.parse(a).browser.version_string[:2])

class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<h1>oops, something went bad, please wait for out futurist robots to fix that ^_^</h1>')

# this class will be be inherited by all other classes, this will get the cookie, and remove the slash if added where unnecessary
class BaseHandler(tornado.web.RequestHandler):
    @tornado.web.removeslash
    def get_current_user(self):
        return self.get_secure_cookie("mechtari")

# the login page
class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def post(self): # dont be dumb and use get to show the password in the url!
        email = self.get_argument("email") # this will seek in the form where there is name="email" and this is how tornado will get the user data
        password = self.get_argument("pass1")
        try:
            dbmail = yield db.users.find_one({"_id": email})
            if dbmail:
                pas = dbmail["prs"]["pass"]
                if hashh.verify(password, pas) == True :
                    del dbmail["prs"]["pass"] # dont save the password in the cookie!
                    try:
                        del dbmail["pdn"] # in the first time, the user has no product
                    except KeyError:
                        pass
                    try:
                        del dbmail["pup"] # in the first time, the user has no product
                    except KeyError:
                        pass
                    hop = json_util.dumps(dbmail)
                    self.set_secure_cookie("mechtari", hop)
                    '''to understand how cookies wokr, just compare between those two values in your browser
                    self.set_cookie("plain_text_email", dbmail["_id"])
                    self.set_secure_cookie("crypted_email", dbmail["_id"])
                    '''
                    self.clear_cookie("invite")
                    self.redirect("/profil")
                else: # in case there will be 3 attemps, save the value to the cookie and detect that to redirect to user to registration, but i advice you to save in the database  to avoid the user to delete the cookie everytime
                    cookie = self.get_secure_cookie("invite")
                    count = int(cookie) + 1 if cookie else 1
                    self.set_secure_cookie("invite", str(count))
                    if count > 3:
                        self.redirect("/#forget")
                    else:
                        self.redirect("/#login")
            else:
                self.redirect("/#register")
        except (AutoReconnect):
            self.redirect("/error")

# this is the welcome page
class Profil(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)# todo, use html5 localstorage because the cookie it too big, i used it to free the database calls, but sadly this will be sent for every http message
        pseudo = info["prs"]["pseu"]
        email = info["_id"]
        commune = info["adr"]["com"]
        site = info["adr"]["sit"]
        tel = info["prs"]["tel"]
        orientation = info["avt"]["ori"]
        avat = info["avt"]["avt"]
        try:
            fs = motor.MotorGridFS(db) # initialise gridfs connection
            owner = yield db.users.find_one({"_id":email})
            try:
                achats = len(owner["pdn"])
            except KeyError:
                achats = 0
            try:
                ventes = len(owner["pup"])
            except KeyError:
                ventes = 0
            gridout = yield fs.get(avat)
            avatar = gridout.filename # motor.web.GridFSHandler handles the mime types, so you have not to worry about it :)
            statut = info["prs"]["stt"]
            if statut == "entreprise" :
                telf = info["prs"]["tef"]
                self.render("profile.html", achats=achats, ventes=ventes, site=site, statut=statut, pseudo=pseudo, email=email, tel=tel, commune=commune, telf=telf, avatar=avatar, orientation=orientation)
            else:
                nom = info["prs"]["nom"]
                prenom = info["prs"]["prn"]
                daten = info["prs"]["dtn"]
                sexe = info["prs"]["sxe"]
                self.render("profile.html", achats=achats, ventes=ventes, site=site, statut=statut, pseudo=pseudo, email=email, tel=tel, commune=commune, nom=nom, prenom=prenom, daten=daten, sexe=sexe, avatar=avatar, orientation=orientation)
        except (AutoReconnect):
                self.redirect("/error")

# this is used for the registration to get the type of the user, and show him the right form registration
class Statut(tornado.web.RequestHandler):
    def post(self):
        t1 = datetime.date.today()
        minyear = t1.year - 18
        t2 = t1.replace(year = minyear)
        t3 = t2.isoformat()
        titre = self.get_argument("statut")
        self.render("register.html", titre=titre, datemin = t3)

# the registration form
class Registration(BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        fs = motor.MotorGridFS(db)
        pseudo = self.get_argument("pseudo").lower()
        pass1 = self.get_argument("pass1")
        pass2 = self.get_argument("pass2")
        password = hashh.encrypt(pass1, salt_size = 32, rounds = 5000) # default is 12000 takes 1.2 seconds, i have choosed this because it is fast (less secure), test with your own values
        email = self.get_argument("email").lower()
        try:
            tel = self.get_argument("tel")
            wilaya = self.get_argument("wilaya")
            commune = self.get_argument("commune")
            try:
                coord = villes(commune)
            except KeyError:
                self.redirect("/pirate")
            site = self.get_argument("site")
            try:
                ava = self.request.files['avatar'][0] # get the picture.
                avat = ava["body"] # get the picture contents
                avctype = ava["content_type"] # get the image type

                '''
                to limit picture size, go to IOStream.py and modify def __init__(self, socket, io_loop=None, max_buffer_size=104857600,read_chunk_size=4096)
                and replace 104857600 (100 mega) by your value, personaly i put 1 mega (1048576 octets), or you can override this with your own class.
                '''

                image = Image.open(StringIO.StringIO(buf=avat))
                type = image.format
                (x, y) = image.size
                if x < y:
                    orientation = "portrait"
                else:
                    orientation = "paysage"
                pref = str(time.time()) #ok, c une astuce bidon mais bon...
                nomfich = pref.replace(".", "") + "-" + ava["filename"]
                """
                # use this if  you want to use filesystem instead of gridfs
                pat = path.join(path.dirname(__file__), "users")
                a = "{0}/{1}".format(pat, email)
                if not path.exists(a):
                    #print path.exists("{0}/{1}".format(pat, email))
                    if os.name == "nt":
                        os.system("mkdir users\{0}".format(email))
                    elif os.name == "posix":
                        os.system("mkdir /users/{0} -p".format(email))
                    pth = r"{0}/{1}/{2}".format(pat, email, nomfich)
                    #print pth
                    avatar = image.save(pth)
                else:
                    pth = ""
                    pass #
                """
            except (IOError, TypeError):
                self.write("<h1>Veuillez utiliser un fichier image valide</h1>")

            imid = yield fs.put(avat, content_type=avctype, filename = nomfich) # gridfs id
            statut = self.get_argument("statut")
            if statut == "entreprise":
                telf = self.get_argument("telf")
                if validatorE(email, pseudo, password, tel, telf, pass1, pass2):
                    self.redirect("/pirate")
                else:
                    user={"_id":email,
                        "prs":{
                            "dt":datetime.datetime.now(),
                            "pseu":pseudo,
                            "pass":password,
                            "tel":tel,
                            "tef":telf,
                            "stt":statut},
                        "avt":{
                            "ori":orientation,
                            "avt":imid},
                        "adr":{
                            "wil":wilaya,
                            "com":commune,
                            "cor":coord,
                            "sit":site
                            }
                            }
                    try:
                        yield db.users.insert(user)
                        self.redirect("/#login")
                    except DuplicateKeyError: # if the user already exists
                        self.write("<h1>Utilisateur deja existant!</h1>")
                        self.finish()
            elif statut == "particulier":
                nom = self.get_argument("nom").lower()
                prenom = self.get_argument("prenom").lower()
                daten = self.get_argument("daten")
                datt = daten.split("-")
                (y, m, d) = (datt[0],datt[1],datt[2])
                try:
                    datetime.date(int(y), int(m), int(d))
                except ValueError:
                    self.redirect("/pirate")
                sexe = self.get_argument("sexe")
                if validatorP(email, pseudo, password, tel, pass1, pass2, nom, prenom, daten, sexe):
                    self.redirect("/pirate")
                else:
                    user={"_id":email,
                        "prs":{
                            "dt":datetime.datetime.now(),
                            "pseu":pseudo,
                            "pass":password,
                            "tel":tel,
                            "stt":statut,
                            "nom":nom,
                            "prn":prenom,
                            "dtn":daten,
                            "sxe":sexe},
                        "avt":{
                            "ori":orientation,
                            "avt":imid},
                        "adr":{
                            "wil":wilaya,
                            "com":commune,
                            "cor":coord,
                            "sit":site
                            }
                            }
                    try:
                        yield db.users.insert(user)
                        self.redirect("/#login")
                    except DuplicateKeyError:
                            self.redirect("/passloss")
        except (AutoReconnect):
                self.redirect("/error")

# sell handler
class Vendre(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        namep = self.get_argument("namep").lower()
        description = self.get_argument("description")[:160].lower()
        tags = [ tag.lower() for tag in self.get_arguments("tags")]
        print (namep, description, tags)
        #tag = [x.strip('\\\"\',!*&^%#$;:+') for x in set(tags.split())] this will cut  a sentence to words, uncomment it if you want to use it
        if "" in (namep,description, tags):
            self.redirect("/pirate")
        else:
            try:
                fs = motor.MotorGridFS(db)
                prix = int(self.get_argument("prix")) # html uses strings, so dont forget to convert what you need, here we need integer
                echange = self.get_argument("echange")
                if echange not in ["non", "oui"]:
                    self.redirect("/pirate")
                etat = self.get_argument("etat")
                if etat not in ["se", "be", "ac"]:
                    self.redirect("/pirate")
                date = datetime.datetime.now()

                ava = self.request.files['photo'][0]
                avat = ava["body"]
                avctype = ava["content_type"]
                image = Image.open(StringIO.StringIO(buf=avat))
                type = image.format
                (x, y) = image.size
                if x < y:
                    orientation = "portrait"
                else:
                    orientation = "paysage"
                pref = str(time.time())
                nomfich = pref.replace(".", "") + "-" + ava["filename"]
                try:
                    yield db.users.update({"_id": email},{"$push":{
                                                            "pup":{
                                                                 "spec":{
                                                                         "np":namep,
                                                                         "pri":prix,
                                                                         "dsp":description,
                                                                         "tag":tags,
                                                                         "dt":date,
                                                                         "eta":etat,
                                                                         "chng":echange,
                                                                         "own":simpleencode.b64encode(email),
                                                                         },
                                                                 "avt":{
                                                                           "fto":(yield fs.put(avat, content_type=avctype, filename = nomfich)),
                                                                           "ori":orientation,
                                                                           }
                                                                 }
                                                   }})
                    self.render("uploaded.html", op="vente")
                except (AutoReconnect):
                    self.redirect("/error")
                """
                # same if you dont use gridfs
                pat = path.join(path.dirname(__file__), "users")
                pth = r"{0}/{1}/{2}".format(pat, email, nomfich)
                avatar = image.save(pth)
                """
            except (KeyError, ValueError, TypeError):
                self.write("<h1>pirate<h1>")
            except (IOError):
                self.write("<h1>Veuillez utiliser un fichier image valide</h1>")

# product search
class Search(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        debut = time.time()
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        center = info["adr"]["cor"]

        pseudo = self.get_argument("pseudo").lower()
        if not pseudo:
            pseudo = ""
        tel = self.get_argument("tel")
        if not tel:
            tel = "0700000000"
        else:
            if not re.match("0[5-7][5-9][0-9]{7}$", tel): # used algeria gsm system.
                self.redirect("/pirate")

        nomp = self.get_argument("nom").lower()
        if not nomp:
            nomp = ""
        description = [x.strip(',!*&^%#$;:+') for x in self.get_argument("description").lower().split()]
        if not description:
            description = []

        sommemax = self.get_argument("sommemax")
        if sommemax:
            sommemax = int(sommemax)
        else:
            sommemax = 0

        sommemin = self.get_argument("sommemin")

        # if only one field is put, the min or the max.
        if sommemin and sommemax == 0:
            sommemin = int(sommemin)
            sommemax = 10000000000
        elif sommemin and sommemax != 0:
            sommemin = int(sommemin)
            sommemax = sommemax
        elif sommemin == "":
            sommemin = 0

        commune = self.get_argument("commune")
        if not commune:
            commune = ""

        perim = self.get_argument("perim")
        if not perim:
            center = [0, 0]
            perim = 0
        else:
            perim = float(perim)/6371 # transform meters to get radians http://stackoverflow.com/questions/17415192/how-to-use-geowithin-in-mongodb

        try:
            pseud = yield db.users.find({"prs.pseu":pseudo}).distinct("pup")
            resultpseudo = len(pseud)

            telp = yield db.users.find({"prs.tel":tel}).distinct("pup")
            resultel = len(telp)

            # without aggregation, you will get the root documents and not the sub documents

            resultnomp = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.np":nomp}}, {"$group":{"_id":"sum","pup":{"$sum":1}}}]) # specify and element using a $ for example $_id to group using _id
            if resultnomp["result"]:
                total0 = resultnomp["result"][0]["pup"]
            else:
                total0 = 0

            resultdescription = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.tag":{"$in":description}}}, {"$group":{"_id":"sum","pup":{"$sum":1}}}])
            if resultdescription["result"]:
                total1 = resultdescription["result"][0]["pup"]
            else:
                total1 = 0

            resultsomme = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.pri":{"$gte": sommemin, "$lte": sommemax}}}, {"$group":{"_id":"sum","pup":{"$sum":1}}}])
            if resultsomme["result"]:
                total2 = resultsomme["result"][0]["pup"]
            else:
                total2 = 0

            commun = yield db.users.find({"adr.com":commune}).distinct("pup")
            resultcommune =  len(commun)

            per = yield db.users.find({"adr.cor":{"$geoWithin":{"$center":[center, perim]}}}).distinct("pup")

            resultperim = len(per)

            self.render("resultats.html",resultpseudo=resultpseudo,resultel=resultel,resultnomp=resultnomp,resultdescription=resultdescription,resultsomme=resultsomme,resultcommune=resultcommune,resultperim=resultperim,
                        pseudo=pseudo,tel=tel,nomp=nomp,description=description,sommemax =sommemax,sommemin=sommemin,commune=commune,perim=perim, total0=total0, total1=total1, total2=total2)
        except (AutoReconnect):
                self.redirect("/error")

#seach by pseudo
class SearchePseudo(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        pseudo = self.get_argument("pseudo")
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"prs.pseu":pseudo}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}, {"$project" : {"_id":0, "pup":1}}]) # "$key" to group by key
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#seach by telephone number
class SearchTel(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        tel = self.get_argument("tel")
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"prs.tel":tel}},{"$skip":s}, {"$limit":5},{"$group":{"_id":0,"pup":{"$push":"$pup"}}}, {"$project" : {"_id":0, "pup":1}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#seach by product name
class SearchNom(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        nomp = self.get_argument("nomp")
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.np":nomp}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}, {"$project" : {"_id":0, "pup":1}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#seach by tags
class SearchDescr(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        descr = self.get_argument("description")
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.tag":{"$in":[descr]}}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
            produit = produits["result"]
            avatar = []
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#seach by price ascending
class SearchPrixCr(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        smin = int(self.get_argument("sommemin"))
        smax = int(self.get_argument("sommemax"))
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.pri":{"$gte": smin, "$lte": smax}}},{"$sort":{"pup.spec.pri":1}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s)
        except (AutoReconnect):
                self.redirect("/error")

#seach by price, descending
class SearchPrixDec(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        smin = int(self.get_argument("sommemin"))
        smax = int(self.get_argument("sommemax"))
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.pri":{"$gte": smin, "$lte": smax}}}, {"$sort":{"pup.spec.pri":-1}}, {"$skip":s}, {"$limit":5}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s)
        except (AutoReconnect):
                self.redirect("/error")

#seach by city
class SearchBled(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        com = self.get_argument("commune")
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"adr.com":com}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":"$pup.spec.id","pup":{"$push":"$pup"}}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#seach by perimeter
class SearchCoord(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        perim = float(self.get_argument("perim"))/6371
        s = int(self.get_argument("s"))
        url = self.request.uri
        lin = spliter.split(url)[0]
        link = spliter.split(url)[1]
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        center = info["adr"]["cor"]
        try:
            fs = motor.MotorGridFS(db)
            up = yield db.users.find_one({"_id":email})
            achat = []
            try:
                for i in up["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"adr.cor":{"$within":{"$center":[center, perim]}}}},{"$skip":s}, {"$limit":5}, {"$group":{"_id":"$pup.spec.id","pup":{"$push":"$pup"}}}])
            avatar = []
            produit = produits["result"]
            if produit:
                for prod in produit:
                    for i in prod["pup"]:
                        gridout = yield fs.get(i["avt"]["fto"])
                        name = avatar.append(gridout.filename)
                produits = prod["pup"]
            else:
                produits = []
            npages = len(produits) // 5 # a simple  hack to show or hide next and  previous buttons
            self.render("ventes.html", produits=produits, avatar=avatar, achat=achat, op="srch", email=email, npages=npages, lin=lin, link=link, replace=replace, s=s )
        except (AutoReconnect):
                self.redirect("/error")

#add to cart
class Acheter(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        prod = self.get_argument("prod")
        try:
            pup = yield db.users.find_one({"pup.avt.fto":ObjectId('{0}'.format(prod))}, {"pup.avt.fto.$":1})
            yield db.users.update({"_id":email}, {"$push":{"pdn":pup["pup"][0]}})
            yield db.users.update({"pup.avt.fto":ObjectId('{0}'.format(prod))}, {"$addToSet":{"pup.$.cln":email}})
            self.render("uploaded.html", op="achat")
        except AutoReconnect:
            self.redirect("/error")

#report a bad product
class Report(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        no = self.get_argument("prod")
        nom = simpleencode.decode(str(no), email[5::-1])
        yield db.users.update({"pup.avt.fto":ObjectId('{0}'.format(nom))},{"$addToSet":{"pup.$.abu":email}})
        abus = db.users.find({"pup.avt.fto":ObjectId('{0}'.format(nom))}, {"abus":1})
        nabus = yield abus.count
        yield db.users.update({"pup.avt.fto":ObjectId('{0}'.format(nom))},{"$set":{"pup.$.nab":nabus}})
        self.render("uploaded.html", op="report")

#my uploads
class MesVentes(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            produits = yield db.users.find_one({"_id":email}, {"pup":1})
            avatar = []
            nbr = 0
            try:
                produit = produits["pup"]
                nbr = len(produit)
                for pro in produit:
                    gridout = yield fs.get(pro["avt"]["fto"])
                    name = avatar.append(gridout.filename)
            except (KeyError, TypeError):
                produit = []
            self.render("ventes.html", email=email, produits=produit, avatar=avatar, op="vente", npages=0, lin="", link="", replace="", s=0)
        except (AutoReconnect):
            self.redirect("/error")

#my cart
class MesAchats(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            produits = yield db.users.find_one({"_id":email}, {"pdn":1})
            achat = []
            try:
                for i in produits["pdn"]:
                    achat.append(str(i["avt"]["fto"]))
            except KeyError:
                achat = []
            avatar = []
            nbr = 0
            try:
                produit = produits["pdn"]
                nbr = len(produit)
                for pro in produit:
                    gridout = yield fs.get(pro["avt"]["fto"])
                    name = avatar.append(gridout.filename)
            except (KeyError, TypeError, IndexError):
                produit = []
            except NoFile as e: # we will catch the ObjectId and then delete it!
                '''
                catcher = re.compile("\('\w+'\)") # the harder way, will always work, but need more processing ;)
                id = catcher.findall(str(e))[0].strip("(,)'")
                '''
                id = str(e)[-25:-3] # since the error is always the same, unless the driver change how alert users ;)
                yield db.users.update({"pdn.avt.fto":ObjectId('{0}'.format(id))},{"$pull":{"pdn":{"avt.fto":ObjectId('{0}'.format(id))}}})
            self.render("ventes.html", achat=achat, email=email, produits=produit,  avatar=avatar, op="achat", npages=0, lin="", link="", replace="", s=0 )
        except (AutoReconnect):
            self.redirect("/error")

# delete a product
'''
the tip is to delete gridFS entry, so we will not get deleted products and its data still in gridfs
'''
class Supprimer(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        prod = self.get_argument("supprime") # toujours se souvenir; HTTP travail avec des caracteres donc il faut penser a faire des operation pour extraire la donnee
        produ = simpleencode.decode(str(prod), email[5::-1])
        try:
            fs = motor.MotorGridFS(db)
            yield db.users.update({"pup.avt.fto":ObjectId('{0}'.format(produ))},{"$pull":{"pup":{"avt.fto":ObjectId('{0}'.format(produ))}}})
            yield fs.delete(ObjectId("{0}".format(produ)))
            self.redirect("/ventes")
        except InvalidId:
            self.redirect("pirate")
        except AutoReconnect:
            self.redirect("/error")

# delete from cart, of course, the product is not deleted from database, it is something like Unlike ;)
class Enlever(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        link = self.request.uri
        info = json_util.loads(user)
        email = info["_id"]
        prod = self.get_argument("enleve")
        try:
            yield db.users.update({"_id":email},{"$pull":{"pdn":{"avt.fto":ObjectId("{0}".format(prod))}}})
            self.redirect("/achats")
        except (AutoReconnect):
            self.redirect("/error")

# product page
class Produit(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, id):
        id = self.get_argument("id")
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        try:
            fs = motor.MotorGridFS(db)
            parr = yield db.users.find_one({"pup.avt.fto":ObjectId("{0}".format(id))}, {"adr":1, "avt":1, "prs":1, "pup":{"$elemMatch":{"avt.fto":ObjectId("{0}".format(id))}}})
            up = yield db.users.find_one({"_id":email})
            yield db.users.update({"pup.avt.fto":ObjectId('{0}'.format(id))}, {"$addToSet":{"pup.$.viz":email}})

            avat = []
            try:
                cmnt = parr["pup"][0]["cmn"] # this one for the comments avatar pictures
                for pic in cmnt:
                    gridout = yield fs.get(pic["fto"])
                    name = avat.append(gridout.filename)
            except (KeyError, TypeError):
                cmnt = []

            achats = []
            try:
                for i in up["pdn"]:
                    achats.append(str(i["avt"]["fto"]))
                if id in achats:
                    exist = 1
                else:
                    exist = 0
            except (KeyError, TypeError):
                exist = 0
            # another technique
            #parr = yield db.users.find_one({"pup.avt.fto":ObjectId("{0}".format(id))}, {"adr":1, "avt":1, "prs":1, "pup.spec.$.id":1})
            gridout = yield fs.get(parr["pup"][0]["avt"]["fto"])
            avatar = gridout.filename
            self.render("produit.html", parr=parr, avatar=avatar, email=email, exist=exist, avat=avat)
        except (AutoReconnect):
            self.redirect("/error")

# add a comment
class Comment(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        link = self.request.uri
        info = json_util.loads(user)
        email = info["_id"]
        pseudo = info["prs"]["pseu"]
        avat = info["avt"]["avt"]
        print avat
        fs = motor.MotorGridFS(db)
        cmnt = self.get_argument("description")[:160]
        i = self.get_argument("id")
        id = simpleencode.b64decode(i)[::-1] # dumb technique but it will make him struggle for a moment :p
        tim = int(time.time())
        yield db.users.update({"pup.avt.fto": ObjectId("{0}".format(id))},{"$push":{"pup.$.cmn":{"prs":email, "pse":pseudo, "fto":avat, "txt": cmnt, "id":time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(tim))}}})
        self.redirect("/info?id={0}".format(id))

# todo, report bad comment, sadly art this time (mongodb 2.4.4) cant add a field in level 2 of documents
class BadComment(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        code = self.get_argument("id")
        id = simpleencode.b64decode(code)
        h = yield db.users.update({"pup.cmn.id":id}, {"$addToSet":{"pup.$.cmn":{"abus":email}}})
        self.render("uploaded.html", op="report")

'''
# un comment this class to use google compare instead of amazon compare
class GCompare(BaseHandler):
    #Google product search api, using blocking http calls, he just to test, waiting someone or maybe YOU to make the async version ^^-
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        client = build('shopping', 'v1', developerKey='AIzaSyAyVydijB727EG8YWp1MizQnOzkXhLJVQQ')
        ressource = client.products()
        request = ressource.list(source='public', country='FR', q=u'iphone 3gs')
        t = request.execute()
        for i in range(len(t["items"])):
            print i
            #print t["items"][i]["product"]["inventories"][0]["price"] # les prix
            #print t["items"][0]["product"]["link"] # les liens
'''

# amazon compare, sadly blocking, hope we will get a non-blocking library
class ACompare(BaseHandler):
    def post(self):
        namep = self.get_argument("namep")
        api = amazon.AmazonAPI(access_key_ID, secret_key, Associate_Tag, region="FR")
        res = api.search_n(5, Keywords=namep, SearchIndex='All')
        result = []
        for i in res:
            result.append([i.price_and_currency, i.title, i.offer_url, i.medium_image_url])
        self.render("compare.html", result=result)

# logout handler, simply deleted the cookie
class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("mechtari")
        self.redirect("/")

# when there is javascript but the user hacked it
class NoJsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pirate!")

class Pirate(tornado.web.RequestHandler):
    def get(self):
        self.write("<h1>PIRATE!</h1>")


#here we go with pass reset, in case the user forgot his password
class Rese(BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        try:
            email = self.get_argument("mail")
            timr = datetime.datetime.now()
            code = "".join(random.choice(string.digits) for i in range(4))
            asci = simpleencode.encode(str(timr), code)
            pas = yield db.users.find_one({"_id": email})
            print pas
            if pas :
                yield db.users.update({"_id": email}, {"$push":{"reset":{"timr":asci,"code":code}}})
                send_email(email, asci, code) # uncomment this line if you want to send the complete link to your email box, else, you must get the link from the database and forge it by your self localhost:8000/resetYourCode
                self.render("reset-ok.html", message = "Veuillez acc&eacute;der &agrave; votre boite aux lettres pour compl&eacute;ter l'op&eacute;ration.<br /><br />Vous devez le faire dans moins de 48 heures.")
            else:
                self.redirect("/#register")
        except TypeError:
            self.redirect("/#register")

class Reset(BaseHandler):
    @tornado.gen.coroutine
    def get(self, uri):
        uri = self.request.uri
        try:
            debut = time.time()
            tim = uri[6:] #remove /reset/ from the uri
            cod = yield db.users.find_one({"reset.timr":tim})
            code = cod["reset"][-1]["code"]
            email = cod["_id"]
            dat = simpleencode.decode(tim, code)
            now = datetime.datetime.now()
            temps = datetime.datetime.strptime(dat[:19], "%Y-%m-%d %H:%M:%S")
            valid = now - temps
            if valid.days < 2:
                self.render("reset.html", email=email, tim=tim)
            else:
                self.write("Votre code est périmé, veuillez cliquez <a href='/#forget'>ici</a> pour le renouveler")
                self.finish()
        except (ValueError, TypeError, UnboundLocalError):
            self.write("pirate")
            self.finish()

class Resett(BaseHandler):
    @tornado.gen.coroutine
    def post(self):
        pin = self.get_argument("rcode")
        tim = self.get_argument("tim")
        mail = self.get_argument("email")
        cod = yield db.users.find_one({"reset.timr":tim})
        code = cod["reset"][-1]["code"]
        email = cod["_id"]
        if mail == email:
            if pin == code:
                pass1 = self.get_argument("pass1")
                pass2 = self.get_argument("pass2")
                if pass1 == pass2 > 6: # cool python, essayez 5 == 5 > 3, mais sa marchera pas 5 > 3 == 5 evidemment ;)
                    password = hashh.encrypt(pass1, salt_size = 32, rounds = 5000)
                    yield db.users.update({"_id":email}, {"$set":{"prs.pass":password, "prs.dt":datetime.datetime.now(), "reset":[]}, "$inc":{"modif":1}})
                    self.render("reset-ok.html", message = "Votre mot de passe a &eacute;t&eacute; modifi&eacute; avec succ&egrave;s, cliquez <a href='/#login'>ici</a> pour revenir &agrave; la page d'accueil")
                else:
                    self.write("pirate")
                    self.finish()
            else:
                self.write("code incorrect")
                self.finish()
        else: # someone who tried to hide the email
            self.write("pirate")
            self.finish()

#here the password change (the only thing that the user can change :p )
class Change(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        self.render("change.html")

class Changer(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        ancien = self.get_argument("ancien")
        pass1 = self.get_argument("pass1")
        pass2 = self.get_argument("pass2")
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        dbmail = yield db.users.find_one({"_id": email})
        pas = dbmail[0]["prs"]["pass"]
        if hashh.verify(ancien, pas) == True :
            if pass1 == pass2 > 6:
                password = hashh.encrypt(pass1, salt_size = 32, rounds = 5000)
                yield db.users.update({"_id":email}, {"$set":{"prs.pass":password}, "$inc":{"modif":1}})
                self.clear_cookie("mechtari")
                self.render("reset-ok.html", message = "Votre mot de passe a &eacute;t&eacute; modifi&eacute; avec succ&egrave;s, cliquez <a href='/#login'>ici</a> pour revenir &agrave; la page d'accueil")
            else:
                self.write("pirate")
                self.finish()
        else:
            self.write("pirate")
            self.finish()

# discount
class Rabais(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        id = self.get_argument("id")
        rid = simpleencode.decode(str(id), email[5::-1])
        try:
            rid = simpleencode.decode(str(id), email[5::-1]) # simple hack to avoid making soldes for other products ;)
            new = int(float(self.get_argument("new"))) # if you try to use int("new") you get error, then you must first convert it as float
            emails = yield db.users.find_one({"pup.avt.fto":ObjectId("{0}".format(rid))}, {"pup.cln":1, "_id":0})
            try:
                mails = emails["pup"][0]["cln"]
                if (yield db.users.update({"pup.avt.fto":ObjectId("{0}".format(rid))}, {"$set":{"pup.$.spec.pri":new}})):
                    yield db.rabais.save({"_id":rid, "t":datetime.datetime.now(), "mail":email, "vnd":mails}) # sadly, cant use datetime.datetime.now().date as _id, bson cant store dates without time!
            except KeyError:
                if (yield db.users.update({"pup.avt.fto":ObjectId("{0}".format(rid))}, {"$set":{"pup.$.spec.pri":new}})):
                    yield db.rabais.save({"_id":rid, "t":datetime.datetime.now(), "mail":email, "vnd":[]}) # sadly, cant use datetime.datetime.now().date as _id, bson cant store dates without time!

            self.render("uploaded.html", op="rabai")
        except InvalidId:
            self.redirect("pirate")

# generate the url that contains all the discounts
class Urls(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, url):
        user = self.get_secure_cookie("mechtari")
        info = json_util.loads(user)
        email = info["_id"]
        pseudo = info["prs"]["pseu"]
        url = self.request.uri[8:]
        a = yield db.link.find_one({"_id":url})
        self.render("urls.html", links = a["url"], url=url, pseudo=pseudo)

# here we go with admin handler, will use google openId to connect, for maximum security
class AdminHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("alien")
        if not user_json: return None
        return json_util.loads(user_json)

class Admin(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        # look at the results returned from google ;)
        print self.current_user
        if tornado.escape.xhtml_escape(self.current_user["email"]) == "your_email@gmail.com": # here you put your email (admin) or all those using gmail will access to your admin page if they got the url ;)
            self.redirect("/all")
        else:
            self.write("pirate")

class gAuthHandler(AdminHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        self.set_secure_cookie("alien", tornado.escape.json_encode(user))
        self.redirect("/alien")

class gLogoutHandler(AdminHandler):
    def get(self):
        self.clear_cookie("alien")
        self.write('You are now logged out. Click <a href="/galien/login">here</a> to log back in.')

# get all products
class AllProduits(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        url = self.request.uri
        lin = spliter.split(url)[0]
        if  len(spliter.split(url)) > 1:
            link = spliter.split(url)[1]
            a = re.compile('\d+')
            s = int(a.findall(link)[0])
        else:
            link = ''
            s = 0
        fs = motor.MotorGridFS(db)
        produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{}},{"$skip":s}, {"$limit":10}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
        avatar = []
        produit = produits["result"]
        if produit:
            for prod in produit:
                for i in prod["pup"]:
                    gridout = yield fs.get(i["avt"]["fto"])
                    name = avatar.append(gridout.filename)
            produits = prod["pup"]
        else:
            produits = []
        npages = len(produits) // 10 # a simple  hack to show or hide next and  previous buttons
        self.render("admin.html", produits=produits, avatar=avatar, npages=npages, lin=lin, s=s )

# get outdated product to be cleaned (more than 1 year)
class Perim(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        today = datetime.datetime.now()
        year = datetime.timedelta(365)
        url = self.request.uri
        lin = spliter.split(url)[0]
        if  len(spliter.split(url)) > 1:
            link = spliter.split(url)[1]
            a = re.compile('\d+')
            s = int(a.findall(link)[0])
        else:
            link = ''
            s = 0
        fs = motor.MotorGridFS(db)
        produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.spec.dt":{"$gt":today+year}}},{"$skip":s}, {"$limit":10}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
        avatar = []
        produit = produits["result"]
        if produit:
            for prod in produit:
                for i in prod["pup"]:
                    gridout = yield fs.get(i["avt"]["fto"])
                    name = avatar.append(gridout.filename)
            produits = prod["pup"]
        else:
            produits = []
        npages = len(produits) // 10 # a simple  hack to show or hide next and  previous buttons
        self.render("admin.html", produits=produits, avatar=avatar, npages=npages, lin=lin, s=s )

# get reported products
class AbuProduits(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        url = self.request.uri
        lin = spliter.split(url)[0]
        if  len(spliter.split(url)) > 1:
            link = spliter.split(url)[1]
            a = re.compile('\d+')
            s = int(a.findall(link)[0])
        else:
            link = ''
            s = 0
        fs = motor.MotorGridFS(db)
        produits = yield db.users.aggregate([{"$unwind":"$pup"},{"$match":{"pup.nab":{"$gte":1}}},{"$skip":s}, {"$limit":10}, {"$group":{"_id":0,"pup":{"$push":"$pup"}}}])
        avatar = []
        produit = produits["result"]
        if produit:
            for prod in produit:
                for i in prod["pup"]:
                    gridout = yield fs.get(i["avt"]["fto"])
                    name = avatar.append(gridout.filename)
            produits = prod["pup"]
        else:
            produits = []
        npages = len(produits) // 10 # a simple  hack to show or hide next and  previous buttons
        self.render("admin.html", produits=produits, avatar=avatar, npages=npages, lin=lin, s=s )

# get outdated password to encourage users to rewrite them to be re-hashed with new algorithmes more powerful (Moore law)
class PassPerim(AdminHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        today = datetime.datetime.now()
        year = datetime.timedelta(365)
        result = yield db.users.find({"prs.dt":{"$gt":today+year}}).distinct("_id")
        # todo: implement email sender to alert them
        self.render("pass.html", result = result)
