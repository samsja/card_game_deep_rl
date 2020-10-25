from game_class.game import Game
from game_class.card import Color

bet_allowed = [80 + 10*i for i in range(9)] + [0,250,270,500,float('inf')]

class Bet:

    def __init__(self,bet,color,player):
        if not(bet in bet_allowed):
            raise ValueError(f"bet {bet} should be in {bet_allowed}")

        if (not(isinstance(player,int)) or not(0<=player<Game.nb_player)):
            raise TypeError(f"player should be an integer between 0 and {Game.nb_player} not {type(player)}")

        self.value = bet
        self.color = color
        self.player = player

    def __gt__(self, other):
        return self.value>other.value
    def __ge__(self, other):
        return self.value>=other.value
    def __lt__(self, other):
        return self.value<other.value
    def __le__(self, other):
        return self.value<=other.value

    def __eq__(self, other):
        return (self.color==other.color) and (self.value==other.value)
    def __ne__(self, other):
        return not(self.__eq__(other))

class Coinche:

    nb_player = 4

    def __init__(self,rules):

        self.rules = rules
        self.next_player = 0
        self.bets = []
        self.over = False


    def _create_game(self):
        print("_create_game")
        self.over = True

    def _is_coinchable(self):
        is_coinchable = False

        for bet in self.bets:
            if bet.value !=0:
                is_coinchable = True
        return is_coinchable

    def _add_bet(self,bet):
        self.bets.append(bet)
        self.next_player = (self.next_player +1)%self.nb_player


        if len(self.bets)>=4:
            all_passed = True
            for last_bet in self.bets[-4:-2]: #last three players
                all_passed = all_passed and  (last_bet.value == 0)
        else:
            all_passed = False

        if (bet.value == float('inf')) or all_passed:
            self._create_game()



    def play_a_bet(self,bet_value,color,player):
        """Validate if a bet could be play by the player
        Keyword arguments:
        bet_value -- an int
        color -- a Color enum
        player -- an int for the player index
        """

        if self.over:
            return False

        if player != self.next_player:
            return False

        if bet_value == "coinche":
            bet_value = float("inf")

        if not(bet_value in bet_allowed):
            return False

        bet = Bet(bet_value,color,player)

        if bet.value == float("inf"):
             if not(self._is_coinchable()):
                 return False


        if len(self.bets) == 0:
            self._add_bet(bet)
            return True
        else:
            if bet.value != 0 and bet <= self.bets[-1]:
                return False
            else:
                self._add_bet(bet)
                return True
