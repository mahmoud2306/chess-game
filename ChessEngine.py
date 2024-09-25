"""
This class is responsible for storing all the information about the current state of a chess game and
determining the valid moves at the current state. It will also keep a move log.
"""

class GameState:
    # This class represents the state of a chess game.

    def __init__(self):
        # This method is called when a new instance of GameState is created.

        # Create a 2D list to represent the chess board.
        self.board = [
            ["bR", 'bN', "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", 'wN', "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # Create a dictionary of functions for generating valid moves for each type of chess piece.
        self.moveOperations = {
            'p': self.getMovesForPawn,
            'R': self.getMovesForRook,
            'N': self.getMovesForKnight,
            'B': self.getMovesForBishop,
            'Q': self.getMovesForQueen,
            'K': self.getMovesForKing
        }

        # A boolean indicating whether it is white's turn to move.
        self.whiteToMove = True

        # A list to store the moves made so far in the game.
        self.moveLog = []

        # The initial position of the white king.
        self.whiteKingPosition = (7, 4)

        # The initial position of the black king.
        self.blackKingLocation = (0, 4)

        # Flags indicating whether the game is in checkmate or stalemate.
        self.checkmate = False
        self.stalemate = False

        # A list of pins on the board.
        self.pins = []

        # A list of checks on the board.
        self.checks = []

        # A boolean indicating whether the king is in check.
        self.inCheck = False

        # The coordinates of the square where en passant capture is possible.
        self.ValidenPassant = ()
        self.ValidenPassantLog = [self.ValidenPassant]

        # The current castling rights of the players.
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs
        )]

    def makeMove(self, move):
        # set the ending square of the piece that is being moved to the piece
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # set the starting square of the piece that was moved to empty
        self.board[move.startRow][move.startCol] = "--"
        # log the move for undoing later
        self.moveLog.append(move)
        # switch the player
        self.whiteToMove = not self.whiteToMove
        # update the location of the king if it was moved
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        # if a pawn moved two squares, set the en passant square for the next move
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.ValidenPassant = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.ValidenPassant = ()
        # if it is an en passant move, remove the captured pawn from the board
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        # if it is a pawn promotion, change the pawn to the promoted piece
        if move.pawnPromotion:
            # for now, always promote to queen, but this could be changed later
            promotedPiece = "Q"
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece
        # if it is a castle move, move the rook and update the board
        if move.castle:
            if move.endCol - move.startCol == 2:  # kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # moves the rook
                self.board[move.endRow][move.endCol + 1] = "--"  # erase old rook
            else:  # queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # moves the rook
                self.board[move.endRow][move.endCol - 2] = "--"  # erase old rook
        # add the en passant square to the en passant log
        self.ValidenPassantLog.append(self.ValidenPassant)
        # update the castling rights
        self.updateCastleRights(move)
        # add the current castling rights to the log
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def updateCastleRights(self, move):
        """
        Update the castle rights given the moves
        """
        # If the King moves, they lose the right to castle
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        # If a rook moves from its initial position, it loses the right to castle in that direction
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRight.bks = False
        # If a rook is captured, the player loses the right to castle in that direction
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    def undoMove(self):

        if len(self.moveLog) != 0:  # MAKE SURE THAT THERE IS A MOVE TO UNDO
            move = self.moveLog.pop()  # get the last move from the move log and remove it
            # undo the move by setting the start square to the moved piece and the end square to the captured piece (if any)
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players

            # update the King's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingPosition = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo enpassant is different
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"  # removes the pawn that was added in the wrong square
                # puts thw pawn back on  the correct square it was captured from
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.ValidenPassantLog.pop()  # remove the last enpassant square from the log
            self.ValidenPassant = self.ValidenPassantLog[
                -1]  # set the current enpassant square to the last one in the log

            # undo castling rights
            self.castleRightsLog.pop()  # remove the new castle rights from the move we are undoing
            # set the current castle rights to the last one in the list
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo castle move
            if move.castle:
                if move.endCol - move.startCol == 2:  # kingside
                    # move the rook from the new square back to its original square
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"  # remove the rook from the new square
                else:  # queenside
                    # move the rook from the new square back to its original square
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"  # remove the rook from the new square

            # Add
            self.checkmate = False  # reset the checkmate flag
            self.stalemate = False  # reset the stalemate flag

    def getValidMoves(self):
        """
        all moves considering checks
        """
        moves = []  # empty list to store possible moves
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()  # check for pins and checks
        if self.whiteToMove:
            kingRow = self.whiteKingPosition[0]  # row of white king
            kingCol = self.whiteKingPosition[1]  # column of white king
        else:
            kingRow = self.blackKingLocation[0]  # row of black king
            kingCol = self.blackKingLocation[1]  # column of black king

        if self.inCheck:
            if len(self.checks) == 1:  # if only one check, block check or move king
                moves = self.getAllPossiblemoves()  # get all possible moves
                # to block a check you must move a piece into one of the squares between the enemy piece and king
                check = self.checks[0]  # check information
                checkRow = check[0]  # row of checking piece
                checkCol = check[1]  # column of checking piece
                pieceChecking = self.board[checkRow][checkCol]  # enemy piece causing the check
                AvailiableSquares = []  # squares that pieces can move to
                # if Knight, must capture knight or move king, other pieces can be blocked
                if pieceChecking[1] == "N":
                    AvailiableSquares = [(checkRow, checkCol)]  # add square that knight can be captured
                else:
                    for i in range(1, 8):
                        AvailiableSquare = (kingRow + check[2] * i,
                                            kingCol + check[3] * i)  # check[2] and check[3] are the check directions
                        AvailiableSquares.append(AvailiableSquare)  # add available square
                        if AvailiableSquare[0] == checkRow and AvailiableSquare[1] == checkCol:
                            # once you get to piece end checks
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):
                    # go through backwards when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != "K":  # move doesn't move king, so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in AvailiableSquares:
                            # move doesn't block or capture piece
                            moves.remove(moves[i])  # remove move that doesn't block or capture
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)  # get possible king moves
        else:  # not in check so all moves are fine
            moves = self.getAllPossiblemoves()  # get all possible moves

        if len(moves) == 0:  # either checkMate or staleMate
            # If in check, then it's a checkmate, else it's a stalemate
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            # If there are moves available, it's neither checkmate nor stalemate
            self.checkmate = False
            self.stalemate = False

        # Get castle moves for the current player
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingPosition[0], self.whiteKingPosition[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        # Filter out moves that leave the king in check
        safeMoves = []
        for move in moves:
            self.makeMove(move)
            self.inCheck, _, _ = self.checkForPinsAndChecks()
            if not self.inCheck:
                safeMoves.append(move)
            self.undoMove()

        return moves

    def checkForPinsAndChecks(self):
        pins = []  # squares where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying a check
        inCheck = False  # flag to keep track of whether king is in check or not

        # determine the colors and positions of the allied and enemy kings
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingPosition[0]
            startCol = self.whiteKingPosition[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        # check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pins
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # if square is on the board
                    endPiece = self.board[endRow][endCol]  # get piece on the square
                    if endPiece[0] == allyColor and endPiece[1] != "K":  # if allied piece
                        if possiblePin == ():  # if first allied piece in the direction
                            possiblePin = (endRow, endCol, d[0], d[1])  # mark as possible pin
                        else:  # if second allied piece in the direction, no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:  # if enemy piece
                        type = endPiece[1]  # get type of the piece
                        # 5 possibilities here in this complex conditional
                        # 1. orthogonally away from king and piece is a rock
                        # 2. diagonally away from king and a piece is a bishop
                        # 3. 1 square away diagonally from king and piece is a pawn
                        # 4. any direction and piece is a queen
                        # 5. any direction 1 square away and piece is a king (this is necessary to prevent a king
                        # move to a square controlled by another king)
                        if (0 <= j <= 3 and type == "R") or (4 <= j <= 7 and type == "B") or \
                                (i == 1 and type == "p" and (
                                        (enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) \
                                or (type == "Q") or (i == 1 and type == "K"):  # if enemy piece is applying check
                            if possiblePin == ():  # if no piece blocking, then it's a check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break

                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:  # off board
                    break
        # check  for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # in L shape directions
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks

    def inCheck(self):
        """
        Determine if the current player is in check
        """

        # Check if it's white's turn and return the result of squareUnderAttack function which determines if white king is underattack
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        # If it's not white's turn, and return the result of squareUnderAttack function which determines if black king is underattack
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):

        # Switch to the opponent's turn by changing the value of self.whiteToMove
        self.whiteToMove = not self.whiteToMove
        # Get all possible moves for the opponent (not the current player)
        oopMoves = self.getAllPossiblemoves()
        # Switch back to the current player's turn
        self.whiteToMove = not self.whiteToMove
        # Loop over all the opponent's possible moves and check if any of them can attack the square at position (r, c)
        for move in oopMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        # Return False if no opponent's moves can attack the square at position (r, c)
        return False

    def getAllPossiblemoves(self):
        """
        all moves without considering checks
        """
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveOperations[piece](r, c, moves)  # calls the appropriate move functions based on the piece.
        return moves

    def getMovesForPawn(self, r, c, moves):
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list
        """
        # Initialize variables for checking if the pawn is pinned and in which direction
        piecePinned = False
        pinDirection = ()

        # Check for pinned pawns and set piecePinned and pinDirection accordingly
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # Determine moveAmount, startRow, backRow, enemyColor, and the location of the king based on which player is moving
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = "b"
            kingRow, kingCol = self.whiteKingPosition
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation

        # Initialize variable for checking if a pawn can be promoted
        pawnPromotion = False



        if self.board[r + moveAmount][c] == "--": #this code block checks if the pawn can make a one-square pawn advance

            # If the pawn is not pinned or the pinDirection is in the same direction as the pawn move
            if not piecePinned or pinDirection == (moveAmount, 0):
                # If the pawn reaches the backRow, then it is a pawn promotion move
                if r + moveAmount == backRow:
                    pawnPromotion = True

                # Add the pawn move to the list of possible moves
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion=pawnPromotion))

                # This code block checks if the pawn can make a two-square pawn advance from the starting row
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":
                    # Add the two-square pawn move to the list of possible moves
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))

        if c - 1 >= 0:  # checks if pawn can capture a piece to the left
            # If there is an enemy piece to the left of the pawn, add the capture move to the list of possible moves
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor: # If the pawn reaches the backRow, then it is a pawn promotion move
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion=pawnPromotion))

                # This code block checks if the pawn can perform en passant capture to the left
                if (r + moveAmount, c - 1) == self.ValidenPassant:
                    attackingPiece = blockingPiece = False
                    # If the king is on the same row as the pawn
                    if kingRow == r:
                        if kingCol < c:  # king is left of the pawn
                            # inside range between king and the pawn, outside range between pawn border
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:  # if the king is right of the pawn
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = (c - 2, -1, -1)

                        # Check if there are any other pieces between the king and the pawn (excluding the en passant pawn)
                        for i in insideRange:
                            if self.board[r][i] != "--":  # some other piece beside the enpassant pawn blocks
                                blockingPiece = True

                        # Check if there is any attacking piece (rook or queen) beyond the en passant pawn's border
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):  # attacking piece
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True

                    # If there are no attacking or blocking pieces, add the en passant capture move to the list of possible moves
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant=True))

        if c + 1 <= 7:  # check if capturing to the right is possible
            if not piecePinned or pinDirection == (moveAmount, 1):  # if not pinned or pinned in the same direction
                if self.board[r + moveAmount][c + 1][0] == enemyColor:  # if there is an enemy piece to capture
                    if r + moveAmount == backRow:  # if pawn reaches the back rank, it can promote
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board,
                                      pawnPromotion=pawnPromotion))  # add move to list
                if (r + moveAmount, c + 1) == self.ValidenPassant:  # if en passant capture is possible
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king is left of the pawn
                            # inside range between king and the pawn, outside range between pawn border
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:  # king is right of the pawn
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = (c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":  # some other piece beside the en passant pawn blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):  # attacking piece
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board,
                                          enPassant=True))  # add en passant move to list

    def getMovesForRook(self, r, c, moves):
        """
        Get all the Rock moves for the Rock located at row, col and add these moves to the list
        """
        piecePinned = False  # flag to indicate if the rook is pinned
        pinDirection = ()  # direction of the pin
        # loop through all the pins and check if the rook is pinned
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "Q":
                    # can't remove queen from pin on rock moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])  # remove the pin if it is not a queen
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"  # determine the enemy color
        # loop through all the directions
        for d in directions:
            # loop through all the squares in the direction
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                # check if the square is on the board
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    # check if the rook is not pinned or if it is moving in the pinned direction
                    # or if it is moving in the opposite direction of the pin
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]  # piece on the square
                        # if the square is empty, add the move
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        # if the square has an enemy piece, add the move and stop searching in that direction
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        # if the square has a friendly piece, stop searching in that direction
                        else:
                            break
                # if the square is off the board, stop searching in that direction
                else:
                    break

    def getMovesForKnight(self, r, c, moves):
        """
        Get all the Knight moves for the Knight located at row, col and add these moves to the list
        """
        piecePinned = False  # a flag to check if the piece is pinned or not
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:  # if the current piece is pinned
                piecePinned = True  # set the flag to True
                self.pins.remove(self.pins[i])  # remove the pin
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1),
                       (2, 1))  # all possible knight moves (in L shape directions)
        allyColor = "w" if self.whiteToMove else "b"  # get the color of the allies
        for m in knightMoves:
            endRow = r + m[0]  # get the row index of the potential end square
            endCol = c + m[1]  # get the column index of the potential end square
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # if the potential end square is on the board
                if not piecePinned:  # if the current piece is not pinned
                    endPiece = self.board[endRow][endCol]  # get the piece at the potential end square
                    if endPiece[0] != allyColor:  # if the piece at the potential end square is not an ally
                        moves.append(Move((r, c), (endRow, endCol), self.board))  # add the move to the list of possible moves

    def getMovesForBishop(self, r, c, moves):
        """
        Get all the Bishop moves for the Bishop located at row, col and add these moves to the list
        """
        piecePinned = False  # whether the bishop is pinned to the king
        pinDirection = ()  # the direction of the pin
        for i in range(len(self.pins) - 1, -1, -1):  # iterate over all the pins
            if self.pins[i][0] == r and self.pins[i][1] == c:  # if the bishop is pinned
                piecePinned = True  # bishop is pinned to the king
                pinDirection = (self.pins[i][2], self.pins[i][3])  # get the pin direction
                self.pins.remove(self.pins[i])  # remove the pin
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # possible diagonal directions for bishop
        enemyColor = "b" if self.whiteToMove else "w"  # color of enemy pieces
        for d in directions:
            for i in range(1, 8):  # bishop can move up to 7 squares in any direction
                endRow = r + d[0] * i  # row of potential move
                endCol = c + d[1] * i  # column of potential move
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # if the move is on the board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):  # if the bishop is not pinned or the move is in the direction of the pin
                        endPiece = self.board[endRow][endCol]  # get the piece on the potential move square
                        if endPiece == "--":  # empty space, bishop can move there
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[
                            0] == enemyColor:  # enemy piece, bishop can move there and capture the enemy piece
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piece, bishop cannot move there
                            break
                else:  # move is off the board, bishop cannot move there
                    break

    def getMovesForKing(self, r, c, moves):
        """
        Get all the King moves for the King located at row, col and add these moves to the list
        """
        # Define the moves of a king in row and column directions
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        # Determine the color of the player moving
        allyColor = "w" if self.whiteToMove else "b"
        # Loop through all the possible moves of the king
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # Check if the move is on the board
                endPiece = self.board[endRow][endCol]
                if endPiece != allyColor:  # Check if the move is to an empty square or enemy piece
                    # Place the king on the end square and check for checks
                    if allyColor == "w":
                        self.whiteKingPosition = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:  # If not in check, append the move to the list
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # Place the king back on its original location
                    if allyColor == "w":
                        self.whiteKingPosition = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

    def getMovesForQueen(self, r, c, moves):
        """
        Get all the Queen moves for the Queen located at row, col and add these moves to the list
        """
        self.getMovesForRook(r, c, moves)
        self.getMovesForBishop(r, c, moves)

    def getCastleMoves(self, r, c, moves):
        """
        Generate all valid castle moves for the king at (r, c) and add them to the list of moves
        """
        if self.squareUnderAttack(r, c):
            return  # can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)  # call helper function for kingside castle moves
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)  # call helper function for queenside castle moves

    def getKingsideCastleMoves(self, r, c, moves):
        # Check if the squares between the king and rook are empty
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            # Check if the king is not in check when it moves to the squares between the king and rook
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                # Add the castle move to the list of moves
                moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

    def getQueensideCastleMoves(self, r, c, moves):
        # Check if the squares between the king and the rook are empty
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            # Check if the squares the king moves over are not under attack
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                # Add the castle move to the list of moves
                moves.append(Move((r, c), (r, c - 2), self.board, castle=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        # boolean indicating if white can castle kingside
        self.wks = wks
        # boolean indicating if black can castle kingside
        self.bks = bks
        # boolean indicating if white can castle queenside
        self.wqs = wqs
        # boolean indicating if black can castle queenside
        self.bqs = bqs



class Move:
    """
    This class represents a move in the game of chess. The chess board has row numbering in alphabets and columns in
numbers, meaning that (0, 0) on the chess board has the equivalent position (a, 8) in chess notation, where the
first element represents the file and the second element represents the rank.
    """
    # maps keys to values
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    #initializing variables
    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False, castle=False):
        self.startRow = startSq[0]#integer representing the row of the starting square
        self.startCol = startSq[1]#integer representing the column of the starting square
        self.endRow = endSq[0]#integer representing the row of the ending square
        self.endCol = endSq[1]#integer representing the column of the ending square
        self.pieceMoved = board[self.startRow][self.startCol]# a string representing the piece that was moved (e.g., "wp" for a white pawn)
        self.pieceCaptured = board[self.endRow][self.endCol]#a string representing the piece that was captured (if any)

        self.enPassant = enPassant #a boolean indicating whether the move is an en passant capture
        self.pawnPromotion = self.pieceMoved[1] == "p" and (self.endRow == 0 or self.endRow == 7)  # indicating whether the move is a pawn promotion

        if enPassant:
            self.pieceCaptured = "bp" if self.pieceMoved == "wp" else "wp"  # enpassant captures opposite colored pawn

        # castle moves
        self.castle = castle
        self.isCapture = self.pieceCaptured != "--"
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        It checks whether two Move objects are equal by comparing their moveID attributes. If the other object being
        compared is not an instance of the Move class, the method returns False. This allows instances of the Move class
        to be compared using the == operator, and ensures that only Move objects are compared.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False



    def __str__(self):
        """
        The purpose of this method is to return a string representation of a move, which can be used to display the move
         to a user or to save the move in a log.
        """
        """
        If the move is a castle move (king-side or queen-side), the method returns "O-O" or "O-O-O" respectively, based 
        on the ending column of the move.
        """
        if self.castle:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        """
        If the move is a pawn move, the method checks if it is a capture move or a non-capture move, and returns a 
        string representation accordingly. The string representation for a non-capture move is simply the rank and file 
        of the ending square. The string representation for a capture move includes "x" followed by the rank and file of
        the ending square.
        """
        if self.pieceMoved[1] == "p":
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
        """
        If the move is a pawn promotion move or a piece move, the method returns a string representation based on the 
        piece type and the move type (capture or non-capture). Additionally, the method also adds "+" to the end of the 
        string if the move is a check move, and "#" to the end of the string if the move is a checkmate move.
        """
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare

