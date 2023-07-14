import random

"""
Apply Function annotations 
https://hyperskill.org/learn/step/15664
"""


class TicTac:

    def __init__(self):
        self.human_player = None
        self.ai_player = None
        self.level = 'easy'
        self.cells = ['_'] * 9
        self.options = {'start', 'easy', 'user', 'medium', 'hard'}
        self.actions = {'user': self.user_move,
                        'easy': self.pc_move,
                        'medium': self.pc_move,
                        'hard': self.pc_move}
        self.winning_states = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                               (0, 3, 6), (1, 4, 7), (2, 5, 8),
                               (0, 4, 8), (2, 4, 6)]

    @staticmethod
    def check_state(board, player1, player2, show_outcome):
        states = [board[0:7:3], board[1:8:3], board[2:9:3]]
        states.extend([board[:3], board[3:6], board[6:9]])
        states.extend([board[0:9:4], board[2:7:2]])

        if [player1] * 3 in states:
            return f"{player1} wins" if show_outcome else 'Win'
        elif [player2] * 3 in states:
            return f"{player2} wins" if show_outcome else 'Loss'
        elif '_' in board:
            # 'Game not finished'
            return None
        else:
            return 'Draw'

    def menu(self):
        while True:
            try:
                values = input('Input command: ').split()
                if values[0] == 'exit':
                    return values
                elif len(values) != 3 or values[0] != 'start':
                    raise ValueError
                elif values[1] not in self.options or values[2] not in self.options:
                    raise ValueError
                return values
            except ValueError:
                print('Bad parameters!')

    def show_table(self):
        print('---------')
        for row in [self.cells[:3], self.cells[3:6], self.cells[6:9]]:
            print('|', end=' ')
            print(*row, end=' ')
            print('|', end=' ')
            print()
        print('---------')

    def user_move(self, marker):
        while True:
            try:
                x, y = input('Enter the coordinates: ').split()
                x, y = int(x), int(y)
                if x in range(1, 4) and y in range(1, 4):
                    pos = (x - 1) * 3 + (y - 1)
                    if self.cells[pos] != "_":
                        print('This cell is occupied! Choose another one!')
                    else:
                        self.cells[pos] = marker
                        break
                print('Coordinates should be from 1 to 3!')
            except ValueError:
                print('You should enter numbers!')

    def minimax(self, new_cells, current_player):
        state = self.check_state(new_cells, self.ai_player, self.human_player, show_outcome=False)
        # check for the terminal states and return a value accordingly
        if state == 'Loss':
            return {"score": -10}
        elif state == 'Win':
            return {"score": 10}
        elif state == 'Draw':
            return {"score": 0}

        # an array to collect all the objects
        moves = []
        for i, cell in enumerate(new_cells):
            if cell == '_':
                move = {"index": i}
                new_cells[i] = current_player

                if current_player == self.ai_player:
                    result = self.minimax(new_cells, self.human_player)
                else:
                    result = self.minimax(new_cells, self.ai_player)
                move["score"] = result["score"]

                new_cells[i] = cell

                moves.append(move)

        top_move = None
        if current_player == self.ai_player:
            best_score = -10000
            for i, move in enumerate(moves):
                if move["score"] > best_score:
                    best_score = move["score"]
                    top_move = i
        else:
            best_score = 10000
            for i, move in enumerate(moves):
                if move["score"] < best_score:
                    best_score = move["score"]
                    top_move = i

        return moves[top_move]

    def best_move(self):
        move = None
        for triplet in self.winning_states:
            cell1, cell2, cell3 = triplet
            state = self.cells[cell1] + self.cells[cell2] + self.cells[cell3]
            if '_' in state and \
                    (state.count('X') == 2 or state.count('O') == 2):
                move = triplet[state.index('_')]

        if not move:
            move = random.randrange(0, 9)
        return move

    def pc_move(self, marker):
        print(f'Making move level "{self.level}"')
        while True:
            if self.level == "medium":
                move = self.best_move()
            elif self.level == "hard":
                move_dict = self.minimax(self.cells, marker)
                move = move_dict["index"]
            else:
                move = random.randrange(0, 9)

            if self.cells[move] != "_":
                # This cell is occupied! Choose another one!
                continue
            else:
                self.cells[move] = marker
                break

    def pvp(self, p1_move, p2_move):
        turn = 0
        while True:
            self.actions[p1_move]('X')
            self.show_table()
            turn += 1
            state = self.check_state(self.cells, 'X', 'O', show_outcome=True)
            if turn >= 5 and state:
                print(state)
                break
            self.actions[p2_move]('O')
            self.show_table()
            turn += 1
            state = self.check_state(self.cells, 'O', 'X', show_outcome=True)
            if turn >= 5 and state:
                print(state)
                break

    def start(self):
        commands = self.menu()

        if commands[0] != 'exit':
            self.show_table()
            if 'medium' in commands:
                self.level = 'medium'
            elif 'hard' in commands:
                self.level = 'hard'
                self.ai_player, self.human_player = ('X', 'O') if 'hard' == commands[1] else ('O', 'X')
            self.pvp(commands[1], commands[2])


if __name__ == "__main__":
    print("Input 3 words/commands, the first one must be 'start'")
    print("the next 2 could be 'easy', 'user', 'medium' or 'hard'")
    print("the only command for human interaction is 'user'.\n")
    new_game = TicTac()
    new_game.start()
