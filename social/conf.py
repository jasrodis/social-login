import os
import uuid
import cherrypy
import jinja2
import simplejson as json

import logging
import logging.config

import cherrypy


def colorize(json_obj):
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter

    json_str = json.dumps(json_obj, indent=4, sort_keys=True)

    return highlight(json_str, JsonLexer(), TerminalFormatter())


def render(template_root, template_name, model=None):
    env_loader = jinja2.FileSystemLoader(template_root)
    jinja_env = jinja2.Environment(loader=env_loader)
    template = jinja_env.get_template(template_name)

    if type(model) is not dict:
        model = {}

    return template.render(model)


def read_file_as_json(creds):
    with open(creds) as f:
        return json.loads(f.read())


def session(key):
    if key not in cherrypy.session:
        return None
    return cherrypy.session[key]


def update_session(k, v):
    cherrypy.session[k] = v


def start_server(root_path, root_object):

    cherrypy.server.ssl_module = 'builtin'
    cherrypy.server.ssl_certificate = os.path.join(root_path, 'cert.pem')
    cherrypy.server.ssl_private_key = os.path.join(root_path, 'privkey.pem')

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': root_path,
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './assets'
        }
    }

    cherrypy.config.update({
        'server.socket_port': 443,
        'engine.autoreload.on': False
    })
    
    cherrypy.config.update({
        'log.screen': False,
        'log.access_file': '',
        'log.error_file': ''
    })
    cherrypy.engine.unsubscribe('graceful', cherrypy.log.reopen_files)
    cherrypy.quickstart(root_object, '/', conf)





