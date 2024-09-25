import pygame
import ChessEngine, SmartMoveFinder
import sys
"""
Importing needed modules
"""

Height = 800  # Height Dimension of screen
Width = 800  # Width Dimension of screen
columns = 8  # number of columns in board
rows = 8  # number of rows in board
square_Size = Height // rows  # Size of the square
pieces=['bR','bN','bB','bQ','bK','bp','wR','wN','wB','wQ','wK','wp'] #b stands for black and w stands for white. bR means black rook , wN stands for white knight
Image={} # Dictionary for storing the images of each piece

#Loads images of each piece from the corresponding PNG file then store them in the 'Image' dictionary

for piece in pieces:
    Image[piece]=pygame.image.load(piece+".png")

"""
Creating board
"""
def drawGameState(screen, board):
    # creating the board only
    for row in range(8):
        for col in range(8): #iterating over each row and column
            if (row + col) % 2 == 0:
                color = (255, 255, 255)  # White color
            else:
                color = (128, 128, 128)  # Black color

            pygame.draw.rect(screen, color, (col * square_Size, row * square_Size, square_Size, square_Size))  # surface,color,rectangle

    # loading the images of each piece to board
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "--":
                screen.blit(Image[piece], pygame.Rect(col * square_Size, row * square_Size, square_Size, square_Size))

    pygame.display.flip()


class Main:
    """
    Set up game screen with specified width and height dimensions
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height)) #creating the screen with width and height dimensions
        pygame.display.set_caption('CSAI 350 - chess game project') # caption of the screen
        self.gs = ChessEngine.GameState()

    """
    Create an infinite loop to handle events and update the game until game is over. 
    """
    def mainloop(self):
        Selected_Square = ()  # this keeps track of the last click by the user
        click_of_player = []  # keep track of player clicks(two tuples: initial position of the piece to be moved and where to be moved
        Legal_Moves = self.gs.getValidMoves() #instance of the fucntion getValidMoves from gamestate class
        movement = False  # flag variable for when a move is made
        gameOver = False # flag to check if the game finished
        p1 = True  # Player1=white; true for human
        p2 = False  # Player2=black; false for computer
        while True:
            humanTurn = (self.gs.whiteToMove and p1) or (not self.gs.whiteToMove and p2)#it's a human turn if it's white's turn to move and if player one(white) is a human playing
            for event in pygame.event.get():  # loop through all events in pygame like click events mouse motion events...
                if event.type == pygame.QUIT: #quits the game if the player presses the close button
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: #if player clicks mouse
                    """
                    Convert position of mouse click to row and column on the game board.
                    """
                    if not gameOver and humanTurn:
                        position = pygame.mouse.get_pos()  # (x,y) location of mouse
                        col = position[0] // square_Size
                        row = position[1] // square_Size
                        """
                        If player clicks twice, clear player's clicks
                        """
                        if  Selected_Square == (row, col):
                            Selected_Square= ()  # deselect
                            click_of_player = []  # clear player clicks
                        else:
                            Selected_Square= (row, col)
                            click_of_player.append(Selected_Square) #appends clicked square to the list of clicks

                        """
                        After 2nd click, create move object and check if it's a legal move. If legal, update game state with the move. Also resets selected
                        square and player clicks
                        """
                        if len(click_of_player) == 2:  # after 2nd click
                            move = ChessEngine.Move(click_of_player[0], click_of_player[1],self.gs.board)
                            for i in range(len(Legal_Moves)):
                                if move == Legal_Moves[i]:
                                    self.gs.makeMove(Legal_Moves[i])
                                    movement = True
                                    Selected_Square= ()  # reset user clicks
                                    click_of_player = []
                            """
                            If not legal move, reset player click
                            """
                            if not movement:
                                click_of_player = [Selected_Square]



            #AI move finder logic
            if not gameOver and not humanTurn: #if AI's turn move, find best move
                AIMove = SmartMoveFinder.findBestMove(self.gs, Legal_Moves)
                if AIMove is None: #if there is no best move, do random move
                    AIMove = SmartMoveFinder.findRandomMove(Legal_Moves)
                self.gs.makeMove(AIMove) #updates game state
                movement = True

            if movement: #if movement is made/true
                Legal_Moves = self.gs.getValidMoves() #update list of all possible moves to check if player made valid move, or for the ai to make the best decision
                movement = False

            drawGameState(self.screen,self.gs.board) #game state is drawn on screen
            pygame.display.update() #display the updates


main = Main()
main.mainloop()
