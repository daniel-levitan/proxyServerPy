from socket import *
from datetime import datetime

from constants import *
from functions import *


def parse_http_request(request):
   try:
      request_array = request.split("\r\n")  # This split the whole request into lines
      request_line_array = request_array[0].split() #  This split the first line of the request into parts
      # print(f"Received request for: {request_array[0]}") 

      if len(request_line_array) < 2:
        return False, None

      request_method = request_line_array[0]

      if request_method == "GET":
         return True, request_array[0]
         
   except Exception as e:
      print(f"Error parsing request: {e}")
      print(f"Request: {request}")
      return False, None

   return False, None


def build_headers(status, headers):
    response = f"HTTP/1.1 {status}\r\n"
    response += '\r\n'.join(f"{k}: {v}" for k, v in headers.items())
    response += "\r\n\r\n"
    return response


def build_http_response(method, resource):
   headers = {
      'Date': datetime.now().strftime("%a, %-d %b %Y %H:%M:%S"),
      'Server': 'Levi/1.0 (Mac)',
      'Content-Type': 'text/html'
   }
   
   if method == 'GET':
      print("Inside the get method")
      # Now I need to:
      # Check if there is a folder with the domain name
      # If it doesn't exist, create it, create a request, put the result in a file(can I call it "/")
      # If content is locally presented:
      #    Send it to the requester
      # else:
      #   Fetch the content and save locally as file
      # Anyways, send it back to the requester 


      print(f"Request: {resource}")
      domain_and_resource = resource.split("/")
      host = domain_and_resource[1]
      domain = host.split(".")[1]
      
      if len(domain_and_resource) > 2:
         new_resource = ""
         for token in domain_and_resource[2:]:
            new_resource += "/" + token
      else:
         # There is no file default for the "/", so I store its content in a main.html file
         new_resource = "/main.html"

      content = ""
      fileExists = checkFile(domain, new_resource)
      # fileExists = False

      if fileExists:
         content = getFile(domain, new_resource)
      else:
         # Save file, return content

         # GET CONTENT FROM DESIRED PAGE
         # serverName = domain
         serverPort = 80

         clientSocket = socket(AF_INET, SOCK_STREAM) 
         clientSocket.connect((host, serverPort)) 

         req = "GET " + new_resource +  " HTTP/1.1\r\n" + \
         "Host: " + host + "\r\n" + \
         "User-Agent: curl/7.xx.x\r\n" + \
         "Accept: */*\r\n\r\n"  

         print("Request sent:", req)
         clientSocket.send(req.encode()) 

         content = clientSocket.recv(1024).decode() 
         print("Content:\n", content)
         # print('From Server: ', resp.decode()) 

         clientSocket.close()

         # Save to file
         saveFile(domain, new_resource, content)


      if not content:
         return build_headers('404 Not Found', headers) + NOT_FOUND_TEMPLATE
      return build_headers('200 OK', headers) + content
   
   if method == 'HEAD':
      return build_headers('200 OK', headers)
      
   return build_headers('501 Not Implemented', headers) + NOT_IMPLEMENTED_TEMPLATE
