import random


class Card:
    """A playing card"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        """Returns the value of the card"""
        if self.rank == "Ace":
            return 11
        elif self.rank in ["Jack", "Queen", "King"]:
            return 10
        else:
            return int(self.rank)


class Deck:
    """A deck of playing cards"""
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Builds a deck of 52 cards"""
        for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
            for rank in ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffles the deck"""
        return random.shuffle(self.cards)

    def draw_card(self):
        """Draws a card from the deck"""
        return self.cards.pop()


class Player:
    """A player of blackjack"""
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.split = 0
        self.double = False
        self.bust = False
        self.stand = False

    def draw(self, deck):
        """Adds a card to the player's hand"""
        self.hand.append(deck.draw_card())
        return self

    def show_hand(self):
        """shows the player's hand"""
        for card in self.hand:
            print(card)
        print(f"Total Value: {self.get_hand_value()}")

    def can_double(self):
        if self.get_hand_value(aces=False) in [9, 10, 11]:
            return True
        elif self.get_hand_value() in [9, 10, 11]:
            return True

    def get_hand_value(self, aces=True):
        """Returns the value of the player's hand"""
        value = 0
        aces = 0
        for card in self.hand:
            value += card.value
            if card.rank == "Ace":
                aces += 1
        if aces:
            return self.adjust_for_ace(value, aces)
        else:
            return value

    def adjust_for_ace(self, value, aces):
        """Adjusts the value of a player's hand for aces"""
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def discard(self):
        """Discards the player's hand"""
        self.hand = []
        return self


class Dealer(Player):
    """A dealer of blackjack"""
    def __init__(self, name):
        super().__init__(name)
        self.show = False

    def show_hand(self):
        """Shows the dealers hand"""
        if not self.show:
            print(self.hand[0])
            print("Hidden")
        else:
            for card in self.hand:
                print(card)
            print(f"Total Value: {self.get_hand_value()}")


class Game:
    """a game of blackjack"""
    def __init__(self):
        self.deck = Deck()
        self.dealer = Dealer("Dealer")
        self.lobby = []
        self.pile = []

    def start(self):
        """starts the game"""
        self.lobby = [Player(input("What is your name? ")) for i in range(2)]
        self.deck.shuffle()
        [player.draw(self.deck) for player in self.lobby]
        self.dealer.draw(self.deck)
        [player.draw(self.deck) for player in self.lobby]
        self.dealer.draw(self.deck)
        self.play()

    def show_hands(self, player):
        """shows the hands of the player and the dealer"""
        print("\nDealer's Hand:")
        self.dealer.show_hand()
        print(f"\n{player.name}'s Hand:")
        player.show_hand()

    def play(self):
        """plays the game"""
        while all(not player.bust and not player.stand for player in self.lobby):
            for player in (player for player in self.lobby if not player.bust and not player.stand and not player.double):
                print(self.show_hands(player))
                if player.get_hand_value in [9, 10, 11] and player.double is False:
                    choice = input("Would you like to, Hit ( H ), Stand ( S ) or Double Down ( D )?")
                    if choice.lower() == "d":
                        player.draw(self.deck)
                        player.double = True
                elif player.hand[0] == player.hand[1] and player.split == 0:
                    choice = input("Would you like to, Hit ( H ), Stand ( S ) or Split ( P )?")
                    if choice.lower() == "p":
                        # seperate cards into new players (p1, p2)
                        # set p1 to split = 1
                        # set p2 to split = 2
                        player.split = 1
                else:
                    choice = input("Would you like to, Hit ( H ) or Stand ( S )?")
                if choice.lower() == "h":
                    print("You chose to hit.")
                    player.draw(self.deck)
                    print(f"You drew: {str(player.hand[-1])}\n")
                    if player.get_hand_value() > 21:
                        player.bust = True
                        print("You Busted!\n")
                if choice.lower() == "s":
                    print("You chose to stand.\n")
                    player.stand = True
        self.dealer.show = True
        print("\nDealers Hand")
        print(self.dealer.show_hand())
        if self.dealer.get_hand_value(aces=False) < 17:
            self.dealer.draw(self.deck)
            print(f"Dealer draws a {str(self.dealer.hand[-1])}")
            print(f"Dealer's hand is now {self.dealer.get_hand_value(aces=False)}")
        while self.dealer.get_hand_value() < 17:
            self.dealer.draw(self.deck)
            print(f"Dealer draws a {str(self.dealer.hand[-1])}\n")
            print("Dealers Hand")
            print(self.dealer.show_hand())
        if self.dealer.get_hand_value() > 21:
            print("Dealers Hand")
            print(self.dealer.show_hand())
            print("Dealer Busted!\n")
        else:
            print("Dealer Stands.\n")
            print("Dealers Hand")
            print(self.dealer.show_hand())
        for player in self.lobby:
            if player.bust:
                print(f"{player.name} busted!\n")
            elif player.get_hand_value() > self.dealer.get_hand_value():
                print(f"{player.name} wins!\n")
            else:
                print(f"{player.name} loses!\n")

    def replay(self):
        """asks the player if they want to play again"""
        choice = input("Would you like to play again? ")
        if choice == "yes":
            self.player.discard()
            self.dealer.discard()
            self.start()
        else:
            print("Thanks for playing!")


game = Game()
game.start()
