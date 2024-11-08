INF = float("inf")
N_INF = float("-inf")

def calculate_total_cost(costs, initial_x):
    result = 0
    for i in range(0, len(costs)):
        for j in range(0, len(costs[0])):
            result += costs[i][j]*initial_x[i][j]
    return result

def calculate_initial_x(demand, supply, initial_x, row_index, column_index):
    value = min(demand[column_index], supply[row_index])
    initial_x[row_index][column_index] += value
    supply[row_index] -= value
    demand[column_index] -= value

def calculate_increments(demand, supply, costs, flag):
    pivot_list = demand if flag else supply
    not_pivot_list = supply if flag else demand
    result_increments = [-1] * len(pivot_list)
    for i in range(0, len(pivot_list)):
        min_values = [INF, INF]
        if (not flag and supply[i] == 0) or (flag and demand[i] == 0):
            continue
        for j in range(0, len(not_pivot_list)):
            value = costs[j][i] if flag else costs[i][j]
            if (flag and supply[j] == 0) or (not flag and demand[j] == 0):
                continue
            if value < min_values[0]:
                min_values[1] = min_values[0]
                min_values[0] = value
            elif value < min_values[1]:
                min_values[1] = value
        if min_values[1] != INF:
            result_increments[i] = min_values[1] - min_values[0]
    return result_increments

def check_has_valid_increments(increments):
    for increment in increments:
        if increment != -1:
            return True
    return False

def find_first_index(costs, supply, demand, row_increments, column_increments):
    max_increment, flag, index = N_INF, False, -1
    for i in range(0, len(supply)):
        if row_increments[i] > max_increment:
            max_increment = row_increments[i]
            index = i
    for i in range(0, len(demand)):
        if column_increments[i] > max_increment:
            max_increment = column_increments[i]
            index = i
            flag = True
    return max_increment, flag, index

def find_second_index(costs, supply, demand, index, flag):
    min_value, min_row_index, min_column_index = INF, -1, -1
    if flag:
        for i in range(0, len(supply)):
            if costs[i][index] < min_value and supply[i] != 0:
                min_value = costs[i][index]
                min_row_index = i
                min_column_index = index
    else:
        for i in range(0, len(demand)):
            if costs[index][i] < min_value and demand[i] != 0:
                min_value = costs[index][i]
                min_column_index = i
                min_row_index = index
    return min_value, min_row_index, min_column_index

def iterate_final_time(supply, demand, initial_x):
    index = -1
    for i in range(0, len(supply)):
        if supply[i] != 0:
            index = i
            break
    for i in range(0, len(demand)):
        if demand[i] != 0:
            initial_x[index][i] += demand[i]
            return initial_x

def find_matrix(costs):
    max_in_rows, max_in_columns = [], []
    for i in range(0, len(costs)):
        max_in_rows.append((max(costs[i])))
    for i in range(0, len(costs[0])):
        temp_max = N_INF
        for j in range(0, len(costs)):
            otladka = costs[j][i]
            temp_max = max(temp_max, costs[j][i])
        max_in_columns.append(temp_max)
    result = list(costs)
    for i in range(0, len(costs)):
        for j in range(0, len(costs[0])):
            result[i][j] -= max_in_rows[i] + max_in_columns[j]
    return result

def find_indexes_of_min(matrix, supply, demand):
    min_value, index1, index2 = INF, -1, -1
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            if min_value > matrix[i][j] and supply[i] != 0 and demand[j] != 0:
                min_value, index1, index2 = matrix[i][j], i, j
    matrix[index1][index2] = INF
    return index1, index2



def iterate(supply, demand, matrix):
    initial_x = [[0] * len(demand) for _ in range(0, len(supply))]
    while sum(supply) != 0:
        index1, index2 = find_indexes_of_min(matrix, supply, demand)
        if index1 == -1 or index2 == -1:
            return initial_x
        calculate_initial_x(demand, supply, initial_x, index1, index2)
    return initial_x

def is_balanced(supply, demand):
    return sum(supply) == sum(demand)

def copy_list(this_list):
    result = []
    for i in this_list:
        result.append(i[:])
    return result

