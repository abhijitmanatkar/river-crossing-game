# River Crossing Game by Abhijit Manatkar (2019101108)



This is the river crossing game made for ISS Assignment 3.

### Installation

The game requires Pygame to run.
Install pygame:

```sh
$ pip3 install pygame
```

Run the game with the following command:
```sh
$ python3 game.py
```

### Rounds

- Player 1 and Player 2 play alternately.
- One round consists of each player playing once.
- If only one player manages to cross the river, that player is declared as the winner.
- If both cross, the one with the higher score is the winner.
- In the next round, the speed of moving obstacles increases for the winning player.
- Rounds go on indefinitely unless players decide to stop.

### Enemies/Obstacles

- There are two types of obstacles/enemies: moving and fixed.
- Fixed obstacles are on the land segments between the rivers and are generated randomly.
- Moving obstacles are in the rivers and move alternately from left to right and right to left.
- Colliding with any enemy/obstacle ends the round for the player.

### Scoring

- Scoring is based on obstacles crossed as well as time.
- Crossing moving obstacles adds 10 points.
- Crossing fixed obstacles adds 5 points.
- Every second of game time subtracts 2 points from the score.
- At a given time t, the score can be given as
            score = 10*(no. of moving obstacles crossed) + 5*(no. of fixed obstacles crossed) - 2*t

### Additional Information

- Player moves with different speeds on land and water.
- After every round, winner is displayed.
