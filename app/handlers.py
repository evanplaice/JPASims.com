"""@handlers
Handlers for the site

The glue that binds routes to their corresponding functionality.
"""

from google.appengine.api import mail
import logging
import os
import sys
import webapp2
from webapp2_extras import jinja2

import urls
from views import XMLViewLoader

sys.path.insert(0, os.path.abspath('..'))
from lib.auth import basic_auth
from lib.recaptcha import recaptcha_verify, recaptcha_html


class BaseHandler(webapp2.RequestHandler):
  """The base class for all calls to the templating engine

  This class sets up the initial configuration for jinja2 and makes
  rendering possible in subclasses. It can be called on it's own but
  it's designed to be inherited.
  """

  @webapp2.cached_property
  def jinja2(self):
    j = jinja2.get_jinja2(app=self.app)
    #j.environment.filters.update({
        # Set filters.
        # ...
    #})
    #j.environment.globals.update({
        # Set global variables.
        #'uri_for': webapp2.uri_for,
    #})
    return j

  def render_template(self, template, **context):
    self.response.write(self.jinja2.render_template(template, **context))

  def init(self, **params):
    if hasattr(self, 'context') and hasattr(self, 'meta'):
      return
    self.context = {}
    for url in urls.masterlist:
      if url['uri'] == params.get('_uri','/'):
        self.meta = url
        break

  def get(self, **params):
    self.init(**params)
    logging.debug('Rendering: ' + self.meta['template'])
    self.render_template(self.meta['template'], **self.context)


class StaticHandler(BaseHandler):
  """Handles all calls to static pages

  Where dynamic page generation is not needed, this simply loads the static
  html templates as-is.
  """

  def get(self, **params):
    self.init(**params)
    self.context['title'] = self.meta['title']
    self.context['nav'] = urls.main
    BaseHandler.get(self, **params)


class BasicAuthHandler(StaticHandler):
  """The handler that handles requests that require basic authentication

  Basic authorization is managed by cross referencing the login credentials
  against a data file (accounts.yaml) containing the list of accessible
  accounts.
  """

  @basic_auth
  def get(self, **params):
    StaticHandler.get(self, **params)


class XMLViewHandler(StaticHandler):
  """The handler to build templates that have an attached XML file

  This handler is required for pages that are made up of a template and an
  XML-based content file.
  """

  def get(self, **params):
    self.init(**params)
    xml_uri = params.get('_xml')
    view_uri = params.get('_view')
    self.context['view'] = XMLViewLoader(xml_uri, view_uri).build()
    StaticHandler.get(self, **params)

  def post(self, **params):
    self.get(**params)


class ContactUsHandler(XMLViewHandler):

  def get(self, **params):
    self.init(**params)
    self.context['captcha'] = recaptcha_html(public_key = "6LdbKtISAAAAAP2DDQwJ2WSF3ZqkR9FSQVGH3Qxc", use_ssl = False, error = None)
    XMLViewHandler.get(self, **params)

  def post(self, **params):
    self.get(**params)


class EmailHandler(webapp2.RequestHandler):

  @recaptcha_verify
  def post(self):
    # send the email
    name = self.request.get('name')
    if name is None:
      self.response.write('Submission cancelled: Please enter a name')
    email = self.request.get('email')
    if not mail.is_email_valid(email):
      self.response.write('Submission cancelled: Please enter a valid email')
      return
    contents = self.request.get('contents')
    if contents is None:
      self.response.write('Submission cancelled: Please enter a message')
    message = mail.EmailMessage()
    message.sender = email
    message.to = 'evanplaice@gmail.com'
    message.subject = self.request.get('subject', '')
    message.body = """
    Message sent by %s

    %s
    """ % (name, contents)
    message.send()
    self.response.write('Message successfuly sent...')