def northwest_corner(supply, costs, demand, initial_x=None):
    if initial_x is None:
        initial_x = [[0] * len(demand) for _ in range(0, len(supply))]
    supply_index, demand_index = -1, -1
    for i in range(0, len(supply)):
        if supply[i] != 0:
            supply_index = i
            break
    for i in range(0, len(demand)):
        if demand[i] != 0:
            demand_index = i
            break
    if supply_index == -1 or demand_index == -1:
        return initial_x
    calculate_initial_x(demand, supply, initial_x, supply_index, demand_index)
    return northwest_corner(supply, costs, demand, initial_x)

def vogel_approximation(supply, costs, demand, initial_x = None):
    if initial_x is None:
        initial_x = [[0] * len(demand) for _ in range(0, len(supply))]
    while sum(supply) != 0:
        row_increments = calculate_increments(demand, supply, costs, False)
        column_increments = calculate_increments(demand, supply, costs, True)
        if not (check_has_valid_increments(row_increments)
                or check_has_valid_increments(column_increments)):
            return iterate_final_time(supply, demand, initial_x)
        max_increment, flag, index = find_first_index(costs, supply, demand, row_increments, column_increments)
        min_value, min_row_index, min_column_index = find_second_index(costs, supply, demand, index, flag)
        calculate_initial_x(demand, supply, initial_x, min_row_index, min_column_index)


def russell_approximation(supply, costs, demand):
    additional_matrix = find_matrix(costs)
    return iterate(supply, demand, additional_matrix)


def display_transportation_table(supply, demand, costs):

    sources = [f"A{i+1}" for i in range(0, len(supply))]
    destinations = [f"B{i+1}" for i in range(0, len(demand))]

    source_width = max(len("Source"), max(len(src) for src in sources))
    dest_width = max(len(dest) for dest in destinations)
    supply_width = len("Supply")

    header = f"{'Source'.center(source_width)} | {'Destination'.center(12 * len(destinations)+2)} | {'Supply'.center(supply_width)}"
    sub_header = f"{' '.center(source_width)} | " + " | ".join(f"{dest.center(dest_width):^10}" for dest in destinations) + f" | {' '.center(supply_width)}"
    print(header)
    print(sub_header)
    print("-" * len(sub_header))

    # Display each source with costs and supply
    for i, source in enumerate(sources):
        row = f"{source.center(source_width)} | " + " | ".join(f"{str(cost).center(dest_width):^10}" for cost in costs[i]) + f" | {str(supply[i]).center(supply_width)}"
        print(row)

    # Display demand row
    demand_row = f"{'Demand'.center(source_width)} | " + " | ".join(f"{str(d).center(dest_width):^10}" for d in demand) + " | "
    try:
        demand_row += f"{str(sum(demand)).center(supply_width)}"
    except:
        pass
    print("-" * len(sub_header))
    print(demand_row)



def main():
    print(
    """
    North-west corner Method: 1
    Vogel's approximation Method: 2
    Russell's approximation Method: 3
    """)
    mode = int(input("\tChoose the program option from 1 to 3: "))
    supply = list(map(float, input().split()))
    costs = []
    for i in range(0, len(supply)):
        costs.append(list(map(float, input().split())))
    demand = list(map(float, input().split()))

    print("\tGiven:")
    display_transportation_table(supply, demand, costs)
    print()

    if not is_balanced(supply, demand):
        print("The problem is not balanced!")

    initial_costs = copy_list(costs)
    result = [[]]
    if mode == 1:
        result = northwest_corner(supply, costs, demand)
    elif mode == 2:
        result = vogel_approximation(supply, costs, demand)
    elif mode == 3:
        result = russell_approximation(supply, costs, demand)

    method = "Northwest Corner" if mode == 1 else "Vogel Approximation" if mode == 2 else "Russell Approximation"
    print(f"\tBy {method}")
    print()
    display_transportation_table(['' for _ in supply], ['' for _ in demand], result)
    print()
    print(f"\tAnswer : {calculate_total_cost(initial_costs, result)}")


if __name__ == '__main__':
    main()
