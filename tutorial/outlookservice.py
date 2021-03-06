# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license. See full license at the bottom of this file.
import requests
import uuid
import json

outlook_api_endpoint = 'https://outlook.office.com/api/v2.0{0}'

# Generic API Sending
def make_api_call(method, url, token, user_email, payload = None, parameters = None):
    # Send these headers with all API calls
    headers = { 'User-Agent' : 'python_tutorial/1.0',
                'Authorization' : 'Bearer {0}'.format(token),
                'Accept' : 'application/json',
                'X-AnchorMailbox' : user_email }
                
    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = { 'client-request-id' : request_id,
                        'return-client-request-id' : 'true' }
                        
    headers.update(instrumentation)
    
    response = None
    
    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)
        
    return response

def get_me(access_token):
  get_me_url = outlook_api_endpoint.format('/Me')

  # Use OData query parameters to control the results
  #  - Only return the DisplayName and EmailAddress fields
  query_parameters = {'$select': 'DisplayName,EmailAddress'}

  r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_my_messages(access_token, user_email):
  get_messages_url = outlook_api_endpoint.format('/Me/MailFolders/Inbox/Messages')
  
  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the ReceivedDateTime, Subject, and From fields
  #  - Sort the results by the ReceivedDateTime field in descending order
  query_parameters = {'$top': '10',
                      '$select': 'ReceivedDateTime,Subject,From',
                      '$orderby': 'ReceivedDateTime DESC'}
                      
  r = make_api_call('GET', get_messages_url, access_token, user_email, parameters = query_parameters)
  
  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)
    
def get_my_events(access_token, user_email):
  get_events_url = outlook_api_endpoint.format('/Me/Events')
  
  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the Subject, Start, and End fields
  #  - Sort the results by the Start field in ascending order
  query_parameters = {'$top': '10',
                      '$select': 'Subject,Start,End',
                      '$orderby': 'Start/DateTime ASC'}
                      
  r = make_api_call('GET', get_events_url, access_token, user_email, parameters = query_parameters)
  
  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)
    
def get_my_contacts(access_token, user_email):
  get_contacts_url = outlook_api_endpoint.format('/Me/Contacts')
  
  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the GivenName, Surname, and EmailAddresses fields
  #  - Sort the results by the GivenName field in ascending order
  query_parameters = {'$top': '10',
                      '$select': 'GivenName,Surname,EmailAddresses',
                      '$orderby': 'GivenName ASC'}
                      
  r = make_api_call('GET', get_contacts_url, access_token, user_email, parameters = query_parameters)
  
  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

# MIT License: 
 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the 
# ""Software""), to deal in the Software without restriction, including 
# without limitation the rights to use, copy, modify, merge, publish, 
# distribute, sublicense, and/or sell copies of the Software, and to 
# permit persons to whom the Software is furnished to do so, subject to 
# the following conditions: 
 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software. 
 
# THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.