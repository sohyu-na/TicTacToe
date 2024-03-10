/*34743-02 Information Communications team project*/

<TicTacToe socket programming>
server-client가 TCP 연결을 통해 socket을 주고 받으며 통신 하고, P2P 패러다임을 이용하여 두 시스템 간에 direct한 통신하는 program


![image](https://github.com/sohyu-na/TicTacToe/assets/113418712/941ebf48-31d1-481a-bcaa-bce1247d3777)
![image](https://github.com/sohyu-na/TicTacToe/assets/113418712/fff43b6c-5123-48da-b501-37c92054a52b)
..
![image](https://github.com/sohyu-na/TicTacToe/assets/113418712/d9c98eaa-388f-49ff-885f-c9920eff82ad)




<TCP – background>
TCP(Transmission Control Protocol)는 응용 프로그램 간의 데이터 전송을 위한 안정적인 연결을 제공합니다. 
어플리케이션 계층 프로토콜은 크게 client-server 패러다임과 peer-peer architecture로 나눌 수 있는데, 먼저 client-server paradigm은 하나의 서버에 여러 개의 client가 붙어서 server를 통해 통신하는 방법입니다.
peer-peer architecture는 서버가 따로 없고 네트워크 코어에서 peer들끼리 다이렉트로 통신하는 방법입니다. 
client-server 어플리케이션이 통신을 하기 위해서는 소켓이 필요한데, 그 소켓을 만들어서 통신하는 것을 socket programming이라고 합니다. 
TCP를 통해서 socket programming을 하는 과정은 클라이언트가 소켓을 생성한 뒤 접속하고자 하는 서버의 포트번호와 IP 주소를 이용하여 서버에 컨택을 하면 돌아가고 있는 서버 프로세스(클라이언트의 연결을 기다리며 소켓이 만들어져 있는 상태)에서 클라이언트의 연결을 받아들입니다. 
server 측도 client와의 연결을 위한 소켓을 새로 생성합니다. 그 후에 server와 client는 새로 생성된 socket을 통해 메시지를 주고 받습니다. 통신이 끝나면 소켓을 닫으며 종료합니다. 


<Code Analysis and Explanation>
SERVER.py
- 랜덤으로 0,1을 선택해서 게임을 시작하는 상대를 고른다. 
- 0이면 server가 게임을 시작하고, 1이면 client가 게임을 시작한다. 
- server가 랜덤으로 나온 결과를 ETTTP 형식에 맞춰 client에게 보내준다. 
- client가 응답으로 보낸 ack을 받아서 형식을 확인하고 옳은 형식이면 게임을 시작한다.

CLIENT.py
- 서버로부터 누가 먼저 게임을 시작하는지에 관한 메시지를 받는다. 
- 메시지의 ETTTP 형식을 확인하고 옳지 않은 형식이면 소켓을 닫고
- 옳은 형식이면 누가 먼저 시작하는지 확인한다. 
- 메시지에서 “YOU”이면 client가 시작하고, “ME”이면 server가 시작한다. 
- server에게 잘 받았다는 응답으로 ack를 보낸다. 
- 게임을 시작한다. 

TTT.py
게임 진행에 관한 전반적인 코드
- 게임 보드 GUI (QUIT 버튼과 게임 상황이자 순서(Hold, Ready)를 나타내는 부분, 게임 결과를 나타내는 부분, debug 입력 부분, 게임 보드 부분을 각각 만들기)를 구현한다.
  
- 게임이 시작되면 start_user의 상태는 Ready가 되고, start_user가 누르는 부분은 x로 표시된다. 대기하고 있는 상대의 화면에는 Hold가 표시되고 버튼을 눌러도 무시된다. 
- ready 상태의 화면에서 버튼을 누르면 먼저 그 버튼이 이미 눌린 버튼인지 아닌지 확인하고, 처음 누르는 버튼이라면, 상대 peer에게 SEND 메시지로 버튼의 위치가 보내진다.
- 상대는 SEND 메시지의 ETTTP 형식을 확인하고 형식이 옳으면 ACK 메시지를 보내고 본인의 화면을 업데이트한다.
- ACK를 받은 peer는 그 ACK 메시지의 형식이 옳은지 확인하고 옳으면 본인의 화면을 업데이트한다. 돌아가면서 위와 같은 순서로 게임을 진행한다.

  
- 버튼을 누르지 않고 debug로 직접 입력하면 debug 입력 칸의 메시지를 상대 peer에게 보낸다.
- 게임 보드의 범위를 넘어간 위치를 입력하거나 이미 눌린 버튼을 입력하면 무시된다.
- 상대 peer는 받은 메시지의 ETTTP 형식이 옳으면, 자신의 보드를 업데이트하고 그 응답으로 ACK 메시지를 보낸다.
- ACK를 받은 peer는 ACK 메시지의 형식이 옳은지 확인하고 옳으면 자신의 보드를 업데이트한다. 


- 게임이 끝나면 게임에서 이긴 peer(winner)가 상대 peer에게 결과를 확인하는 RESULT 메시지를 보낸다.
- 게임에서 진 peer(loser)는 result 메시지를 받아서 ETTTP 형식을 확인하고 형식이 옳으면 응답으로 ACK 메시지를 보내고, 자신이 내린 결과와 RESULT 메시지를 통해 받은 결과가 일치하는지 확인한다.
- winner는 loser로부터 받은 ACK 메시지가 ETTTP 형식에 맞는지 확인하고 옳은 형식이면 자신의 결과와 일치하는지 확인하고 두 peer의 게임 결과가 서로 일치하면 winner 게임 보드 GUI에는 Result: You Won! / loser 게임 보드 GUI에는 Result: You Lost! 를 띄운다. 

- SEND, ACK, RESULT 메시지를 주고 받을 때, ETTTP 형식에 맞지 않으면 게임을 종료시킨다.



