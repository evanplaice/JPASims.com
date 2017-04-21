"""@main
The canonical entry point for this data service.

This is the heart of the application. Variables can be set explicitly by adding
them to the 'defaults' dict, or implicitly by adding a RegExp to the route.
"""

import logging
import os
import webapp2

import routes

# Detect whether this the 'Development' server
DEV = os.environ['SERVER_SOFTWARE'].startswith('Dev')

# Enable logging on the 'Development' server
if(DEV):
  logging.getLogger().setLevel(logging.DEBUG)
else:
  logging.getLogger().setLevel(logging.CRITICAL)

application = webapp2.WSGIApplication(routes.masterlist, debug=False)