#include <iostream>
#include <string>
#include <vector>
#if !defined _WIN32 && !defined _WIN64 && !defined WIN32 && !defined WIN64
#include <algorithm>
#endif
#include <random>
#include <chrono>
#ifndef EXIT_SUCCESS
#define EXIT_SUCCESS 0 
#endif
#ifndef EXIT_FAILURE
#define EXIT_FAILURE 1 
#endif
#ifndef EOF
#define EOF (-1)
#endif
#ifndef UNREFERENCED_PARAMETER
#define UNREFERENCED_PARAMETER(P) (void(P))
#endif
#ifndef TIME_POINT_TYPE
#if defined _WIN32 || defined _WIN64 || defined WIN32 || defined WIN64
#define TIME_POINT_TYPE std::chrono::steady_clock::time_point
#else
#define TIME_POINT_TYPE std::chrono::system_clock::time_point
#endif
#endif
typedef unsigned short Count;
constexpr size_t PASSWORD_LENGTH = 4;
constexpr Count MAXIMUM_ATTEMPT_COUNT = 5;


enum class Symbol : unsigned char
{
	RedStar = 0x00/* 0b0000 */,
	RedHeart = 0x01/* 0b0001 */,
	RedPawprint = 0x02/* 0b0010 */,
	RedBlossom = 0x03/* 0b0011 */,
	BluePuzzle = 0x04/* 0b0100 */,
	BlueLeaf = 0x05/* 0b0101 */,
	BlueCrescent = 0x06/* 0b0110 */,
	BlueNote = 0x07/* 0b0111 */
};

enum class Status : char
{
	Initialized = 0, 
	Generated = 1, 
	Set = 2, 
	Solving = 3, 
	Successful = 4, 
	Failed = -1
};

enum class Result : char
{
	Incorrect = -1, 
	Misplaced = 0, 
	Right = 1
};

class Problem
{
private:
	std::mt19937 seed = std::mt19937(std::random_device{}());
	std::vector<Symbol> symbols{};
	Count remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
	Status status = Status::Initialized;
	
public:
	Problem()
	{
		this->symbols.clear();
		this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
		this->status = Status::Initialized;
	}
	bool generate()
	{
		this->symbols = std::vector<Symbol>(PASSWORD_LENGTH);
		std::uniform_int_distribution<unsigned short> dist(static_cast<unsigned short>(Symbol::RedStar), static_cast<unsigned short>(Symbol::BlueNote));
		for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
			this->symbols[idx] = static_cast<Symbol>(dist(this->seed));
		this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
		this->status = Status::Generated;
		return true;
	}
	bool set(const std::vector<Symbol>& group)
	{
		if (group.size() == PASSWORD_LENGTH)
		{
			this->symbols = group;
			this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
			this->status = Status::Set;
			return true;
		}
		else
			return false;
	}
	Status getStatus() const
	{
		return this->status;
	}
	bool submit(const std::vector<Symbol>& submissions, Status& s, std::vector<Result>& results)
	{
		if (Status::Generated <= this->status && this->status <= Status::Solving && this->remainingAttemptCount >= 1 && submissions.size() == PASSWORD_LENGTH)
		{
			results = std::vector<Result>(PASSWORD_LENGTH, Result::Right);
			bool flag = true;
			for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
				if (submissions[idx] != this->symbols[idx])
				{
					results[idx] = find(this->symbols.begin(), this->symbols.end(), submissions[idx]) == this->symbols.end() ? Result::Incorrect : Result::Misplaced;
					flag = false;
				}
			--this->remainingAttemptCount;
			this->status = flag ? Status::Successful : (this->remainingAttemptCount < 1 ? Status::Failed : Status::Solving);
			s = this->status;
			return true;
		}
		else
		{
			s = this->status;
			results.clear();
			return false;
		}
	}
};

