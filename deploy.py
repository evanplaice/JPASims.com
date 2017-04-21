"""@compile
Static site compiler

Crawls the site and downloads the all of the pages in their satic format.
Deploying a static-only version of the saves on processing time and allows
the files to be deployed to any type of HTTP server.
"""
import os
import urllib2
from app.urls import masterlist

port = '8081'
local_folder = os.getcwd() + os.sep + 'static' + os.sep + 'html' + os.sep
print 'Outputting to: ' + local_folder

print '\nCompiling:'
for page in masterlist:
  http = urllib2.urlopen('http://localhost:' + port + page['url'])
  file_name = page['template']
  path = local_folder + file_name
  local_file = open(path, 'w')
  local_file.write(http.read())
  local_file.close()
  print ' - ' + file_name + ' compiled successfully...'