import random, time, sys

from Boggle import BoggleSolver, BoggleBoard, BoggleWordDict

def main(argv):
    dice_set = [
        ['P', 'F', 'A', 'S', 'K', 'F'],
        ['T', 'U', 'I', 'C', 'O', 'M'],
        ['Z', 'N', 'R', 'N', 'L', 'H'],
        ['M', 'I', 'QU', 'N', 'H', 'U'],
        ['E', 'H', 'W', 'V', 'T', 'R'],
        ['T', 'E', 'R', 'T', 'Y', 'L'],
        ['N', 'S', 'I', 'E', 'E', 'U'],
        ['D', 'I', 'Y', 'S', 'T', 'T'],
        ['J', 'B', 'O', 'A', 'O', 'B'],
        ['N', 'A', 'E', 'A', 'E', 'N'],
        ['A', 'C', 'S', 'O', 'P', 'H'],
        ['T', 'S', 'E', 'I', 'S', 'O'],
        ['G', 'E', 'W', 'H', 'E', 'N'],
        ['R', 'E', 'V', 'L', 'D', 'Y'],
        ['D', 'L', 'X', 'E', 'I', 'R'],
        ['T', 'O', 'A', 'T', 'O', 'W']
    ]

    board = BoggleBoard(dice_set)

    argc = len(argv)
    min_word_len = 3

    if argc >= 2:
        width, height = 4, 4

        if argc >= 4:
            width, height = int(argv[2]), int(argv[3])

        if argc == 5:
            min_word_len = int(argv[4])

        letters = list(argv[1].upper())
        state = [[None for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                state[y][x] = letters[x + y * width]
        board.set_state(state)
    else:
        board.shuffle()

    words = load_words_from_file('dict.txt')
    word_dict = BoggleWordDict(words, board, min_word_len)

    solver = BoggleSolver(board, word_dict, min_word_len)

    start_time = time.time()
    solutions = solver.solve()
    end_time = time.time()
    benchmark = end_time - start_time

    print('Time: ' + str(benchmark) + ' seconds\n')

    while True:
        word = input('Enter used word (return to stop):')

        if word == "":
            break

        for solution in solutions:
            if solution[0] == word:
                solutions.remove(solution)

    score = 0
    for solution in solutions:
        print(solution[0] + ': ' + str(solution[1]))
        score += solution[1]

    print('\nFinal Score:', score)

    return

def load_words_from_file(filepath):
    words = []

    with open(filepath, 'r') as f:
        while True:
            line = f.readline()

            if line == "":
                break

            words.append(line[:-1])

    return words

if __name__ == "__main__":
    main(sys.argv)
