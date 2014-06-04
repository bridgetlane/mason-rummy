# Written by Bridget Lane

# Run in Python 3.2.0

import random
import os

class Card(object):
    def __init__(self, card):
        self.val = card[0]
        self.suit = card[1]
    def __str__(self):
        string = str(self.val) + str(self.suit)
        return string
    def card_point_value(self):
        if self.val == "T" or self.val == "J" or self.val == "Q" or \
        self.val == "K" or self.val == "P":
            return "10"
        elif self.val == "A":
            return "15"
        else:
            return self.val
    def test_meld(self, cards):
        teststart = cards[0].val
        vals = []
        for i in cards:
            if i.val == teststart:
                vals.append("yes")
            else:
                vals.append("no")
        if "no" in vals:
            return False
        suits = []
        for i in cards:
            if i.suit not in suits:
                suits.append(i.suit)
            else:
                return False
        return True
    def test_run(self, cards):
        testsuit = cards[0].suit
        suits = []
        for i in cards:
            if i.suit == testsuit:
                suits.append("yes")
            else:
                suits.append("no")
        if "no" in suits:
            return False
        vals = []
        for i in cards:
            if i.val == "T":
                vals.append(10)
            elif i.val == "J":
                vals.append(11)
            elif i.val == "Q":
                vals.append(12)
            elif i.val == "K":
                vals.append(13)
            elif i.val == "A":
                vals.append(14)
            else:
                vals.append(int(i.val))
        vals.sort()
        testpos = [vals[0]]
        for i in range(len(vals)-1):
            testpos.append(testpos[i]+1)
        testneg = [vals[0]]
        for i in range(len(vals)-1):
            testneg.append(testneg[i]-1)
        if vals != testpos and vals != testneg:
            return False
        else:
            return True
    def extends_run(self, card, ontable):
        self.card = card
        self.ontable = ontable
        vals = []
        for i in self.ontable:
            c1 = self.card.test_run(i)
            if c1 == False:
                vals.append(False)
            else:
                test = i[:]
                test.append(self.card)
                c2 = self.card.test_run(test)
                if c2 == True:
                    vals.append(True)
                else:
                    vals.append(False)
        return vals
    def extends_meld(self, card, ontable):
        self.card = card
        self.ontable = ontable
        vals = []
        for i in self.ontable:
            c1 = self.card.test_meld(i)
            if c1 == False:
                vals.append(False)
            else:
                test = i[:]
                test.append(self.card)
                c2 = self.card.test_meld(test)
                if c2 == True:
                    vals.append(True)
                else:
                    vals.append(False)
        return vals
        
class Hand(object):
    def __init__(self, cards):
        self.hand = cards
    def __str__(self):
        if self.hand == []:
            string = "No cards currently in your hand."
            return string
        else:
            string = "The cards currently in your hand are "
            for i in self.hand:
                string += str(i)
                string += ", "
            string = string[:-2]
            return string
    def hand_point_value(self):
        value = 0
        for i in self.hand:
            val = int(i.card_point_value())
            value += val
        return value

def clear_screen():
    if os.name == "posix": 
        clear_cmd = "clear"
    elif os.name == "nt":
        clear_cmd = "cls"
    else:
        raise Exception("\n\n\n*** Unsupported System ***\n\
Application Terminating !!!\n\n\n")
    os.system(clear_cmd)
    
