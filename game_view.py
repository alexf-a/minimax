class GameView:
    '''
    A game view for a two-player, sequential move, zero-sum,
    perfect-information game.
    '''

    def __init__(self, state, strategy):
        '''(GameView, GameState.__class__,
            Strategy.__class__) -> NoneType

        Create GameView self for game described by state, where
        computer uses given strategy.
        '''
        player = input('Type c if you wish the computer to play first ')
        if player == 'c':
            p = 'p2'
        else:
            p = 'p1'
        self.state = state(p, interactive=True)
        self.strategy = strategy()

    def play(self):
        ''' (GameView) -> NoneType

        Play a game.
        '''
        print(self.state.instructions)
        print(self.state)
        print()
        while not self.state.over:
            if self.state.next_player == 'p1':
                m = self.state.get_move()
                while not m in self.state.possible_next_moves():
                    # The move was illegal.
                    print('Illegal move: {}\nPlease try again.\n'.format(m))
                    print(self.state.instructions)
                    print(self.state)
                    m = self.state.get_move()
                print('You choose: {}'.format(m))
            else:
                # The computer makes a move.
                m = self.strategy.suggest_move(self.state)
                print('The computer chooses: {}'.format(m))
            self.state = self.state.apply_move(m)
            print('New game state: ', str(self.state))
            print()

        if self.state.winner('p2'):
            # p2, the computer, wins
            print('Beat ya!')
        elif self.state.winner('p1'):
            # p1, the human challenger, wins
            print('Congrats -- you won!!')
        else:
            print('We tied...')


if __name__ == '__main__':    
    from tippy_game_state import TippyGameState
    from subtract_square_state import SubtractSquareState
    game_state = ({'t': TippyGameState, 's': SubtractSquareState})
    from strategy_random import StrategyRandom
    from strategy_minimax import StrategyMinimax
    from strategy_minimax_memoize import StrategyMinimaxMemoize
    from strategy_minimax_prune import StrategyMinimaxPrune
    from strategy_minimax_myopic import StrategyMinimaxMyopic
    strategy = ({'memoize': StrategyMinimaxMemoize, 
                 'prune': StrategyMinimaxPrune, 
                'myopic': StrategyMinimaxMyopic, 
                'minimax': StrategyMinimax, 
                'random': StrategyRandom})
    g = ''
    while not g in game_state.keys():
        g = input('t to play Tippy, s for Subtract-A-Square: ')
    s = ''
    while not s in strategy.keys():
        s = input('Enter random, minimax, '
                  'memoize, prune or myopic for a strategy: ')
    GameView(game_state[g], strategy[s]).play()