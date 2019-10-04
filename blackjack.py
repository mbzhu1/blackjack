import random
import time

# player and deck creation functions
def create_card(suit_number, number):
    # creates a card which is a list with a string and integer value
    assert number in range(1,14) # must be a number between 1 and 13 inclusive
    assert suit_number in range(1,5) # must be a number between 1 and 4 inclusive
    suit = ''
    if(suit_number == 1):
        suit = 'diamonds'
    if(suit_number == 2):
        suit = 'hearts'
    if(suit_number == 3):
        suit = 'clubs'
    if(suit_number == 4):
        suit = 'spades'
    return [suit, number]

def suit(card):
    # returns the string of the card's suit
    return card[0]

def number(card):
    # returns number of the card as an integer
    return card[1]

def create_deck():
    deck = []
    for i in range(1,5):
        for j in range(1,14):
            deck.append(create_card(i, j))
    random.shuffle(deck)
    return deck

def deal_card(player):
    new_card = deck.pop()
    player.append(new_card)
    display_card(new_card)

def set_number_of_players():
    temp_str = input("How many players are playing?:")
    while not temp_str.isdigit():
        print("\nThat's not a number!")
        temp_str = input("\nHow many players are playing?:")
    return int(temp_str)

# visual effects functions
def display_card(card):
    # prints out the description of a card
    print(str(number(card)), "of", suit(card))

def display_hand(player):
    for card in player:
        display_card(card)

def sum_hand(player): 
    total = [0]
    for card in player:
        current = number(card)
        if(current == 1):
            return special_sum_hand(player)
        if current > 10:
            current = 10
        total[0] += current
    return total

def sum_hand_without_ace(player): 
    total = 0
    for card in player:
        current = number(card)
        if current > 10:
            current = 10
        total += current
    return total

def special_sum_hand(player):
    hand = []
    result = []
    for card in player:
        hand.append(number(card))
    result.append(sum_hand_without_ace(player))
    for numbers in hand:
        if(numbers == 1):
            temp = result.pop()
            result.append(temp)
            result.append(temp+10)
    return optimal_sort(result)

def optimal_sort(list_of_possible_scores):
    greater_than_21 = []
    less_than_21 = []
    for possible_score in list_of_possible_scores:
        if(possible_score > 21):
            greater_than_21.append(possible_score)
        else:
            less_than_21.append(possible_score)
    less_than_21.sort(reverse=True)
    return less_than_21 + greater_than_21

def convert_to_str(new_list):
    result = str(new_list[0])
    for x in new_list[1:]:
        result = result + " or " + str(x)
    return result

# check functions
def has_blackjack(player):
    if(sum_hand(player)[0] == 21):
        return True
    return False

def is_busted(player):
    if(sum_hand(player)[0] > 21):
        return True
    return False

def dealer_has_natural_blackjack():
    if number(dealer[1]) in [10, 11, 12, 13] and has_blackjack(dealer):
        print("\nDealer has blackjack!")
        return True
    return False

# variables
horizontal_line = "_________________________________"
players = [] # contains list of lists that contain each players cards
dealer = [] # contains dealer's cards
scores = [] # contains the resulting scores for each player
deck = create_deck()
number_of_players = set_number_of_players()

# set up game
def game_setup():
    for i in range(number_of_players):  #create a list for each player
        players.append([])
        print("\nPlayer", str(i + 1) + "'s Cards")
        deal_card(players[i])
        deal_card(players[i])
    print("\nDealer's Cards:")
    new_card = deck.pop() 
    dealer.append(new_card)
    print("-- of ------") #keep dealer's first card hidden
    deal_card(dealer)

def play_turn(player_index):
    continue_turn = True
    print(horizontal_line)
    while(continue_turn):
        print("\nPlayer", str(player_index + 1) + "'s Turn")
        display_hand(players[player_index])
        print("Score:", convert_to_str(sum_hand(players[player_index])))
        hit = input("\nWould you like to hit? [y/n]")
        if hit == 'y':
            deal_card(players[player_index])
            if(is_busted(players[player_index])):
                scores.append(sum_hand(players[player_index])[0])
                print("\nYou have busted!")
                continue_turn = False
        else:
            print("\nPlayer", str(player_index + 1) + "'s Turn Ended")
            continue_turn = False

def dealer_turn():
    print(horizontal_line)
    print("\nDealer's Turn Starts")
    time.sleep(1)
    display_hand(dealer)
    print("Score:", convert_to_str(sum_hand(dealer)))
    while(sum_hand(dealer)[0] <= 16):
        print("\nDealer drew a ")
        deal_card(dealer)
        time.sleep(0.75)
    if is_busted(dealer):
        print("\nThe Dealer busted!")

def endgame(): 
    print(horizontal_line)
    dealer_score = sum_hand(dealer)
    print("\nDealer's Score:", dealer_score[0])
    for i in range(number_of_players):
        player_score = sum_hand(players[i])
        print("\nPlayer", str(i + 1) + "'s Score:", player_score[0])
        if is_busted(players[i]):
            print("Player", str(i + 1), "busted and lost!")
        elif player_score[0] > dealer_score[0] or is_busted(dealer):
            print("Player", str(i + 1), "beat the dealer!")
        elif player_score[0] == dealer_score[0]:
            print("Player", str(i + 1), "tied with the dealer!")
        else:
            print("Player", str(i + 1), "lost to the dealer!")
    print("\n\n")
    
def play():
    game_setup()
    for i in range(number_of_players):
        play_turn(i)
    dealer_turn()
    endgame()

play()