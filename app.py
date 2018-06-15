import cherrypy
import os
import redis
import json
import redisconfig


class Root(object):
    @cherrypy.expose
    def index(self):
        with open("html/index.html", "r") as indexFile:
            data = indexFile.read()
        return data

    @cherrypy.expose
    def toptenstocks(self):
        r = None
        if (cherrypy.request.method == "GET"):
            cherrypy.response.headers['Content-Type'] = "text/json"
            try:
                redistogo_url = os.environ.get("REDISTOGO_URL")
                if (not redistogo_url):
                    pool = redis.ConnectionPool(host=redisconfig.host,
                                                port=redisconfig.port,
                                                db=redisconfig.db,
                                                decode_responses=redisconfig
                                                .decode_responses_value)
                    r = redis.Redis(connection_pool=pool)
                else:
                    r = redis.from_url(redistogo_url,
                                       decode_responses=redisconfig
                                       .decode_responses_value)
            except:
                print("Error Connecting to Redis")
                raise cherrypy.HTTPError(status=500)
            return json.dumps(r.lrange("BhavCopy", 0, -1))
        else:
            raise cherrypy.HTTPError(status=400)

    @cherrypy.expose
    def getstockdata(self, name=None):
        r = None
        if (cherrypy.request.method == "GET"):
            cherrypy.response.headers['Content-Type'] = "text/json"
            try:
                redistogo_url = os.environ.get("REDISTOGO_URL")
                if (not redistogo_url):
                    pool = redis.ConnectionPool(host=redisconfig.host,
                                                port=redisconfig.port,
                                                db=redisconfig.db,
                                                decode_responses=redisconfig
                                                .decode_responses_value)
                    r = redis.Redis(connection_pool=pool)
                else:
                    r = redis.from_url(redistogo_url,
                                       decode_responses=redisconfig
                                       .decode_responses_value)
            except:
                print("Error Connecting to Redis")
                raise cherrypy.HTTPError(status=500)
            if (name):
                name = name + " " * (12 - len(name))
                print(r.hgetall(name))
                return json.dumps(r.hgetall(name))
            else:
                return json.dumps({"Error": "E100"})
        else:
            raise cherrypy.HTTPError(status=400)


if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    port_number = os.environ.get("PORT")
    if(port_number):
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': int(port_number)})
    cherrypy.quickstart(Root(), '/', config)
