''' 
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0 
            self.user['text'] = 'O'
            self.computer['text'] = 'X' 
            self.l_status_bullet.config(fg='red') 
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,()) 
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        상대방이 보낸 메시지를 읽어오는 함수
        메시지를 받아서 형식 체크 후 
        형식이 맞으면 받은 메시지의 위치를 포함한 ACK메시지를 보냄
        형식이 안맞으면 소켓 종료 후 게임 종료
        loc 변수에 메시지의 위치를 버튼 번호로 바꾸어 저장 후
        보드에 업데이트하고 차례 바꿈
        '''
        ###################  Fill Out  #######################
        get_msg = self.socket.recv(100).decode()
        get_msg = get_msg.replace(" ","").split('\r\n') 

        msg_valid_check = False                      
        if get_msg[0][:4]=="SEND" and check_msg(get_msg, self.recv_ip):
            msg_valid_check = True 

        if msg_valid_check==False: 
            self.socket.close()   
            self.quit()
            return
        else:  
            msg_mv1=get_msg[2][10] 
            msg_mv2=get_msg[2][12]
            ack_msg="ACK ETTTP/1.0\r\nHost : "+self.send_ip+"\r\nNew-Move : ("+msg_mv1+","+msg_mv2+")\r\n\r\n"
            self.socket.send(ack_msg.encode(encoding='utf-8'))

        loc=int(msg_mv1)*3 +int(msg_mv2)
        ######################################################   
            
            
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.computer, loc, get=True)
        if self.state == self.active:  
            self.my_turn = 1
            self.l_status_bullet.config(fg='green')
            self.l_status ['text'] = ['Ready']
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        입력창으로부터 debug 메시지를 입력 받아서 상대방에게 전송
        *내 차례가 아니거나 이미 선택된 버튼, 유효하지 않은 버튼 번호면 무시
        상대방이 받고 ACK를 보내면 ACK를 받아서 형식 확인 후 
        형식 맞으면 보드 업데이트 
        형식 안맞으면 소켓 종료, 게임 종료
        '''
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        debug_msg=d_msg.replace(" ","").split('\r\n')
        row=int(debug_msg[2][10])      
        col=int(debug_msg[2][12])
        loc = row*3+col   
        
        
        if loc<0 or loc>8 : #버튼 0-8 범위 밖일때 
            self.t_debug.delete(1.0,"end") 
            return

        if self.board[loc] != 0 :  #already taken
            self.t_debug.delete(1.0,"end") 
            return
        else :    
            self.socket.send(d_msg.encode(encoding='utf-8'))
            
        debug_ack_msg=self.socket.recv(100).decode()
        debug_ack_msg=debug_ack_msg.replace(" ","").split('\r\n')
        
        debug_valid_check =False
        if debug_ack_msg[0][:3]=="ACK" and check_msg(debug_ack_msg,self.recv_ip):
            debug_valid_check =True

        if debug_valid_check ==False:
            self.socket.close()
            self.quit()
            return
        
        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        버튼 클릭시 상대방에게 메시지를 보내는 함수 
        상대방이 받고 ACK를 보내면 ACK를 받아서 형식 확인 후 
        형식 맞으면 true 리턴
        형식 안맞으면 소켓 종료, 게임 종료
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################
        send_msg="SEND ETTTP/1.0 \r\n Host: "+self.send_ip+"\r\nNew-Move: ("+str(row)+", "+str(col)+") \r\n\r\n"
        self.socket.send(send_msg.encode(encoding='utf-8'))

        ack_msg=self.socket.recv(100).decode()
        ack_msg=ack_msg.replace(" ","").split('\r\n') 

        ack_valid_check = False
        if ack_msg[0][:3]=="ACK" and check_msg(ack_msg, self.recv_ip):
            ack_valid_check = True
        
        if ack_valid_check==False: 
            self.socket.close()   
            self.quit() 
            return
        else:
            return True
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        게임의 결과가 나와 상대방이 일치하는지 확인하는 함수 
        이긴 쪽이 Winner: ME 를 포함한 메시지를 보냄

        진 쪽이 메시지를 받고 형식 확인 후
        형식이 맞으면 Winner: YOU 를 포함한 ACK를 보낸 후
        진 쪽이 받은 메시지의 winner와 나의 winner 비교 후 결과 일치하면 true 리턴 불일치하면 false 리턴
        형식이 안맞으면 소켓 종료, 게임 종료

        이긴 쪽이 ACK를 받고 형식 확인 후
        형식이 맞으면 
        이긴 쪽이 받은 메시지의 winner와 나의 winner를 비교 후 결과 일치하면 true 리턴 불일치하면 false 리턴
        형식이 안맞으면 소켓 종료, 게임 종료
        '''
        # no skeleton
        ###################  Fill Out  #######################

        if get == False: #winner
            send_result_msg ="RESULT ETTTP/1.0\r\nHost: "+self.send_ip+"\r\nWinner: ME\r\n\r\n"
            self.socket.send(send_result_msg.encode(encoding='utf-8'))
        
        if get == True: #loser
            get_result_msg=self.socket.recv(100).decode()
            get_result_msg=get_result_msg.replace(" ","").split('\r\n')

            if get_result_msg[0][:6]=="RESULT" and check_msg(get_result_msg,self.recv_ip): 
                send_ack_result_msg ="RESULT ETTTP/1.0\r\nHost: "+self.send_ip+"\r\nWinner: YOU\r\n\r\n" 
                self.socket.send(send_ack_result_msg.encode(encoding='utf-8'))
                if get_result_msg[2][7:] == "ME" and winner =="YOU": 
                    return True
                else:
                    return False
            else: 
                self.socket.close()
                self.quit()
                return 

        if get == False: #winner
            get_ack_result_msg=self.socket.recv(100).decode()
            get_ack_result_msg=get_ack_result_msg.replace(" ","").split('\r\n')

            if get_ack_result_msg[0][:6]=="RESULT" and check_msg(get_ack_result_msg,self.recv_ip): #format 만족
                if get_ack_result_msg[2][7:] == "YOU" and winner =="ME": #loser의 winner가 YOU이고 winner의 winner가 ME면
                    return True 
                else:
                    return False 
            else: 
                self.socket.close()
                self.quit()
                return 
        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # End of Root class


def check_msg(msg, recv_ip):
    '''
    공백 제거하고 '\r\n'으로 split한 msg의 ETTTP/1.0이 맞는지, 나의 ip가 맞는지 확인하는 함수 
    '''
    ###################  Fill Out  #######################

    if msg[0][len(msg[0])-9:] == "ETTTP/1.0" and msg[1][5:] == recv_ip:  
        return True
    else:
        return False
    ######################################################  
