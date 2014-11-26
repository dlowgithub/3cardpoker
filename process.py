import tweepy
import time
import random


# initialize some globals
bank = {}
state = {}
deck = []
handrank = {}
pairsplusbonus = {}
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def evalHand (card1,card2,card3):
	# This will return the pairs plus and hand rankings
	card1Value=cards.index(card1[0:len(card1)-1])
	card1Suit=card1[len(card1)-1:len(card1)]
	#card2Value=card2[0:len(card2)-1]
	card2Value=cards.index(card2[0:len(card2)-1])
	card2Suit=card2[len(card2)-1:len(card2)]
	#card3Value=card3[0:len(card3)-1]
	card3Value=cards.index(card3[0:len(card3)-1])
	card3Suit=card3[len(card3)-1:len(card3)]

	#print "Card1: " + card1Value + " " + card1Suit	


	# This is for hand ordering
	if (card1Value<card2Value) and (card1Value<card3Value):
		if (card2Value<card3Value):
			truevalue = (card3Value*125 + card2Value*15 +card1Value)
		else:
			truevalue = (card2Value*125 + card3Value*15 +card1Value)
	elif (card2Value<card1Value) and (card2Value<card3Value):
		if (card1Value<card3Value):
			truevalue = (card3Value*125 + card1Value*15 +card2Value)
		else:
			truevalue = (card1Value*125 + card3Value*15 +card2Value)
	else:
		if (card2Value<card1Value):
			truevalue = (card1Value*125 + card2Value*15 +card3Value)
		else:
			truevalue = (card2Value*125 + card1Value*15 +card3Value)


	# Check to see if its a valid hand (no repeated cards)
	if (card1==card2) or (card2==card3) or (card1==card3):
		# This is a duplicate card
		#print "Duplicate Hand" + card1+card2+card3
		value = 0

	# Check for a set
	elif (card1Value==card2Value==card3Value):
		value = 10000000
		#print "Set" + card1+card2+card3
		return(30,truevalue+value)

	# Check for a pair
	elif ((card1Value==card2Value) and (card2Value!=card3Value)) or ((card1Value==card3Value) and (card3Value!=card2Value)) or ((card2Value==card3Value) and (card2Value!=card1Value)):
		#print "Pair" + card1+card2+card3
		value = 10000
		return(1,truevalue+value)

	# Check for a flush
	elif (card1Suit==card2Suit) and (card2Suit==card3Suit):
		# Check for a straight flush
		if ((card2Value==card3Value+1) and (card2Value==card1Value+2)) or ((card3Value==card2Value+1) and (card3Value==card1Value+2)) or ((card1Value==card2Value+1) and (card1Value==card3Value+2)) or ((card2Value==card3Value+2) and (card2Value==card1Value+1)) or ((card3Value==card2Value+2) and (card3Value==card1Value+1)) or ((card1Value==card2Value+2) and (card1Value==card3Value+1)) or ((card3Value==12) and ((card2Value==1 and card1Value==2) or (card2Value==2 and card1Value==1))) or ((card2Value==12) and ((card3Value==1 and card1Value==2) or (card3Value==2 and card1Value==1))) or ((card1Value==12) and ((card2Value==1 and card3Value==2) or (card2Value==2 and card3Value==1))):
			#print "Straight Flush" + card1+card2+card3
			value = 100000000
			return(40,truevalue+value)

		else:
			#print "Flush" + card1+card2+card3
			value = 100000
			return(4,truevalue+value)

	# Check for a straight
	elif ((card2Value==card3Value+1) and (card2Value==card1Value+2)) or ((card3Value==card2Value+1) and (card3Value==card1Value+2)) or ((card1Value==card2Value+1) and (card1Value==card3Value+2)) or ((card2Value==card3Value+2) and (card2Value==card1Value+1)) or ((card3Value==card2Value+2) and (card3Value==card1Value+1)) or ((card1Value==card2Value+2) and (card1Value==card3Value+1)) or ((card3Value==12) and ((card2Value==1 and card1Value==2) or (card2Value==2 and card1Value==1))) or ((card2Value==12) and ((card3Value==1 and card1Value==2) or (card3Value==2 and card1Value==1))) or ((card1Value==12) and ((card2Value==1 and card3Value==2) or (card2Value==2 and card3Value==1))):

		#print "Straight" + card1+card2+card3
		value = 1000000
		return(4,truevalue+value)
	# We have nothing
	else:
		# See if its a placard3Valueable
		value=0
		if (card1Value>9) or (card2Value>9) or (card3Value>9):
			return(0,truevalue+value)
		else:
			return(0,0)



