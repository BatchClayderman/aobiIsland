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
	def set(self:object, symbols:tuple|list) -> bool:
		if isinstance(symbols, (tuple, list)) and len(symbols) == 4 and all(isinstance(symbol, int) and 0 <= symbol <= 7 for symbol in symbols):
			self.__symbols = tuple(symbol for symbol in symbols)
			self.__remainingAttemptCount = Problem.MaximumAttemptCount
			self.__status = Status.Set
			return True
		else:
			return False
	def generate(self:object) -> bool:
		self.__symbols = tuple(randbelow(8) for idx in range(4))
		self.__remainingAttemptCount = Problem.MaximumAttemptCount
		self.__status = Status.Generated
		return True
	def getStatus(self:object) -> Status:
		return self.__status
	def submit(self:object, submissions:tuple|list) -> tuple:
		if Status.Generated <= self.__status <= Status.Solving and self.__remainingAttemptCount >= 1 and isinstance(submissions, (tuple, list)) and len(submissions) == 4:
			flag, results = True, [Result.Right] * 4
			for idx in range(4):
				if self.__symbols[idx] != submissions[idx]:
					results[idx] = Result.Misplaced if submissions[idx] in self.__symbols else Result.Incorrect
					flag = False
			self.__remainingAttemptCount -= 1
			self.__status = Status.Solving
			if flag:
				self.__status = Status.Successful
			elif self.__remainingAttemptCount < 1:
				self.__status = Status.Failed
			return (True, self.__status, tuple(results))
		else:
			return (False, self.__status, None)

class Solver:
	MaximumAttemptCount = 5 # This value must be not smaller than ``Problem.MaximumAttemptCount``. 
	@staticmethod
	def solve(problem:Problem) -> tuple:
		if isinstance(problem, Problem) and Status.Generated <= problem.getStatus() <= Status.Solving:
			# Gathering #
			submissions, attemptCount = tuple(range(4)), 0
			isSubmitted, status, results = problem.submit(submissions)
			if isSubmitted:
				attemptCount += 1
				if Status.Successful == status:
					print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
					return (True, attemptCount, submissions)
				elif Status.Failed == status:
					print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
					return (True, attemptCount, None)
				else:
					answers, writingFlags, symbolTypeCount = [[] for idx in range(4)], [True] * 4, 0
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
			if symbolTypeCount >= 4:
				print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
			else:
				print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				submissions = tuple(range(4, 8))
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
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
						print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
				else:
					return (False, attemptCount, None)
			del writingFlags
			
			# Searching #
			def getFirstArrangement() -> tuple|None:
				for a in answers[0]:
					for b in answers[1]:
						for c in answers[2]:
							for d in answers[3]:
								if len({a, b, c, d}) == symbolTypeCount:
									return (a, b, c, d)
				return None
			while attemptCount <= Solver.MaximumAttemptCount:
				submissions = getFirstArrangement() # This is the core code. 
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
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
						print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				else:
					return (False, attemptCount, None)
			return (False, attemptCount, None)
		else:
			return (False, 0, None)


def main() -> int:
	problem = Problem()
	if len(argv) >= 5:
		try:
			symbols = tuple(int(symbol) for symbol in argv[1:5])
			print("Successfully set. " if problem.set(symbols) else "Failed to set. ")
		except:
			print("Failed to set due to the failure of integer conversion. ")
		isValid, remainingAttemptCount, answers = Solver.solve(problem)
		if isValid:
			if isinstance(answers, tuple):
				print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
				return EXIT_SUCCESS
			else:
				print("Failed to solve. ")
				return EXIT_FAILURE
		else:
			print("The problem is invalid. ")
			return EOF
	else:
		try:
			groupCount = float(argv[1])
			if groupCount >= 4096:
				groupCount = 4096
			elif groupCount > 1:
				groupCount = round(groupCount)
			else:
				groupCount = 1
		except:
			groupCount = 1
		successCount, failureCount, invalidityCount, totalAttemptCount, totalTime = 0, 0, 0, 0, 0
		if groupCount >= 4096:
			print("The program has entered the traversal mode. ")
			for a in range(8):
				for b in range(8):
					for c in range(8):
						for d in range(8):
							problem.set((a, b, c, d))
							startTime = perf_counter()
							isValid, attemptCount, answers = Solver.solve(problem)
							endTime = perf_counter()
							if isValid:
								if isinstance(answers, tuple):
									successCount += 1
									totalAttemptCount += attemptCount
									totalTime += endTime - startTime
								else:
									failureCount += 1
							else:
								invalidCount += 1
			print(															\
				"The program has traversed {0} {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		else:
			print("The group count has been set to {0}. ".format(groupCount))
			startTime = perf_counter()
			for _ in range(groupCount):
				problem.generate()
				startTime = perf_counter()
				isValid, attemptCount, answers = Solver.solve(problem)
				endTime = perf_counter()
				if isValid:
					if isinstance(answers, tuple):
						successCount += 1
						totalAttemptCount += attemptCount
						totalTime += endTime - startTime
					else:
						failureCount += 1
				else:
					invalidCount += 1
			print(															\
				"The program has conducted {0} random {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		if successCount >= 1:
			totalTime *= 1000000
			averageTime = totalTime / successCount
			print(																					\
				"Among the successful groups, the average attempt count is {0} / {1} = {2:.6f}, and the average time is {3} / {1} = {4:.6f} {5}. ".format(			\
					totalAttemptCount, successCount, totalAttemptCount / successCount, totalTime, averageTime, "microseconds" if averageTime > 1 else "microsecond"		\
				)																				\
			)
		if invalidityCount:
			return EOF
		elif successCount == groupCount:
			return EXIT_SUCCESS
		else:
			return EXIT_FAILURE



if "__main__" == __name__:
	exit(main())