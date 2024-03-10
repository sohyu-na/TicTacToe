''' 
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg

if __name__ == '__main__':
    
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    
    while True:
        client_socket, client_addr = server_socket.accept()
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        '''
        랜덤으로 0과 1중에 선택한 start변수를 사용
        start가 0일때 First-Move: ME 메시지를 보내 client한테 server가 시작함을 알림
        start가 1일때 First-Move: YOU 메시지를 보내 client한테 client가 시작함을 알림
        '''
        if start == 0:  #server 시작
            start_msg = 'SEND ETTTP/1.0\r\nHost: '+client_addr[0]+'\r\nFirst-Move: ME\r\n\r\n'
        else:           #client 시작
            start_msg = 'SEND ETTTP/1.0\r\nHost: '+client_addr[0]+'\r\nFirst-Move: YOU\r\n\r\n'
        client_socket.send(start_msg.encode(encoding='utf-8'))

        ######################### Fill Out ################################
        ''' 
        Client가 보낸 ACK메시지를 받고 
        ACK 형식이 맞으면 게임 시작, 안맞으면 소켓 종료
        '''
        start_ack_msg = client_socket.recv(100).decode()
        start_ack_msg = start_ack_msg.replace(" ","").split('\r\n')#공백 제거,\r\n을 구분자로 split

        start_ack_valid_check = False
        if start_ack_msg[0][:3] =="ACK" and check_msg(start_ack_msg,MY_IP):
            start_ack_valid_check = True
        
        if start_ack_valid_check ==False:
            client_socket.close()
            break 
        ###################################################################
        # 게임 시작
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        break
    server_socket.close()