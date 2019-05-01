from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random


class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4   # Using MaxDepth as 4


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves: 
            next_state = board.next_state(self.id, move[1])
            moves.append( move ) 
            a=self.dfMiniMaxwithAlphaBeta(next_state, 1, -float('inf'), float('inf')) 
            vals.append( a )
            
        try:
            bestMove = moves[vals.index( max(vals) )]
        except:
            print("It's a draw! But the game wouldn't stop (unless Steven fixes it) :( Enjoy reading the traceback message below!\n\n")

        return bestMove

    # MiniMax with Alpha-Beta function
    def dfMiniMaxwithAlphaBeta(self, board, depth, alpha, beta): 

        if depth == self.MaxDepth: 
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []
        validMovesLeft = False
        
        for move in valid_moves:
            validMovesLeft = True
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
                alphaMode = False
            else:
                next_state = board.next_state(self.id, move[1])
                alphaMode = True
                
            moves.append( move )
            vals.append( self.dfMiniMaxwithAlphaBeta(next_state, depth + 1, alpha, beta) )

            if alphaMode:
                alpha = max(alpha, max(vals))
                if alpha >= beta:
                    break
            else:
                beta = min(min(vals), beta)
                if alpha >= beta:
                    break
        # give a Warning if the search depth is bigger than the current available moving steps 
        # and use calculate the Winning probability with current state. 
        if validMovesLeft == False:
            print("Depth limited!")
            return self.evaluateBoardState(board)

        # Alpha-Beta mode, return max value with odd level, return min value with even level. 
        if alphaMode:
            bestVal = max(vals)
        else:
            bestVal = min(vals)

        return bestVal


    def evaluateBoardState(self, board): 
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width     
            board.height    
            board.last_move
            board.num_to_connect
            board.winning_zones 
            board.score_array 
            board.current_player_score 

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        
        # update score_array of current board
        for i in range(board.height):
            for j in range(board.width):
                if(board.board[i][j]==1):
                    board.update_scores(j,abs(i-(board.height-1)),1,True)
                elif(board.board[i][j]==2):
                    board.update_scores(j,abs(i-(board.height-1)),2,False)

        # Calculate current Agent's Winning score
        p = self.scoreCaculate(board, self.id)
        # Calculate the other Agent's Winning score
        pf = self.scoreCaculate(board, self.id%2+1)

        # Return current Agent's Winning probability
        if (p==0 and pf==0):
            return 0.5
        else:
            return p/(p+pf)

    # Calculate function for calculating the score of available winning steps in one player
    def scoreCaculate(self, board, id):
        p = 0
        for i in range(len(board.score_array[id-1])):
            if (board.score_array[id-1][i] == 4):
                p += 12500
            elif (board.score_array[id-1][i] == 3 and board.score_array[id%2][i] == 0):
                p += 198
            elif (board.score_array[id-1][i] == 2 and board.score_array[id%2][i] == 0):
                p += 72
            elif (board.score_array[id-1][i] == 1 and board.score_array[id%2][i] == 0):
                p += 9
            elif (board.score_array[id-1][i] == 0 and board.score_array[id%2][i] == 0):
                p += 1
        return p