# process commands function
def parseInput(username,id,msg):
	# Get the first token which is the command
	cmd=msg.partition(' ')[0]

	command=cmd.lower()

	if command == 'deal':
		print 'deal'
	elif command == 'register':  
		register(username)
		#print 'register'
	elif command == 'ante':  
		ante(username,msg)
	elif command == 'fold':  
		fold(username)
	elif command == 'play':  
		play(username)
	else:
		print 'invalid' 
		print command

# register users
def register(username):

	# Check to see if user exists

	if username in bank.keys():
		# print "User already exists, doing nothing"
		if state[username]=='none':
			message='You are already registered, to play, please send ante and your bet. Example: ante 1 1'
		else:
			message='You are already in a hand. If you want to play your current hand, send play'
			
	else:
		# Add user to bank
		bank[username]=100

		# Add user to state
		state[username]='none'
	
		#print 'registered ' + username
		message='You are now registered and have been credited 100, to play, please send ante and your bet. Example: ante 1 1'
	api_return = api.send_direct_message(screen_name=username,text=message)

# User is going to play a hand
def ante (username,msg):

	if state[username] !='none':
		# Player is already in a hand
		rawStatus=state[username]
		pairsplus,ante,card1,card2,card3=rawStatus.split(':')
		message='You are already in a hand. You cards are ' + card1 + ', ' + card2 + ', ' + card3 + '. You must play or fold'
		api_return = api.send_direct_message(screen_name=username,text=message)
		#print 'player in hand already\n'
		return

	#print 'dealing hand'

	# Parse input
	# If there are 2 bets, one is an ante and one is pairs plus
	if msg.count(' ')==2:
		cmd,pairsplus,ante = msg.split(' ');
		if pairsplus.isdigit() and ante.isdigit():
			wager=int(pairsplus) + int(ante)
			neededbank=int(pairsplus)+(int(ante)*2)
		else:
			message='This is an invalid bet, please try again'
			api_return = api.send_direct_message(screen_name=username,text=message)
			return
	# If there is 1 bet, there is no pairs plus bet
	elif msg.count(' ')==1:
		cmd,ante = msg.split(' ');
		if ante.isdigit():
			wager=int(ante)
			pairsplus=0
			neededbank=int(ante)*2
		else:
			#print 'Invalid bet'
			message='This is an invalid bet, please try again'
			api_return = api.send_direct_message(screen_name=username,text=message)
			return
	else:
		message='Invalid bet, please ante again'
		api_return = api.send_direct_message(screen_name=username,text=message)
		return

	# See if the player has enough money
	if bank[username] < neededbank or int(ante) < 0 or int(pairsplus) < 0:
		#print 'invalid bet'
		#print bank[username]
		#print neededbank
		message='Invalid bet, please ante again'
		api_return = api.send_direct_message(screen_name=username,text=message)
		return
	
	# Withdraw funds from bank from user
	#print bank
	bank[username] = bank[username] - int(wager)
	#print bank

	# Deal cards
	cards=deck[:]
	hand=[]

	# Get first card
	cardlen = len(cards)-1
	selCard = random.randint(0,cardlen)
	hand.append(deck[selCard])
	# I think this is the problem, should be removing from cards and not from the deck
	card1=cards[selCard]
	#card2=deck[selCard]
	cards.remove(card1)
	#print "Card1:"+ card1
	#print cards
	cards.sort()

	# Get second card
	# This is not getting me a random card for some reason
	cardlen-=1
	selCard = random.randint(0,cardlen)
	hand.append(deck[selCard])
	card2=cards[selCard]
	#card2=deck[selCard]
	#print "card2:" + card2
	cards.remove(card2)
	cards.sort()

	# Get third card
	cardlen-=1
	selCard = random.randint(0,cardlen)
	hand.append(deck[selCard])
	card3=cards[selCard]
	#card3=deck[selCard]
	#print "card3:" + card3
	cards.remove(card3)
	cards.sort()

	#print cards

	# Sort hand
	#hand.sort()

	#print hand
	#print ' Cards:' + handCard
	handCards=str(pairsplus) + ':' + str(ante) + ':' + card1 + ':' + card2 + ':' + card3

	# Update users state
	state[username]=handCards

	message='Your cards are: ' + card1 + ' ' + card2 + ' ' + card3 + '. If you want to play, send play. If you want to fold, send fold'
	api_return = api.send_direct_message(screen_name=username,text=message)

