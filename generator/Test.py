from Graph import cartesian, dotted, polar
from Todo import weeklyTodo

if __name__ == '__main__':
    # weeklyTodo
    """
    Generates a biweekly todo list booklet.

    Keyword arguments:
    filename -- output PDF document name
    items -- list of topics for a given week
    shading -- a 2D list of topics (rows) vs. days (cols); values indcate percent grey
    legend -- list of 2-item tupes indicating grey value and label
    pagesize -- size of page as (width, height) tuple
    margins -- size of margins around page
    booklet -- flag to generate half-page booklet; full-page if false
    binding -- size of spacing between list and binding on each page
    gridline -- thickness of lines around cells
    gridcolor -- color of grid lines around cells
    """
    r, l = 5, 9 # rec and lec shading colors
    shading = [ [0,l,r,l,r,0],
                [0,l,r,l,r,0],
                [0,l,r,l,r,0],
                [l,0,l,0,l,0],
                [l,0,l,0,0,0],
                [0,l,0,0,0,0],
                [0,0,0,0,0,0]  ]
    legend = [(r, 'Recitation'),(l,'Lecture')]
    weeklyTodo("output.pdf",items=['6.002','6.004','6.006','6.831','4.341','21W.789','Miscellanea'][::-1], shading=shading, legend=legend, gridcolor=60, gridline=1, booklet=0)

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
