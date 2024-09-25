# chess-game
## Overview

In this project, I applied adversarial search concepts to develope a two player chess game against an AI using python programming language. The implementation was done in the GUI enviroment using the pygame module. To accomplish this three python files were created which are: main.py, ChessEngine.py and SmartMoveFinder.py . Below is the explaination of each file: 

**1) main.py**

This file uses Pygame library to create a simple chess game with a graphical user interface. Also, it handles events, updates game state and draws the game board on screen. 

Inside the file there is there is the **Main class** which creates and runs the chess game and initializes Pygame, sets the dimensions of the game screen, and sets the caption for the screen.

![image](https://github.com/user-attachments/assets/098705a4-f150-4ddc-81b9-082f63858596)

The **mainloop** method creates an infinite loop to handle events and update the game until the game is over. It sets some variables that keep track of the game’s state, whether it is a human turn or an AI turn, and if the game is over.

![image](https://github.com/user-attachments/assets/622323de-8d2a-41e4-8139-8ef5e2f9c567)

There is also **drawGameState** Function which is responsible for displaying the current state of the chess game on the screen using the Pygame library.

![image](https://github.com/user-attachments/assets/e8654aaf-1bd9-49eb-ba44-ac4112f22c07)


**2) ChessEngine.py**

This allows two players to take turns making moves on the board and enforcing the rules of the game.

The **GameState** class	contains a 2D list representing the chess board, a dictionary of functions for generating valid moves for each chess piece type, variables indicating whose turn it is to move, a list of the moves made so far in the game, and other variables and functions that generally represent the state of the chess game.

![image](https://github.com/user-attachments/assets/7abd5208-756e-486a-a288-0d6d073f3e52)

**makeMove** function updates board state and game metadata when a player makes a move. It logs moves made, checks for pawn promotion, operates on the castle move, updates castling rights and many others.

![image](https://github.com/user-attachments/assets/a2053594-af2d-48c7-8007-9e2d1024136c)

**getValidMoves** function returns a list of all valid moves, considers checks and pins, handles checkmate and stalemate scenarios

![image](https://github.com/user-attachments/assets/e5a56cbc-ff2f-4cd0-aa2f-99eeed0ba8e4)

Finally in the **Move** class maps the row numbering in alphabets and columns in numbers. This means that (0,0) on the chess board has the equivalent position (a, 8) in chess notation

![image](https://github.com/user-attachments/assets/9278fb3c-c568-4e5a-b007-cf8716c0d4d9)


**3) SmartMoveFinder.py**

In this stage, I built the AI engine into the game for the human player to play against. Using the MinMax algorithm, the Computer AI returns the best move at a certain time based on the current pieces through the findBestMove function. 

There is **findBestMove** function which utilizes a min max algorithm to return the best move for the AI, minimizing point loss and maximizing point gain based on the values of each chess piece in the current game state.

![image](https://github.com/user-attachments/assets/96e5c10f-3b09-4df1-a722-15f725003fe6)




![image](https://github.com/user-attachments/assets/a25620b8-ef96-4481-992c-b2e17f381d57)