class Player(object):
    def __init__(self, hand, name):
        self.hand = hand
        self.score = hand.hand_point_value()
        self.name = name
    def __str__(self):
        string = "Player Name: " + str(self.name) + "\nPlayer Score: " + \
        str(self.score) + "\nPlayer Hand: " + str(self.hand)
        return string
    def take_turn(self, players, discarded, deck, laiddown):
        self.players = players
        self.discardpile = discarded
        self.deck = deck
        self.down = laiddown
        print("Discard Pile: " + str(self.discardpile[0]) + "\n")
        print(self.hand)
        print()
        marker = (self.players.index(self.name))
        print("The cards you have laid down are: ")
        for i in self.down[marker]:
            for j in i:
                print(str(j), end=" ")
            print()
        print()
        print("Menu D: Which Card to Draw\n1. Draw from stock pile\
        \n2.  Draw from discard pile\n")
        draw_choice = input("Please select 1 or 2: ")
        while draw_choice != "1" and draw_choice != "2":
            print("Please select a valid menu option.")
            draw_choice = input("Please select 1 or 2: ")
        if draw_choice == "1":
            if self.deck == []:
                temp = self.discardpile
                self.discardpile = temp[0]
                temp.remove(self.discardpile)
                self.deck = temp[::-1]
            self.hand.hand.append(self.deck[0])
            self.deck = self.deck[1:]
        if draw_choice == "2":
            self.hand.hand.append(self.discardpile[0])
            self.discardpile = self.discardpile[1:]
        print()
        menuEchoice = True
        while menuEchoice == True:
            print("\nMenu E: Next Action\n1. Play down cards\n2. Discard")
            userEinput = input("Please select a choice. ")
            print()
            if userEinput != "1" and userEinput != "2":
                print("Please select a valid menu option.")
                menuEchoice = True
            if userEinput == "1":
                print("Menu F: Select Cards")
                hand_num = []
                for i in range(len(self.hand.hand)):
                    print(str(i+1)+". "+self.hand.hand[i].val, end=" ")
                    hand_num.append(str(i+1))
                    if self.hand.hand[i].suit == "C":
                        print("Clubs")
                    elif self.hand.hand[i].suit == "D":
                        print("Diamonds")
                    elif self.hand.hand[i].suit == "H":
                        print("Hearts")
                    elif self.hand.hand[i].suit == "S":
                        print("Spades")
                    elif self.hand.hand[i].suit == "P":
                        print("Patriots")
                choice = "True"
                while choice == "True":
                    card_choices = eval(input("What cards would you \
like to play? "))
                    choice = "False"
                    if type(card_choices) == int:
                        card_choices = "(" + str(card_choices) + ",)"
                        card_choices = eval(card_choices)
                    for i in range(len(card_choices)):
                        if str(card_choices[i]) not in hand_num:
                            print("Your selection(s) are not valid. Please \
choose again.")
                            choice = "True"
                            break
                        else:
                            choice = "False"
                cards_to_play = []
                for i in card_choices:
                    cards_to_play.append(self.hand.hand[i-1])
                if len(cards_to_play) >= 3:
                    card = cards_to_play[0]
                    valid_meld = card.test_meld(cards_to_play)
                    valid_run = card.test_run(cards_to_play)
                    if valid_meld == True or valid_run == True:
                        marker = (self.players.index(self.name))
                        self.down[marker].append(cards_to_play)
                        for i in cards_to_play:
                            self.hand.hand.remove(i)
                marker = (self.players.index(self.name))
                if len(cards_to_play) <= 2:
                    valid = []
                    not_valid = []
                    for i in cards_to_play:
                        for j in range(len(self.down[marker])):
                            run = i.extends_run(i, [self.down[marker][j]])
                            if True in run:
                                self.down[marker][j].append(i)
                                valid.append(i)
                                for i in cards_to_play:
                                    self.hand.hand.remove(i)
                            else:
                                meld = i.extends_meld(i, [self.down[marker][j]])
                                if True in meld:
                                    self.down[marker][j].append(i)
                                    valid.append(i)
                                    for i in cards_to_play:
                                        self.hand.hand.remove(i)
                                else:
                                    not_valid.append(i)
                    print("\nThe cards you have down are:")
                    str3 = ""
                    for i in self.down:
                        for j in i:
                            str2 = ""
                            for g in j:
                                str2 += (str(g) + " ")
                            print(str2)
                            str3 += str2
                    for i in cards_to_play:
                        if str(i) not in str3:
                            print("\n" + str(i) + " could not be laid down.\n")
                    for i in valid:
                        self.hand.hand.remove(i)
                    print(self.hand)
                    menuEchoice = True
            if userEinput == "2":
                menuEchoice = False
                print("Please select a card to discard.")
                card_select = []
                for i in range(len(self.hand.hand)):
                    print(str(i+1)+". "+self.hand.hand[i].val, end=" ")
                    card_select.append(str(i+1))
                    if self.hand.hand[i].suit == "C":
                        print("Clubs")
                    elif self.hand.hand[i].suit == "D":
                        print("Diamonds")
                    elif self.hand.hand[i].suit == "H":
                        print("Hearts")
                    elif self.hand.hand[i].suit == "S":
                        print("Spades")
                    elif self.hand.hand[i].suit == "P":
                        print("Patriots")
                choice = "True"
                while choice == "True":
                    try:
                        to_discard = input("What card would you like to \
discard? ")
                        choice = "False"
                    except:
                        print("Your selection is not valid.  Please enter \
the integer of one card.")
                        choice = "True"
                    if to_discard not in card_select:
                        print("Your selection is not valid.  Please enter \
the integer of one card.")
                        choice = "True"
                self.discardpile.append(self.hand.hand[int(to_discard) - 1])
                self.hand.hand.remove(self.hand.hand[int(to_discard) - 1])
        clear_screen()
        return [self.players, self.discardpile, self.deck, self.down]
    
