import numpy as np

def makeBoard():
  return np.zeros((7, 6))

def makeMove(board, player, move):
  newBoard = np.copy(board)
  if 0 not in newBoard[move]:
    return False
  i = np.where(newBoard[move] == 0)[0][0]
  newBoard[move][i] = player
  return newBoard

def checkWin(board):

  if len(np.where(board == 0)[0]) == 0:
    return 0
  
  #HORIZONTAL, THROUGH i
  for i in range(4):
    for j in range(6):
      line = [board[i + x][j] for x in range(4)]
      if len(set(line)) == 1 and line[0] != 0:
        return line[0]

  #VERTICAL THROUGH j
  for i in range(7):
    for j in range(3):
      line = [board[i][j + x] for x in range(4)]
      if len(set(line)) == 1 and line[0] != 0:
        return line[0]

  #DIAGONAL +
  for i in range(4):
    for j in range(3):
      line = [board[i + x][j + x] for x in range(4)]
      if len(set(line)) == 1 and line[0] != 0:
        return line[0]

  #DIAGONAL -
  for i in range(4):
    for j in range(5, 2, -1):
      line = [board[i + x][j - x] for x in range(4)]
      if len(set(line)) == 1 and line[0] != 0:
        return line[0]
        
  return None

def randomMove(board, player):
  occurances = np.where(board == 0)
  availableRows = np.unique(occurances[0])
  return np.random.choice(availableRows)

def getLegal(board, action):
  if action in np.where(board == 0)[0]:
    return True
  return False

def setupScreen():
  pygame.init()
  display_screen = pygame.display.set_mode((800,600))

def drawGrid(board):
  plt.imshow(np.flip(np.transpose(board), 0))
  plt.show(block=False)
  #plt.pause(0.05)