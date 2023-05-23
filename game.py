class Puzzle:
    """The creation of the Puzzle object and the related functionality."""

    def __init__(self):

        self.x_dim = 4
        self.y_dim = 4
        self.x_pos = 2
        self.y_pos = 2
        self.board = []
        self.cell_size = None
        self.initial_position = True
        self.border_length = None
        self.border = None
        self.row = None
        self.column_labels = None
        self.try_puzzle = True
        self.solution_found = False

    def check_dimensions(self, operation, message, error_message):
        """
        Verify the input dimensions and the user's next move.

        :param operation: string indicating the operation, must be 'board', 'start_position' or 'move'
        :param message: string indicating the input message
        :param error_message: string indicating the error message for the exception
        :return: tuple with integer values x, y
        """
        while True:
            dimensions = input(message).split()
            try:
                if len(dimensions) != 2:
                    raise ValueError
                x = int(dimensions[0])
                y = int(dimensions[1])
                if operation == "board":
                    # Check for positive values
                    if x <= 0 or y <= 0:
                        raise ValueError
                elif operation == "start_position" or operation == "move":
                    # Check for valid dimensions
                    if not 0 < x <= self.x_dim or not 0 < y <= self.y_dim:
                        raise ValueError
                    # Check for invalid move
                    elif operation == "move" and (self.board[-y][x] == f"{' ' * self.cell_size}*" or
                                                  self.board[-y][x] == f"{'_' * (self.cell_size + 1)}"):
                        raise ValueError
                return x, y
            except ValueError:
                print(error_message, end=" ")

    def setup(self):
        """
        Set the dimensions of the board.

        Set the initial position of the horse and
        call the self.setup_board() method to create the board.
        """
        self.x_dim, self.y_dim = self.check_dimensions("board",
                                                       "Enter your board dimensions: ",
                                                       "Invalid dimensions!")
        self.x_pos, self.y_pos = self.check_dimensions("start_position",
                                                       "Enter the knight's starting position: ",
                                                       "Invalid position!")

        while True:
            answer = input("Do you want to try the puzzle? (y/n): ")
            if answer in ["n", "y"]:
                self.try_puzzle = True if answer == "y" else False
                break
            print("Invalid input!")

        self.setup_board()

    def setup_board(self):
        """
        Create chessboard.
        """
        self.cell_size = len(str(self.x_dim))
        self.border_length = self.x_dim * (self.cell_size + 2) + 3
        self.border = f"{' ' * self.cell_size}{'-' * self.border_length}"  # ---------------
        self.row = ["_" * (self.cell_size + 1)] * self.x_dim  # ['__', '__', '__', '__']
        self.row.append("|")

        # Create rows
        for i in range(self.y_dim, 0, -1):
            new_row = self.row[:]
            new_row.insert(0, f"{' ' * (self.cell_size - len(str(i)))}{i}|")  # ' for example: 5|' or '10|'
            self.board.append(new_row)  # # ['2|', '__', '__', '__', '__', '|']

        # Set starting position on board
        self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}X"  # ['2|', '__', ' X', '__', '__', '|']

        # Column labels
        self.column_labels = f"{' ' * (self.cell_size + 1)}"
        for i in range(1, self.x_dim + 1):
            self.column_labels += f" {' ' * ((self.cell_size + 1) - len(str(i)))}{i}"  # 1  2  3  4

        self.initial_position = True

    def print_board(self):
        """
        Print current state of the chessboard.
        """
        print(self.border)
        for line in self.board:
            print(" ".join(line))  # 2| __  X __ __ |
        print(self.border)
        print(self.column_labels)  # 1  2  3  4

    def possible_moves(self, x, y):
        """
        Return the number of possible moves

        The knight moves in an L-shape, so it has to move 2 squares horizontally and 1 square vertically,
        or 2 squares vertically and 1 square horizontally.

        :param x: integer representing the x position of the horse
        :param y: integer representing the y position of the horse

        :return: integer indicating the number of possible moves or
        a list with the coordinates of possible moves
        """
        moves = 0
        coordinates = []
        for place in [(1, 2), (-1, 2), (1, -2), (-1, -2)]:
            if (self.x_dim, self.y_dim) >= self.check(x + place[0], y + place[1]):
                landing = self.board[-(y + place[1])][x + place[0]]  # "___"
                if self.initial_position and landing != f"{' ' * self.cell_size}*":
                    self.board[-(y + place[1])][x + place[0]] = f"{' ' * self.cell_size}A"
                    coordinates.append([x + place[0], y + place[1]])
                elif landing == f"{'_' * (self.cell_size + 1)}":
                    moves += 1

            if (self.x_dim, self.y_dim) >= self.check(x + place[1], y + place[0]):
                landing = self.board[-(y + place[0])][x + place[1]]
                if self.initial_position and landing != f"{' ' * self.cell_size}*":
                    self.board[-(y + place[0])][x + place[1]] = f"{' ' * self.cell_size}A"
                    coordinates.append([x + place[1], y + place[0]])
                elif landing == f"{'_' * (self.cell_size + 1)}":
                    moves += 1
        if self.initial_position:
            return coordinates
        return moves

    def check(self, x_value, y_value):
        """
        Check that the values are within the correct range.

        :param x_value: integer indicating the knight's position in x
        :param y_value: integer indicating the knight's position in y
        :return: A tuple with the same values if they are within the correct range, otherwise it returns
        larger dimensions to prevent the condition from passing in the method self.possible_moves
        """

        if x_value not in range(1, self.x_dim + 1) or y_value not in range(1, self.y_dim + 1):
            return self.x_dim + 1, self.y_dim + 1
        return x_value, y_value

    def best_moves(self):
        """
        Show the best moves for the current position.

        Warnsdorff's rule is a strategy that helps choose the best move based on the knight's position and
        the board status. To apply it, we need to do the following:
        - Check if each of the eight knight's moves is possible;
        - Check how many moves are possible from that landing position.
        """
        available_moves = list()
        if self.initial_position:
            available_moves = self.possible_moves(self.x_pos, self.y_pos)
            self.initial_position = False
            if not available_moves:
                return available_moves

        top_moves = dict()
        for x, y in available_moves:
            num_moves = self.possible_moves(x, y)
            if not self.solution_found:
                top_moves[num_moves] = [x, y]
            else:
                self.board[-y][x] = f"{' ' * self.cell_size}{num_moves}"

        if not self.solution_found:
            best_x, best_y = top_moves[min(top_moves)]
            return best_x, best_y, available_moves
        else:
            self.print_board()
            return available_moves

    def reset_possible_moves(self, possible_moves):
        """
        Reset the available moves on the board.

        :param possible_moves: list containing the available moves
        """
        for x, y in possible_moves:
            self.board[-y][x] = f"{'_' * (self.cell_size + 1)}"

    def user_game(self):
        """
        Knight's tour puzzle user interaction
        """
        moves = self.best_moves()
        squares_visited = 0
        while True:
            self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}*"
            squares_visited += 1
            new_x, new_y = self.check_dimensions("move", "Enter your next move: ", "Invalid move!")
            self.reset_possible_moves(moves)
            self.x_pos = new_x
            self.y_pos = new_y
            self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}X"
            self.initial_position = True
            moves = self.best_moves()
            if not moves:
                break
        squares_visited += 1
        self.print_board()
        if squares_visited != self.x_dim * self.y_dim:
            print("No more possible moves!")
            print(f"Your knight visited {squares_visited} squares!")
        else:
            print("What a great tour! Congratulations!")

    def find_solution(self):
        """
        Find a solution to the puzzle

        :return: boolean that indicates whether a solution exists
        """
        starting_pos = self.x_pos, self.y_pos
        results = self.best_moves()
        num_squares_visited = 0
        count = 0
        pos_squares_visited = []
        while True:
            count += 1
            num_squares_visited += 1
            self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}*"
            pos_squares_visited.append([self.x_pos, self.y_pos])
            self.x_pos, self.y_pos = results[0], results[1]
            self.reset_possible_moves(results[2])
            self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}X"
            self.initial_position = True
            results = self.best_moves()
            if not results:
                break
        self.board[-self.y_pos][self.x_pos] = f"{' ' * self.cell_size}X"
        num_squares_visited += 1
        if num_squares_visited != self.x_dim * self.y_dim:
            return False
        elif not self.try_puzzle:
            pos_squares_visited.append([self.x_pos, self.y_pos])
            for i, (x, y) in enumerate(pos_squares_visited):
                self.board[-y][x] = f"{' ' * ((self.cell_size + 1) - len(str(i + 1)))}{i + 1}"
        self.x_pos, self.y_pos = starting_pos
        self.solution_found = True
        return True


if __name__ == "__main__":
    knight_puzzle = Puzzle()

    knight_puzzle.setup()

    response = knight_puzzle.find_solution()
    if not response:
        print("No solution exists!")
    elif knight_puzzle.try_puzzle:
        knight_puzzle.board = []
        knight_puzzle.setup_board()
        knight_puzzle.user_game()
    else:
        print("Here's the solution!")
        knight_puzzle.print_board()