class ScoreTable(object):
    def __init__(self, names, scores, win, lost):
        self.names = names
        self.scores = scores
        self.win = win
        self.lost = lost
    def __str__(self):
        if self.names == []:
            return "None\n"
        else:
            longest_name = max(self.names, key=len)
            string = ("{:<{x}}".format("Name", x=len(longest_name)) + "  " + \
            "Score  Games Won  Games Lost\n")
            for i in range(len(self.names)):
                string += ("{:<{x}}".format(self.names[i], \
                x=len(longest_name)) + "  " + "{:<5}".format(self.scores[i]) \
                + "  " + "{:<9}".format(self.win[i]) + "  " + \
                "{:<10}".format(self.lost[i]) + "\n")
            return string
    def read_scores(self):
        try:
            scores = open("scores.csv", "rU")
            scores.readline()
            info = scores.readlines()
            scores.close()
            no_newline = []
            for i in info:
                no_newline.append(i[:-1])
            info = no_newline
            no_str_quotes = []
            for i in info:
                temp = i.replace('\"', "")
                temp2 = temp.replace("\'", "")
                no_str_quotes.append(temp2)
            info = no_str_quotes
            names = self.names
            wins = self.win
            losses = self.lost
            best = self.scores
            for i in info:
                n, w, l, b = i.split(",")
                if n in names:
                    mark = names.index(n)
                    if int(b) < int(best[mark]):
                        best[mark] = b
                    win_count = int(w) + int(wins[mark])
                    wins[mark] = str(win_count)
                    loss_count = int(l) + int(losses[mark])
                    losses[mark] = str(loss_count)
                else:
                    names.append(n)
                    wins.append(w)
                    losses.append(l)
                    best.append(b)
            biglist = [names, wins, losses, best]
            self.names = names
            self.scores = best
            self.win = wins
            self.lost = losses
            return biglist
        except:
            scores = open("scores.csv", "w")
            scores.write('"name","games won","games lost","best score"\n')
            scores.close()
            return None
    def save_scores(self):
        scores = open("scores.csv", "w")
        scores.write('"name","games won","games lost","best score"\n')
        for i in range(len(self.names)):
            scores.write('"' + str(self.names[i]) + '"' + "," + '"' + \
            str(self.win[i]) + '"' + "," + '"' + str(self.lost[i]) + '"' \
            + "," + '"' + str(self.scores[i]) + '"\n')

def all_scores():
    game = ScoreTable([], [], [], [])
    game.read_scores()
    return game

def view_scores():
    game = all_scores()
    print(game)

def twopgame(playernames):
    card_names = ["2C","3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", \
    "JC", "QC", "KC", "AC", "2D","3D", "4D", "5D", "6D", "7D", "8D", "9D", \
    "TD", "JD", "QD", "KD", "AD", "2H","3H", "4H", "5H", "6H", "7H", "8H", \
    "9H", "TH", "JH", "QH", "KH", "AH", "2S","3S", "4S", "5S", "6S", "7S", \
    "8S", "9S", "TS", "JS", "QS", "KS", "AS", "2P","3P", "4P", "5P", "6P",\
    "7P", "8P", "9P", "TP", "JP", "QP", "KP", "AP"]
    deck = []
    for i in card_names:
        deck.append(Card(i))
    copydeck = deck
    for i in range(0, 3):
        deck = copydeck
        random.shuffle(deck)
        hand1 = Hand(deck[:10])
        deck = deck[10:]
        hand2 = Hand(deck[:10])
        deck = deck[10:]
        discardpile = [deck[0]]
        deck = deck[1:]
        player1 = Player(hand1, playernames[0])
        player2 = Player(hand2, playernames[1])
        laiddown = [[],[]]
        p1score = []
        p2score = []
        while player1.hand.hand != [] or player2.hand.hand != []:
            turn1 = player1.take_turn(playernames, discardpile, deck, \
            laiddown)
            discardpile = turn1[1]
            deck = turn1[2]
            laiddown = turn1[3]
            if player1.hand.hand != []:
                turn2 = player2.take_turn(playernames, discardpile, deck, \
                laiddown)
                discardpile = turn2[1]
                deck = turn2[2]
                laiddown = turn2[3]
            else:
                print("\nRound up.\n")
                break
        p1score.append(hand1.hand_point_value())
        p2score.append(hand2.hand_point_value())
    p1_totalscore = 0
    p2_totalscore = 0
    for i in p1score:
        p1_totalscore += int(i)
    for i in p2score:
        p2_totalscore += int(i)
    p1_totalscore = str(p1_totalscore)
    p2_totalscore = str(p2_totalscore)
    p1win = 0
    p1lost = 0
    p2win = 0
    p2lost = 0
    if p1_totalscore < p2_totalscore:
        p1win += 1
        p2lost += 1
    elif p2_totalscore < p1_totalscore:
        p1lost += 1
        p2win += 1
    p1win = str(p1win)
    p1lost = str(p1lost)
    p2win = str(p2win)
    p2lost = str(p2lost)
    game = ScoreTable(playernames, [p1_totalscore, p2_totalscore], \
    [p1win, p2win], [p1lost, p2lost])
    game.read_scores()
    game.save_scores()

