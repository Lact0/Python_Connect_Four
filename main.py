from visuals import *
from ai import *
#from bitAi import *
import random
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

def handleForEthan(board):
  possibleMoves = np.unique(np.where(board == 0)[0])
  move = None
  while move not in possibleMoves:
    move = getConnectFourDecision()
  return move

def handleWin(board, firstAgent, secondAgent):
  players = (firstAgent, secondAgent)
  outcome = checkWin(board)
  if outcome is None:
    return False
  if outcome == 0:
    dispBoard(board, 'Tie!')
  else:
    dispBoard(board, players[int((1 - outcome) / 2)] + ' Wins!')
  return True

def playGame(isFirst = True):
  board = makeBoard()
  dispBoard(board, 'Player Turn' if isFirst else 'AI Turn')
  start = True
  sign = -1 * (not isFirst) + 1 * isFirst
  endStr = ''
  while True:
    if isFirst or (not start):
      move = handleForEthan(board)
      board = makeMove(board, sign, move)
      dispBoard(board, 'AI Turn')
      if checkWin(board) is not None:
        endStr = 'You Won! (or Tie, I\'m too lazy to check.)'
        break
    else:
      start = False
        
    oldTime = time.time()
    
    move = minimax(board, 6, not isFirst)[1]
    timeChange = int(time.time() - oldTime)
    print('AI Chose', move, 'In', timeChange, 'seconds')
    board = makeMove(board, -sign, move)
    dispBoard(board, 'Player Turn')
    if checkWin(board) is not None:
      endStr = 'You Lost! (or Tie, I\'m too lazy to check.)'
      break
  centerText(0, endStr)
  screen.refresh()
  curses.napms(10000)

def playMonte(isFirst = True, moveTime = 1):
  board = makeBoard()
  tree = monteCarloTree(board, True)
  dispBoard(board, 'Player Turn' if isFirst else 'AI Turn')
  start = True
  sign = -1 + 2 * isFirst
  percent = 50
  finalStr = ''
  while True:
    if isFirst or (not start):
      move = handleForEthan(board)
      board = makeMove(board, sign, move)
      tree.makeMove(move)
      dispBoard(board, 'AI Turn')
      if checkWin(board) is not None:
        finalStr = 'You Won! (or Tie, I\'m too lazy to check.)'
        break
    else:
      start = False
    oldTime = time.time()
    mult = (1 - (abs(percent - 50) / 50) ** 3.2)
    i = 0
    bars = -1
    while (currentTime := time.time() - oldTime) < mult * moveTime:
      tree.step()
      i += 1
      newBars = int(currentTime / moveTime / mult * 20)
      if newBars > bars:
        bars = newBars
        barString = '|' + '█' * bars + ' ' * (20 - bars) + '|'
        centerText(26, barString)
      screen.refresh()

    root = tree.root.children
    move = tree.getBestMove()[0]
    timeChange = int(time.time() - oldTime)
    think = 'After', i, 'iterations and', timeChange, 'seconds, the AI Chose', str(move + 1) + '.'
    percent = round(root[move].wins / root[move].visits * 100, 2)
    pred = 'It believes it has a ' + str(percent) + '% chance of winning.'
    screen.refresh()
    newBoard = makeMove(board, -sign, move)
    if newBoard is False:
      print('Tree:', tree.root.board, tree.root.children)
      for move in tree.root.children:
        print(move, tree.root.children[move].board)
    board = newBoard
    tree.makeMove(move)
    dispBoard(board, 'Player Turn')
    screen.addstr(28, 0, ' '.join([str(x) for x in think]))
    screen.addstr(29, 0, pred)
    if checkWin(board) is not None:
      finalStr = 'You Lost! (or Tie, I\'m too lazy to check.)'
      break
  centerText(0, finalStr)
  screen.refresh()
  #curses.napms(10000)
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

def quantumConnectFour():
  board = makeBoard()
  while True:
    dispBoard(board, 'Player 1\'s Pre-Turn')
    curses.napms(50)
    move1 = handleForEthan(board)
    dispBoard(board, 'Player 2\'s Pre-Turn')
    curses.napms(50)
    move2 = handleForEthan(board)
    flip = random.randint(0, 1)
    newMove = None
    if flip:
      board = makeMove(board, 1, move1)
      if handleWin(board, 'Player 1', 'Player 2'):
        break
      dispBoard(board, 'Player 1 Was Chosen to go First!')
      curses.napms(1750)
      dispBoard(board, 'Player 2\'s Turn')
      move = handleForEthan(board)
    else:
      board = makeMove(board, -1, move2)
      if handleWin(board, 'Player 1', 'Player 2'):
        break
      dispBoard(board, 'Player 2 Was Chosen to go First!')
      curses.napms(1750)
      dispBoard(board, 'Player 1\'s Turn')
      move = handleForEthan(board)
    board = makeMove(board, (1 - flip) * 2 - 1, move)
    if handleWin(board, 'Player 1', 'Player 2'):
        break
    dispBoard(board, 'New Turn!')
    curses.napms(1000)

connectFourMenu.nodes['Minimax Ai'].func = playGame
connectFourMenu.nodes['Monte Carlo Ai'].func = playMonte
connectFourMenu.nodes['Vs. Self'].func = quantumConnectFour

connectFourMenu.run()