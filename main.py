import numpy as np
import pickle

ties = 0
player1wins = 0
player2wins = 0

def score(boardList, piece):
  total = 0
  for x in range(8):
    for y in range (8):
      if boardList[x][y] == piece:
        total += 1
  return total

def flipPieces(boardList, x, y, deltaX, deltaY, myPiece, opponentPiece):
  while boardList[x][y] == opponentPiece:
    boardList[x][y] = myPiece
    x += deltaX
    y += deltaY


def checkFlip(boardList, x, y, deltaX, deltaY, piece, opponent):
  if (x >= 0 and x < 8 and y >= 0 and y < 8):
    if(boardList[x][y] == opponent):
      x += deltaX
      y += deltaY
      while (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
        if(boardList[x][y] == '.'):
          return False
        if(boardList[x][y] == piece):
          return True
        x += deltaX
        y += deltaY
  return False

def validMove(boardList, x, y, piece):
  # Check that the coordinates are empty
  if boardList[x][y] != '.':
    return False
  # Figure out the character of the opponent's piece
  opponent = 'O'
  if piece == 'O':
    opponent = 'X'
  # If we can flip in any direction, it is valid
  # Check to the left
  if checkFlip(boardList, x - 1, y, -1, 0, piece, opponent):
    return True
  # Check to the right
  if checkFlip(boardList, x + 1, y, 1, 0, piece, opponent):
    return True
  # Check down
  if checkFlip(boardList, x, y - 1, 0, -1, piece, opponent):
    return True
  # Check up
  if checkFlip(boardList, x, y + 1, 0, 1, piece, opponent):
    return True
  # Check down-left
  if checkFlip(boardList, x - 1, y - 1, -1, -1, piece, opponent):
    return True
  # Check down-right
  if checkFlip(boardList, x + 1, y - 1, 1, -1, piece, opponent):
    return True
  # Check up-left
  if checkFlip(boardList, x - 1, y + 1, -1, 1, piece, opponent):
    return True
  # Check up-right
  if checkFlip(boardList, x + 1, y + 1, 1, 1, piece, opponent):
    return True
    
  return False # If we get here, we didn't find a valid flip direction


class State:
  
  
  def __init__(self,p1,p2):
    self.board = np.full((8,8),".")
    #set four entries to be two X's and two O's
    self.board[3][4] = "X"
    self.board[4][3] = "X"
    self.board[3][3] = "O"
    self.board[4][4] = "O"
    self.p1 = p1
    self.p2 = p2
    self.isEnd = False
    self.boardHash = None
    self.playerSymbol = "X" #first player symbol

  def getHash(self):
    return str(self.board.reshape(64))

  def showBoard(self):
    print(self.board)

  def availablePositions(self):
    #this is the function that returns all possible moves from a particular board
    positions = []
    for i in range(8):
      for j in range(8):
        if validMove(self.board,i,j,self.playerSymbol):
          positions.append((i,j))
    return positions


  def makeMove(self,boardList, x, y, piece): #this function is copied over to state class
    # Put the piece at x,y
    boardList[x][y] = piece
    # Figure out the character of the opponent's piece
    opponent = 'O'
    if piece == 'O':
      opponent = 'X'

    # Check to the left
    if checkFlip(boardList, x - 1, y, -1, 0, piece, opponent):
      flipPieces(boardList, x - 1, y, -1, 0, piece, opponent)
    # Check to the right
    if checkFlip(boardList, x + 1, y, 1, 0, piece, opponent):
      flipPieces(boardList, x + 1, y, 1, 0, piece, opponent)
    # Check down
    if checkFlip(boardList, x, y-1, 0, -1, piece, opponent):
      flipPieces(boardList, x, y-1, 0, -1, piece, opponent)
    # Check up
    if checkFlip(boardList, x, y + 1, 0, 1, piece, opponent):
      flipPieces(boardList, x, y + 1, 0, 1, piece, opponent)
    # Check down-left
    if checkFlip(boardList, x-1, y - 1, -1, -1, piece, opponent):
      flipPieces(boardList, x-1, y - 1, -1, -1, piece, opponent)
    # Check down-right
    if checkFlip(boardList, x + 1, y - 1, 1, -1, piece, opponent):
      flipPieces(boardList, x + 1, y - 1, 1, -1, piece, opponent)
    # Check up-left
    if checkFlip(boardList, x - 1, y + 1, -1, 1, piece, opponent):
      flipPieces(boardList, x - 1, y + 1, -1, 1, piece, opponent)
    # Check up-right
    if checkFlip(boardList, x + 1, y + 1, 1, 1, piece, opponent):
      flipPieces(boardList, x + 1, y + 1, 1, 1, piece, opponent)


  def updateState(self,move): #a move is made
    print("Before move:")
    print(self.board)
    self.makeMove(self.board,move[0],move[1],self.playerSymbol)
    #self.board[position[0]][position[1]] = self.playerSymbol
    if self.playerSymbol == "X":
      self.playerSymbol = "O"
    else:
      self.playerSymbol = "X"
    print(move)
    print("After move:")
    print(self.board)
    print(self.playerSymbol)
    print("Available moves are",self.availablePositions())

  #this function states when game is over
  def gameOver(self):
    playerReset = self.playerSymbol
    moves = self.availablePositions()
    if (len(moves) == 0):
      if self.playerSymbol == "X":
        self.playerSymbol = "O"
      else:
        self.playerSymbol = "X"
      Othermoves = self.availablePositions()
      # self.playerSymbol = playerReset#maybe recomment again
      if len(Othermoves) == 0:
        return True
      else:
        return False
    return False

  def winner(self):
    # global player1wins
    # global player2wins
    # global ties

    #this is your function to check if there is a winner
    if self.gameOver() == True:
      self.isEnd = True
      XScore = score(self.board,"X")
      OScore = score(self.board,"O")
      if XScore > OScore:
        return 1
      elif XScore < OScore:
        return -1
      else:
        return 0

    # not end
    self.isEnd = False
    return None

  #only when the game ends (but should we do it per move?)
  def giveReward(self):
    result = self.winner()
    # backpropagate reward
    if result == 1:
      self.p1.feedReward(1)
      self.p2.feedReward(0)
    elif result == -1:
      self.p1.feedReward(0)
      self.p2.feedReward(1)
    else:
      self.p1.feedReward(0.1)
      self.p2.feedReward(0.1)

  def reset(self):
    #resets the board
    self.board = np.full((8,8),".")
    self.boardHash = None
    self.isEnd = False
    self.playerSymbol = "X"
    self.board[3][4] = "X"
    self.board[4][3] = "X"
    self.board[3][3] = "O"
    self.board[4][4] = "O"
    player1wins = 0
    player2wins = 0
    ties = 0

  def defineWinner(self):
    global player1wins
    global player2wins
    global ties
    if self.winner() == 1:
      print("Winner is X!")
      player1wins += 1
    elif self.winner() == -1:
      print("Winner is O!")
      player2wins += 1
    elif self.winner() == 0:
      print("Tie")
      ties += 1
########################################get to here########################

  def play(self, rounds=10000):
    global player1wins
    global player2wins
    global ties
    ties = 0
    player1wins = 0
    player2wins = 0
    for i in range(rounds):
      if i % 1000 == 0:
        print("Round {}".format(i))
      while not self.isEnd:
        # Player 1
        positions = self.availablePositions()
        if len(positions) != 0:
          p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
          # take action and update board state
          self.updateState(p1_action)
          board_hash = self.getHash()
          self.p1.addState(board_hash)
        #Player 2
        self.playerSymbol = "O"
        positions = self.availablePositions()
        if len(positions) != 0:
          # Player 2
          p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
          self.updateState(p2_action)
          board_hash = self.getHash()
          self.p2.addState(board_hash)

        win = self.winner()
        if win is not None:
          #print("Winner is", self.defineWinner())
          self.defineWinner()
          self.showBoard()
          # ended with p1 either win or draw
          self.giveReward()
          self.p1.reset()
          self.p2.reset()
          self.reset()
          break



  #play with a human
  def play2(self):
    while not self.isEnd:
      # Player 1
      positions = self.availablePositions()
      p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
      # take action and upate board state
      self.updateState(p1_action)
      self.showBoard()
      # check board status if it is end
      win = self.winner()
      if win is not None:
        if win == 1:
          print(self.p1.name, "wins!")
        else:
          print("tie!")
        self.reset()
        break

      else:
        # Player 2
        positions = self.availablePositions()
        p2_action = self.p2.chooseAction(positions)

        self.updateState(p2_action)
        self.showBoard()
        win = self.winner()
        if win is not None:
            if win == -1:
                print(self.p2.name, "wins!")
            else:
                print("tie!")
            self.reset()
            break
"""
  def showBoard(self):
    # p1: x  p2: o
    for i in range(3):
      print('-------------')
      out = '| '
      for j in range(3):
        if self.board[i, j] == 1:
            token = 'x'
        if self.board[i, j] == -1:
            token = 'o'
        if self.board[i, j] == 0:
            token = ' '
        out += token + ' | '
      print(out)
    print('-------------')
"""






class Player:
  def __init__(self, name, exp_rate=0.3): #exp_rate = 0.3 means 70% of the time, our agent will take a greedy action, which is choosing the baction based on our current estimation of states-value, and 30% of the time our agent will take a random action; this is the exploration/explotation tradeoff
    self.name = name
    self.states = [] #records all positions taken
    self.lr = 0.2
    self.exp_rate = exp_rate
    self.decay_gamma = 0.9
    self.states_value = {} #state -> value

  def getHash(self, board):
    return str(board.reshape(64))


  def chooseAction(self, positions, current_board, symbol):
    if np.random.uniform(0, 1) <= self.exp_rate:
      # take random action
      idx = np.random.choice(len(positions))
      action = positions[idx]
    else:
      value_max = -999
      for p in positions:
        next_board = current_board.copy()
        next_board[p] = symbol
        next_boardHash = self.getHash(next_board)
        if self.states_value.get(next_boardHash) is None:
          value = 0
        else:
          value = self.states_value.get(next_boardHash)
        # print("value", value)
        if value > value_max:
          value_max = value
          action = p
    # print("{} takes action {}".format(self.name, action))
    return action

  # append a hash state
  def addState(self, state):
    self.states.append(state)

  # at the end of game, backpropagate and update states value
  def feedReward(self, reward):
    #this seems like the function that needs to be understood; it updates the rewards throughout the game
    for st in reversed(self.states):
      if self.states_value.get(st) is None:
        self.states_value[st] = 0
      self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
      reward = self.states_value[st]

  def reset(self):
    self.states = []

  def savePolicy(self):
    fw = open('policy_' + str(self.name), 'wb')
    pickle.dump(self.states_value, fw)
    fw.close()

  def loadPolicy(self, file):
    fr = open(file, 'rb')
    self.states_value = pickle.load(fr)
    fr.close()


class HumanPlayer:
  def __init__(self, name):
    self.name = name

  def chooseAction(self, positions):
    while True:
      row = int(input("Input your action row:"))
      col = int(input("Input your action col:"))
      action = (row, col)
      if action in positions:
        return action

  # append a hash state
  def addState(self, state):
    pass

  # at the end of game, backpropagate and update states value
  def feedReward(self, reward):
    pass

  def reset(self):
    pass


def percentage(numGames, player1wins, player2wins, ties):
  #global player1wins
  #global player2wins
  #global ties
  print("Player 1 won", player1wins, "times")
  print("Player 2 won", player2wins, "times")
  print("There were ties", ties, "times")
  print("Number of games:", numGames, "\n")

  percentOne = (player1wins / numGames) * 100
  percentTwo = (player2wins / numGames) * 100
  ties = (ties / numGames) * 100

  print("Player 1 percentage:", percentOne)
  print("Player 2 percentage:", percentTwo)
  print("Ties percentage:", ties)
  
def randomVRandom():
  #if moving the initial values to winner() doesnt work, move back here
  # ties = 0
  # player1wins = 0
  # player2wins = 0
  numGames = 5
  st = State(p1,p2)
  st.play(numGames)
  print("Result of random AI vs random AI")
  percentage(numGames, player1wins, player2wins, ties)
  st.reset()

def randomVTrained():
  #ties = 0
  #player1wins = 0
  #player2wins = 0
  numGames = 5
  st = State(p1,p2)
  st.play(numGames)

  
  p1.savePolicy()
  st.play(numGames)
  print("Result of random AI vs trained AI")
  percentage(numGames, player1wins, player2wins, ties)
  st.reset()

def trainedVTrained():
  # ties = 0
  # player1wins = 0
  # player2wins = 0
  numGames = 100
  st = State(p1,p2)
  st.play(numGames)
  
  p1.savePolicy()
  p2.savePolicy()
  p1.loadPolicy("policy_p1")
  p2.loadPolicy("policy_p2")

  st.play(numGames)
  print("Result of trained AI vs trained AI")
  percentage(numGames, player1wins, player2wins, ties)
  st.reset()

if __name__ == "__main__":
  #training
  p1 = Player("p1")
  p2 = Player("p2")
  
  st = State(p1,p2)

  """
  print(st.board)
  while True:
    print("{}'s turn".format(st.playerSymbol))
    print(st.availablePositions())
    x = int(input("Enter row 0-7: "))
    y = int(input("Enter column 0-7: "))
    st.updateState((x,y))
    print(st.board)
  """
 
  trainedVTrained()
  # randomVTrained()
  # randomVRandom()



  """
  print("training....")

  # st.play(2)
  p1.savePolicy()#save policy for trained ai 1
  p2.savePolicy()#trained ai 2

  #play with a human
  p1 = Player("computer", exp_rate=0)
  p1.loadPolicy("policy_p1")

  p2 = HumanPlayer("human")

  st = State(p1,p2)
  st.play2()
  """
  
 

