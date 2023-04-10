from visuals import *
from ai import *
#from bitAi import *
import time

board = makeBoard()
board = makeMove(board, 1, 3)
board = makeMove(board, -1, 2)
board = makeMove(board, 1, 2)
board = makeMove(board, -1, 3)

#dispBoard(board, 1, screen)
#move = getConnectFourDecision(screen)
#board = makeMove(board, 1, move)
#dispBoard(board, 2, screen)

def playGame(isFirst = True):
  board = makeBoard()
  drawGrid(board)
  start = True
  sign = -1 * (not isFirst) + 1 * isFirst
  while True:
    if isFirst or (not start):
      print('Make Move:')
      move = None
      possibleMoves = np.unique(np.where(board == 0)[0])
      while True:
        move = input()
        if move.isdigit() and int(move) < 7 and (int(move) in possibleMoves):
          move = int(move)
          break
        print('INCORRECT, YOU IDIOT')
      board = makeMove(board, sign, move)
      drawGrid(board)
      if checkWin(board) is not None:
        print('You Won! (or Tie, I\'m too lazy to check.)')
        break
    else:
      start = False
        
    oldTime = time.time()
    
    move = minimax(board, 6, not isFirst)[1]
    timeChange = int(time.time() - oldTime)
    print('AI Chose', move, 'In', timeChange, 'seconds')
    board = makeMove(board, -sign, move)
    drawGrid(board)
    if checkWin(board) is not None:
      print('You Lost! (or Tie, I\'m too lazy to check.)')
      break

def playMonte(isFirst = True, moveTime = 30):
  board = makeBoard()
  tree = monteCarloTree(board, True)
  dispBoard(board, 'Your' if isFirst else 'AI', screen)
  start = True
  sign = -1 + 2 * isFirst
  percent = 50
  while True:
    if isFirst or (not start):
      move = getConnectFourDecision(screen)
      board = makeMove(board, sign, move)
      tree.makeMove(move)
      dispBoard(board, 'AI', screen)
      if checkWin(board) is not None:
        curses.endwin()
        print('You Won! (or Tie, I\'m too lazy to check.)')
        break
    else:
      start = False
    oldTime = time.time()
    mult = (1 - (abs(percent - 50) / 50) ** 3.2)
    i = 0
    while (currentTime := time.time() - oldTime) < mult * moveTime:
      tree.step()
      i += 1
    root = tree.root.children
    move = tree.getBestMove()[0]
    timeChange = int(time.time() - oldTime)
    print('After', i, 'iterations and', timeChange, 'seconds, the AI Chose', str(move) + '.')
    percent = round(root[move].wins / root[move].visits * 100, 2)
    print('It believes it has a ' + str(percent) + '% chance of winning.')
    newBoard = makeMove(board, -sign, move)
    if newBoard is False:
      print('Tree:', tree.root.board, tree.root.children)
      for move in tree.root.children:
        print(move, tree.root.children[move].board)
    board = newBoard
    tree.makeMove(move)
    dispBoard(board, 'Player', screen)
    if checkWin(board) is not None:
      curses.endwin()
      print('You Lost! (or Tie, I\'m too lazy to check.)')
      break
  return board
#playMonte()

def playDbMonte(isFirst = True, moveTime = 30):
  board = makeBoard()
  dbStep(board)
  drawGrid(board)
  start = True
  sign = -1 * (not isFirst) + 1 * isFirst
  while True:
    if isFirst or (not start):
      print('Make Move:')
      move = None
      possibleMoves = np.unique(np.where(board == 0)[0])
      while True:
        move = input()
        if move.isdigit() and int(move) < 7 and (int(move) in possibleMoves):
          move = int(move)
          break
        print('INCORRECT, YOU IDIOT')
      board = makeMove(board, sign, move)
      drawGrid(board)
      if checkWin(board) is not None:
        print('You Won! (or Tie, I\'m too lazy to check.)')
        break
    else:
      start = False
    oldTime = time.time()
    i = 0
    while (currentTime := time.time() - oldTime) < moveTime:
      dbStep(board)
      i += 1
    move = dbBestMove(board)
    timeChange = int(time.time() - oldTime)
    newBoard = makeMove(board, -sign, move)
    print('After', i, 'iterations and', timeChange, 'seconds, the AI Chose', str(move) + '.')
    percent = dbGetConfidence(newBoard)
    print('It believes it has a ' + str(percent) + '% chance of winning.')
    board = newBoard
    drawGrid(board)
    if checkWin(board) is not None:
      print('You Lost! (or Tie, I\'m too lazy to check.)')
      break