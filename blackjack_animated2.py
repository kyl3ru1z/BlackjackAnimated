import random as random
from tkinter import *

root = Tk()
root.title("Black Jack")
root.tk_setPalette('#161')
root.resizable(False, False)
class Card:
    def __init__(self, suit, pip):
        self.suit = suit
        self.pip = pip

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        for suit in ["clubs", "diamonds", "hearts", "spades"]:
            for pip in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "a", "j", "k", "q"]:
                self.cards.append(Card(suit, pip))

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()

    def softReset(self):
        self.cards.clear()
        self.build()
        self.shuffle()

class Player:
    def __init__(self):
        self.hand = []
        self.data = []
        self.score = 0
        self.numCards = 0
        self.gameScore = 0
        self.hasHardAce = False
        self.counter = 100

    def draw(self, whichDeck):
        self.hand.append(whichDeck.drawCard())
        self.update()

    def update(self):
        self.score = 0
        self.numCards = 0
        self.hasHardAce = False

        for i in range(len(self.hand)):
            self.numCards += 1
            if self.hand[i].pip == "a" and self.score <= 11:
                self.hasHardAce = True
                self.score += 10

            if self.hand[i].pip == "j" or self.hand[i].pip == "k" or self.hand[i].pip == "q":
                self.score += 10
            elif self.hand[i].pip == "a":
                self.score += 1
            else:
                self.score += int(self.hand[i].pip)

        if self.score >= 22 and self.hasHardAce:
            self.score -= 10
            self.hasHardAce = False

    def softReset(self):
        self.hand.clear()
        self.data.clear()
        self.score = 0
        self.numCards = 0
        self.hasHardAce = False

def showDealerHand():
    dealer.data.clear()
    for i in range(len(dealer.hand)):
        pngCard = PhotoImage(file=f"cards/{dealer.hand[i].suit}-{dealer.hand[i].pip}-75.png")
        dealer.data.append(pngCard)

    x = 30
    y = 80

    for imageObj in dealer.data:
        imageObj.x = x
        imageObj.y = y
        id = canvas.create_image(x, y, anchor=NW, image=imageObj)
        imageObj.canvasID = id
        x += 80
        y += 0

    dealerScoreLabel.config(text=f"Dealer Score: {dealer.score}")

def animateCard(who):
    if who == "Player":
        player.counter -= 1
        player.data[len(player.data)-1].x = player.data[len(player.data)-1].x - 5
        if player.data[len(player.data)-1].x <= 30:
            player.data[len(player.data)-1].x = 30
        canvas.coords(player.data[len(player.data)-1].canvasID, player.data[len(player.data)-1].x, player.data[len(player.data)-1].y)
        if player.counter > 0:
            canvas.after(1, lambda: animateCard(who))
        if player.counter == 0:
            player.counter = 100
    elif who == "Dealer":
        dealer.counter -= 1
        dealer.data[len(dealer.data)-1].x = dealer.data[len(dealer.data)-1].x - 5
        if dealer.data[len(dealer.data)-1].x <= 30:
            dealer.data[len(dealer.data)-1].x = 30
        canvas.coords(dealer.data[len(dealer.data)-1].canvasID, dealer.data[len(dealer.data)-1].x, dealer.data[len(dealer.data)-1].y)
        if dealer.counter > 0:
            canvas.after(1, lambda: animateCard(who))
        if dealer.counter == 0:
            dealer.counter = 100

def addCardPhoto(who):
    if who == "Player":
        player.draw(deck)
        for i in range(len(player.hand)):
            if i == len(player.hand) - 1:
                pngCard = PhotoImage(file=f"cards/{player.hand[i].suit}-{player.hand[i].pip}-75.png")
                player.data.append(pngCard)

        player.data[len(player.data) - 1].x = 530
        player.data[len(player.data) - 1].y = 290
        id = canvas.create_image(530, 290, anchor=NW, image=player.data[len(player.data) - 1])
        player.data[len(player.data) - 1].canvasID = id
        if len(player.data) > 1:
            player.data[len(player.data) - 1].x += player.data[len(player.data) - 2].x + 50
    elif who == "Dealer":
        dealer.draw(deck)
        for i in range(len(dealer.hand)):
            if i == len(dealer.hand) - 1:
                if i == 0:
                    if dealer.hand[i].suit == "spades" or dealer.hand[i].suit == "clubs":
                        pngCard = PhotoImage(file="cards/back-blue-75-3.png")
                        dealer.data.append(pngCard)
                    elif dealer.hand[i].suit == "diamonds" or dealer.hand[i].suit == "hearts":
                        pngCard = PhotoImage(file="cards/back-red-75-3.png")
                        dealer.data.append(pngCard)
                else:
                    pngCard = PhotoImage(file=f"cards/{dealer.hand[i].suit}-{dealer.hand[i].pip}-75.png")
                    dealer.data.append(pngCard)

        dealer.data[len(dealer.data) - 1].x = 530
        dealer.data[len(dealer.data) - 1].y = 80
        id = canvas.create_image(30, 80, anchor=NW, image=dealer.data[len(dealer.data) - 1])
        dealer.data[len(dealer.data) - 1].canvasID = id
        if len(dealer.data) > 1:
            dealer.data[len(dealer.data) - 1].x += dealer.data[len(dealer.data) - 2].x + 50

