"""TDT4113_Assignment_2: Program for playing rock, paper, scissor"""
__author__ = 'Marianne Hernholm'
import random
from statistics import mode
from matplotlib import pyplot


class Player:
    """Base class for players"""

    def __init__(self):
        """Constructor for parent-class Player"""

    def select_action(self):
        """Selects which action to perform given playing strategy,
           given further functionality in the subclasses"""
        return

    def receive_result(self, singlegame):
        """Find out what opponent played and who won,
           report if necessary (most common and historian need this)"""
        return

    def enter_name(self):
        """Specifies name of class and reports it to the interface,
           give name to player for nice output"""
        return


class RandomPlayer(Player):
    """Subclass of Player: This player chooses its actions randomly"""
    def __init__(self):
        # Inherits all properties and modules of the Player parent-class
        Player.__init__(self)

    # This player selects its actions randomly from the options (Rock:0,Paper:1,Scissor2)
    def select_action(self):
        action = random.randint(0, 2)
        return action

    def enter_name(self):
        return 'Random Player '


class SequentialPlayer(Player):
    """Subclass of Player: This player chooses its actions sequentially"""
    def __init__(self):
        Player.__init__(self)
        self.prev_action = None

    def select_action(self):
        if self.prev_action == 0:
            action = 1  # Scissor
        elif self.prev_action == 1:
            action = 2  # Paper
        elif self.prev_action == 2:
            action = 0  # Rock
        else:
            action = random.randint(0,2)
        # Set prev_action = action so it doesnt always choose 1, but follows the sequence
        self.prev_action = action
        return action

    def enter_name(self):
        return 'Sequential Player '


class MostCommonPlayer(Player):
    """Subclass of Player: This player chooses action based on opponents most common choice"""
    def __init__(self):
        Player.__init__(self)
        # Count what opponent is doing, a counter for each possible move
        self.opponent_actions = [0, 0, 0]   # op_ac = [rock, paper scissor]

    def select_action(self):
        """Counts opponents actions over time,
        assumes opponent will play most played action again,
        and thus plays to counter this"""

        # If opponent has played no games, or chosen actions same amount of times, we pick randomly
        if self.opponent_actions[0] == self.opponent_actions[1] == self.opponent_actions[2]:
            action = random.randint(0, 2)
            return action

        # Strategy: Assume opponent will repeat its most played action and play to counter this
        # Rock most played -> play paper
        elif self.opponent_actions[0] > self.opponent_actions[1] and \
             self.opponent_actions[0] > self.opponent_actions[2]:
            action = 2  # Paper
            return action

        # Scissors most played -> play rock
        elif self.opponent_actions[1] > self.opponent_actions[0] and \
             self.opponent_actions[1] > self.opponent_actions[2]:
            action = 0  # Rock
            return action

        # Paper most played -> play scissor
        else:
            action = 1  # Scissor
            return action

    # We want to remember opponents action so the player can learn to play better against them
    def receive_result(self, singlegame):
        # If main player is player1, increment player2's actions to opponents_actions
        if self == singlegame.player1:
            self.opponent_actions[singlegame.action2] += 1
        else:
            # If main player is player2, increment player1's actions to opponents_actions
            self.opponent_actions[singlegame.action1] += 1

    def enter_name(self):
        return 'Most Common Player '


class Historian(Player):
    """Subclass of Player: This player looks for patterns in opponents strategy"""
    def __init__(self):
        Player.__init__(self)
        # Remember tells us which sub-string (1, 2 or 3) to look for in memory
        self.remember = 3 # random.randint(1,3)
        # Need to keep track of ALL plays that have been made to analyze the
        # opponents strategy
        self.opponent_history = []  # List of opponents actions

    def select_action(self):
        # Play randomly if history-data is insufficient (too few games have been played)

        # Get sequence from end of opponent_history
        pattern = self.opponent_history[-self.remember:]
        print('Sequence: ',pattern)

        if self.remember >= len(self.opponent_history):
            action = random.randint(0, 2)
            return action

        # While loop for determining action, given a value for remember
        i = 0                       # Iterator
        relevant_actions = []       # List for the relevant subseq.
        # [-self.remember] is the relevant subsequence, we don not want to iterate through it again
        while i != (len(self.opponent_history) - self.remember):
            # print(self.opponent_history[-self.remember:])
            # Slicer op_history with given remember
            # Slice i python: list[start_slice:end_slice+1],
            # if not given end_arg it automatically slices whole list
            # Look for subseq. matching last actions opponent played
            if (self.opponent_history[i: i+self.remember]) == (self.opponent_history[-self.remember:]):
                relevant_actions.append(self.opponent_history[i + self.remember])

            i += 1  # Increment i to traverse opponents history

            # If the relevant subsequence and its successor-action
            # was found at least once in opponent_history
            # -> Use mode to get the successor-action that was most commonly played
            # --> Then play to counter this
        if len(relevant_actions) != 0:
            print('rel actions:', relevant_actions)

            opponent_action = mode(relevant_actions)  # Mode gets most frequently occurring post-subsequence action
            print('Opponent action: ', opponent_action)
            action = (opponent_action + 2) % 3
            print(action) # Gives action we want to play to counter opponent action
            return action
            # If no relevant subsequence can be found, play randomly
        else:
            action = random.randint(0, 2)
            return action

    # We want to remember opponents action so the player can learn to play better against them
    def receive_result(self, singlegame):
        # If main player is player1, append player2's action to opponents history
        if self == singlegame.player1:
            self.opponent_history.append(singlegame.action2)
            print('opponent history: ', self.opponent_history)
        # If main player is player2, append player1's action to opponents history
        else:
            self.opponent_history.append(singlegame.action1)

    def enter_name(self):
        return 'Historian Player '


