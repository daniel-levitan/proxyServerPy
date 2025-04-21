from socket import *

from http_functions import *
from constants import *


def main():
   server_socket = socket(AF_INET, SOCK_STREAM) 
   server_socket.bind(('', SERVER_PORT)) 
   server_socket.listen(1)

   print('The server is ready to receive')

   num_of_connections = 0
   while True:
      connection_socket, addr = server_socket.accept() 
      num_of_connections += 1
      print(f"Connection {num_of_connections} New connection from {addr}")         

      request = connection_socket.recv(1024).decode() 
      # print("THE REQUEST:\n", request)

      ok, parsed_request = parse_http_request(request)

      if ok:
         # print(f">>> This is the parsed request:\n{parsed_request}")
         params = parsed_request.split()
         response = build_http_response(params[0], params[1])
         connection_socket.send(response.encode()) 
      else:
         print("Wrong request")

      connection_socket.close()


if __name__ == '__main__':
   main()