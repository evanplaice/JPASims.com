"""@handlers
Handlers for the datastore

The glue that binds routes to their corresponding functionality.
"""

import json
import logging
import os
import sys
import webapp2
from webapp2_extras import jinja2

import models

sys.path.insert(0, os.path.abspath('..'))
from lib.auth import basic_auth


class DataHandler(webapp2.RequestHandler):
  """The handler that manages models

  This handler is used to interact with the datastore.
  """

  def get(self, **params):
    model = params.get('_model')
    action = params.get('_action')
    query_string = self.request.query_string
    if '=' in query_string:
      url_params = dict([x.split("=") for x in query_string.split("&")])
      params = dict(params.items() + url_params.items())
    else:
      params = params
    module = __import__('api.models', fromlist=[model])
    model_instance = getattr(module, model)()
    (content_type, result) = getattr(model_instance, action)(**params)
    self.response.headers.add_header('content-type', content_type, charset='utf-8')
    self.response.write(result)
    logging.debug('GET - Model: ' + model + ', Action: ' + action)
  
  @basic_auth
  def post(self, **params):
    model = params.get('_model')
    action = params.get('_action')
    data = json.loads(self.request.body)
    module = __import__('api.models', fromlist=[model])
    model_instance = getattr(module, model)()
    result = getattr(model_instance, action)(data)
    self.response.write(result)
    logging.debug('POST - Model: ' + model + ', Action: ' + action)

  @basic_auth
  def delete(self, **params):
    model = params.get('_model')
    action = params.get('_action')
    module = __import__('api.models', fromlist=[model])
    model_instance = getattr(module, model)()
    result = getattr(model_instance, action)()
    self.response.write(result)
    logging.debug('DELETE - Model: ' + model + ', Action: ' + action)