class SingleGame:
    """Class to conduct and represent a single game,
    asks two players for their choices, finds winner, writes it nicely to screen"""

    def __init__(self, player1, player2):
        # The two players
        self.player1 = player1
        self.player2 = player2

        # Variables for the chosen action of each player
        self.action1 = None
        self.action2 = None

        # Variables for keeping score for each player
        self.winner = None

    def perform_game(self):
        """Report on the players' performance and outcome of the game
        winner gets 1 point, loser gets 0 points"""

        # These prints checks player was assigned as right type
        print('Player1 is a: ', type(self.player1))
        print('Player2 is a: ', type(self.player2))

        # Select actions for each player
        self.action1 = self.player1.select_action()
        self.action2 = self.player2.select_action()

        # Receives result for each players
        self.player1 = self.player1.receive_result(self)
        self.player2 = self.player2.receive_result(self)

        # Implementing rules for determining the champion
        # Rules are 0 beats 1, 1 beats 2, 2 beats 0
        if ((self.action1 == 0) and (self.action2 == 1)) or ((self.action1 == 1) and (self.action2 == 2)) or ((self.action1 == 2) and (self.action2 == 0)):
            self.winner = 1     # winner == 1 means player 1 won

        elif ((self.action2 == 0) and (self.action1 == 1)) or ((self.action2 == 1) and (self.action1 == 2)) or ((self.action2 == 2) and (self.action1 == 0)):
            self.winner = 2     # winner == 2 means player2 won

        else:
            self.winner = 0     # winner == 0 means tie

        print(self.show_result())

        return self.winner

    def show_result(self):
        """Textual reporting of single game; what was chosen and who won"""
        result_text = 'Player1 :played action: ' + str(self.action1) + '\n' + \
                      'Player 2 :played action: ' + str(self.action2) + '\n' + \
                      'The winner was: ' + str(self.winner) + '\n'
        return result_text


class Tournament:
    """Class for testing our players, creates players, runs individual games,
    reports back to players, keeps track of who wins, reports in the end"""
    player_alternatives = {1: RandomPlayer(), 2: SequentialPlayer(), 3: MostCommonPlayer(), 4: Historian()}

    def __init__(self, player1, player2, number_of_games):
        self.player1 = self.player_alternatives[player1]
        self.player2 = self.player_alternatives[player2]
        # Getting names of the player-types for nice output
        self.player1_name = self.player1.enter_name()
        self.player2_name = self.player2.enter_name()
        self.number_of_games = number_of_games

        # Number of ties scores[0], # times player1 has won scores[1], # times player 2 has won scores[2]
        self.scores = [0, 0, 0]
        self.winner = None

    def arrange_singlegame(self):
        """System asks players for actions, checks who wins, reports choices and results"""
        single_game = SingleGame(self.player1, self.player2)
        winner = single_game.perform_game()

        # Score keeping - (+1 for win, 0 for loss)
        self.scores[winner] += 1

    def arrange_tournament(self):
        """Complete number_of_games singlegames"""
        # Plots for the learning-graph
        game_count = 0
        winning_statistics1 = []
        winning_statistics2 = []
        # Arrange # games given by user
        while self.number_of_games > 0:
            self.arrange_singlegame()

            # Problem fix: noticed that graph crashed when first game was a tie, so just append 0 in that case
            try:
                winning_statistics1.append(self.scores[1]/(self.scores[1] + self.scores[2]))
                winning_statistics2.append(self.scores[2]/(self.scores[1]) + self.scores[2])

            except:
                winning_statistics1.append(0)  # The first game was a tie
                winning_statistics2.append(0)

            game_count += 1
            self.number_of_games -= 1

        # Plot of development graph for player1 using pyplot-tools
        pyplot.plot(winning_statistics1)
        pyplot.title('Tournament statistics')
        pyplot.xlabel('Number of games played')
        pyplot.ylabel('Win percentage development')
        # pyplot.ylim(0, 1)
        pyplot.grid()
        pyplot.show()

        print(self.tournament_result())

    def tournament_result(self):
        """Acquire results from the tournament"""
        # PLayer1 is the winner
        if self.scores[1] > self.scores[2]:
            self.winner = self.player1
            result_text = 'Winner of the tournament is: ' + 'player1: ' + self.player1_name

        # Player2 is the winner
        elif self.scores[2] > self.scores[1]:
            self.winner = self.player2
            result_text = 'Winner of the tournament is: ' + 'player2: ' + self.player2_name

        # The game tied
        else:
            self.winner = None  # tie
            result_text = 'The tournament concluded in a tie!'

        return result_text


def main():
    """Standard main function to run program"""

    # Choose player-type for first player
    player_choice = int(input('What kind of player do you want to play?: \n Press 1: RandomPlayer \n Press 2: '
                              'SequentialPlayer \n Press3: MostCommonPlayer \n Press4: HistorianPlayer'))

    # Choose player-type for opponent player
    player_opponent = int(input('What kind of player do you want to play against?: '))

    # Decide number of games to be played
    num_games = int(input('Choose amount of games to play: '))

    # Play a game
    game = Tournament(player_choice, player_opponent, num_games)
    game.arrange_tournament()

    return ''


RUN_MAIN = main()
