"""@models
The home of all bigtable data models.

This file all of the canonical data models used throughout the application.
"""

import cgi
import datetime
from google.appengine.ext import db
import json
import logging
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from lib import xml


class BaseModel(db.Model):
  """The base model used to store common helper methods.

  Contains methods for outputting text in a variety of different formats.
  """

  def _format(self, type):
    if type == 'json':
      return self.__to_json()
    if type == 'xml':
      return self.__to_xml()
    if type == 'dict':
      return self.__to_dict()
    if type == 'list':
      return self.__to_list()
    if type == 'html':
      return self.__to_html()
    if type == 'text':
      return self.__to_text()
  
  def __get_data(self, escape_html=False):
    if not escape_html:
      return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
    else:
      return dict([(p, self.__escape_html(unicode(getattr(self, p)))) for p in self.properties()])
    
  def __escape_html(self, text):
    return cgi.escape(text).encode('ascii', 'xmlcharrefreplace')
    
  def __to_list(self):
    return ('text/plain', [i.__get_data() for i in self.results])

  def __to_json(self):
    return ('application/json', json.dumps([i.__get_data() for i in self.results]))

  def __to_xml(self, rootName=None):
    return ('application/xml', xml.serialize([i.__get_data(escape_html=True) for i in self.results], rootName))

  def __to_text(self):
    output = ''
    for i in self.results:
      for key, value in i.__get_data().iteritems():
        output += value + '\t'
      output += '\r\n'
    return ('text/plain', output)

  def __to_html(self):
    output = '<table border>\r\n'
    output += '<tr>\r\n'
    headers = self.results[0].__get_data()
    for key, value in headers.iteritems():
      output += '<td>' + self.__escape_html(unicode(key)) + '</td>\r\n'
    output += '</tr>\r\n'
    for row in self.results:
      output += '<tr>\r\n'
      for key, value in row.__get_data().iteritems():
        output += '<td>' + self.__escape_html(unicode(value)) + '</td>\r\n'
      output += '</tr>\r\n'
    output += '</table>\r\n'
    return ('text/html', output)


class Inventory(BaseModel):
  """The Model used to store parts that are for sale.

  This model is setup to be queried by matching attributes or by using a
  more complex search/filtering mechanism.
  """

  manufacturer = db.StringProperty()
  part_number = db.StringProperty()
  serial_number = db.StringProperty()
  category = db.StringProperty(indexed=True)
  type = db.StringProperty(indexed=True)
  description = db.StringProperty()
  group = db.IntegerProperty()
  location = db.StringProperty()
  sold = db.BooleanProperty()
  
  def __insert(self, **entity):
    item = Inventory()
    item.manufacturer = entity.get('manufacturer', '')
    item.part_number = entity.get('part_number', '')
    item.serial_number = entity.get('serial_number', '')
    item.category = entity.get('category', '')
    item.type = entity.get('type', '')
    item.description = entity.get('description', '')
    item.group = int(entity.get('group', '0'))
    item.location = entity.get('location', '')
    item.sold = entity.get('sold', False)
    item.put()

  def __query(self, **params):
    category = params.get('category','').replace('+',' ')
    type = params.get('type','').replace('+',' ')
    order = params.get('order','')
    by = params.get('by')
    offset = params.get('offset', '0')
    limit = params.get('limit', '100')
    gql = 'SELECT * FROM Inventory '
    if category != '':
      gql += 'WHERE category = \'' + category + '\' '
    if type != '' and category != '':
      gql += 'AND type = \'' + type + '\' '
    if type != '' and category == '':
      gql += 'WHERE type = \'' + type + '\' '
    if order != '' and by != '':
      gql += 'ORDER BY ' + order + ' ' + by + ' '
    gql += 'LIMIT ' + limit
    if offset != '0':
      gql += ' OFFSET ' + offset
    return gql

  def count(self, **params):
    gql = self.__query(**params)
    count = db.GqlQuery(gql).count()
    return ('text/plain', count)

  def search(self, **params):
    gql = self.__query(**params)
    self.results = db.GqlQuery(gql)
    format = params.get('format', 'json')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_id(self, **params):
    id = int(params.get('_id'))
    self.results = [Inventory.get_by_id(id)]
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_manufacturer(self, **params):
    manufacturer = params.get('_manufacturer')
    self.results = Inventory.all().filter("manufacturer =", manufacturer).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_part(self, **params):
    part_number = params.get('_part')
    self.results = Inventory.all().filter("part_number =", part_number).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_serial(self, **params):
    serial_number = params.get('_serial')
    self.results = Inventory.all().filter("serial_number =", serial_number).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_category(self, **params):
    category = params.get('_category')
    self.results = Inventory.all().filter("category =", category).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_type(self, **params):
    type = params.get('_type')
    self.results = Inventory.all().filter("type =", type).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_group(self, **params):
    group = int(params.get('_group'))
    self.results = Inventory.all().filter("group =", group).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def by_location(self, **params):
    location = params.get('_location')
    self.results = Inventory.all().filter("location =", location).fetch(1000)
    format = params.get('format', 'text')
    if self.results:
      return self._format(format)
    else:
      return ('text/plain', '')

  def truncate(self):
    db.delete(Inventory.all(keys_only=True))
    return 'Inventory truncated successfully...'

  def batch_import(self, data):
    for item in data:
      self.__insert(
        manufacturer = item[1],
        part_number = item[2],
        serial_number = item[3],
        category = item[4],
        type = item[5],
        description = item[6],
        group = item[7],
        location = item[8],
        sold = (True if item[9] is 1 else False)
      );
    return 'Inventory successfully updated with ' + str(len(data)) + ' items...'