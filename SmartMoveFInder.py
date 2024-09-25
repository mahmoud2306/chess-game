import random

ScoreOfPiece = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1} #maps the value of each chess piece to a point system
CHECKMATE = 1000 #used for minmax algorithm to represent very high score
STALEMATE = 0 #used for minmax algorithm to represent very low score

"""
Select random valid move from the list of valid moves
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

"""
Select best move from the list of valid moves using piece value system
"""
def findBestMove(gs, validMoves): #inputs: current game state, list of valid moves
    turnMultiplier = 1 \
        if gs.whiteToMove else -1  #1=white's turn to move, -1 = black's turn to move

    opponentMinMaxScore = CHECKMATE #opponent min max score is initially set as a very high score
    bestPlayerMove = None
    random.shuffle(validMoves) #valid move list is shuffled so that ai does not choose same move when multiple moves have the same score
    for playerMove in validMoves:  # Iterate over all valid moves for the player whose turn it is
        gs.makeMove(playerMove)  # Make the move on the game state
        opponentsMoves = gs.getValidMoves()  # Get all valid moves for the opponent

        opponentMaxScore = -CHECKMATE  # Initialize the maximum score for the opponent as the worst possible (checkmate)
        for opponentsMove in opponentsMoves:  # Iterate over all valid moves for the opponent
            gs.makeMove(opponentsMove)  # Make the move on the game state
            if gs.checkmate:  # If the game is in checkmate after the move, set the score to the worst possible (checkmate)
                score = -turnMultiplier * CHECKMATE
            elif gs.stalemate:  # If the game is in stalemate after the move, set the score to the neutral score (stalemate)
                score = STALEMATE
            else:  # Otherwise, calculate the score based on the material difference on the board
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:  # If the score is higher than the previous maximum, update the maximum score
                opponentMaxScore = score
            gs.undoMove()  # Undo the move on the game state to explore other possible moves for the opponent
        if opponentMaxScore < opponentMinMaxScore:  # If the maximum score for the opponent is better than the previous best score, update the best score and move
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()  # Undo the move on the game state to explore other possible moves for the player
    return bestPlayerMove  # Return the best move found based on the material difference on the board


#Score the board based on material
def scoreMaterial(board):
    score = 0 #initialize score to zero
    for row in board: #iterate over each row of the board
        for square in row: #iterate over each square in the row
            if square[0] == 'w': #if the piece is white, add its score to the score variable
                score += ScoreOfPiece[square[1]]
            elif square[0] == 'b': #if the piece is black, subtract its score from the score variable
                score -= ScoreOfPiece[square[1]]
    return score #return the final score

