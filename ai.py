from sqlitedict import SqliteDict
from connect4 import *
import json
import math

treePath = "Database/tree.sqlite"
db = SqliteDict(treePath, outer_stack=False)
#Board to key is board.tobytes()
#Key to Board is np.reshape(np.frombuffer(key), (7, 6))
#{parents: [], player: bool, wins: int, visits: int, children: {}, terminal: bool}

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

class monteCarloNode():
  def __init__(this, board, player):
    this.board = board
    this.player = player
    this.wins = 0
    this.visits = 0
    this.children = {}
    this.leaf = True
    this.terminal = checkWin(this.board)
    
  def expand(this):
    possibleMoves = np.unique(np.where(this.board == 0)[0])
    moves = sorted(possibleMoves, key=lambda x: abs(3 - x))
    sign = -1 + 2 * this.player
    for move in moves:
      newBoard = makeMove(this.board, sign, move)
      child = monteCarloNode(newBoard, not this.player)
      this.children[move] = child
    this.leaf = False

class monteCarloTree():
  def __init__(this, rootBoard, rootPlayer):
    this.root = monteCarloNode(rootBoard, rootPlayer)
    this.c = 2 ** .5

  def step(this):
    nodeAddress = this.selectAndExpand()
    this.simAndProp(nodeAddress)

  def getBestMove(this):
    bestMove = (None, -1, False)
    possibleMoves = this.root.children
    for move in possibleMoves:
      child = this.root.children[move]
      info = (move, child.wins / max(1, child.visits), True)
      if info[1] > bestMove[1]:
        bestMove = info
    return bestMove

  def makeMove(this, move):
    if this.root.leaf:
      this.root.expand()
    if move not in this.root.children:
      return False
    this.root = this.root.children[move]
    return True
      
  def selectAndExpand(this):
    currentNode = this.root
    address = []
    while not currentNode.leaf:
      bestMove = (None, -1)
      for move in currentNode.children:
        child = currentNode.children[move]
        winRate = child.wins / max(1, child.visits)
        innerTerm = math.log(currentNode.visits) / max(1, child.visits)
        otherTerm = this.c * (innerTerm) ** .5
        info = (move, winRate + otherTerm)
        if info[1] > bestMove[1]:
          bestMove = info
      address.append(bestMove[0])
      currentNode = currentNode.children[bestMove[0]]
    if currentNode.terminal is None:
      currentNode.expand()
      firstMove = [x for x in currentNode.children][0]
      address.append(firstMove)
    return address

  def simAndProp(this, address):
    lastNode = this.root
    for move in address:
      lastNode = lastNode.children[move]
      
    board = np.copy(lastNode.board)
    toGo = lastNode.player
    while (winner := checkWin(board)) is None:
      possibleMoves = np.unique(np.where(board == 0)[0])
      move = np.random.choice(possibleMoves)
      #move = minimax(board, 1, toGo)[1]
      sign = -1 + toGo * 2
      newBoard = makeMove(board, sign, move)
      if newBoard is False:
        print(board, newBoard, move, sign)
      board = newBoard
      toGo = not toGo

    currentNode = this.root
    address.append(None)
    for move in address:
      currentNode.visits += 1
      if winner == 0:
        currentNode.wins += .5
      elif currentNode.player == lastNode.player:
        currentNode.wins += 1
      if move is not None:
        currentNode = currentNode.children[move]

def dbStep(rootBoard):
  key, board = dbSelectNode(rootBoard)
  dbExpand(key, board)
  winner = dbSimulate(board, db[key]['player'])
  dbBackpropSim(key, winner)
  pass

def dbExpand(key, rootBoard):
  node = db[key]
  possibleMoves = np.unique(np.where(rootBoard == 0)[0])
  sign = -1 + 2 * node['player']
  for move in possibleMoves:
    newBoard = makeMove(rootBoard, sign, move)
    newKey = newBoard.tobytes()
    node['children'][move] = newKey
    if newKey in db:
      #NEED TO PROPOGATE THE CHILD'S WINS AND VISITS BACK UPWARDS
      db[newKey]['parents'].append(key)
      continue
    child = {'parents': [key], 'player': not node['player'], 'wins': 0, 'visits': 0,
            'children': {}, 'terminal': checkWin(newBoard)}
    db[newKey] = child
  db[key] = node

def resetTree(areYouSure):
  if not areYouSure:
    print('Insufficient Parameters, you idiot.')
  for key in db:
    del db[key]
  root = {'parents': [], 'player': True, 'wins': 0, 'visits': 0,
            'children': {}, 'terminal': None}
  db[makeBoard().tobytes()] = root
  print('Tree Wiped.')

def dbSelectNode(rootBoard, c = 2 ** .5):
  key = rootBoard.tobytes()
  if key not in db:
    print(rootBoard)
  node = db[key]
  while len(node['children']) > 0:
    maxValue = -1
    maxKey = None
    for move in node['children']:
      childKey = node['children'][move]
      childNode = db[childKey]
      winRate = childNode['wins'] / max(1, childNode['visits'])
      ucb = math.log(node['visits']) / max(1, childNode['visits'])
      ucb = (ucb ** .5) * c
      if ucb > maxValue:
        maxValue = ucb
        maxKey = childKey
    node = db[maxKey]
    key = maxKey
  return (key, np.reshape(np.frombuffer(key), (7, 6)))

def dbSimulate(board, player):
  while (outcome := checkWin(board)) is None:
    sign = -1 + 2 * player
    possibleMoves = np.unique(np.where(board == 0)[0])
    move = np.random.choice(possibleMoves)
    board = makeMove(board, sign, move)
    player = not player
  return outcome

def dbBackpropSim(key, winner):
  queue = [key]
  while len(queue) > 0:
    newQueue = []
    for key in queue:
      node = db[key]
      sign = -1 + 2 * node['player']
      node['visits'] += 1
      if winner == 0:
        node['wins'] += .5
      elif winner == sign:
        node['wins'] += 1
      for parentKey in node['parents']:
        newQueue.append(parentKey)
      db[key] = node
    queue = newQueue  
    
def dbBackpropNode(parentKey, childKey):
  pass

def dbBestMove(board):
  key = board.tobytes()
  children = db[key]['children']
  maxMove = -1
  maxScore = 2
  for move in children:
    childKey = db[key]['children'][move]
    childNode = db[childKey]
    score = childNode['wins'] / max(1, childNode['visits'])
    if score < maxScore:
      maxScore = score
      maxMove = move
  return maxMove

def dbGetConfidence(board):
  key = board.tobytes()
  node = db[key]
  return round(node['wins'] / node['visits'] * 100, 2)