import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
                # board[i][j] = True means planting a mine on that spot

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        # cell[0] == currRow, cell[1] == currCol

        for i in range(cell[0] - 1, cell[0] + 2):
            # iterating over currRow - 1 until currRow + 2 which means upto currRow + 1
            for j in range(cell[1] - 1, cell[1] + 2):
                # iterating over currCol - 1 until currCol + 2 which means upto currCol + 1
                # Ignore the cell itself
                if ((i, j) == cell):
                    continue

                if (i == cell[0] - 1 and j == cell[1] - 1) \
                        or (i == cell[0] - 1 and j == cell[1] + 1) \
                        or (i == cell[0] + 1 and j == cell[1] - 1) \
                        or (i == cell[0] + 1 and j == cell[1] + 1):
                    # modification: skipping the diagonals
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a `count` of the number of those cells which are mines.
    """

    # this is a single sentence like {A, B, C, D, E, F, G, H} = 2

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if it's like {A, B} = 2, we can say that all of the cells are mines
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if it's like {A, B} = 0, we can say that all of the cells are safe
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # the passed `cell` is a mine (we are sure of it)
        # we can remove it from the sentence and reduce the count by 1 where it was present
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            # reducing count by one because we are removing a cell that is known to be mine
            # so, the sentence should have count 1 less

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # we can simply remove the `cell` from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width
        # heght and width are just the max number of rows and cols

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_neighbors(self, cell, count):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        neighbor_cells = []

        # Loop over all cells within one row and column
        # cell[0] == currRow, cell[1] == currCol

        for i in range(cell[0] - 1, cell[0] + 2):
            # iterating over currRow - 1 until currRow + 2 which means upto currRow + 1
            for j in range(cell[1] - 1, cell[1] + 2):
                # iterating over currCol - 1 until currCol + 2 which means upto currCol + 1
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                if (i == cell[0] - 1 and j == cell[1] - 1) \
                        or (i == cell[0] - 1 and j == cell[1] + 1) \
                        or (i == cell[0] + 1 and j == cell[1] - 1) \
                        or (i == cell[0] + 1 and j == cell[1] + 1):
                    # modification: skipping the diagonals
                    continue

                if (0 <= i < self.height and 0 <= j < self.width) and \
                        ((i, j) not in self.mines and (i, j) not in self.safes):
                    # we don't need the known mines and known safes in the new sentence
                    # print("adding neighbors: ", (i, j))
                    neighbor_cells.append((i, j))

                if (i, j) in self.mines:
                    count -= 1
                    # this count will be used to create a new sentence


        return neighbor_cells, count

    def remove_duplicate_knowledge(self):
        unique_knowledge = []
        for currSen in self.knowledge:
            if currSen not in unique_knowledge:
                unique_knowledge.append(currSen)
        self.knowledge = unique_knowledge

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)
        print("Adding new safe cell: ", cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        neighbor_cells, count = self.get_neighbors(cell, count)
        new_sentence = Sentence(neighbor_cells, count)
        self.knowledge.append(new_sentence)
        print("Adding new knowledge: ", new_sentence)

        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        for curr_sentence in self.knowledge:
            if len(curr_sentence.cells) == 0:
                self.knowledge.remove(curr_sentence)

            safe_cells = list(curr_sentence.known_safes())
            known_mines = list(curr_sentence.known_mines())
            for safe in safe_cells:
                self.mark_safe(safe)
                print("Adding new safe cell (From inference): ", safe)
            for mine in known_mines:
                self.mark_mine(mine)
                print("Marking mine (From inference): ", mine)

        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge
        """
        More generally, any time we have two sentences set1 = count1 and set2 = count2 where
        set1 is a `subset` of set2 , then we can construct the new sentence 
        set2 - set1 = count2 - count1
        """
        inferred_knowledge = []
        for curr_sentence in self.knowledge:
            if curr_sentence == new_sentence:
                continue
            elif curr_sentence.cells.issuperset(new_sentence.cells):
                inferred_knowledge.append(
                    Sentence(curr_sentence.cells - new_sentence.cells, curr_sentence.count - new_sentence.count))

            elif new_sentence.cells.issuperset(curr_sentence.cells):
                inferred_knowledge.append(
                    Sentence(new_sentence.cells - curr_sentence.cells, new_sentence.count - curr_sentence.count))

        if len(inferred_knowledge) > 0:
            print("Adding new inferred knowledge base: ")
            for inf_knlg in inferred_knowledge:
                print(inf_knlg)
        self.knowledge.extend(inferred_knowledge)

        self.remove_duplicate_knowledge()

        # marking again
        for curr_sentence in self.knowledge:
            if len(curr_sentence.cells) == 0:
                self.knowledge.remove(curr_sentence)

            safe_cells = list(curr_sentence.known_safes())
            known_mines = list(curr_sentence.known_mines())
            for safe in safe_cells:
                self.mark_safe(safe)
                print("Adding new safe cell (From inference): ", safe)
            for mine in known_mines:
                self.mark_mine(mine)
                print("Marking mine (From inference): ", mine)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        candidate_cells = self.safes - self.moves_made
        if len(candidate_cells) == 0:
            return None

        return candidate_cells.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves_left = set()
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) not in self.mines and (row, col) not in self.moves_made:
                    moves_left.add((row, col))

        # print("moves left: " , len(moves_left))

        if len(moves_left) == 0:
            return None
        return random.choice(tuple(moves_left))
