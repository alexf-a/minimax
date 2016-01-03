# minimax
A Minimax algorithm, with speed optimizations

####To run...####

Make sure Python 3 is installed.

Simply run game_view.py in your Python shell, and follow the instructions!

You will have the option to play two different games...

And you will be able to play each against a computer opponent of your choice...

Subtract-a-Square is a game whereby you and your opponent take turns subtracting squared-integers from a randomly picked number, until the loser cannot subtract any further.

Tippy is like X's and O's, except the winner strives to form a "Tippy" with consecutive elements.

XX <br />
&nbsp; XX

and 

OO <br />
&nbsp; OO

Are Tippies. 

Your computer opponent can be a random move selector, or an Artificial Intelligence (Minimax). 

####The A.I has 3 speed-optimized forms:####

1) Prune: Predictably unfruitful parts of the game state tree are "pruned" out of further computation.

2) Memoization: Already-computed game states are cached to avoid redundancy.

3) Myopic: A maximum depth of computation down the game state tree is set. 