# User is going to play cards they have 
def fold (username):

	if state[username] =='none':
		# Player does not have cards
		# print 'player does not have cards\n'
		message='You are not in a hand. You must ante to play. Example: ante 1 1'
		api_return = api.send_direct_message(screen_name=username,text=message)
		return
	# State can back to none so player can play another hand
	state[username]='none'
	message='You fold, to play another hand, send ante and your bet. You now have ' + str(bank[username]) + ' in your bankroll'
	api_return = api.send_direct_message(screen_name=username,text=message)

# User is going to play cards they have 
def play (username):

	if state[username] =='none':
		# Player does not have cards
		print 'player does not have cards\n'
		return

	# Grab state and setup deck
	cards=deck[:]
	hand=[]

	#print "Playing, checking state"
	#print state
	rawStatus=state[username]
	
	#print "Raw Status" + str (rawStatus)


	pairsplus,ante,card1,card2,card3=rawStatus.split(':')

	# Charge the player a unit to play
	bank[username] = bank[username] - int(ante)
	# print bank

	hand.append(card1)
	hand.append(card2)
	hand.append(card3)

	# remove cards from deck
	#print cards
	cards.remove(card1)
	cards.remove(card2)
	cards.remove(card3)
	#print "Removed cards"
	#print cards

	sortedhand=hand[0]+hand[1]+hand[2]

	#print 'did I win:' + str(sortedhand)
	
	playerBonus,playersHand = evalHand(card1,card2,card3)
	
	# If there is a pairs plus bet, check for payout
	if int(playerBonus) > 0:	
		#pairsBonus=pairsplusbonus[sortedhand]
		#print 'Pairs Plus Bonus: ' + str(playerBonus)
		# Player also gets their original pairs plus bet back
		bank[username] = bank[username] + (int(pairsplus)*int(playerBonus)) + int(pairsplus)
		#print "paying: " + str((int(pairsplus)*int(playerBonus)) + int(pairsplus))
		message='You win a pairs plus bonus of ' + str((int(pairsplus)*int(playerBonus)) + int(pairsplus)) 

	
		# Pay off ante bonus
		if playerBonus == 5:
			bank[username] = bank[username] + int(ante)
			message=message + ' and an ante bonus of ' + str(ante)
			statusMessage='@' + str(username) + ' just got a straight with ' + card1 + ', ' + card2 + ', ' + card3
			api.update_status(statusMessage)
		elif playerBonus == 30:
			bank[username] = bank[username] + (int(ante) * 4)
			message=message + ' and an ante bonus of ' + str(ante * 4)
			statusMessage='. @' +str(username) + ' just got three of a kind with ' + card1 + ', ' + card2 + ', ' + card3
			api.update_status(statusMessage)
		elif playerBonus == 40:
			bank[username] = bank[username] + (int(ante) * 5)
			message=message + ' and an ante bonus of ' + str(ante * 5)
			statusMessage='. @' +str(username) + ' just got a straight flush with ' + card1 + ', ' + card2 + ', ' + card3
			api.update_status(statusMessage)
		message=message + '. '
		api_return = api.send_direct_message(screen_name=username,text=message)

	message=""

		

	#print bank
	#print 'Players Hand stength: ' + str(playersHand)

	# Get the deailers hand

        cardlen = len(cards)-1
        selCard = random.randint(0,cardlen)
        #hand.append(deck[selCard])
        dealerCard1=cards[selCard]
	#print "Dealer Card 1:" + dealerCard1
        cards.remove(dealerCard1)

        cardlen = len(cards)-1
        selCard = random.randint(0,cardlen)
        #hand.append(deck[selCard])
        dealerCard2=cards[selCard]
	#print "Dealer Card 2:" + dealerCard2
        cards.remove(dealerCard2)

        cardlen = len(cards)-1
        selCard = random.randint(0,cardlen)
        #hand.append(deck[selCard])
        dealerCard3=cards[selCard]
	#print "Dealer Card 3:" + dealerCard3
        cards.remove(dealerCard3)


	#print "Dealer's hand: " + dealerCard1 + dealerCard2 + dealerCard3

	dealerBonus,dealerHand = evalHand(dealerCard1,dealerCard2,dealerCard3)
	
	#print "dealers strength: " + str(dealerHand)

	if dealerHand==0:
		# Dealer fold, player wins
		# print "Dealer folds,player wins"
		# You pay 3 here because the player gets their original bets back also
		bank[username] = bank[username] + (int(ante)*3)
		#print "paying: " + str ((int(ante)*3))
		message=message + 'Dealer shows ' + dealerCard1 + ' ' + dealerCard2 + ' ' + dealerCard3 + ' and folds. You win your ante bet of ' + str(ante)
	elif playersHand>dealerHand:
		#print "player wins"
		bank[username] = bank[username] + (int(ante)*4)
		#print "paying: " + str ((int(ante)*4))
		message=message + 'Dealer shows ' + dealerCard1 + ' ' + dealerCard2 + ' ' + dealerCard3 + ' and loses. You win your ante and play bets for a total of ' + str(ante*2)
	else:
		message=message + 'Dealer shows ' + dealerCard1 + ' ' + dealerCard2 + ' ' + dealerCard3 + ' and wins'
		#print "dealer wins"

	api_return = api.send_direct_message(screen_name=username,text=message)
	message='To play again, send ante with your bet. You now have ' + str(bank[username]) + ' in your bankroll'
	api_return = api.send_direct_message(screen_name=username,text=message)

	# Player is no longer in a hand
	state[username] ='none'
	
	#print bank

