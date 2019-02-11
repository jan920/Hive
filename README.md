# Hive
Python version of board game Hive


## How to play:
Running game.py will start the game

#### Rules:
http://www.ultraboardgames.com/hive/game-rules.php

#### Explanation:

So far game can by played by two players against each other later on game with basic opponent will be released

Each turn all moves available according to the rules will be printed as well as content of each players hand
In case beetles are also placed it will be printed if there is anything under them

Dash symbols("-") are placeholders where stones can't be placed

Zeros("0") represent free spaces where stones could possibly be placed if allowed by rules

Stones are printed in a way that first letter represents 
type of stone("B" for beetle, "A" for ant, "G" for grasshopper, "S" for spider, "Q" for queen), second 
is index of the specific stone("1", "2", "3"), except for Queen which does not represent index, the last is a letter
representing colour of the owner of the stone("B")

Example of this would be "S0W" which is stone of type spider index 0 and it's owner is white player


#### Enjoy the game!