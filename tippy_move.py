from move import Move


class TippyMove(Move):
    '''An 'x'/'o' move at column x and row y in a Tippy game.
    
    x, y (int) - coordinates on the grid.
    '''
    
    def __init__(self, x, y):
        '''(TippyMove, int, int) -> NoneType
        
        Initialize a TippyMove self at x, y position on TippyGameState grid.
        
        >>> t = TippyMove(1, 1)
        NoneType
        '''
        self.x = x
        self.y = y
    
    def __repr__(self):
        ''' (TippyMove) -> str

        Return an evaluable string version of TippyMove self's 
        initializer.
        
        >>> t = TippyMove(2, 1, 'x')
        >>> t
        TippyMove(2, 1, 'x')
        '''
        return 'TippyMove({}, {})'.format(str(self.x), str(self.y))
    
    def __str__(self):
        ''' (TippyMove) -> str

        Return a user friendly string version of TippyMove self.

        >>> t = SubtractSquareMove(2, 1)
        >>> print(t)
        Row: 1, Column: 2
        '''
        return 'Row {}, Column: {}'.format(str(self.y), str(self.x))

    def __eq__(self, other):
        ''' (TippyMove, TippyMove) -> bool

        Return TippyMove self and other are the same. 

        >>> t1 = TippyMove(3, 3)
        >>> t2 = TippyMove(1, 2)
        >>> t1 == t2
        False
        >>> t3 = TippyMove(3, 3)
        >>> t1 == t3
        True
        '''
        return (isinstance(other, TippyMove) and self.x == other.x
                and self.y == other.y)
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()