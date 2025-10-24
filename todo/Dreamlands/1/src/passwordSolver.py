from sys import argv, exit
from secrets import randbelow
from time import perf_counter
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class Status:
	Initialized = 0
	Generated = 1
	Set = 2
	Solving = 3
	Successful = 4
	Failed = -1

class Result:
	Incorrect = -1
	Misplaced = 0
	Right = 1

class Problem:
	MaximumAttemptCount = 5
	def __init__(self:object) -> object:
		self.__symbols = None
		self.__remainingAttemptCount = Problem.MaximumAttemptCount
		self.__status = Status.Initialized
	def generate(self:object) -> bool:
		self.__symbols = tuple(randbelow(8) for idx in range(4))
		self.__remainingAttemptCount = Problem.MaximumAttemptCount
		self.__status = Status.Generated
		return True
	def set(self:object, symbols:tuple|list) -> bool:
		if isinstance(symbols, (tuple, list)) and len(symbols) == 4 and all(isinstance(symbol, int) and 0 <= symbol <= 7 for symbol in symbols):
			self.__symbols = tuple(symbol for symbol in symbols)
			self.__remainingAttemptCount = Problem.MaximumAttemptCount
			self.__status = Status.Set
			return True
		else:
			return False
	def getStatus(self:object) -> Status:
		return self.__status
	def submit(self:object, submissions:tuple|list) -> tuple:
		if Status.Generated <= self.__status <= Status.Solving and self.__remainingAttemptCount >= 1 and isinstance(submissions, (tuple, list)) and len(submissions) == 4:
			results, flag = [Result.Right] * 4, True
			for idx in range(4):
				if submissions[idx] != self.__symbols[idx]:
					results[idx] = Result.Misplaced if submissions[idx] in self.__symbols else Result.Incorrect
					flag = False
			self.__remainingAttemptCount -= 1
			self.__status = Status.Successful if flag else (Status.Failed if self.__remainingAttemptCount < 1 else Status.Solving)
			return (True, self.__status, tuple(results))
		else:
			return (False, self.__status, None)

class Solver:
	MaximumAttemptCount = 5 # This value must be not smaller than ``Problem.MaximumAttemptCount``. 
	
	@staticmethod
	def getFirstArrangement(answers, symbolTypeCount) -> tuple|None:
		for a in answers[0]:
			for b in answers[1]:
				for c in answers[2]:
					for d in answers[3]:
						if len({a, b, c, d}) == symbolTypeCount:
							return (a, b, c, d)
		return None
	@staticmethod
	def solve(problem:Problem, isPrint:bool = False) -> tuple:
		if isinstance(problem, Problem) and isinstance(isPrint, bool) and Status.Generated <= problem.getStatus() <= Status.Solving:
			# Gathering #
			submissions, attemptCount, answers, writingFlags, symbolTypeCount = tuple(range(4)), 0, [[] for idx in range(4)], [True] * 4, 0
			isSubmitted, status, results = problem.submit(submissions)
			if isSubmitted:
				attemptCount += 1
				if Status.Successful == status:
					if isPrint:
						print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
					return (True, attemptCount, submissions)
				elif Status.Failed == status:
					if isPrint:
						print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
					return (True, attemptCount, None)
				else:
					for idx in range(4):
						if Result.Right == results[idx]:
							answers[idx] = [submissions[idx]]
							writingFlags[idx] = False
							symbolTypeCount += 1
							for secondaryIdx in range(4):
								if writingFlags[secondaryIdx]:
									answers[secondaryIdx].append(submissions[idx])
						elif Result.Misplaced == results[idx]:
							symbolTypeCount += 1
							for secondaryIdx in range(4):
								if secondaryIdx != idx and writingFlags[secondaryIdx]:
									answers[secondaryIdx].append(submissions[idx])
			else:
				return (False, attemptCount, None)
			if symbolTypeCount < 4:
				if isPrint:
					print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				submissions = tuple(range(4, 8))
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
						return (True, attemptCount, None)
					else:
						for idx in range(4):
							if Result.Right == results[idx]:
								answers[idx] = [submissions[idx]]
								writingFlags[idx] = False
								symbolTypeCount += 1
								for secondaryIdx in range(4):
									if writingFlags[secondaryIdx]:
										answers[secondaryIdx].append(submissions[idx])
							elif Result.Misplaced == results[idx]:
								symbolTypeCount += 1
								for secondaryIdx in range(4):
									if secondaryIdx != idx and writingFlags[secondaryIdx]:
										answers[secondaryIdx].append(submissions[idx])
						if isPrint:
							print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
				else:
					return (False, attemptCount, None)
			elif isPrint:
				print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
			del writingFlags
			
			# Searching #
			while attemptCount <= Solver.MaximumAttemptCount:
				submissions = Solver.getFirstArrangement(answers, symbolTypeCount) # This is the core code. 
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
						return (True, attemptCount, None)
					else:
						for idx in range(4):
							if Result.Right == results[idx]:
								answers[idx] = [submissions[idx]]
							elif Result.Misplaced == results[idx]:
								if submissions[idx] in answers[idx]:
									answers[idx].remove(submissions[idx])
								else:
									return (False, attemptCount, None)
							else:
								return (False, attemptCount, None)
						if isPrint:
							print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				else:
					return (False, attemptCount, None)
			return (False, attemptCount, None)
		else:
			return (False, 0, None)

