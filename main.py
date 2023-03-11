from ai import *
import time

board = makeBoard()

setupScreen()
drawGrid(board)

while True:
  print('Make Move:')
  move = int(input())
  board = makeMove(board, 1, move)
  drawGrid(board)
  if checkWin(board) is not None:
    print('You Won! (or Tie, I\'m too lazy to check.)')
    break
  oldTime = time.time()
  move = minimax(board, 5)[1]
  timeChange = int(time.time() - oldTime)
  print('AI Chose', move, 'In', timeChange, 'seconds')
  board = makeMove(board, -1, move)
  drawGrid(board)
  if checkWin(board) is not None:
    print('You Lost! (or Tie, I\'m too lazy to check.)')
    break
    