def threepgame(playernames):
    card_names = ["2C","3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", \
    "JC", "QC", "KC", "AC", "2D","3D", "4D", "5D", "6D", "7D", "8D", "9D", \
    "TD", "JD", "QD", "KD", "AD", "2H","3H", "4H", "5H", "6H", "7H", "8H", \
    "9H", "TH", "JH", "QH", "KH", "AH", "2S","3S", "4S", "5S", "6S", "7S", \
    "8S", "9S", "TS", "JS", "QS", "KS", "AS", "2P","3P", "4P", "5P", "6P",\
    "7P", "8P", "9P", "TP", "JP", "QP", "KP", "AP"]
    deck = []
    for i in card_names:
        deck.append(Card(i))
    copydeck = deck
    for i in range(0, 3):
        deck = copydeck
        random.shuffle(deck)
        hand1 = Hand(deck[:10])
        deck = deck[10:]
        hand2 = Hand(deck[:10])
        deck = deck[10:]
        hand3 = Hand(deck[:10])
        deck = deck[10:]
        discardpile = [deck[0]]
        deck = deck[1:]
        player1 = Player(hand1, playernames[0])
        player2 = Player(hand2, playernames[1])
        player3 = Player(hand3, playernames[2])
        laiddown = [[],[],[]]
        p1score = []
        p2score = []
        p3score = []
        while player1.hand.hand != [] or player2.hand.hand != [] \
        or player3.hand.hand != []:
            turn1 = player1.take_turn(playernames, discardpile, deck, \
            laiddown)
            discardpile = turn1[1]
            deck = turn1[2]
            laiddown = turn1[3]
            if player1.hand.hand != []:
                turn2 = player2.take_turn(playernames, discardpile, deck, \
                laiddown)
                discardpile = turn2[1]
                deck = turn2[2]
                laiddown = turn2[3]
                if player2.hand.hand != []:
                    turn3 = player3.take_turn(playernames, discardpile, deck, \
                    laiddown)
                    discardpile = turn3[1]
                    deck = turn3[2]
                    laiddown = turn3[3]
                else:
                    print("\nRound up.\n")
                    break
            else:
                print("\nRound up.\n")
                break
        p1score.append(hand1.hand_point_value())
        p2score.append(hand2.hand_point_value())
        p3score.append(hand3.hand_point_value())
    p1_totalscore = 0
    p2_totalscore = 0
    p3_totalscore = 0
    for i in p1score:
        p1_totalscore += int(i)
    for i in p2score:
        p2_totalscore += int(i)
    for i in p3score:
        p3_totalscore += int(i)
    p1_totalscore = str(p1_totalscore)
    p2_totalscore = str(p2_totalscore)
    p3_totalscore = str(p3_totalscore)
    p1win = 0
    p1lost = 0
    p2win = 0
    p2lost = 0
    p3win = 0
    p3lost = 0
    if (p1_totalscore < p2_totalscore) and (p1_totalscore < p3_totalscore):
        p1win += 1
        p2lost += 1
        p3lost += 1
    elif (p2_totalscore < p1_totalscore) and (p2_totalscore < p3_totalscore):
        p1lost += 1
        p2win += 1
        p3lost += 1
    elif (p3_totalscore < p1_totalscore) and (p3_totalscore < p2_totalscore):
        p1lost += 1
        p2lost += 1
        p3win += 1
    p1win = str(p1win)
    p1lost = str(p1lost)
    p2win = str(p2win)
    p2lost = str(p2lost)
    p3win = str(p3win)
    p3lost = str(p3lost)
    game = ScoreTable(playernames, [p1_totalscore, p2_totalscore, \
    p3_totalscore], [p1win, p2win, p3win], [p1lost, p2lost, p3lost])
    game.read_scores()
    game.save_scores()

