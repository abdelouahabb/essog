#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
from pymongo import MongoClient # no need for asynchronous calls since there will be always only one call at time, no other clients
import sys
from urllib import urlopen
import datetime
from base64 import urlsafe_b64encode
import base64
 
from tornado.options import define, options
 
# get your facebook application here https://developers.facebook.com/apps
define("port", default=8888, help="run on the given port", type=int)
define("facebook_api_key", help="your Facebook application API key",
       default="")
define("facebook_secret", help="your Facebook application secret",
       default="")

db = MongoClient().essog

diff = datetime.timedelta(1)
now = datetime.datetime.now()

url = urlsafe_b64encode(str(now))

list = db.rabais.find({"t":{"$lt":now+diff, "$gte":now-diff}}).distinct("_id")

if list:
    link = "http://localhost:8000/info?id="  
    urls = []
    for i in list:
        urls.append(link+str(i))
    db.link.save({"_id":url, "url":urls}) # push those links, because dident know how to post more than one link to facebook, so the hack is to save them to the database an recall them

    message = "Bonsoir chers clients, Voici les nouveaux rabais de la journée sur ce lien: "
    
    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
                (r"/", MainHandler),
                (r"/auth/login", AuthLoginHandler)]
            settings = dict(
                cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                login_url="/auth/login",
                xsrf_cookies=True,
                facebook_api_key=options.facebook_api_key,
                facebook_secret=options.facebook_secret)
            tornado.web.Application.__init__(self, handlers, **settings)
     
     
    class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
            user_json = self.get_secure_cookie("alien")
            if not user_json: return None
            return tornado.escape.json_decode(user_json)
     
     
    class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
        @tornado.web.authenticated
        @tornado.web.asynchronous
        def get(self):
            self.facebook_request("/me/accounts", self._on_accounts, access_token=self.current_user["access_token"])
        
        def _on_accounts(self, account):
            if account is None:
                # Session may have expired
                print "on accounts failed"
                return
                sys.exit()
            
            print "here we go!"
            print account
            for acc in account["data"]:
                if acc["id"] == "345632575539519":
                    print acc["access_token"]
                    # put your application id
                    self.facebook_request("/345632575539519/feed", post_args={"message":"{0}".format(message), "link": "http://www.essog.dz/{0}".format(url)}, access_token=acc["access_token"], callback=self.async_callback(self._on_page_post))
                    print "bzzzz"
     
        def _on_page_post(self, post):
            if not post:
                # Post failed
                return
            sys.exit()
     
    class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
        @tornado.web.asynchronous
        def get(self):
            my_url = (self.request.protocol+"://"+self.request.host+"/auth/login?next="+tornado.escape.url_escape(self.get_argument("next", "/")))
            if self.get_argument("code", False):
                self.get_authenticated_user(
                    redirect_uri=my_url,
                    client_id=self.settings["facebook_api_key"],
                    client_secret=self.settings["facebook_secret"],
                    code=self.get_argument("code"),
                    callback=self._on_auth)
                return
            self.authorize_redirect(redirect_uri=my_url,
                                    client_id=self.settings["facebook_api_key"],
                                    extra_params={"scope": "publish_stream, manage_pages"})
        
        def _on_auth(self, user):
            if not user:
                raise tornado.web.HTTPError(500, "Facebook auth failed")
            self.set_secure_cookie("alien", tornado.escape.json_encode(user))
            self.redirect(self.get_argument("next", "/"))
    
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()