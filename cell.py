# cells
import entity
import vectors

class Grid:
    "defines the collision grid. cells begin at zero"
    def __init__(self, (gw, gh), (cw, ch)):
        Grid.gridwidth, Grid.gridheight = gw, gh
        Grid.cellwidth, Grid.cellheight = cw, ch
        Grid.dcells = {}

        # '2d' matrix, gridheight rows and gridwidth columns
        #Grid.cells = [[[] for i in range(0, Grid.gridwidth)] for j in range(0, Grid.gridheight)]


# for cells only axis aligned bounding boxes really need to be checked
def _cellfrompos(e):
    y = [a[1] for a in e.vertices()]
    x = [a[0] for a in e.vertices()]        

    rowmin = int(min(y) / Grid.cellwidth)
    rowmax = int(max(y) / Grid.cellwidth)
    colmin = int(min(x) / Grid.cellwidth)
    colmax = int(max(x) / Grid.cellwidth)

    return(list((row, col) for row in range(rowmin, rowmax + 1) for col in range(colmin, colmax + 1)))

def add(e):
    for row, col in _cellfrompos(e):
            if not Grid.dcells.has_key((row, col)):
                Grid.dcells[row, col] = []
            if e not in Grid.dcells[row, col]:      # "moving" an object is done by deleting it and adding it
                #Grid.cells[row][col].append(e)     # at the new location, so this check shouldn't be necessary, but whatever
                Grid.dcells[row, col].append(e)
                e.cells.append((row, col))

def delete(e):
    for row, col in e.cells:
        Grid.dcells[row, col].remove(e)
        if not Grid.dcells[row, col]:
            del (Grid.dcells[row, col])
    e.cells = []

def incell(e, cell):
    #return(e in Grid.cells[cell[0]][cell[1]])
    if Grid.dcells.has_key((cell[0], cell[1])):
        return(e in Grid.dcells[cell[0], cell[1]])
    else:
        return(False)