def get_deck():
    print("Please enter a .deck file name or the word 'no' to escape.")
    filechoice = True
    while filechoice == True:
        filename = input("Please enter a .deck file. ")
        try:
            if filename == "no":
                break
            else:
                deck_file = open(filename, "rU")
                info = deck_file.readlines()
                deck_file.close()
                stringinfo = ""
                for i in info:
                    stringinfo += i
                info = stringinfo
                deck = info.split()
                for i in deck:
                    if "\n" in i:
                        i.remove("\n")
                num_cards = 0
                for i in deck:
                    num_cards += 1
                if num_cards != 65:
                    print("This deck is incorrect, it must have exactly 65 \
cards.  Please enter another .deck file.")
                    filechoice= True
                else:
                    filechoice = False
        except:
            print("Please enter a valid file name, or 'no.'")
            filechoice = True
    print()
    return [filename, deck]

def twopsdgame(playernames):
    filename, deck = get_deck()
    if filename != "no":
        Card_deck = []
        for i in deck:
            Card_deck.append(Card(i))
        for i in range(0, 3):
            deck = Card_deck
            hand1 = Hand(deck[:10])
            deck = deck[10:]
            hand2 = Hand(deck[:10])
            deck = deck[10:]
            discardpile = [deck[0]]
            deck = deck[1:]
            player1 = Player(hand1, playernames[0])
            player2 = Player(hand2, playernames[1])
            laiddown = [[],[]]
            p1score = []
            p2score = []
            while player1.hand.hand != [] or player2.hand.hand != []:
                turn1 = player1.take_turn(playernames, discardpile, deck, \
                laiddown)
                discardpile = turn1[1]
                deck = turn1[2]
                laiddown = turn1[3]
                if player1.hand.hand != []:
                    turn2 = player2.take_turn(playernames, discardpile, deck, \
                    laiddown)
                    discardpile = turn2[1]
                    deck = turn2[2]
                    laiddown = turn2[3]
                else:
                    print("\nRound up.\n")
                    break
            p1score.append(hand1.hand_point_value())
            p2score.append(hand2.hand_point_value())
        p1_totalscore = 0
        p2_totalscore = 0
        for i in p1score:
            p1_totalscore += int(i)
        for i in p2score:
            p2_totalscore += int(i)
        p1_totalscore = str(p1_totalscore)
        p2_totalscore = str(p2_totalscore)
        p1win = 0
        p1lost = 0
        p2win = 0
        p2lost = 0
        if p1_totalscore < p2_totalscore:
            p1win += 1
            p2lost += 1
        elif p2_totalscore < p1_totalscore:
            p1lost += 1
            p2win += 1
        p1win = str(p1win)
        p1lost = str(p1lost)
        p2win = str(p2win)
        p2lost = str(p2lost)
        game = ScoreTable(playernames, [p1_totalscore, p2_totalscore], \
        [p1win, p2win], [p1lost, p2lost])
        game.read_scores()
        game.save_scores()    

