# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 12:35:13 2021

@author: Michael
Game of Pigs: like a dice rolling game with points and chance to lose all 
points and turn or lose the game altogether. 
    - game has 2 players, each take turn to pass or roll
    - game ends when a player reached target score or one is eliminated
v2. - Let players choose number of players playing at the same time 
"""
import random

# -1 scores means player eliminated
class GameOfPigs(object):
    def __init__(self, num_players: int = 2):
        self.players = []
        self.num_players = num_players
        self.scores = []    
        self.current_turn = 0
        # could be list of dictionary for name of players as key
        self.winning_score = None
        self.scoring_table = {0 : 0,
                              1 : 5,
                              2 : 5,
                              3 : 10,
                              4 : 15}
        self.scoring_names = {
            0 : 'Sider', 
            1 : 'Razorback',
            2 : 'Trotter',
            3 : 'Snouter',
            4 : 'Leaning Jowler'
        }
        
    def roll(self) -> (int, int, int):
        return (random.randint(0, 4), random.randint(0, 4), random.randint(0, 99))
        # outcome - (pig 1 position, pig 2 position, 
        #               touching (1%) or piggyback(5%))
        
    def roll_result(self, outcome):
        print(f"You rolled {self.scoring_names[outcome[0]]}",
              f"and {self.scoring_names[outcome[1]]}")

    def score(self, outcome: (int, int), current_score: int) -> int:
        if outcome[2] == 0: # piggyback 1%
            self.scores[self.current_turn] = -1
            self.num_players -= 1
            self.current_turn = (self.current_turn + 1) % len(self.players)
            print("Uh oh, Piggyback! You've been eliminated :(")
        elif outcome[2] < 20: # oinker 20%
            self.scores[self.current_turn] = 0
            self.current_turn = (self.current_turn + 1) % len(self.players)
            print("Oinker! You've lost all your points and your turn!")
        else:
            if outcome[0] == outcome[1]:
                if outcome[0] == 0:
                    self.scores[self.current_turn] += 1
                    print("Double Sider! You've earned 1 point")
                elif outcome[0] == 1:
                    self.scores[self.current_turn] += 20
                    print("Double Razorback! You've earned 20 points")
                elif outcome[0] == 2:
                    self.scores[self.current_turn] += 20
                    print("Double Trotter! You've earned 20 points")
                elif outcome[0] == 3:
                    self.scores[self.current_turn] += 40
                    print("Double Snouter! You've earned 40 points")
                elif outcome[0] == 4:
                    self.scores[self.current_turn] += 60
                    print("Double Leaning Jowler! You've earned 60 points")
            else:   # add up scores based on different positions
                score = self.scoring_table[outcome[0]]
                score += self.scoring_table[outcome[1]]
                self.scores[self.current_turn] += score
                print(f"Mixed bag, You scored {score} points")
        
    def play_game(self):
        print("Game starts")
        num_players = int(input("How many are playing?"))
        while num_players < 2:
            print("Must have more than 1 player to play this game")
            num_players = int(input("How many are playing?"))
        for i in range(num_players):
            name = input(f'Enter player {i + 1} name: ')
            self.players.append(name)
            self.scores.append(0)
        self.winning_score = int(input("Enter the target score: "))
        
        # self.winning_score = 100
        # self.players.append('Mike')
        # self.scores.append(0)
        # self.players.append('Joe')
        # self.scores.append(0)
            
        while (self.scores[self.current_turn] < self.winning_score 
               and self.num_players > 1):
            print('Current turn', self.players[self.current_turn])
            btn = input("Do you want to roll(r) or pass(p)? ").lower()
            # btn = 'r'
            if btn == 'r' or btn == 'roll':
                outcome = self.roll()
                print('outcome: ', outcome)
                self.roll_result(outcome)
                self.score(outcome, self.scores[self.current_turn])
            elif btn == 'p' or btn == 'pass':
                self.current_turn = (self.current_turn + 1) % len(self.players)
            else:
                print('Invalid input')
                continue
            # move on to the next active player
            while self.scores[self.current_turn] == -1:
                self.current_turn = (self.current_turn + 1) % len(self.players)

            for i in range(len(self.players)):
                print(self.players[i], 'has', self.scores[i], 'points')
            
            # input(' next round ')
        print('Game over and the winner is', self.players[self.current_turn],
              'with', self.scores[self.current_turn], 'points')
                
game = GameOfPigs()
game.play_game()

