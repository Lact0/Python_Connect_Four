import curses
from images import *

TITLE = '<Quantum> Connect Four'
UP = 65
DOWN = 66
LEFT = 68
RIGHT = 67
SPACE = 32
ENTER = 10

screen = curses.initscr()
#curses.resizeterm(34, 58)
curses.curs_set(0)
curses.noecho()
ROWS, COLS = screen.getmaxyx()
#Usually 53 & 83
#Chromebook is 34, 58

titleStart = int((COLS - len(TITLE)) / 2)
screen.addstr(0, titleStart, TITLE)

screen.refresh()
while False:
  c = screen.getch()
  screen.addstr(1, 0, '      ')
  screen.addstr(1, 0, str(c))
  screen.refresh()

curses.endwin()

class Menu():
  def __init__(this, rootNodeTitle):
    this.nodes = {}
    this.nodes[rootNodeTitle] = MenuScreen(rootNodeTitle)
    this.rootNodeTitle = rootNodeTitle

  def addScreen(this, parentTitle, title):
    this.nodes[parentTitle].addChild(title)
    this.nodes[title] = MenuScreen(title, parentTitle)

  def addImage(this, title, image):
    this.nodes[title].setImage(image)
  
  def run(this, screen):
    currentNode = this.nodes[this.rootNodeTitle]
    while True:
      options = currentNode.draw(screen)
      selected = 0
      screen.addstr(options[selected][0], options[selected][1], '>')
      screen.refresh()
      while (inp := screen.getch()) != ENTER:
        previous = selected
        if inp == DOWN:
          selected += 1
        if inp == UP:
          selected -= 1
        selected += len(options)
        selected %= len(options)
        screen.addstr(options[previous][0], options[previous][1], ' ')
        screen.addstr(options[selected][0], options[selected][1], '>')
        screen.refresh()
        
      newScreen = options[selected][2]
      if newScreen == 'Back':
        currentNode = this.nodes[currentNode.parent]
      elif newScreen == 'Exit':
        curses.endwin()
        return
      else:
        currentNode = this.nodes[options[selected][2]]
        

class MenuScreen():
  def __init__(this, title, parent = None):
    this.title = title
    this.parent = parent
    this.children = []
    this.img = None
    this.imgHeight = 0
    this.showTitle = True

  def setImage(this, image):
    this.imgHeight = image.count('\n') - 2
    this.img = image.replace('\n', '')

  def addChild(this, childName):
    this.children.append(childName)

  def draw(this, screen):
    screen.clear()
    
    rows, cols = screen.getmaxyx()
    if this.showTitle:
      titleStart = int((cols - len(this.title)) / 2)
      screen.addstr(0, titleStart, this.title)

    if this.img is not None:
      screen.addstr(2 - (not this.showTitle), 0, this.img)

    optionStartRow = 3 + this.imgHeight - (not this.showTitle) - (this.img is None) 
    options = [x for x in this.children]
    if this.parent is not None: 
      options.append('Back')
    else:
      options.append('Exit')

    optionInfo = []
      
    for i in range(len(options)):
      optionText = options[i]
      colStart = int((cols - len(optionText)) / 2)
      screen.addstr(optionStartRow + i, colStart, optionText)

      #Info is (Row, Col, Name)
      info = (optionStartRow + i, colStart - 1, optionText)
      optionInfo.append(info)
    
    return optionInfo

def dispBoard(board, turn, screen):
  screen.clear()

  turnText = turn +  ' Turn'
  turnStartPos = int((COLS - len(turnText)) / 2)
  screen.addstr(0, turnStartPos, turnText)
  
  for i in range(7):
    for j in range(6):
      r = (5 - j) * 4 + 2
      c = i * 8 + 3
      if board[i][j] == 1:
        screen.addstr(r, c, '/‾‾\\')
        screen.addstr(r + 1, c, '\\__/')
      elif board[i][j] == -1:
        screen.addstr(r, c, '/▒▒\\')
        screen.addstr(r + 1, c, '\\▒▒/')

  screen.addstr(25, 0, connectFourBar.replace('\n', ''))
  screen.refresh()

def getConnectFourDecision(screen):
  pos = 0
  screen.addstr(26, 4, '/\\')
  screen.refresh()
  while (inp := screen.getch()) != ENTER:
    if inp == LEFT:
      screen.addstr(26, pos * 8 + 4, '  ')
      pos += 6
      pos %= 7
      screen.addstr(26, pos * 8 + 4, '/\\')
    elif inp == RIGHT:
      screen.addstr(26, pos * 8 + 4, '  ')
      pos += 1
      pos %= 7
      screen.addstr(26, pos * 8 + 4, '/\\')
    screen.refresh()
  return pos

connectFourMenu = Menu('Connect Four')
connectFourMenu.addScreen('Connect Four', 'Classic')
connectFourMenu.nodes['Connect Four'].showTitle = False
connectFourMenu.addScreen('Connect Four', 'Quantum')
connectFourMenu.addScreen('Classic', 'Minimax Ai')
connectFourMenu.addScreen('Classic', 'Monte Carlo Ai')
connectFourMenu.addScreen('Quantum', 'Vs. Self')
connectFourMenu.addImage('Connect Four', titleScreenImage)
#connectFourMenu.run(screen)

