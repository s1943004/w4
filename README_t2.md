task2
====
Prerequisite: based on Python 3.6  
It can be used on the command line:   
**[s1943004@baltic10 task2]$ python3 task2.py**

It contains:  
**1. task2.py**  
This is the main function.

    Parameters
    ---------
    m: int
        the amount of areas included in the file given
    data: list
        save data from .data file
    coord: dictionary
        save X,Y coordinates according to different areas after being divided
    header:
        a list, including names of all areas

    Process
    -------
    1. ReadFile: read data from the file given
    2. Convert: put data in a dictionary of certain structure
    3. ShowPlot: plot the data and show

**2. TIGISIO**   
Self-built package, which includes 4 .py file:

**2.1  ______init__.py** :  
> This is a python package, importing functions which are used in the main function.

**2.2 readfile.py** :  
> contains 'ReadFile(fname)' function:   
load data from a file containing XY coordinates classified by their areas

###### Details of function:  
    Parameters
    ----------
    fname: filename
        the name of file needed to read,
        including its relative or absolute directory

    Yields
    ------
    data: list
        contains dataset from the file read and saves them line by line
    inFile: file
        temporarily represents the file we need to read

    Returns
    -------
    data: list
        as shown in 'Yields'

    Example
    -------
    >>> data = TIGISIO.ReadFile('../RawData/natural_neighbourhoods.dat')
**2.3  convert.py** :  
> contains 'Convert(data)' function :  
convert dataset from list 'data' to dictionary 'dic' of certain structure
###### Details of function:
    Parameters
    ----------
    data: list
        dataset extracted from the given file by

    Yields
    ------
    dic: dictionary
        'Key's represent names of different areas;
        'Value' represent X,Y coordinates in OSGB system.
    i: int
        variable that is used to control the loop(less than the length of data)
    j: int
        the number of some areas' X,Y coordinates
        (For some areas, whose data are all in the same row)    
    k: int
        the amount of different areas in the given file
    l: int
        variable that is used to control the loop
    s: list
        contains all the names of different areas
    is_dataset: bool
        distinguishs between 'header' and 'dataset'
        (When 'is_dataset' is False, data is about 'header'; otherwise X,Y)

    Process
    -------
    1. discard empty lines and comments; the line before header is empty,so set is_dataset = False when empty lines.
    2. save header to list 's'; save the number of header as k; set is_dataset=True to preprare for saving dataset
    3. dataset starting with'[', needs to be extracted their coordinates are saved in the same line using separators'[(),]' to resplit them
    4. dataset starting with '(':
      a line only contains XY coordinate of a point, using separators'[(),]' to resplit them

    Returns
    -------
    dic: dictionary
        as shown in 'Yields'
    k: int
        as shown in 'Yields'
    s: list
        as shown in 'Yields'

    Example
    -------
    >>> coord,m,header= TIGISIO.Convert(data)

**2.4  showplot.py** :     
> contains 'ShowPlot(dic,k,s)' function:   
plot the data and show
###### Details of function:
plot point according XY coordinates and show plots      
    Parameters
    ----------
    dic: dictionary
        'Key' represent names of different areas;
        'Value' represent X,Y coordinates in OSGB system.      
    k: int
        the amount of different areas in the given file
    s: list
        contains all the names of different areas

    Yields
    ------
    k: int
         a variable used to control the loop(the serial number of Y coordinate)

    Example
    -------
    >>> TIGISIO.ShowPlot(coord,m,header)
