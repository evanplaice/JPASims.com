"""@routes
Route configurations for the site

The sub-lists make up the different sections of the site. Generate a master
list by combining them at the bottom.
"""

from webapp2 import Route, RedirectHandler
from handlers import DataHandler

public = [
  Route('/inventory/count',                         DataHandler,  defaults={'_model':'Inventory', '_action':'count'}),
  Route('/inventory/search',                        DataHandler,  defaults={'_model':'Inventory', '_action':'search'}),
  Route('/inventory/item/<_id>',                    DataHandler,  defaults={'_model':'Inventory', '_action':'by_id'}),
  Route('/inventory/manufacturer/<_manufacturer>',  DataHandler,  defaults={'_model':'Inventory', '_action':'by_manufacturer'}),
  Route('/inventory/part/<_part>',                  DataHandler,  defaults={'_model':'Inventory', '_action':'by_part'}),
  Route('/inventory/serial/<_serial>',              DataHandler,  defaults={'_model':'Inventory', '_action':'by_serial'}),
  Route('/inventory/category/<_category>',          DataHandler,  defaults={'_model':'Inventory', '_action':'by_category'}),
  Route('/inventory/type/<_type>',                  DataHandler,  defaults={'_model':'Inventory', '_action':'by_type'}),
  Route('/inventory/group/<_group>',                DataHandler,  defaults={'_model':'Inventory', '_action':'by_group'}),
  Route('/inventory/location/<_location>',          DataHandler,  defaults={'_model':'Inventory', '_action':'by_location'})
]

protected = [
  Route('/inventory/import',        DataHandler,  defaults={'_model':'Inventory', '_action':'batch_import'}),
  Route('/inventory/truncate',      DataHandler,  defaults={'_model':'Inventory', '_action':'truncate'})
]

masterlist = public + protected