def dealCard(who):
    addCardPhoto(who)
    animateCard(who)

def updateScore(isPartialScore):
    if isPartialScore:
        playerScoreLabel.config(text=f"Player Score: {player.score}")
        if dealer.hand[1].pip == "j" or dealer.hand[1].pip == "k" or dealer.hand[1].pip == "q":
            dealerScoreLabel.config(text="Dealer Score: 10")
        elif dealer.hand[1].pip == "a":
            dealerScoreLabel.config(text="Dealer Score: 1")
        else:
            dealerScoreLabel.config(text=f"Dealer Score: {dealer.hand[1].pip}")
    else:
        playerScoreLabel.config(text=f"Player Score: {player.score}")
        dealerScoreLabel.config(text=f"Dealer Score: {dealer.score}")

    if len(dealer.data) >= 2:
        roundEval("none", False)
    else:
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        dealButton.config(state=DISABLED)


def roundEval(whoWon, roundOver):
    if roundOver:
        hitButton.config(state=DISABLED)
        standButton.config(state=DISABLED)
        dealButton.config(state=NORMAL)
    else:
        hitButton.config(state=NORMAL)
        standButton.config(state=NORMAL)
        dealButton.config(state=DISABLED)

    if player.score == 21:
        hitButton.config(state=DISABLED)

    if whoWon == "Player":
        player.gameScore += 10
        dealer.gameScore -= 10
    elif whoWon == "Dealer":
        player.gameScore -= 10
        dealer.gameScore += 10
    else:
        pass

    gameScoreLabel.config(text=f"[ P {player.gameScore} : D {dealer.gameScore} ]")

def hitButtonClicked():
    dealCard("Player")
    playerScoreLabel.config(text=f"Player Score: {player.score}")

    player.update()
    if player.score >= 22:
        showDealerHand()
        roundEval("Dealer", True)
    elif player.numCards >= 5 and player.score < 22:
        showDealerHand()
        roundEval("Player", True)
    elif player.score == 21:
        hitButton.config(state=DISABLED)

def dealButtonClicked():
    deck.softReset()
    player.softReset()
    dealer.softReset()

    canvas.after(100, lambda: updateScore(False))
    canvas.after(500, lambda: dealCard("Player"))
    canvas.after(1000, lambda: dealCard("Dealer"))
    canvas.after(1500, lambda: dealCard("Player"))
    canvas.after(2000, lambda: dealCard("Dealer"))
    canvas.after(2500, lambda: updateScore(True))

def standButtonClicked():
    showDealerHand()
    dealerHit()

def dealerHit():
    dealer.update()
    if dealer.score <= 15:
        dealCard("Dealer")
        updateScore(False)
        canvas.after(500, dealerHit)
    else:
        if dealer.score >= 22:
            roundEval("Player", True)
        elif dealer.numCards == 5 and dealer.score < 22:
            roundEval("Dealer", True)
        else:
            if player.score > dealer.score:
                roundEval("Player", True)
            else:
                roundEval("Dealer", True)


deck = Deck()
player = Player()
dealer = Player()

canvas = Canvas(root, bd=20, bg='#161', height=400, width=600, relief=RIDGE)
hitButton = Button(root, text="Hit", font=("Arial Black", 18), command=hitButtonClicked,  width=12, height=0, fg="green yellow", bg='#161')
standButton = Button(root, text="Stand", font=("Arial Black", 18), command=standButtonClicked,  width=12, height=0, fg="green yellow", bg='#161')
dealButton = Button(root, text="Deal", font=("Arial Black", 18), command=dealButtonClicked, width=12, height=0, fg="green yellow", bg='#161')
playerScoreLabel = Label(canvas, text=f"Player Score: {player.score}", fg="green yellow", bg='#161', font=("Arial Black", 18))
dealerScoreLabel = Label(canvas, text=f"Dealer Score: {dealer.score}", fg="green yellow", bg='#161', font=("Arial Black", 18))
gameScoreLabel = Label(canvas, text=f"[ P {player.gameScore} : D {dealer.gameScore} ]", fg="green yellow", bg='#161', font=("Arial Black", 18))

canvas.pack()
playerScoreLabel.pack(padx=15)
canvas.create_window(134, 260, window=playerScoreLabel)
dealerScoreLabel.pack(padx=15)
canvas.create_window(134, 50, window=dealerScoreLabel)
gameScoreLabel.pack(padx=15)
canvas.create_window(520, 50, window=gameScoreLabel)
hitButton.pack(side=LEFT)
standButton.pack(side=LEFT)
dealButton.pack(side=LEFT)

hitButton.config(state=DISABLED)
standButton.config(state=DISABLED)
dealButton.config(state=NORMAL)

root.mainloop()
