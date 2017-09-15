assignments = []

#define rows and columns as strings
rows = 'ABCDEFGHI'
cols = '123456789'

#define helper function to combine
def cross(a, b):
      return [s+t for s in a for t in b]

#create the sudoku boxes
boxes = cross(rows, cols)

# 3 units handle the row, column and square units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# 2 additional units handle the 2 diagonals 
diagonal_unit1 = [[rows[d] + cols[d] for d in range(len(rows))]]
diagonal_unit2 = [[rows[d] + cols[::-1][d] for d in range(len(rows))]]

unitlist = row_units + column_units + square_units + diagonal_unit1 + diagonal_unit2

# creating dictionaries to store units/peers
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
    #loop through the unit list to identify all 2-digit combinations (pairs) to add to the list
    for unit in unitlist:
        pairs = [] 
        twins = []
        for box in unit: 
            if len(values[box]) == 2:
                pairs.append(values[box])   
            # from the list of pairs, select values which occur exactly twice (twins)
            if pairs.count(values[box]) == 2: 
                twins.append(values[box])
        #loop through each box of the unit again which the value is greater than 1 ( already solved)
        for box in unit: 
            if len(values[box]) > 1:
                item = values[box]
                #check each digit of the twin for a match in the remaining unit values
                for t in twins:
                    #make sure the twin is not included in the removal
                    for i in item:
                        if t != item:
                            digit1 = t[0]
                            digit2 = t[1]
                        #remove matching digits and update dictionary using assign_value
                            if digit1 == i:
                                assign_value(values, box, values[box].replace(digit1, ''))
                            if digit2 == i:
                                assign_value(values, box, values[box].replace(digit2, ''))
    return values
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

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
    #create a dictionary to store the values
    dict = {} 
    default = '123456789'
    
    #next zip the key,value lists and loop through them to create dict
    # grid string should be converted to a character list while zipping
    for (k,v) in zip(boxes, list(grid)):
        if v == '.': 
            dict[k]= default
        else: 
            dict[k] = v

    #finally return the dictionary
    return dict
    
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
    # Eliminate Strategy
    single_vals = [v for v in values.keys() if len(values[v]) == 1]
    for sv in single_vals:
        v = values[sv]
        for peer in peers[sv]:
            values[peer] = values[peer].replace(v,'')

def only_choice(values):
   # Only Choice Strategy
    for unit in unitlist:
            for digit in '123456789':
                dplaces = [box for box in unit if digit in values[box]]
                if len(dplaces) == 1:
                    values[dplaces[0]] = digit

def reduce_puzzle(values):
    #loop through elimination + only choice strategies in an attempt to solve the puzzle
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        eliminate(values)
        
        #Naked Twins Strategy
        naked_twins(values)
        
        # Only Choice Strategy
        only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # First, call the reduce_puzzle function to reduce the puzzle as much as possible
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Try to solve the unfilled squares with the fewest available possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus
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
     # solve first calls the grid-values function to build the dict then tries to solve it in the search function
    return search(grid_values(grid))
    

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
