"""@views
View loaders for the site

The factories that transform data structures into human-readable markup.
"""

import os
import logging
from lxml import etree as ElementTree
#from xml.etree import ElementTree

class DataViewBase:
  """The base view that makes up all of the database views

  This class handles the setup and parsing of database data.
  """
  def __init__(self, view_uri):
    self.view_uri = view_uri

  def build(self, query):
    self.data = data

class XMLViewBase:
  """The base view that makes up all of the XML views

  This class handles the setup and parsing of XML views. Everything step
  involved in building an XML view is contained in this class except the
  page-specific markup generation.
  """
  def __init__(self, xml_uri, view_uri):
    self.xml_uri = xml_uri
    self.view_uri = view_uri

  def build(self):
    if not 'http://' in self.xml_uri:
      path = os.path.join(os.path.join(os.path.split(__file__)[0], 'xml'), self.xml_uri)
    else:
      path = self.xml_uri
    self.xml = self.parse(path)
    logging.debug('XMLViewLoader: Parsing ' + self.xml_uri)
    view = getattr(self, self.view_uri)()
    logging.debug("XMLViewLoader: Bulding the '" + self.view_uri + "' view")
    return view

  def parse(self, path):
    
    return ElementTree.parse(path)


class XMLViewLoader(XMLViewBase):
  """The complete collection of page-specific XML views

  This class containes all of the page-specific views. Each function contains
  one view. All of the file handling and parsing happens in the parent class
  so these can be dedicated to only markup generation.
  """

  def news(self):
    view = ''
    for entry in self.xml.findall('entry'):
      date = entry.find('date').text
      content = entry.find('content')
      view += '<div class="h2">{0}</div>\n'.format(date)
      view += '<div class="p1">\n'
      for element in content:
        if element.tag == 'text':
          view += '  <div class="text">{0}</div>\n'.format(element.text)
        if element.tag == 'listtitle':
          view += '  <div class="listtitle">{0}</div>\n'.format(element.text)
        if element.tag == 'bullets':
          view += '  <ul>\n'
          for listitem in element:
            view += '    <li>{0}</li>\n'.format(listitem.text)
          view += '  </ul>\n'
        if element.tag == 'numbered':
          view += '  <ol>\n'
          for listitem in element:
            view += '    <li>{0}</li>\n'.format(listitem.text)
          view += '  </ol>\n'
      view += '</div>\n'
    return view

  def sims(self):
    view = ''
    for sim in self.xml.findall('sim'):
      number = sim.attrib['number']
      identifier = sim.find('identifier').text
      gallery = sim.find('gallery').text
      images = int(sim.find('images').text)
      description = sim.find('description').text
      spec = sim.find('spec').text
      sold = sim.find('sold').text
      watermark = ' simsold' if sold == 'yes' else ''
      view += '<!-- Sim-{0}, {1} -->\r\n'.format(number, identifier)
      view += '<div class="sim{0}">\r\n'.format(watermark)
      view += '  <div class="simpic_container">\r\n'
      view += '    <img class="simpic" src="/placeholder.gif" style="background-image:url(\'/sims/sim{0}_preview.jpg\');\" alt="{1}" />\r\n'.format(number, identifier)
      if gallery == 'yes':
        view += '    <a href="/sims/sim{0}_1.jpg" rel="lightbox[sim{0}]"><div class="galleryicon"></div>\r\n'.format(number)
        for image in range(2, images):
          view += '    <a href="/sims/sim{0}_{1}.jpg" rel="lightbox[sim{0}]" style="display:none;"></a>\r\n'.format(number, image)
      view += '  </div>\r\n'
      if gallery == 'yes':
        view +=  '</a>\r\n'  
      view += '  <div class="simtitle">{0} Full Flight Simulator</div>\r\n'.format(identifier)
      view += '  <div class="simtext p1">{0}</div>\r\n'.format(description)
      view += '  <a class="detail" href="/{0}">Click Here for Detailed Simulator Specifications</a>\r\n'.format(spec)
      view += '</div>\r\n'
    return view

  def parts(self):
    view = ''
    count = 1
    for entry in self.xml.findall('entry'):
      id = entry.attrib['id']
      title = entry.find('title').text
      content = entry.find('description').text
      if count % 2 == 0:
        bgcolor = "#FFFFFF"
      else:
        bgcolor = "#E0E0E0" 
      view += '<div style="padding-bottom:5px;background-color:{0};">\n'.format(bgcolor)
      view += '  <div style="">{0}</div>\n'.format(title)
      view += '  <div class="text" style="font-size:small;">{0}</div>\n'.format(content)
      view += '</div>\n'
      count += 1
    return view

  def devices(self):
    view = ''
    for device in self.xml.findall('device'):
      if device.find('sold').text != 'yes':
        number = device.attrib['number']
        identifier = device.find('identifier').text
        gallery = device.find('gallery').text
        images = int(device.find('images').text)
        description = device.find('description').text
        features = device.find('features')
        parts = device.find('parts')
        view += '<!-- Device-{0}, {1}-->\r\n'.format(number, identifier)
        view += '<div class="device">\r\n'
        view += '  <div class="devicepic_container">\r\n'
        view += '    <img class="devicepic" src="/placeholder.gif" style="background-image:url(\'/devices/device{0}_preview.jpg\');" alt="{1}" />\r\n'.format(number, identifier)
        if gallery == 'yes':
          view += '    <a href="/devices/device{0}_1.jpg" rel="lightbox[device{0}]"><div class="galleryicon"></div>\r\n'.format(number)
          for image in range(2, images):
            view += '    <a href="/devices/device{0}_{1}.jpg" rel="lightbox[device{0}]" style="display:none;"></a>\r\n'.format(number, image)
        view += '  </div>\r\n'
        if gallery == 'yes':
          view += '  </a>\r\n'
        view += '  <div class="devicetitle">{0}</div>\r\n'.format(identifier)
        view += '  <div class="devicetext p1">{0}</div>\r\n'.format(description)
        if features is not None:
          view += '  <div class="p1" style="background:url(\'/hr.gif\') no-repeat bottom;width:200px;overflow:hidden;margin-top:15px;">Features Listing:</div>\r\n'
          view += '  <div class="p1">\r\n'
          view += '    <ul>\r\n'
          for item in features:
            view += '      <li>{0}</li>\r\n'.format(item.text)
          view += '    </ul>\r\n'
          view += '  </div>\r\n'
        if parts is not None:
          view += '  <div class="devicelisting p1">Parts Listing:</div>\r\n'
          view += '  <div class="p1">\r\n'
          view += '    <ul>\r\n'
          for item in parts:
            view += '      <li>{0}</li>\r\n'.format(item.text)
          view += '    </ul>\r\n'
          view += '  </div>\r\n'
        view += '</div>\n'
    return view

  def contacts(self):
    view = ''
    for facility in self.xml.findall('facility'):
      name = facility.find('name').text
      phone = facility.find('phone')
      phone2 = facility.find('phone2')
      fax = facility.find('fax')
      address1a = facility.find('address1a')
      address1b = facility.find('address1b')
      view += '<div class="c_name">{0}</div>\n'.format(name)
      view += '<div class="c_nfo">\n'
      if phone is not None:
        view += '  Phone: {0}<br />\n'.format(phone.text)
      if phone2 is not None:
        view += '  Phone2: {0}<br />\n'.format(phone2.text)
      if fax is not None:
        view += '  Fax: {0}<br />\n'.format(fax.text)
      if address1a is not None:
        view += '  Address:\n'
        view += '  {0}<br />\n'.format(address1a.text)
      if address1b is not None:
        view += '  {0}<br />\n'.format(address1b.text)
      view += '</div>\n'
    for contact in self.xml.findall('contact'):
      name = contact.find('name').text
      title = contact.find('title').text
      phone = contact.find('phone')
      phone2 = contact.find('phone2')
      fax = contact.find('fax')
      email = contact.find('email')
      email2 = contact.find('email2')
      address1a = facility.find('address1a')
      address1b = facility.find('address1b')
      address2a = facility.find('address2a')
      address2b = facility.find('address2b')
      view += '<div class="c_name">{0}</div>\n'.format(name)
      view += '<div class="c_nfo">\n'
      view += '  {0}<br />\n'.format(title)
      if phone is not None:
        view += '  Phone: {0}<br />\n'.format(phone.text)
      if phone2 is not None:
        view += '  Phone2: {0}<br />\n'.format(phone2.text)
      if fax is not None:
        view += '  Fax: {0}<br />\n'.format(fax.text)
      if email is not None:
        view += '  E-Mail: <a href="mailto:{0}">{0}</a><br />\n'.format(email.text)
      if email2 is not None:
        view += '  E-Mail2: <a href="mailto:{0}">{0}</a><br />\n'.format(email2.text)
      if address1a is not None:
        view += '  Address:\n'  
        view += '  {0}<br />\n'.format(address1a.text)
      if address1b is not None:
        view += '  {0}<br />\n'.format(address1b.text)
      if address2a is not None:
        view += '  Address2:\n'
        view += '  {0}<br />\n'.format(address2a.text)
      if address2b is not None:
        view += '  {0}<br />\n'.format(address2b.text)
      view += '</div>\n'
    return view