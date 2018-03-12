# Note : This is to acknowledge the fact that in this code, I have used the
# functions (like eliminate, only_choice etc.) provided by udacity during the
# lecture sessions.

assignments = []

# Creating the board
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [(s+t) for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r,cols) for r in rows]
column_units = [cross(rows,c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diagonal_1 = [[r+c for r,c in zip(rows,cols)]]
rows_reverse = rows[::-1]
diagonal_2 = [[r+c for r,c in zip(rows_reverse,cols)]]

diagonal_units = diagonal_1 + diagonal_2

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    for unit in unitlist:
        
        potential_twins = [box for box in unit if len(values[box])==2]
        if (len(potential_twins)>1):
            for i in enumerate(potential_twins):
                val = values[potential_twins[i[0]]]
                j = i[0]+1
                twin = False
                while (not twin) and (j < len(potential_twins)):
                    if values[potential_twins[j]] == val:
                        twin = True
                    else:
                        j += 1
                if twin:
                    for box in unit:
                        if (box != potential_twins[i[0]]) and (box != potential_twins[j]):
                            for digit in val:
                                values = assign_value(values,box,values[box].replace(digit,''))
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
    

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    '''
    Eliminate the values from unsolved boxes that already have a designated location
    Args:
        values : The dictionary containing boxes with relevant values
    Returns:
        values : The dictionary after eliminating the above mentioned values
    '''
    solved_values = [box for box in values.keys() if len(values[box])==1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
    

def only_choice(values):
    '''
    Assigns a value to a box if no other unsolved box has a possibility to accomodate that value
    Args:
        values : The dictionary containing boxes with relevant values
    Returns:
        values : The dictionary after assigning the above mentioned value
    '''
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    '''
    A function to iterate over the values till a solution is found or till no further
    changes can be made
    Args:
        values : The dictionary containing boxes with relevant values
    Returns:
        values - If a solution is found or the function is stalled
        False  - If the solution resulted in an error leading to a case where there's
                 no possible value for a box
    '''
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = naked_twins(only_choice(eliminate(values)))
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''
    A function to apply Depth first search in case the function above resulted in 
    a stalled puzzle
    Args:
        values : The dictionary containing boxes with relevant values
    Returns:
        values - If a solution is found
        False  - If the solution resulted in an error leading to a case where there's
                 no possible value for a box
    '''
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
