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
        random.shuffle(self.cards)

    def draw_card(self):
        """Draws a card from the deck"""
        return self.cards.pop()


class Player:
    """A player of blackjack"""
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.value = 0
        self.aces = 0
        self.split = False

    def draw(self, deck):
        """Adds a card to the player's hand"""
        self.hand.append(deck.draw_card())
        return self

    def show_hand(self):
        """shows the player's hand"""
        for card in self.hand:
            print(card)
        print(f"Total Value: {self.get_hand_value()}")

    def get_hand_value(self):
        """Returns the value of the player's hand"""
        self.value = 0
        self.value2 = 0
        self.aces = 0
        if self.split:
            for card in self.hand[0]:
                self.value += card.value
                if card.rank == "Ace":
                    self.aces += 1
                self.value = self.adjust_for_ace(self.value, self.aces)
            self.aces = 0
            for card in self.hand[1]:
                self.value2 += card.value
                if card.rank == "Ace":
                    self.aces += 1
                self.value2 = self.adjust_for_ace(self.value2, self.aces)
        else:
            for card in self.hand:
                self.value += card.value
                if card.rank == "Ace":
                    self.aces += 1
        self.value = self.adjust_for_ace(self.value, self.aces)
        return self.value, self.value2

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
        self.player = Player("Player")
        self.dealer = Dealer("Dealer")

    def start(self):
        """starts the game"""
        self.deck.shuffle()
        self.player.draw(self.deck)
        self.dealer.draw(self.deck)
        self.player.draw(self.deck)
        self.dealer.draw(self.deck)
        self.show_hands()
        self.play()

    def show_hands(self):
        """shows the hands of the player and the dealer"""
        print("\nPlayer's Hand:")
        self.player.show_hand()
        print("\nDealer's Hand:")
        self.dealer.show_hand()

    def play(self):
        """plays the game"""
        while True:
            choice = input("Would you like to hit or stand? ")
            if choice == "hit":
                self.player.draw(self.deck)
                self.show_hands()
                if self.player.get_hand_value() > 21:
                    print("You busted!")
                    break
            elif choice == "stand":
                self.dealer.show = True
                while self.dealer.get_hand_value() < 17:
                    self.dealer.draw(self.deck)
                self.show_hands()
                if self.dealer.get_hand_value() > 21:
                    print("Dealer busted!")
                elif self.dealer.get_hand_value() > self.player.get_hand_value():
                    print("Dealer wins!")
                elif self.dealer.get_hand_value() < self.player.get_hand_value():
                    print("Player wins!")
                else:
                    print("It's a tie!")
                break
            else:
                print("Please enter a valid choice.")

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
game.replay()