class Helper:
	@staticmethod
	def printHelp() -> None:
		print("This is a possible password solution for the first palace of Dreamland in the ``Obi Island: Dreamland`` mobile game. \n")
		print("1) If a non-value option or a value $x$ satisfying $x < 1.5$ is passed, the program will solve a random group. ")
		print("2) If a value $x$ satisfying $1.5 \\leqslant x < 4095.5$ is passed, the program will solve $\\left\\lfloor x + \\cfrac{1}{2}\\right\\rfloor$ random groups. ")
		print("3) If a value $x$ satisfying $x \\geqslant 4095.5$ is passed, the program will traverse all the 4096 groups. ")
		print("4) If one or more groups of 4 integers within the interval $[0, 7]$ are passed, the program will solve specifically. ")
		print("5) Otherwise, this help information will display. \n")


def main() -> int:
	argc, groupCount, problem, isPrint, successCount, failureCount, invalidityCount, totalAttemptCount, totalTime = len(argv), 0, Problem(), False, 0, 0, 0, 0, 0
	if 2 == argc:
		if argv[1].lower() in ("inf", "+inf"):
			groupCount = 4096
		else:
			try:
				groupCount = round(float(argv[1])) if "." in argv[1] else int(argv[1], 0)
				groupCount = 4096 if groupCount >= 4096 else (1 if groupCount <= 1 else groupCount)
			except:
				groupCount = 1
		if groupCount <= 4095:
			print("The group count has been set to {0}. ".format(groupCount))
			for _ in range(groupCount):
				if isPrint:
					print("Successfully generated. " if problem.generate() else "Failed to generate. ")
				else:
					problem.generate()
				startTime = perf_counter()
				isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
				endTime = perf_counter()
				if isValid:
					if isinstance(answers, tuple):
						if isPrint:
							print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
						successCount += 1
						totalAttemptCount += attemptCount
						totalTime += endTime - startTime
					else:
						if isPrint:
							print("Failed to solve. ")
						failureCount += 1
				else:
					if isPrint:
						print("The problem is invalid. ")
					invalidCount += 1
			print(															\
				"The program has conducted {0} random {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		else:
			print("The program has entered the traversal mode. ")
			for a in range(8):
				for b in range(8):
					for c in range(8):
						for d in range(8):
							if isPrint:
								print(("Successfully" if problem.set((a, b, c, d)) else "Failed to") + " set ({0}, {1}, {2}, {3}). ".format(a, b, c, d))
							else:
								problem.set((a, b, c, d))
							startTime = perf_counter()
							isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
							endTime = perf_counter()
							if isValid:
								if isinstance(answers, tuple):
									if isPrint:
										print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
									successCount += 1
									totalAttemptCount += attemptCount
									totalTime += endTime - startTime
								else:
									if isPrint:
										print("Failed to solve. ")
									failureCount += 1
							else:
								if isPrint:
									print("The problem is invalid. ")
								invalidityCount += 1
			print(															\
				"The program has traversed 4096 groups, where {0} succeeded, {1} failed, and {2} {3} invalid. ".format(		\
					successCount, failureCount, invalidityCount, "were" if invalidityCount > 1 else "was"			\
				)														\
			)
	elif argc >= 5:
		count, groups = 4, []
		for idx in range(1, argc):
			if argv[idx] in ("0", "1", "2", "3", "4", "5", "6", "7"):
				if count >= 4:
					groups.append([ord(argv[idx][0]) - 48])
					count = 1
					groupCount += 1
				else:
					groups[-1].append(ord(argv[idx][0]) - 48)
					count += 1
		if groupCount and len(groups) == groupCount:
			for group in groups:
				if isPrint:
					print(("Successfully" if problem.set(group) else "Failed to") + " set {0}. ".format(group))
				else:
					problem.set(group)
				startTime = perf_counter()
				isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
				endTime = perf_counter()
				if isValid:
					if isinstance(answers, tuple):
						if isPrint:
							print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
						successCount += 1
						totalAttemptCount += attemptCount
						totalTime = endTime - startTime
					else:
						if isPrint:
							print("Failed to solve. ")
						failureCount += 1
				else:
					if isPrint:
						print("The problem is invalid. ")
					invalidityCount += 1
			print(															\
				"The program has conducted {0} specified {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		else:
			Helper.printHelp()
	else:
		Helper.printHelp()
	if successCount >= 1:
		totalTime *= 1000000
		averageTime = totalTime / successCount
		print(																					\
			"Among the successful groups, the average attempt count is {0} / {1} = {2}, and the average time is approximately {3:.6f} / {1} = {4:.6f} {5}. ".format(	\
				totalAttemptCount, successCount, totalAttemptCount / successCount, totalTime, averageTime, "microseconds" if averageTime > 1 else "microsecond"		\
			)																				\
		)
	errorLevel = EOF if not groupCount or invalidityCount else (EXIT_SUCCESS if successCount == groupCount else EXIT_FAILURE)
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel))
		input()
	except:
		print()
	return errorLevel



if "__main__" == __name__:
	exit(main())