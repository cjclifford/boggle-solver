import random, time

from Boggle import BoggleSolver, BoggleBoard, BoggleWordDict

def main():
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

    width, height = 4, 4

    board = BoggleBoard(dice_set)
    board.shuffle()

    # best 4x4
    state = [
        ['O', 'T', 'E', 'H'],
        ['S', 'R', 'T', 'S'],
        ['P', 'E', 'A', 'I'],
        ['A', 'L', 'M', 'S']
    ]
    board.set_state(state)

    min_word_len = 3
    words = load_words_from_file('dict.txt')
    word_dict = BoggleWordDict(words, board, min_word_len)

    solver = BoggleSolver(board, word_dict, min_word_len)
    solver.solve()

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
    main()