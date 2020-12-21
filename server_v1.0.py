from websocket_server import WebsocketServer  

records=[] # 聊天记录

# 当新的客户端连接时会提示                                                                        
# Called for every client connecting (after handshake)                          
def new_client(client, server):                                                 
        print("New client connected and was given id %d" % client['id'])        
        server.send_message_to_all("Hey all, client id %d has joined us." % client['id'])
        print(server.clients)
        # print(server.clients[0]['id'])         
                                                                            
# 当旧的客户端离开                                                                         
# Called for every client disconnecting                                         
def client_left(client, server):                                                
        print("Client(%d) disconnected" % client['id']) 
        # print(server.clients)                        
                                                                            
# 接收客户端的信息。                                                                             
# Called when a client sends a message                                          
def message_received(client, server, message):                                  
        if len(message) > 200:                                                  
                message = message[:200]+'..'
                # if message == 'talk':
                #    server.send_message(client, "Input the client id")                                     
        print("Client(%d) said: %s" % (client['id'], message))
        new_record(client, message)
        print(records) 
        send_message_to_other(server, client, "Client(%d) said: %s" % (client['id'], message))
        # server.send_message_to_other(client,"Client(%d) said: %s" % (client['id'], message))
        # print(client)
        # server.send_message(client, message)                                                                                    

# 转发消息给其他客户端
def send_message_to_other(server, self_client, msg):
	for client in server.clients:
		if client != self_client:
			server.send_message(client, msg)

# 转发消息给特定客户端
def send_message_to_client(server, id, msg):
	for client in server.clients:
		if client['id'] == id:
			server.send_message(client, msg)

def new_record(self_client, msg):
        to_client_id = []
        for client in server.clients:
                if client != self_client:
                        to_client_id.append(client['id'])
	
        record={
		'client id'    : self_client['id'],
                'to client id' : to_client_id,
		'message'      : msg
	}
	
        records.append(record)

# def id_received(client, server, message): 

PORT=9001                                                                       
server = WebsocketServer(PORT, "0.0.0.0")                                       
server.set_fn_new_client(new_client)                                            
server.set_fn_client_left(client_left)                                          
server.set_fn_message_received(message_received)                          
server.run_forever()
                                                                                