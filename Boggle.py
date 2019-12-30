import random, time

class BoggleSolver:
    def __init__(self, board, word_dict, min_word_len):
        self.board = board
        self.word_dict = word_dict
        self.min_word_len = min_word_len
        self.max_word_len = self.board.width * self.board.height
        self.solutions = []

    def solve(self):
        print(self.board)

        start_time = time.time()
        self.solve_for_board()
        end_time = time.time()
        benchmark = end_time - start_time
        print('Benchmark: ' + str(benchmark) + ' seconds')

        solutions = [solution.word for solution in self.solutions]
        solutions.sort()

        print(", ".join(solutions))
        print(str(len(self.solutions)) + " words")

        total = 0

        for solution in self.solutions:
            total += solution.score

        print('score: ' + str(total))

    def solve_for_board(self):
        width = self.board.width
        height = self.board.height

        for y in range(width):
            for x in range(height):
                progress = int((x + y * width) / (width * height) * 100)
                print("[{:100}] {}%".format("".join(["|" for _ in range(progress)]), progress))
                self.solve_for_root(x, y, self.solutions, [], "")
        progress = 100
        print("[{:100}] {}%\n".format("".join(["|" for _ in range(progress)]), progress))

    def solve_for_root(self, x, y, solutions, visited, current):
        # dont check already visited letters in run
        if [x, y] in visited:
            return

        width = self.board.width
        height = self.board.height

        # dont check out-of-bounds positions
        if x not in range(width) or y not in range(height):
            return

        # mark current position as visited and add the letter to the run
        visited.append([x, y])
        current += self.board.state[y][x]

        length = len(current)

        if length > self.max_word_len:
            return

        # validate word length and lookup word in dictionary
        if length >= self.min_word_len:
            key = current[:self.min_word_len]

            if hash(key) not in self.word_dict.words.keys():
                return

            word_set = self.word_dict[key]

            prefix_in_dict = False

            for word in word_set:
                if word.word.startswith(current):
                    prefix_in_dict = True

                    if word.word == current and word not in self.solutions:
                        solutions.append(word)

            if not prefix_in_dict:
                return

        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if y_offset == 0 and x_offset == 0:
                    continue

                self.solve_for_root(x + x_offset, y + y_offset, solutions, visited[:], current)

class BoggleBoard:
    def __init__(self, dice_set, width=4, height=4):
        self.width = width
        self.height = height
        self.dice_set = dice_set
        self.state = [[None for _ in range(width)] for _ in range(height)]

    def __str__(self):
        board_string = ""

        for row in self.state:
            for cell in row:
                board_string += '{:3}'.format(cell)
            board_string += "\n"

        return board_string

    def shuffle(self):
        for i in range(len(self.dice_set)):
            while True:
                rand_x = random.randint(0, self.width - 1)
                rand_y = random.randint(0, self.height - 1)

                if self.state[rand_y][rand_x] != None:
                    continue

                rand_face = random.randint(0, 5)

                self.state[rand_y][rand_x] = self.dice_set[i][rand_face]

                break

    def set_state(self, state):
        self.state = state
        self.width = len(state[0])
        self.height = len(state)

class BoggleWordDict:
    def __init__(self, words, board, min_word_len):
        self.words = {}
        self.min_word_len = min_word_len
        self.generate_word_dict(words, board)
        # for key in self.words.keys():
        #     print(key)

    def __contains__(self, item):
        return item in self.words

    def __getitem__(self, item):
        return self.words[hash(item)]

    # TODO: more efficient hashing with minimum sequence bucketing
    def generate_word_dict(self, words, board):
        for word in words:
            length = len(word)
            max_word_len = board.width * board.height

            if length < self.min_word_len or length >= max_word_len:
                continue

            boggle_word = BoggleWord(word, self.min_word_len)

            # self.words[word] = boggle_word

            if hash(boggle_word) in self.words.keys():
                self.words[hash(boggle_word)].append(boggle_word)
            else:
                self.words[hash(boggle_word)] = [boggle_word]

class BoggleWord:
    def __init__(self, word, min_word_len):
        self.word = word
        self.min_word_len = min_word_len
        self.update_score()

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.word == other.word
        return NotImplemented

    def __hash__(self):
        return hash(self.word[:self.min_word_len])

    def update_score(self):
        length = len(self.word)

        # TODO: verify scores with rules
        if length in  [3, 4]:
            score = 1
        elif length in [5, 6, 7]:
            score = length - 3
        else:
            score = 8

        self.score = score