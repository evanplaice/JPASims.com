"""@routes
Route configurations for the site

The sub-lists make up the different sections of the site. Generate a master
list by combining them at the bottom.
"""

from webapp2 import Route, RedirectHandler
from handlers import StaticHandler, XMLViewHandler, BasicAuthHandler, ContactUsHandler, EmailHandler

main = [
  Route('/',                      XMLViewHandler,   defaults={'_uri':'home', '_xml':'news.xml', '_view':'news'}),
  Route('/about-us',              StaticHandler,    defaults={'_uri':'about-us'}),
  Route('/press-releases',        StaticHandler,    defaults={'_uri':'press-releases'}),
  Route('/projects',              StaticHandler,    defaults={'_uri':'projects'}),
  Route('/kalitta-update',        StaticHandler,    defaults={'_uri':'kalitta-update'}),
  Route('/atlas-air-update',      StaticHandler,    defaults={'_uri':'atlas-air-update'}),
  Route('/kalitta-move',          StaticHandler,    defaults={'_uri':'kalitta-move'}), 
  Route('/kalitta-construction',  StaticHandler,    defaults={'_uri':'kalitta-construction'}),
  Route('/sim-products',          StaticHandler,    defaults={'_uri':'sim-products'}),
  Route('/tcas',                  StaticHandler,    defaults={'_uri':'tcas'}),
  Route('/rios',                  StaticHandler,    defaults={'_uri':'rios'}),
  Route('/sims-for-sale',         XMLViewHandler,   defaults={'_uri':'sims-for-sale', '_xml':'sims.xml', '_view':'sims'}),
  Route('/parts-for-sale',        StaticHandler,    defaults={'_uri':'parts-for-sale'}),
  Route('/devices-for-sale',      XMLViewHandler,   defaults={'_uri':'devices-for-sale', '_xml':'devices.xml', '_view':'devices'}),
  Route('/training',              StaticHandler,    defaults={'_uri':'training'}),
  Route('/consulting',            StaticHandler,    defaults={'_uri':'consulting'}),
  Route('/links',                 StaticHandler,    defaults={'_uri':'links'}),
  Route('/contact-us',            ContactUsHandler, defaults={'_uri':'contact-us', '_xml':'contacts.xml', '_view':'contacts'}),
  Route('/copyright',             StaticHandler,    defaults={'_uri':'copyright'})
]

admin = [
  Route('/admin/import',          BasicAuthHandler, defaults={'_uri':'import'})
]

private = [
  Route('/_typefaces',            BasicAuthHandler, defaults={'_uri':'_typefaces'}) 
]

redirects = [
]

meta = [
  Route('/email',                 EmailHandler)
]

masterlist = main + admin + private + redirects + meta