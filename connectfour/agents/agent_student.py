from connectfour.agents.computer_player import RandomAgent
from connectfour.agents.agent import Agent
import random


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves() #是一个generator，生成有效的点，col从0到6
        vals = [] #分别两个List
        moves = []

        for move in valid_moves: 
            # id就是1或2; move就是(5,1)typle指定哪个点; move[0]就是指5，move[1]就是指1
            next_state = board.next_state(self.id, move[1]) #就是假设move[1]放进去了之后的Board对象
            moves.append( move ) #moves就是收集从第0行到第6行可以出现在棋盘上可添加的步数
            a=self.dfMiniMax(next_state, 1, -float('inf'), float('inf')) #计算概率的，Mini Max
            vals.append( a ) #可能是搜集各个点的概率,每次的str(self.dfMiniMax(next_state, 1))值都不同
            
        try:
            bestMove = moves[vals.index( max(vals) )] #最大概率点，所对的index也就是柱，对用到moves里面的具体步法
        except:
            print("It's a draw! But the game wouldn't stop (unless Steven fixes it) :( Enjoy reading the traceback message below!\n\n")

        print ("best move is: " + str(bestMove))

        return bestMove


    def dfMiniMax(self, board, depth, alpha, beta): #利用递归的算法计算出所有步骤所对的分数，此方法要研究
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth: #目前全都是走这一步
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
            vals.append( self.dfMiniMax(next_state, depth + 1, alpha, beta) )

            if alphaMode:
                alpha = max(alpha, max(vals))
                if alpha >= beta:
                    break
            else:
                beta = min(min(vals), beta)
                if alpha >= beta:
                    break
        
        if validMovesLeft == False:
            print("Depth limited!")
            return self.evaluateBoardState(board)

        if alphaMode:
            bestVal = max(vals)
        else:
            bestVal = min(vals)

        return bestVal


    def evaluateBoardState(self, board): #已经是一个合法的board了
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
            board.width     7
            board.height    6
            board.last_move
            board.num_to_connect
            board.winning_zones ？可能不需要用到
            board.score_array ？
            board.current_player_score ？

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

        for i in range(board.height):
            for j in range(board.width):
                if(board.board[i][j]==1):
                    board.update_scores(j,abs(i-(board.height-1)),1,True)
                elif(board.board[i][j]==2):
                    board.update_scores(j,abs(i-(board.height-1)),2,False)

        p = 0

        for i in range(len(board.score_array[self.id-1])):
            if (board.score_array[self.id-1][i] == 4):
                p += 5000
            elif (board.score_array[self.id-1][i] == 3 and board.score_array[self.id%2][i] == 0):
                p += 792
            elif (board.score_array[self.id-1][i] == 2 and board.score_array[self.id%2][i] == 0):
                p += 288
            elif (board.score_array[self.id-1][i] == 1 and board.score_array[self.id%2][i] == 0):
                p += 36
            elif (board.score_array[self.id-1][i] == 0 and board.score_array[self.id%2][i] == 0):
                p += 4

        pf = 0

        for j in range(len(board.score_array[self.id%2])):
            if (board.score_array[self.id%2][j] == 4):
                pf += 5000
            elif (board.score_array[self.id%2][j] == 3 and board.score_array[self.id-1][j] == 0):
                pf += 792
            elif (board.score_array[self.id%2][j] == 2 and board.score_array[self.id-1][j] == 0):
                pf += 288
            elif (board.score_array[self.id%2][j] == 1 and board.score_array[self.id-1][j] == 0):
                pf += 36
            elif (board.score_array[self.id%2][j] == 0 and board.score_array[self.id-1][j] == 0):
                pf += 4

        if (p==0 and pf==0):
            return 0.5
        else:
            return p/(p+pf)

