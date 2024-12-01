import threading
import score

connect4_board = [
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0']
]

grid = '0' * 42
limit = 9
next_play = [5, 5, 5, 5, 5, 5, 5]


def make_state(grid, i, p):
    index = next_play[i] * 7 + i
    state = grid[:index] + p + grid[index + 1:]
    return state


def maximize(counter, state, use_threads=False):  # computer
    if limit - counter == 0:
        return None, score.get_score(state)

    max_column = -1
    max_evaluation = -1000000  # Large negative value

    if use_threads:
        results = [None] * 7  # To store results from each thread
        threads = []

        def threaded_job(i):
            if next_play[i] != -1:
                new_state = make_state(state, i, '1')
                heuristic = minimize(counter + 1, new_state)[1]
                if(heuristic > max_evaluation):
                    max_evaluation=heuristic


        for i in range(7):
            if next_play[i] != -1:
                thread = threading.Thread(target=threaded_job, args=(i,))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        for i, result in enumerate(results):
            if result and result[1] > max_evaluation:
                max_column, max_evaluation = result

    else:  # Non-threaded recursive execution
        for i in range(7):
            if next_play[i] != -1:
                heuristic = minimize(counter + 1, make_state(state, i, '1'))[1]
                if heuristic > max_evaluation:
                    max_column = i
                    max_evaluation = heuristic

    return max_column, max_evaluation


def minimize(counter, state):  # human
    if limit - counter == 0:
        return None, score.get_score(state)

    min_column = -1
    min_evaluation = 1000000  # Large positive value

    for i in range(7):
        if next_play[i] != -1:
            heuristic = maximize(counter + 1, make_state(state, i, '2'))[1]
            if heuristic < min_evaluation:
                min_column = i
                min_evaluation = heuristic

    return min_column, min_evaluation


# Main game loop
while sum(next_play) != -7:
    print("Computer turn:")
    mmm = maximize(1, grid, use_threads=True)  # Use threads only for the first call
    col = mmm[0]
    print("\nMy heuristic is\n")
    print(mmm[1])

    if col is None:
        print("Game over!")
        break

    connect4_board[next_play[col]][col] = '1'
    index = next_play[col] * 7 + col
    grid = grid[:index] + '1' + grid[index + 1:]
    next_play[col] -= 1

    for i in range(6):
        print(connect4_board[i])

    x = int(input("Enter a column: "))
    if next_play[x] != -1:
        connect4_board[next_play[x]][x] = '2'
        index = next_play[x] * 7 + x
        grid = grid[:index] + '2' + grid[index + 1:]
        next_play[x] -= 1
    else:
        print("Column full! Try again.")

    for i in range(6):
        print(connect4_board[i])
