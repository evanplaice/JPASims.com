"""@urls
Site-wide list of urls and their attibutes

Any information about pages that may need to be passed into
the templating engine is specified here.
"""

main = [
  { 'uri':'home',                 'url':'/',                      'template':'home.html',               'title':'Home' },
  { 'uri':'about-us',             'url':'/about-us',              'template':'about-us.html',           'title':'About Us' },
  { 'uri':'press-releases',       'url':'/press-releases',        'template':'press-releases.html',     'title':'Press Releases' },
  { 'uri':'projects',             'url':'/projects',              'template':'projects.html',           'title':'Projects' },
  { 'uri':'sim-products',         'url':'/sim-products',          'template':'sim-products.html',       'title':'Sim Products' },
  { 'uri':'sims-for-sale',        'url':'/sims-for-sale',         'template':'sims-for-sale.html',      'title':'Sims For Sale' },
  { 'uri':'parts-for-sale',       'url':'/parts-for-sale',        'template':'parts-for-sale.html',     'title':'Sim Parts For Sale' },
  { 'uri':'devices-for-sale',     'url':'/devices-for-sale',      'template':'devices-for-sale.html',   'title':'Devices For Sale' },
  { 'uri':'training',             'url':'/training',              'template':'training.html',           'title':'Training Services' },
  { 'uri':'consulting',           'url':'/consulting',            'template':'consulting.html',         'title':'Consulting' },
  { 'uri':'links',                'url':'/links',                 'template':'links.html',              'title':'Links' },
  { 'uri':'contact-us',           'url':'/contact-us',            'template':'contact-us.html',         'title':'Contact Us' }
]

sub = [
  { 'uri':'kalitta-update',       'url':'/kalitta-update',        'template':'kalitta-update.html',         'title':'Kalitta Air B747-200 Update' },
  { 'uri':'atlas-air-update',     'url':'/atlas-air-update',      'template':'atlas-air-update.html',       'title':'Atlas Air 747-200 Avionics Update' },
  { 'uri':'kalitta-move',         'url':'/kalitta-move',          'template':'kalitta-move.html',           'title':'Kalitta Air B747-200 Installation' },
  { 'uri':'kalitta-construction', 'url':'/kalitta-construction',  'template':'kalitta-construction.html',   'title':'Kalitta Air B747-200 Simulator Facility' },
  { 'uri':'tcas',                 'url':'/tcas',                  'template':'tcas.html',                   'title':'TCAS Overview' },
  { 'uri':'rios',                 'url':'/rios',                  'template':'rios.html',                   'title':'RIOS Overview' },
  { 'uri':'copyright',            'url':'/copyright',             'template':'copyright.html',              'title':'Copyright' }
]

admin = [
  { 'uri':'import',               'url':'/admin/import',          'template':'import.html',                 'title':'Inventory - Import' }
]

private = [
  { 'uri':'_typefaces',           'url':'/_typefaces',            'template':'_typefaces.html',             'title':'Typeface Testing' }
]

masterlist = main + sub + admin + private