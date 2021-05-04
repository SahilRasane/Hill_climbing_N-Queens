import random
import numpy as np
import copy


class hill_climbing():
    def __init__(self):
        self.main()

    def board(self, n):
        array = []
        board = [[0 for i in range(0, n)] for j in range(0, n)]
        

        for i in range(0,n):
            while True:
                col = random.randint(0, n-1)
                row = random.randint(0, n-1)

                if col not in array:
                    array.append(col)
                    if board[row][col] == 0:
                        board[row][col] = 1
                        break
        return board

    def heuristic(self, board, n):
        hcost=0
        dcost=0
        heu_cost=0
        for i in range (0,n):
            for j in range (0,n):
                if board[i][j] == 1:
                    hcost = hcost-2
                    for h in range (0,n):
                        if board[i][h] == 1:
                            hcost = hcost+1
                        if board[h][j] == 1:
                            hcost = hcost+1
                    q = i+1
                    e = j+1
                    while q < n and e < n:
                        if board[q][e] == 1:
                            dcost = dcost+1
                        q = q+1
                        e = e+1
                    q = i-1
                    e = j+1
                    while q >= 0 and e < n:
                        if board[q][e] == 1:
                            dcost = dcost+1
                        q = q-1
                        e = e+1
                    q = i+1
                    e = j-1
                    while q < n and e >= 0:
                        if board[q][e] == 1:
                            dcost = dcost+1
                        q = q+1
                        e = e-1
                    q = i-1
                    e = j-1
                    while q >= 0 and e >= 0:
                        if board[q][e] == 1:
                            dcost = dcost+1
                        q = q-1
                        e = e-1
        heu_cost = (dcost+hcost)/2
        return int(heu_cost)

    def compare(self, board, n, choice):
        lower_cost = self.heuristic(board, n)
        old_cost = lower_cost
        lowest_cost_board = board
        succ_count = 0
        min_board = (np.empty((n, n), dtype=int)) * 0
        for row in range(0, n):
            for col in range(0, n):
                if board[row][col] == 1:
                    for new_row in range(0, n):
                        if board[new_row][col] != 1:
                            new_board = copy.deepcopy(board)
                            new_board[row][col] = 0
                            new_board[new_row][col] = 1
                            new_cost = self.heuristic(new_board, n)
                            if new_cost < lower_cost:
                                lower_cost = new_cost
                                lowest_cost_board = new_board
                                succ_count = 0
                                min_board[new_row, col] = new_cost
                            elif new_cost == lower_cost and choice == 2:
                                succ_count = 1
                                min_board[new_row, col] = new_cost

        if old_cost < lower_cost and choice == 2:
            return lowest_cost_board, lower_cost + 1
        elif succ_count == 1 and choice == 2:
            mins = np.where(min_board == lower_cost)
            r = random.randint(0, len(mins[0]) - 1)
            srow = mins[0][r]
            scol = mins[1][r]
            new_board = board
            for i in range(0, n):
                if new_board[i][scol] == 1:
                    new_board[i][scol] = 0
            new_board[srow][scol] = 1
            lowest_cost_board = new_board
            return lowest_cost_board, lower_cost
        else:
            return lowest_cost_board, lower_cost


    def sideways_move(self, n):
        print ("Sideways move :")
        success_steps = []
        failure_steps = []

        for i in range(100):
            success_counter = sideways_count = step_count = sideways_count_temp = 0
            board = self.board(n)
            ocost = self.heuristic(board,n)
            if i < 4:
                print('++++++++++++++++\n')
                print ("Board Number " + str(i + 1))
                print('++++++++++++++++\n')
                print (np.array(board))
                print ("Number of conflicts: " + str(ocost))
            if ocost == 0:
                print ("Initial config has heuristic 0. Success")
                sideways_count = 100

            while sideways_count != 100:
                ocost = self.heuristic(board, n)
                temp = self.compare(board, n, 2)
                ncost = temp[1]
                new_board = temp[0]

                if ncost == 0:
                    step_count += 1
                    success_counter += 1
                    if i < 4:
                        print ('Success found for board')
                        print (np.array(new_board))
                    break
                if ncost == ocost:
                    sideways_count += 1
                    step_count += 1
                    board = new_board
                    #print np.array(board)
                if ncost < ocost:
                    ocost = ncost
                    board = new_board
                    if i < 4:
                        print ("Board with lower heuristic value of " + str(ncost) + " found.\n Board is")
                        print (np.array(board))
                    step_count += 1
                    sideways_count_temp += sideways_count
                    sideways_count = 0
                if ncost > ocost:
                    step_count += 1
                    print ("No better heuristic found. Failure occured at step " + str(step_count))
                    break

            if success_counter > 0:
                #print ("Steps to reach Success is " + str(step_count))
                success_steps.append(step_count)
            elif sideways_count > 0 and success_counter == 0:
                if i < 4:
                    print ("Failure occurred! Number of steps taken is " + str(step_count))
                failure_steps.append(step_count + sideways_count_temp)

        print ("Steps for success are")
        print (success_steps)
        print ("Steps for failures are")
        print (failure_steps)
        stot = len(success_steps)
        ftot = len(failure_steps)
        print ("Percentage of success is " + str(stot))
        ssum = fsum = 0
        try:
            for i in success_steps:
                ssum += i
            average1 = ssum / (stot)
            print ("Average number of steps for success are " + str(average1))
        except ZeroDivisionError:
            return None
        try:
            for i in failure_steps:
                fsum += i
            average2 = fsum / (ftot)
            print ("Average number of steps for failure are " + str(average2))
        except ZeroDivisionError:
            return None

    def random_restart_sideways(self, n):
        print ("Random restart with sideways move :")
        success_steps = []
        restart_average = []
        for m in range(100):
            i = step_count = 0
            success_found = False
            while success_found != True:
                success_counter = sideways_count = 0
                board = self.board(n)
                ocost = self.heuristic(board,n)
                if ocost == 0:
                    sideways_count = 100

                while sideways_count != 100:
                    temp = self.compare(board, n, 2)
                    ncost = temp[1]
                    new_board = temp[0]

                    if ncost == 0:
                        step_count += 1
                        success_counter += 1
                        break
                    if ncost == ocost:
                        sideways_count += 1
                        step_count += 1
                        board = new_board
                    if ncost < ocost:
                        ocost = ncost
                        board = new_board
                        step_count += 1
                        sideways_count = 0
                if success_counter > 0:
                    #print ("Steps to reach Success is " + str(step_count))
                    success_found = True
                    success_steps.append(step_count)
                    restart_average.append(i + 1)
                elif sideways_count > 0 and success_counter == 0:
                    i += 1
        print ("Steps for all success are")
        print (success_steps)
        print ("Number of restarts required each time")
        print (restart_average)
        stot = len(success_steps)
        rtot = len(restart_average)
        sum = 0
        for k in success_steps:
            sum += k
        saverage = sum/stot
        print ("Average number of steps for success are " + str(saverage))
        sum = 0
        for l in restart_average:
            sum += l
        raverage = (float(sum))/rtot
        print ("Average number of random restarts required are " + str(raverage))

    def steepest_ascent(self, n):
        count = 0
        fail_count = 0
        random_seq = 0
        succ_steps = 0
        fail_steps = 0
        for i in range(500):
            steps=0
            board = self.board(n)
            cost = self.heuristic(board, n)
            if random_seq < 4:
                    print('++++++++++++++++')
                    print('Board: ', (random_seq+1))
                    print('++++++++++++++++')
            while 1:
                if random_seq<4:
                    print('Number of conflicts : ', cost, '\n')
                    print(np.array(board))
                ncost = cost
                var1 = self.compare(board, n, 1)
                new_board = var1[0]
                cost = var1[1]
                if ncost != cost:
                    steps += 1
                if cost == 0:
                    count += 1
                    succ_steps += steps
                    break
                if ncost == cost:
                    fail_steps += steps
                    fail_count += 1
                    break
                board = new_board
            if random_seq < 4:
                if cost == 0:
                    print('Number of conflicts : ', cost, '\n')
                    print(np.array(new_board))
                    print('SOLUTION FOUND')
                else:
                    print('NO SOLUTION FOUND')
                random_seq += 1
        print('\nThe Percentage of successful Solution:', count/5)
        print('The Percentage of failure Solution:', fail_count/5)
        print('The average number of steps when it succeeds:', succ_steps/count)
        print('The average number of steps when it fails:', fail_steps/fail_count)


    def random_hill_without_sideways(self,n):

        restart_count = 0
        steps = 0
        succ_iter_cost = 0
        ncost=0
        for i in range (100):
            board = self.board(n)
            cost = self.heuristic(board, n)
            succ_iter_cost += steps
            steps=0
            while 1:
                ncost = cost
                var1 = self.compare(board, n, 1)
                new_board = var1[0]
                cost = var1[1]
                if ncost != cost:
                    steps += 1
                if cost == 0:
                    break
                if ncost == cost:
                    new_board = self.board(n)
                    cost = self.heuristic(board, n)
                    restart_count += 1
                board = new_board

        print('\nAverage number of random restarts without sideways move:', restart_count/100)
        print('Average number of steps required without sideways move', succ_iter_cost/100)

    def main(self):
        s = input("Input the board size: ")
        s = int(s)
        print('\n', s, 'Queen Problem Solution Using Steepest Ascent Hill Climbing\n')
        self.steepest_ascent(s)
        print('\n', s, 'Queen Problem Solution Using Sideways Move in Hill Climbing\n')
        self.sideways_move(s)
        print('\n', s, 'Queen Problem Solution Using Random Restart Without Sideways Move in Hill Climbing\n')
        self.random_hill_without_sideways(s)
        print('\n', s, 'Queen Problem Solution Using Random Restart With Sideways Move in Hill Climbing\n')
        self.random_restart_sideways(s)


hill_climbing()