def threepsdgame(playernames):
    filename, deck = get_deck()
    if filename != "no":
        Card_deck = []
        for i in deck:
            Card_deck.append(Card(i))
        for i in range(0, 3):
            deck = Card_deck
            hand1 = Hand(deck[:10])
            deck = deck[10:]
            hand2 = Hand(deck[:10])
            deck = deck[10:]
            hand3 = Hand(deck[:10])
            deck = deck[10:]
            discardpile = [deck[0]]
            deck = deck[1:]
            player1 = Player(hand1, playernames[0])
            player2 = Player(hand2, playernames[1])
            player3 = Player(hand3, playernames[2])
            laiddown = [[],[], []]
            p1score = []
            p2score = []
            p3score = []
            while player1.hand.hand != [] or player2.hand.hand != [] \
            or player3.hand.hand != []:
                turn1 = player1.take_turn(playernames, discardpile, deck, \
                laiddown)
                discardpile = turn1[1]
                deck = turn1[2]
                laiddown = turn1[3]
                if player1.hand.hand != []:
                    turn2 = player2.take_turn(playernames, discardpile, deck, \
                    laiddown)
                    discardpile = turn2[1]
                    deck = turn2[2]
                    laiddown = turn2[3]
                    if player2.hand.hand != []:
                        turn3 = player3.take_turn(playernames, discardpile, \
                        deck, laiddown)
                        discardpile = turn3[1]
                        deck = turn3[2]
                        laiddown = turn3[3]
                    else:
                        print("\nRound up.\n")
                        break
                else:
                    print("\nRound up.\n")
                    break
            p1score.append(hand1.hand_point_value())
            p2score.append(hand2.hand_point_value())
            p3score.append(hand3.hand_point_value())
        p1_totalscore = 0
        p2_totalscore = 0
        p3_totalscore = 0
        for i in p1score:
            p1_totalscore += int(i)
        for i in p2score:
            p2_totalscore += int(i)
        for i in p3score:
            p3_totalscore += int(i)
        p1_totalscore = str(p1_totalscore)
        p2_totalscore = str(p2_totalscore)
        p3_totalscore = str(p3_totalscore)
        p1win = 0
        p1lost = 0
        p2win = 0
        p2lost = 0
        p3win = 0
        p3lost = 0
        if (p1_totalscore < p2_totalscore) and (p1_totalscore < p3_totalscore):
            p1win += 1
            p2lost += 1
            p3lost += 1
        elif (p2_totalscore < p1_totalscore) and \
        (p2_totalscore < p3_totalscore):
            p1lost += 1
            p2win += 1
            p3lost += 1
        elif (p3_totalscore < p1_totalscore) and \
        (p3_totalscore < p2_totalscore):
            p1lost += 1
            p2lost += 1
            p3win += 1
        p1win = str(p1win)
        p1lost = str(p1lost)
        p2win = str(p2win)
        p2lost = str(p2lost)
        p3win = str(p3win)
        p3lost = str(p3lost)
        game = ScoreTable(playernames, [p1_totalscore, p2_totalscore, \
        p3_totalscore], [p1win, p2win, p3win], [p1lost, p2lost, p3lost])
        game.read_scores()
        game.save_scores()

def choose_players(numplayers):
    players = []
    game = all_scores()
    prevplayers = game.names
    for i in range(numplayers):
        menuBchoice = True
        while menuBchoice == True:
            print("\nMenu B: Choose Player Type")
            print("1. new player\n2. returning player\n")
            choice2 = input("How would you like to select your player? ")
            if choice2 != "1" and choice2 != "2":
                print("Please enter a 1 or 2.")
            else:
                menuBchoice = False
        menuCchoice = True
        while menuCchoice == True:
            if choice2 == "1":
                player = input("Please enter a player name. ")
                if player in prevplayers:
                    print("That player already exists.")
                else:
                    players.append(player)
                    menuCchoice = False
            elif choice2 == "2":
                print("Menu C: Choose Previous Player")
                for player in range(len(prevplayers)):
                    print((player + 1), end=" ")
                    print(prevplayers[player])
                chooseplayer = input("Please select a player. ")
                try:
                    playerint = int(chooseplayer) - 1
                    menuCchoice = False
                except:
                    print("Please enter a valid choice.")
                    menuCchoice = True
                if playerint not in range(len(prevplayers)):
                    print("Please enter a valid choice.")
                    menuCchoice = True
                else:
                    menuCchoice = False
                    players.append(prevplayers[playerint])
                    prevplayers.remove(prevplayers[playerint])
    print()
    return players

def main():
    menuAchoice = True
    while menuAchoice == True:
        print("Menu A: Main Menu")
        print("1. View scores\n2. Play 2-player game\n3. Play 3-player game\
        \n4. Play 2-player game with stacked deck\n5. Play 3-player game \
with stacked deck\n6. Quit\n")
        choice = input("Please enter a valid menu choice. ")
        if choice != "1" and choice != "2" and choice != "3" and choice != "4"\
        and choice != "5" and choice != "6":
            print("Please enter a 1, 2, 3, 4, 5, or 6.")
        else:
            menuAchoice = False
        if choice == "1":
            view_scores()
            menuAchoice = True
        elif choice == "2":
            players = choose_players(2)
            twopgame(players)
            menuAchoice = True
        elif choice == "3":
            players = choose_players(3)
            threepgame(players)
            menuAchoice = True
        elif choice == "4":
            players = choose_players(2)
            twopsdgame(players)
            menuAchoice = True
        elif choice == "5":
            players = choose_players(3)
            threepsdgame(players)
            menuAchoice = True
        elif choice == "6":
            menuAchoice = False

main()