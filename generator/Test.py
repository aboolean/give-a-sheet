from Graph import cartesian, dotted
from Todo import weeklyTodo

if __name__ == '__main__':
    # itemizedTodo
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    items -- list of topics for a given week
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    halfpage -- two half-page duplicates (portrait), else one full-page spread (landscape)
    booklet -- flag to split columns evenly among two pages, along with left labels
    binding -- size of spacing between designated pages; ignored if 'booklet' is false
    includeweekend -- includes column(s) for weekend, else includes weekdays only and a single notes column
    collapseweekend -- Sat and Sun are collapsed into a single 'Weekend' column and notes column is omitted; ignored if 'includeweekend' is false
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    

    # cartesian
    """
    Generates a page of Cartesian graph paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between graphs
    gridspace -- size of individual grid cells
    checkered -- true for checkered grid
    gridline -- thickness of lines around cells
    boxline -- thickness of border around graph(s), 0 for no box
    checkeredcolor -- color of checkered boxes
    gridcolor -- color of grid lines around cells
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of background of each cell
    layout -- number of graphs per page in (x, y) tuple
    """
    # dotted("output.pdf")

    # dotted
    """
    Generates a page of vertex-dotted grid paper.

    Keyword arguments:
    filename -- output PDF document name
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    spacer -- size of spacing between grids (if multiple)
    gridspace -- size of individual grid cells, space between dots
    dotsize -- diameter of each individual dot
    boxline -- thickness of border around graph(s), 0 for no box
    dotcolor -- color of dot at each cell vertex
    boxcolor -- color of box surrounding graph(s)
    bgndcolor -- color of grid background
    layout -- number of graphs per page in (x, y) tuple
    """
    # cartesian("output.pdf")
