from sys import exit
from collections import OrderedDict
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class CardRecorder:
	allCardsWithJokers = OrderedDict((("Y", 1), ("X", 1)) + tuple((i, 4) for i in "2AKQJT9876543")).items()
	allCardsWithoutJokers = OrderedDict(tuple((i, 4) for i in "2AKQJT9876543")).items()
	def __init__(self:object, cardType:str|None = None, displaySize:int = 5, exclusion:str|None = None) -> object:
		self.__clearingCommand = "cls" if __import__("platform").system().upper() == "WINDOWS" else "clear"
		self.__system = __import__("os").system
		if cardType in ("斗地主", "三两一"):
			self.__cardType = cardType
		else:
			self.__cardType = "斗地主"
		self.__displaySize = displaySize if isinstance(displaySize, int) and displaySize >= 1 else 5
		self.__reset()
		self.__remove(exclusion)
	def __reset(self:object) -> None:
		self.__history = []
		self.__remainingCards = OrderedDict(CardRecorder.allCardsWithJokers if self.__cardType in ("斗地主", ) else CardRecorder.allCardsWithoutJokers)
	def __testRemoval(self:object, token:dict|OrderedDict|str|tuple|list) -> bool:
		if isinstance(token, (dict, OrderedDict)):
			for key, value in token.items():
				if not isinstance(key, str) or not isinstance(value, int) or value < 0 or key not in self.__remainingCards or self.__remainingCards[key] < value:
					return False
			return True
		elif isinstance(token, str):
			d = {}
			for card in token:
				if card in self.__remainingCards:
					d.setdefault(card, 0)
					d[card] += 1
				else:
					return False
			for key, value in d.items():
				if self.__remainingCards[key] < value:
					return False
			return True
		elif isinstance(token, (tuple, list)):
			for keyValue in token:
				if (																						\
					not isinstance(keyValue, (tuple, list)) or len(keyValue) != 2										\
					or not isinstance(keyValue[0], str) or not isinstance(keyValue[1], int) or keyValue[1] < 0				\
					or keyValue[0] not in self.__remainingCards or self.__remainingCards[keyValue[0]] < keyValue[1]		\
				):
					return False
			return True
		else:
			return False
	def __remove(self:object, token:dict|OrderedDict|str|tuple|list) -> bool:
		if self.__testRemoval(token):
			self.__history.append(tuple(self.__remainingCards.items()))
			if isinstance(token, (dict, OrderedDict)):
				for key, value in token.items():
					self.__remainingCards[key] -= value
			elif isinstance(token, str):
				for card in token:
					self.__remainingCards[card] -= 1
			elif isinstance(token, (tuple, list)):
				for key, value in token:
					self.__remainingCards[key] -= value
			return True
		else:
			return False
	def __clearScreen(self:object) -> int:
		return self.__system(self.__clearingCommand)
	def __display(self:object) -> None:
		self.__clearScreen()
		if self.__cardType == "斗地主":
			possibleBombs = []
			if self.__remainingCards["Y"] and self.__remainingCards["X"]:
				possibleBombs.append("YX")
			for card in self.__remainingCards.keys():
				if self.__remainingCards[card] == 4:
					possibleBombs.append(card)
			print("Possible bombs: {0}".format("/".join(possibleBombs) if possibleBombs else "None"), end = "\n\n")
		print("Remaining cards: ")
		length = len(self.__remainingCards)
		offset = (self.__displaySize - length % self.__displaySize) % self.__displaySize
		offsetTuple = ("", ) * offset
		keys, values = offsetTuple + tuple(self.__remainingCards.keys()), offsetTuple + tuple(self.__remainingCards.values())
		for i in range((length + offset) // self.__displaySize):
			for j in range(self.__displaySize):
				print("\t{0}".format(keys[i * self.__displaySize + j]), end = "")
			print()
			for j in range(self.__displaySize):
				print("\t{0}".format(values[i * self.__displaySize + j]), end = "")
			print("\n")
	def __input(self:object, _prompt:str = "") -> str|None:
		prompt = _prompt if isinstance(_prompt, str) else ""
		try:
			return input(prompt)
		except:
			print()
			return None
	def __withdraw(self:object) -> bool:
		if self.__history:
			self.__remainingCards = OrderedDict(self.__history.pop())
			return True
		else:
			return False
	def __judge(self:object, token:dict|OrderedDict|str|tuple|list) -> bool:
		return True
	def interact(self:object) -> bool:
		lastToken = None
		while True:
			self.__display()
			if lastToken:
				print("The last effective token is {0}. ".format(lastToken))
			print("E = Exit\tR = Reset\tW = Withdraw" if self.__history else "E = Exit\tR = Reset")
			token = self.__input("Please input the token: ").upper()
			if token:
				if token == "E":
					answer = self.__input("Are you sure you want to exit [yN]? ")
					if isinstance(answer, str) and answer.upper() in ("Y", "YES", "1", "TRUE"):
						self.__clearScreen()
						return True
				elif token == "R":
					answer = self.__input("Are you sure you want to reset [yN]? ")
					if isinstance(answer, str) and answer.upper() in ("Y", "YES", "1", "TRUE"):
						self.__reset()
						lastToken = None
				elif token == "W":
					self.__withdraw()
					lastToken = None
				elif self.__judge(token) and self.__remove(token):
					lastToken = token
				else:
					print("The token is invalid for the card type entitled \"{0}\" in Chinese. ".format(self.__cardType))
					print("Please press the enter key to continue. ")
					self.__input()


def main() -> int:
	cardRecorder = CardRecorder()
	return EXIT_SUCCESS if cardRecorder.interact() else EXIT_FAILURE



if "__main__" == __name__:
	exit(main())