# Consumer keys and access tokens, used for OAuth
f = open('keys', 'r')
consumer_key,consumer_secret,access_token,access_token_secret=f.read().splitlines()
#print consumer_key
f.close
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Follow anyone who follows you that you aren't following
for follower in tweepy.Cursor(api.followers).items():
   	if (not(follower.following)):
    		follower.follow()
		username=follower.screen_name
		message='Thanks for following, to start playing send: register'
		api_return = api.send_direct_message(screen_name=username,text=message)

# Get the last ID processed
f = open('lastid', 'r')
lastid=f.read()
f.close

# Grab the time stamp to be used to run
timestamp=time.time()

# Load state table
with open('state', 'r') as f:
	for read_data in f:
		# remove extra characters
		input = read_data.rstrip()
		user, status = input.split(' ')
		state[user]=status
f.close

# Load bank
with open('bank', 'r') as f:
	for read_data in f:
		# remove extra characters
		input = read_data.rstrip()
		user, bankroll = input.split(' ')
		bank[user]=int(bankroll)
f.close


# Load handrankings
with open('handrankings', 'r') as f:
	for read_data in f:
		# remove extra characters
		input = read_data.rstrip()
		hand, rank = input.split(':')
		handrank[hand]=rank
f.close

# Load pairsplusbonus
with open('pairsplus', 'r') as f:
	for read_data in f:
		# remove extra characters
		input = read_data.rstrip()
		hand, bonus = input.split(':')
		pairsplusbonus[hand]=bonus
f.close

# Load deck
i=10
with open('deck', 'r') as f:
	for read_data in f:
		# remove extra characters
		input = read_data.rstrip()
		deck.append(input)
f.close

# TODO: Need to add a verification that the users are still active
# and following the dealer bot

# Get the last time stamp processed
# Receive a message
myDMs = api.direct_messages(since_id=lastid)

# Go through all messages
for status in reversed(myDMs):
	#print "ID:" + status.id_str + " Text: " + status.text + " by @" + status.sender.screen_name
	id=status.id_str
	msg=status.text
	username=status.sender.screen_name
	#print id

	parseInput(username,id,msg)

# Write state table
f = open('state','w')
for k in state.keys():
	output = k + ' ' + state[k] + '\n'
	f.write(output)
f.close

# Write bank table
f = open('bank','w')
for k in bank.keys():
	output = k + ' ' + str(bank[k]) + '\n'
	f.write(output)
f.close

# Write the last ID processed
if id > lastid:
	f = open('lastid', 'w')
	f.write(id)
	f.close

#print "state"
#print state

#print "Bank"
#print bank
