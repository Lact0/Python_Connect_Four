def getBitBoard():
  return (0, 0)

def getMask(board):
  return board[0] & board[1]

def checkPlayerWin(board, player):
  pos = board[player]
  m = pos & (pos >> 7)
  if m & (m >> 14):
    return True
    
  m = pos & (pos >> 6)
  if m & (m >> 12):
    return True
    
  m = pos & (pos >> 8)
  if m & (m >> 16):
    return True
    
  m = pos & (pos >> 1)
  if m & (m >> 2):
    return True
    
  return False

def checkWin(board):
  player1 = checkPlayerWin(board, True)
  player2 = checkPlayerWin(board, False)
  if not player1 and not player2:
    return (False, False)
  if player1:
    return (True, 1)
  if player2:
    return (True, -1)
  #IF BOARD IS FILLED
  return (True, 0)

def make_move(board, player, move):
  newBoard = (board[0], board[1])
  playerBoard = newBoard[player]
  newBoard[player] = playerBoard | (playerBoard + (1 << (move*7)))
  return newBoard