''' 
  ETTTP_Client_skeleton.py
 
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

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    #socket():소켓 생성
    with socket(AF_INET, SOCK_STREAM) as client_socket: #with 범위 내에서만 실행/벗어나면 자동 close()
        client_socket.connect(SERVER_ADDR) #서버 접속
        
        ###################################################################
        '''
        서버로부터 메시지 받고 
        받은 메시지의 형식 확인 후 안맞으면 소켓 종료하고 
        형식이 맞고 시작이 YOU이면 start변수에 1을, ME이면 start 변수에 0을 설정
        '''
        start_msg = client_socket.recv(100).decode()
        start_msg = start_msg.replace(" ","").split('\r\n') #공백 제거,\r\n을 구분자로 split
    
        if start_msg[0][:4] =="SEND" and check_msg(start_msg,MY_IP):
            if start_msg[2][11:]=="YOU": #client 시작 
                start=1
            else:                        #server 시작 
                start=0
        else:
            client_socket.close() 
    
        ######################### Fill Out ################################
        '''
        start변수가 1이면 First-Move: YOU 를 포함한 ACK전송
        start변수가 0이면 First-Move: ME 를 포함한 ACK전송
        '''
        if start ==1:
            ack_msg ='ACK ETTTP/1.0\r\nHost: '+SERVER_IP+'\r\nFirst-Move: YOU\r\n\r\n'
        else:
            ack_msg ='ACK ETTTP/1.0\r\nHost: '+SERVER_IP+'\r\nFirst-Move: ME\r\n\r\n'
        client_socket.send(ack_msg.encode(encoding='utf-8'))

        ###################################################################
        # 게임 시작
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        