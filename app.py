#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import handlers, os
from motor.web import GridFSHandler

#trying to make a random port number because Heroku dont like the 8000 number?
define("port",default=8000,type=int)

urls = [
    (r"/", handlers.MainHandler),
    (r"/register", handlers.Statut),
    (r"/nojs/*", handlers.NoJsHandler),
    (r"/profile", handlers.Registration),
    (r"/profil/*", handlers.Profil),
    (r"/login", handlers.LoginHandler),
    (r"/reset", handlers.Rese),
    (r"/reset([a-zA-Z0-9=]*)", handlers.Reset),
    (r"/pass-back", handlers.Resett),
    (r"/logout", handlers.LogoutHandler),
    (r"/pirate", handlers.Pirate),
    (r"/vendre", handlers.Vendre),
    (r"/chercher", handlers.Search),
    (r"/supprimer", handlers.Supprimer),
    (r"/enlever", handlers.Enlever),
    (r"/ventes/*", handlers.MesVentes),
    (r"/achats/*", handlers.MesAchats),
    (r"/search-pseudo", handlers.SearchePseudo),
    (r"/search-tel", handlers.SearchTel),
    (r"/search-nomp", handlers.SearchNom),
    (r"/search-desc", handlers.SearchDescr),
    (r"/search-sommcr", handlers.SearchPrixCr),
    (r"/search-somdsc", handlers.SearchPrixDec),
    (r"/search-commune", handlers.SearchBled),
    (r"/search-coord", handlers.SearchCoord),
    (r"/comment", handlers.Comment),
    (r"/cart", handlers.Acheter),
    (r"/change", handlers.Change),
    (r"/pass-change", handlers.Changer),
    (r"/info/*([a-zA-Z0-9]+)*", handlers.Produit),
    (r"/rabais/([a-zA-Z0-9=]+)", handlers.Urls),
    (r"/report", handlers.Report),
   # (r"/bad", handlers.BadComment),
        
   # (r"/google", handlers.GCompare),
    (r"/amazon", handlers.ACompare),
    (r"/rabai", handlers.Rabais),
    (r"/alien", handlers.Admin),
    (r"/all", handlers.AllProduits),
    (r"/abu", handlers.AbuProduits),
    (r"/perime", handlers.Perim),
    (r"/password", handlers.PassPerim),
    (r"/galien/login", handlers.gAuthHandler),
    (r"/galien/logout", handlers.gLogoutHandler),
    (r"/(.+)", GridFSHandler, {"database": handlers.db}),
    #(r"/(.*)", tornado.web.StaticFileHandler, {"path":r"{0}".format(os.path.dirname(__file__))})
]

settings = dict({
    "template_path": os.path.join(os.path.dirname(__file__),"templates"),
    "static_path": os.path.join(os.path.dirname(__file__),"static"),
    "cookie_secret": os.urandom(10), # avec os.urandom(un chiffre) il aura du mal le pauvre pirate a deviner la cle secrete
    "xsrf_cookies": True,
    "gzip": True,
    "login_url": "/#login", # c ici que le decorateur @tornado.web.authenticated renvoie l'utilisateur s'il n'est pas 'logged in'
})

application = tornado.web.Application(urls,**settings)


if __name__ == "__main__":
    options.parse_command_line()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
