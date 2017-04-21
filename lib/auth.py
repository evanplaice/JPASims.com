"""@auth
Auth decorators and their helper functions

Neatly packaged auth decorators that can be easily attached to any handler.
"""

import base64
import logging
import os
import sys
from webapp2_extras import security
import yaml

sys.path.insert(0, os.path.abspath('..'))
import lib.recaptcha

def basic_auth(func):
  def callf(webappRequest, *args, **kwargs):
    # Parse the header to extract a user/password combo.
    # We're expecting something like "Basic XZxgZRTpbjpvcGVuIHYlc4FkZQ=="
    auth_header = webappRequest.request.headers.get('Authorization')

    if auth_header == None:
      __basic_login(webappRequest)
    else:
      (username, password) = base64.b64decode(auth_header.split(' ')[1]).split(':')
      if(__basic_lookup(username) == __basic_hash(password)):
        return func(webappRequest, *args, **kwargs)
      else:
        __basic_login(webappRequest)
  return callf

def __basic_login(webappRequest):
    webappRequest.response.set_status(401, message="Authorization Required")
    webappRequest.response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'

def __basic_lookup(username):
  accounts_file = os.getcwd() + os.sep + 'accounts.yaml'
  account_data = file(accounts_file, 'r')
  accounts = yaml.load(account_data)['basic']
  for account in accounts:
    if account['username'] == username:
      return account['password']

def __basic_hash(password):
  return security.hash_password(password, method='sha1')