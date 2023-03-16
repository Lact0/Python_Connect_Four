from ai import *
import time

setupScreen()

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
      tree.makeMove(move)
      drawGrid(board)
      if checkWin(board) is not None:
        print('You Won! (or Tie, I\'m too lazy to check.)')
        break
    else:
      start = False
    oldTime = time.time()
    i = 0
    while time.time() - oldTime < moveTime:
      tree.step()
      i += 1
    root = tree.root.children
    #print([(x, root[x].wins / root[x].visits) for x in root])
    move = tree.getBestMove()[0]
    timeChange = int(time.time() - oldTime)
    #print('AI Chose', move, 'In', timeChange, 'seconds')
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
    drawGrid(board)
    if checkWin(board) is not None:
      print('You Lost! (or Tie, I\'m too lazy to check.)')
      break

playMonte()