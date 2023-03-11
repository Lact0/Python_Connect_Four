from connect4 import *

def value(board):
  state = checkWin(board)
  if state is not None:
    return checkWin(board) * 10
  return 0

def minimax(board, depth, maxPlayer = False, a = -100, b = 100, memo = {}):
  
  if depth == 0 or checkWin(board) is not None:
    return (value(board), None)
  val = -100 if maxPlayer else 100
  best = (val, None)

  key = np.array2string(board) + str(depth)
  reversedKey = np.array2string(np.flip(board, 0)) + str(depth)
  if key in memo:
    return memo[key]
  if reversedKey in memo:
    ret = memo[reversedKey]
    return (6 - ret[0], ret[1])

  possibleMoves = np.unique(np.where(board == 0)[0])
  moves = sorted(possibleMoves, key=lambda x: abs(3 - x))
  for move in moves:
    sign = 1 if maxPlayer else -1
    newBoard = makeMove(board, sign, move)
    moveVal = .99 * minimax(newBoard, depth - 1, not maxPlayer, a, b, memo)[0]
    
    if maxPlayer:
      if moveVal > best[0]:
        best = (moveVal, move)
      if moveVal > b:
        break
      a = best[0]
    else:
      if moveVal < best[0]:
        best = (moveVal, move)
      if moveVal < a:
        break
      b = best[0]

  memo[key] = best
  
  return best