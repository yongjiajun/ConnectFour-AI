from connectfour.agents.computer_player import RandomAgent
import random

class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1
        self.run = 0
        self.bestMoveCtr = 0

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
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        self.bestMoveCtr += 1
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

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
            board.width (7)
            board.height (6)
            board.last_move (row, column)
            board.num_to_connect (4)
            board.winning_zones ()
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
        
        print("DEBUG: New run: " + str(self.run) + " Best move: " + str (self.bestMoveCtr) + '\n')
        print("Board width: " + str(board.width) + '\n')
        print("Board height: " + str(board.height) + '\n')
        print("Board last_move: " + str(board.last_move) + '\n')
        print("Board num_to_connect: " + str(board.num_to_connect) + '\n')
        print("Board winning_zones: " + str(board.winning_zones) + '\n')
        print("Board score_array: " + str(board.score_array) + '\n')
        print("Board current_player_score: " + str(board.current_player_score) + '\n')
		
        self.run += 1
        return random.uniform(0, 1)