#if defined _DEBUG || defined DEBUG
class Formatter
{
public:
	static std::string format(const Symbol symbol)
	{
		return std::to_string(static_cast<unsigned short>(symbol));
	}
	static std::string format(const std::vector<Symbol>& symbols)
	{
		if (symbols.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(symbols[0]);
			const size_t length = symbols.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(symbols[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const Result result)
	{
		return std::to_string(static_cast<short>(result));
	}
	static std::string format(const std::vector<Result>& results)
	{
		if (results.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(results[0]);
			const size_t length = results.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(results[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const std::vector<std::vector<Symbol>>& symbolArrays)
	{
		if (symbolArrays.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(symbolArrays[0]);
			const size_t length = symbolArrays.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(symbolArrays[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const std::vector<std::vector<Symbol>>& answers, const Count symbolTypeCount)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(answers) + " -> " + std::to_string(symbolTypeCount);
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const std::vector<std::vector<Symbol>>& answers)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(answers);
	}
	static std::string format(const Status status)
	{
		switch (status)
		{
		case Status::Initialized:
			return "Initialized";
		case Status::Generated:
			return "Generated";
		case Status::Set:
			return "Set";
		case Status::Solving:
			return "Solving";
		case Status::Successful:
			return "Successful";
		case Status::Failed:
			return "Failed";
		default:
			return "Unknown";
		}
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const Status status)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(status);
	}
	/*
	static std::string symbol2string(const Symbol symbol)
	{
		switch (symbol)
		{
		case Symbol::RedStar:
			return "红五角星";
		case Symbol::RedHeart:
			return "红色爱心";
		case Symbol::RedPawprint:
			return "红色爪印";
		case Symbol::RedBlossom:
			return "红八角花";
		case Symbol::BluePuzzle:
			return "蓝色拼图";
		case Symbol::BlueLeaf:
			return "蓝色树叶";
		case Symbol::BlueCrescent:
			return "蓝色月牙";
		case Symbol::BlueNote:
			return "蓝色音符";
		default:
			return "未知符号";
		}
	}
	static std::string result2string(const Result result)
	{
		switch (result)
		{
		case Result::Right:
			return "正确";
		case Result::Misplaced:
			return "易位";
		case Result::Incorrect:
			return "错误";
		default:
			return "未知";
		}
	}
	static std::string symbols2string(const std::vector<Symbol>& symbols, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (symbols.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::symbol2string(symbols[0]);
			const size_t length = symbols.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::symbol2string(symbols[idx]);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	static std::string results2string(const std::vector<Result>& results, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (results.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::result2string(results[0]);
			const size_t length = results.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::result2string(results[idx]);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	static std::string symbolArrays2string(const std::vector<std::vector<Symbol>>& symbolArrays, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (symbolArrays.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::symbols2string(symbolArrays[0], prefix, separator, suffix, returnIfEmpty);
			const size_t length = symbolArrays.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::symbols2string(symbolArrays[0], prefix, separator, suffix, returnIfEmpty);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	*/
};
#endif

class Solver
{
private:
	static std::vector<Symbol> getFirstArrangement(const std::vector<std::vector<Symbol>>& answers, const Count symbolTypeCount)
	{
		for (const Symbol& a : answers[0])
			for (const Symbol& b : answers[1])
				for (const Symbol& c : answers[2])
					for (const Symbol& d : answers[3])
					{
						Count count = 1;
						if (b != a)
							count += 1;
						if (c != a && c != b)
							count += 1;
						if (d != a && d != b && d != c)
							count += 1;
						if (symbolTypeCount == count)
							return std::vector<Symbol>{ a, b, c, d };
					}
		return std::vector<Symbol>{};
	}
	
public:
	static bool solve(Problem& problem, Count& attemptCount, std::vector<Symbol>& symbols)
	{
		Status status = problem.getStatus();
		attemptCount = 0;
		symbols.clear();
		if (Status::Generated <= status && status <= Status::Solving)
		{
			/* Gathering */
			std::vector<Symbol> submissions{ Symbol::RedStar, Symbol::RedHeart, Symbol::RedPawprint, Symbol::RedBlossom };
			std::vector<Result> results{};
			std::vector<std::vector<Symbol>> answers(PASSWORD_LENGTH);
			bool writingFlags[PASSWORD_LENGTH] = { true,  true, true, true };
			Count symbolTypeCount = 0;
			bool isSubmitted = problem.submit(submissions, status, results);
			if (isSubmitted)
			{
				++attemptCount;
				switch (status)
				{
				case Status::Successful:
#if defined _DEBUG || defined DEBUG
					std::cout << Formatter::format(attemptCount, submissions, results, status);
#endif
					symbols = submissions;
					return true;
				case Status::Failed:
#if defined _DEBUG || defined DEBUG
					std::cout << Formatter::format(attemptCount, submissions, results, status);
#endif
					return true;
				case Status::Initialized:
				case Status::Generated:
				case Status::Set:
				case Status::Solving:
				default:
					for (size_t idx = 0; idx < 4; ++idx)
						switch (results[idx])
						{
						case Result::Right:
							answers[idx] = std::vector<Symbol>{ submissions[idx] };
							writingFlags[idx] = false;
							++symbolTypeCount;
							for (size_t secondaryIdx = 0; secondaryIdx < 4; ++secondaryIdx)
								if (writingFlags[secondaryIdx])
									answers[secondaryIdx].push_back(submissions[idx]);
							break;
						case Result::Misplaced:
							++symbolTypeCount;
							for (size_t secondaryIdx = 0; secondaryIdx < 4; ++secondaryIdx)
								if (secondaryIdx != idx && writingFlags[secondaryIdx])
									answers[secondaryIdx].push_back(submissions[idx]);
							break;
						case Result::Incorrect:
						default:
							break;
						}
					break;
				}
			}
			else
				return false;
			if (symbolTypeCount < 4)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << Formatter::format(attemptCount, submissions, results, answers) << std::endl;
#endif
				submissions = std::vector<Symbol>{ Symbol::BluePuzzle, Symbol::BlueLeaf, Symbol::BlueCrescent, Symbol::BlueNote };
				isSubmitted = problem.submit(submissions, status, results);
				if (isSubmitted)
				{
					++attemptCount;
					switch (status)
					{
					case Status::Successful:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						symbols = submissions;
						return true;
					case Status::Failed:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						return true;
					case Status::Initialized:
					case Status::Generated:
					case Status::Set:
					case Status::Solving:
					default:
						for (size_t idx = 0; idx < 4; ++idx)
							switch (results[idx])
							{
							case Result::Right:
								answers[idx] = std::vector<Symbol>{ submissions[idx] };
								writingFlags[idx] = false;
								++symbolTypeCount;
								for (size_t secondaryIdx = 0; secondaryIdx < 4; ++secondaryIdx)
									if (writingFlags[secondaryIdx])
										answers[secondaryIdx].push_back(submissions[idx]);
								break;
							case Result::Misplaced:
								++symbolTypeCount;
								for (size_t secondaryIdx = 0; secondaryIdx < 4; ++secondaryIdx)
									if (secondaryIdx != idx && writingFlags[secondaryIdx])
										answers[secondaryIdx].push_back(submissions[idx]);
								break;
							case Result::Incorrect:
							default:
								break;
							}
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, answers, symbolTypeCount) << std::endl;
#endif
						break;
					}
				}
				else
					return false;
			}
#if defined _DEBUG || defined DEBUG
			else
				std::cout << Formatter::format(attemptCount, submissions, results, answers, symbolTypeCount) << std::endl;
#endif
			
			/* Searching */
			while (attemptCount < MAXIMUM_ATTEMPT_COUNT)
			{
				submissions = Solver::getFirstArrangement(answers, symbolTypeCount); // This is the core code. 
				if (problem.submit(submissions, status, results))
				{
					++attemptCount;
					switch (status)
					{
					case Status::Successful:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						symbols = submissions;
						return true;
					case Status::Failed:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						return true;
					case Status::Initialized:
					case Status::Generated:
					case Status::Set:
					case Status::Solving:
					default:
						for (size_t idx = 0; idx < 4; ++idx)
							switch (results[idx])
							{
							case Result::Right:
								answers[idx] = std::vector<Symbol>{ submissions[idx] };
								break;
							case Result::Misplaced:
								if (find(answers[idx].begin(), answers[idx].end(), submissions[idx]) == answers[idx].end())
									return false;
								else
									answers[idx].erase(std::remove(answers[idx].begin(), answers[idx].end(), submissions[idx]), answers[idx].end());
								break;
							case Result::Incorrect:
								return false;
							default:
								break;
							}
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, answers) << std::endl;
#endif
						break;
					}
				}
				else
					return false;
			}
			return false;
		}
		else
			return false;
	}
};

class Helper
{
public:
	static void printHelp()
	{
		std::cout << "This is a possible password solution for the first palace of Dreamland in the ``Obi Island: Dreamland`` mobile game. " << std::endl << std::endl;
		std::cout << "1) If a non-value option or a value $x$ satisfying $x < 1.5$ is passed, the program will solve a random group. " << std::endl;
		std::cout << "2) If a value $x$ satisfying $1.5 \\leqslant x < 4095.5$ is passed, the program will solve $\\left\\lfloor x + \\cfrac{1}{2}\\right\\rfloor$ random groups. " << std::endl;
		std::cout << "3) If a value $x$ satisfying $x \\geqslant 4095.5$ is passed, the program will traverse all the 4096 groups. " << std::endl;
		std::cout << "4) If one or more groups of 4 integers within the interval $[0, 7]$ are passed, the program will solve specifically. " << std::endl;
		std::cout << "5) Otherwise, this help information will display. " << std::endl << std::endl;
		return;
	}
};



int main(int argc, char* argv[])
{
	Count groupCount = 0, successCount = 0, failureCount = 0, invalidityCount = 0, totalAttemptCount = 0;
	Problem problem{};
	std::chrono::nanoseconds totalTime = static_cast<std::chrono::nanoseconds>(0);
	if (2 == argc)
	{
		std::string argv1(argv[1]);
		std::transform(argv1.begin(), argv1.end(), argv1.begin(), [](const char ch) { return 'A' <= ch && ch <= 'Z' ? static_cast<char>(ch | 0x20) : ch; });
		if ("inf" == argv1 || "+inf" == argv1)
			groupCount = 4096;
		else if (argv1.find('.') == std::string::npos)
		{
			const std::string prefix = argv1.substr(0, 2);
			long long int x = 1;
			if ("0b" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 2);
			else if ("0o" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 8);
			else if ("0x" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 16);
			else
			{
				const char* p = argv[1];
				while ('0' == *p)
					++p;
				x = strtoll(p, nullptr, 0);
			}
			groupCount = static_cast<Count>(x >= 4096 ? 4096 : (x <= 1 ? 1 : x));
		}
		else
		{
			const long double x = round(strtold(argv[1], nullptr));
			groupCount = static_cast<Count>(x >= 4096 ? 4096U : (x <= 1 ? 1 : x));
		}
		if (groupCount <= 4095)
		{
			std::cout << "The group count has been set to " << std::to_string(groupCount) << ". " << std::endl;
			for (Count _ = 0; _ < groupCount; ++_)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << (problem.generate() ? "Successfully generated. " : "Failed to generate. ") << std::endl;
#else
				problem.generate();
#endif
				Count attemptCount = 0;
				std::vector<Symbol> answers{};
				const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
				const bool isValid = Solver::solve(problem, attemptCount, answers);
				const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
				if (isValid)
					if (answers.empty())
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "Failed to solve. " << std::endl;
#endif
						++failureCount;
					}
					else
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
						++successCount;
						totalAttemptCount += attemptCount;
						totalTime += endTime - startTime;
					}
				else
				{
#if defined _DEBUG || defined DEBUG
					std::cout << "The problem is invalid. " << std::endl;
#endif
					++invalidityCount;
				}
			}
			std::cout << "The program has conducted " << std::to_string(groupCount) << " random " << (groupCount > 1 ? "groups" : "group") << ", where " << std::to_string(successCount) << " succeeded, " << std::to_string(failureCount) << " failed, and " << std::to_string(invalidityCount) << " " << (invalidityCount > 1 ? "were" : "was") << " invalid. " << std::endl;
		}
		else
		{
			std::cout << "The program has entered the traversal mode. " << std::endl;
			for (unsigned char a = 0; a < 8; ++a)
				for (unsigned char b = 0; b < 8; ++b)
					for (unsigned char c = 0; c < 8; ++c)
						for (unsigned char d = 0; d < 8; ++d)
						{
							const std::vector<Symbol> group{ static_cast<Symbol>(a), static_cast<Symbol>(b), static_cast<Symbol>(c), static_cast<Symbol>(d) };
#if defined _DEBUG || defined DEBUG
							std::cout << (problem.set(group) ? "Successfully" : "Failed to") << " set " << Formatter::format(group) << ". " << std::endl;
#else
							problem.set(group);
#endif
							Count attemptCount = 0;
							std::vector<Symbol> answers{};
							const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
							const bool isValid = Solver::solve(problem, attemptCount, answers);
							const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
							if (isValid)
								if (answers.empty())
								{
#if defined _DEBUG || defined DEBUG
									std::cout << "Failed to solve. " << std::endl;
#endif
									++failureCount;
								}
								else
								{
#if defined _DEBUG || defined DEBUG
									std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
									++successCount;
									totalAttemptCount += attemptCount;
									totalTime += endTime - startTime;
								}
							else
							{
#if defined _DEBUG || defined DEBUG
								std::cout << "The problem is invalid. " << std::endl;
#endif
								++invalidityCount;
							}
						}
			std::cout << "The program has traversed 4096 groups, where " << std::to_string(successCount) << " succeeded, " << std::to_string(failureCount) << " failed, and " << std::to_string(invalidityCount) << " " << (invalidityCount > 1 ? "were" : "was") << " invalid. " << std::endl;
		}
	}
	else if (argc >= 5)
	{
		Count count = 4;
		std::vector<std::vector<Symbol>> groups{};
		for (int idx = 1; idx < argc; ++idx)
			if ('0' <= argv[idx][0] && argv[idx][0] <= '7')
			{
				if (count >= PASSWORD_LENGTH)
					if (groupCount >= 65535)
						break;
					else
					{
						groups.push_back(std::vector<Symbol>{ static_cast<Symbol>(argv[idx][0] - '0')});
						count = 1;
						++groupCount;
					}
				else
				{
					groups.back().push_back(static_cast<Symbol>(argv[idx][0] - '0'));
					++count;
				}
			}
		if (groupCount && groups.size() == groupCount)
			for (const std::vector<Symbol>& group : groups)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << (problem.set(group) ? "Successfully" : "Failed to") << " set " << Formatter::format(group) << ". " << std::endl;
#else
				problem.set(group);
#endif
				Count attemptCount = 0;
				std::vector<Symbol> answers{};
				const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
				const bool isValid = Solver::solve(problem, attemptCount, answers);
				const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
				if (isValid)
					if (answers.empty())
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "Failed to solve. " << std::endl;
#endif
						++failureCount;
					}
					else
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
						++successCount;
						totalAttemptCount += attemptCount;
						totalTime += endTime - startTime;
					}
				else
				{
#if defined _DEBUG || defined DEBUG
					std::cout << "The problem is invalid. " << std::endl;
#endif
					++invalidityCount;
				}
			}
		else
			Helper::printHelp();
	}
	else
		Helper::printHelp();
	if (successCount >= 1)
	{
		const long double averageTime = static_cast<long double>(totalTime.count()) / successCount;
		std::cout << "Among the successful groups, the average attempt count is " << std::to_string(totalAttemptCount) << " / " << std::to_string(successCount) << " = " << std::to_string(static_cast<long double>(totalAttemptCount) / successCount) << ", and the average time is " << std::to_string(totalTime.count()) << " / " << std::to_string(successCount) << " = " << std::to_string(averageTime) << " " << (averageTime > 1 ? "nanoseconds" : "nanosecond")  << ". " << std::endl;
	}
	const int errorLevel = !groupCount || invalidityCount ? EOF : (successCount == groupCount ? EXIT_SUCCESS : EXIT_FAILURE);
	std::cout << "Please press the enter key to exit (" << std::to_string(errorLevel) << "). " << std::endl;
	rewind(stdin);
	fflush(stdin);
	UNREFERENCED_PARAMETER(getchar());
	return errorLevel;
}