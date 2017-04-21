"""@recaptcha
Recaptcha capture decorator for human validation

Adapted from http://pypi.python.org/pypi/recaptcha-client
"""

import urllib
from google.appengine.api import urlfetch


API_SSL_SERVER  ="https://api-secure.recaptcha.net"
API_SERVER      ="http://api.recaptcha.net"
VERIFY_SERVER   ="api-verify.recaptcha.net"


def recaptcha_verify(func):
  def callf(webappRequest, *args, **kwargs):
    challenge = webappRequest.request.get('recaptcha_challenge_field')
    response  = webappRequest.request.get('recaptcha_response_field')
    remoteip  = webappRequest.request.remote_addr
    (valid, error) = __submit(challenge, response, "6LdbKtISAAAAAGZraDRVJUQfr5Kje0eHMRbsGTc_", remoteip)
    if not valid:
      webappRequest.response.write(error)
      return
    else:
      return func(webappRequest, *args, **kwargs)
  return callf

def recaptcha_html (public_key, use_ssl = False, error = None):
  """Gets the HTML to display for reCAPTCHA

  public_key -- The public api key
  use_ssl -- Should the request be sent over ssl?
  error -- An error message to display (from RecaptchaResponse.error_code)
  """

  error_param = ''
  if error:
    error_param = '&error=%s' % error
  if use_ssl:
    server = API_SSL_SERVER
  else:
    server = API_SERVER
  return """
<script type="text/javascript" src="%(ApiServer)s/challenge?k=%(PublicKey)s%(ErrorParam)s"></script>

<noscript>
  <iframe src="%(ApiServer)s/noscript?k=%(PublicKey)s%(ErrorParam)s" height="300" width="500" frameborder="0"></iframe><br />
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type='hidden' name='recaptcha_response_field' value='manual_challenge' />
</noscript>
""" % { 'ApiServer':server, 'PublicKey':public_key, 'ErrorParam':error_param }

def __submit (recaptcha_challenge, recaptcha_response, private_key, remote_ip):
  """
  Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
  for the request

  recaptcha_challenge_field -- The value of recaptcha_challenge_field from the form
  recaptcha_response_field -- The value of recaptcha_response_field from the form
  private_key -- your reCAPTCHA private key
  remoteip -- the user's ip address
  """

  if not (recaptcha_response and recaptcha_challenge):
    return (False, 'incorrect-captcha-sol')
  if not (len(recaptcha_response) and len(recaptcha_challenge)):
    return (False, 'incorrect-captcha-sol')

  headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'User-agent'  : 'reCAPTCHA GAE Python'
  }

  params = urllib.urlencode ({
	  'privatekey': private_key,
    'remoteip'  : remote_ip,
	  'challenge' : recaptcha_challenge,
	  'response'  : recaptcha_response,
	})

  response = urlfetch.fetch(**{
    'url'     : 'http://%s/verify' % VERIFY_SERVER,
    'payload' : params,
    'method'  : urlfetch.POST,
    'headers' : headers
  })

  # response was fine
  if response.status_code == 200:
    # get the return values
    return_values = response.content.splitlines();
    return_code = return_values[0]

    if return_code == "true":
      # yep, filled perfectly
      return (True, None)
    else:
      # nope, something went wrong
      error = return_values[1]
      return (False, error)
  else:
    # recaptcha server was not reachable
    return (False, "recaptcha-not-reachable")