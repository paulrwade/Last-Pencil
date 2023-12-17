import random

from hstest import *
import re


class LastPencilTest(StageTest):
    @dynamic_test()
    def CheckOutput(self):
        main = TestedProgram()
        output = main.start().lower()
        lines = output.strip().split('\n')
        if len(lines) != 1 or "how many pencils" not in output:
            return CheckResult.wrong("When the game starts, it should output only one line asking the user about the "
                                     "number of pencils they would like to use with the \"How many pencils\" string")

        output2 = main.execute("1").replace(" ", "")
        if len(output2.split()) != 1:
            return CheckResult.wrong("When the user replies with the number of pencils, the game should print 1 "
                                     "non-empty line asking who will be the first player.\n"
                                     f"{len(output2.split())} lines were found in the output.")
        if not re.match(r".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)", output2):
            return CheckResult.wrong("When the user replies with the number of pencils, the game should ask who will "
                                     "be the first player ending with the \"(\"Name1\", \"Name2\")\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckNumericNumber(self):
        main = TestedProgram()
        main.start()
        for inp in ["a", "_", "test", "|", "|||||", " ", "-", "two", "10g", "k5", "-0.2", "0.3"]:
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or ("numeric" not in output):
                return CheckResult.wrong("When the user provides the number of pencils as a non-numeric sequence, the "
                                         "game should inform user that their input is incorrect and prompt the user "
                                         "for input again with the \"The number of pencils should be numeric\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckNotZeroNumber(self):
        main = TestedProgram()
        main.start()
        for i in range(1, 6):
            output = main.execute("0").lower()
            if ("number of pencils" not in output) or ("positive" not in output):
                return CheckResult.wrong("When the user provides \"0\" as a number of pencils, the game should "
                                         "inform the user that their input is incorrect and prompt the user for input "
                                         "again with the \"The number of pencils should be positive\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckBothIncorrect(self):
        main = TestedProgram()
        main.start()
        for inp in ['0', 'a', '0', '+']:
            check_str = 'positive' if inp == '0' else 'numeric'
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or (check_str not in output):
                return CheckResult.wrong(f"When the user provides \"{inp}\" as a number of pencils, the game should "
                                         f"inform the user that their input is incorrect and prompt the user for input "
                                         f"again with the \"The number of pencils should be {check_str}\" string.")
        output2 = main.execute("1").replace(" ", "")
        if not re.match(r".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)", output2):
            return CheckResult.wrong("When the user inputs the number of pencils correctly, the game should ask "
                                     "who will be the first player ending with the \"(\"Name\", \"Name2\")\" string.")
        return CheckResult.correct()

    @dynamic_test(data=[[i, j] for i in [2, 3, 4, 5, 9, 13, 17, 21, 101] for j in [True, False]])
    def CheckGame(self, number, first_starts):
        main = TestedProgram()
        main.start()
        output = main.execute(str(number)).replace(" ", "")

        left_name = output[output.rfind('(') + 1:output.rfind(',')]
        right_name = output[output.rfind(',') + 1:output.rfind(')')]

        prev_player, next_player = (left_name, right_name) if first_starts else (right_name, left_name)

        output2 = main.execute(left_name + right_name).lower()
        if any(token not in output2 for token in ["choose between", left_name.lower(), right_name.lower()]):
            return CheckResult.wrong(f"When the user provides a name that is not '{left_name}' or '{right_name}', "
                                     f"the game should inform the user that their input is incorrect "
                                     f"and prompt the user for input again "
                                     f"with the \"Choose between '{left_name}' and '{right_name}'\" string.")

        output3 = main.execute(prev_player).lower()
        lines = [s for s in re.split(r'[\r\n]+', output3.strip()) if s != '']

        if first_starts:
            if len(lines) != 2:
                return CheckResult.wrong("When the player provides the correct initial game conditions, the program "
                                         f"should print 2 non-empty lines if {prev_player} is the first player.")
            pencils = [s.strip() for s in lines if '|' in s]
            if len(pencils) != 1:
                return CheckResult.wrong("When the player provides the correct initial game conditions, the program "
                                         "should print one line that contains vertical bar symbols "
                                         f"if {prev_player} is the first player.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|' one.")
            if len(pencils[0]) != int(number):
                return CheckResult.wrong("The line with pencils should contain as many '|' symbols as the player "
                                         "provided in the start.")

            if not any((prev_player.lower() in s) and ("turn" in s) for s in lines):
                return CheckResult.wrong(f"When the player provides the initial game conditions there should "
                                         f"be a line in the output that contains the \"{prev_player}\'s turn\" "
                                         f"string if {prev_player} is the first player.")
        else:
            if len(lines) != 5:
                return CheckResult.wrong("When the player provides the correct initial game conditions and "
                                         f"if {prev_player} goes first, your program should print 5 non-empty lines "
                                         f"in such order:\n"
                                         f"2 for {prev_player}\n"
                                         f"1 for {prev_player}'s move\n"
                                         f"2 for {next_player}")

            lines_prev = lines[:2]
            turn = lines[2].strip()
            lines_next = lines[2:]

            pencils = [s.strip() for s in lines_prev if '|' in s]

            if len(pencils) != 1:
                return CheckResult.wrong("When the player provides the correct initial game conditions, "
                                         "the program should print one line for each player, that contains '|' "
                                         f"symbols if {prev_player} is the first player.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")
            if len(pencils[0]) != number:
                return CheckResult.wrong("When the player provides the correct initial game conditions,"
                                         f"the {prev_player}'s line with pencils should contain as many '|' symbols "
                                         f"as the player provided.")

            if not any((prev_player.lower() in s) and ("turn" in s) for s in lines_prev):
                return CheckResult.wrong(f"When the player provides the correct initial game conditions there "
                                         f"should be a line in the output for the {prev_player}'s turn that contains "
                                         f"\"{prev_player}\" and \"turn\" strings if '{prev_player}' is the "
                                         f"first player.")

            if turn not in ['1', '2', '3']:
                return CheckResult.wrong(f"When the player provides the correct initial game conditions and the first "
                                         f"player is {prev_player}, your program should print 5 non-empty lines, third "
                                         f"of them is {prev_player}'s turn, so it should be either '1', '2' or '3'.")

            bot_take = (number - 1) % 4

            if bot_take != 0 and int(turn) != bot_take:
                return CheckResult.wrong(f"The {prev_player}'s move doesn't follow a winning strategy. Example:\n"
                                         f"If there are {number} pencils left and it's {prev_player}'s turn, he "
                                         f"takes {turn} pencils instead of {bot_take}.")

            pencils = [s.strip() for s in lines_next if '|' in s]

            if len(pencils) != 1:
                return CheckResult.wrong("When the player provides the correct initial game conditions, there "
                                         "should be exactly one line in the output for each player that contains '|' "
                                         f"symbols if {prev_player} is the first player.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")
            if len(pencils[0]) != number - int(turn):
                return CheckResult.wrong("When the player provides the correct initial game conditions,"
                                         f"the {next_player}'s line with pencils should contain as many '|' symbols as "
                                         f"there is left after the {prev_player}'s turn.")

            if not any((next_player.lower() in s) and ("turn" in s) for s in lines_next):
                return CheckResult.wrong(f"When the player provides the correct initial game conditions there "
                                         f"should be a line in the output for {next_player}'s turn that contains "
                                         f"\"{next_player}\" and \"turn\" substrings if '{prev_player}' is the "
                                         f"first player.")

        on_table = number
        if not first_starts:
            on_table -= int(lines[2])
            prev_player, next_player = next_player, prev_player

        for j in ["4", "a", "0", "-1", "_", "|", "|||||"]:
            output = main.execute(j).lower()
            if any(token not in output for token in ['possible values', '1', '2', '3']):
                return CheckResult.wrong(f"If the player enters values different from "
                                         f"'1', '2', or '3', the game should inform the user that "
                                         f"their input is incorrect and prompt the user for input again "
                                         f"with the \"Possible values: '1', '2', '3'\" string.")
            if prev_player.lower() not in output and next_player.lower() in output:
                return CheckResult.wrong(f"When {prev_player} provides values different from "
                                         f"'1', '2', or '3', you need to prompt {prev_player} for input again.\n"
                                         f"However, the {next_player}'s name was found in your output.")

        while on_table > 0:
            i = random.randint(1, 3)
            output = main.execute(str(i)).lower()
            if i >= on_table:
                if on_table != i:
                    if any(token not in output for token in ['too many', 'pencils']):
                        return CheckResult.wrong("If the player enters the number of pencils that is greater than the "
                                                 "current number of pencils on the table, the game should inform the "
                                                 "user that their input is incorrect and prompt the user for input "
                                                 "again with the \"too many pencils\" string.")

                    output = main.execute(str(on_table)).lower()
                lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

                if len(lines) != 1 or (next_player.lower() not in lines[0]) or (
                        'win' not in lines[0] and 'won' not in lines[0]):
                    return CheckResult.wrong("When the last pencil is taken, the program should print one line that "
                                             "informs who is the winner in this game with \"*Name*\" and "
                                             "\"win\"/\"won\" strings.")

                if not main.is_finished():
                    return CheckResult.wrong("Your program should not request anything when there are no pencils left.")

                return CheckResult.correct()

            on_table -= i
            lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

            if on_table == 1:
                if len(lines) != 4:
                    return CheckResult.wrong(f"if {next_player} is left with 1 pencil "
                                             f"after {prev_player} inputs the number of pencils they will take, "
                                             f"your program should print 4 "
                                             f"non-empty lines in such order:\n"
                                             f"2 for {next_player}\n"
                                             f"1 for {next_player}'s move\n"
                                             f"1 for game-results")
                lines_prev = lines[:2]
                turn = lines[2].strip()
                result = lines[3]

                pencils = [s.strip() for s in lines_prev if '|' in s]

                if len(pencils) != 1:
                    return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                             "there should be exactly one line in the output for each player that "
                                             "contains '|'.")
                if len(list(set(pencils[0]))) != 1:
                    return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")
                if len(pencils[0]) != on_table:
                    return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                             f"the lines with pencils for {next_player} should contain as many '|' "
                                             f"symbols as there are pencils left.")

                if not any((next_player.lower() in s) and ("turn" in s) for s in lines_prev):
                    return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                             f"there should be a line in the output for {next_player}'s turn that "
                                             f"contains \"{next_player}\" and \"turn\" substrings.")
                if turn != "1":
                    return CheckResult.wrong(f"If {next_player} is left with 1 pencil, they can't take any other "
                                             f"number of pencils except for 1.")
                if (prev_player.lower() not in result) or ('win' not in result and 'won' not in result):
                    return CheckResult.wrong("When the last pencil is taken, the program should print one line that "
                                             "informs who is the winner in this game with \"*Name*\" and "
                                             "\"win\"/\"won\" strings.")

                if not main.is_finished():
                    return CheckResult.wrong("Your program should not request anything when there are no pencils left.")

                return CheckResult.correct()

            if len(lines) != 5:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                         "your program should print 5 non-empty lines "
                                         f"in such order:\n"
                                         f"2 for {next_player}\n"
                                         f"1 for {next_player}'s move\n"
                                         f"2 for {prev_player}")
            lines_prev = lines[:2]
            turn = lines[2].strip()
            lines_next = lines[2:]

            pencils = [s.strip() for s in lines_prev if '|' in s]

            if len(pencils) != 1:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, there "
                                         "should be exactly one line in output for each player, that contains '|'.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The pencils-lines should not contain any other symbols except the '|'.")
            if len(pencils[0]) != on_table:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                         f"the lines with pencils for {next_player} should contain as many '|' symbols "
                                         f"as there are pencils left.")

            if not any((next_player.lower() in s) and ("turn" in s) for s in lines_prev):
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, "
                                         f"there should be a line in output for the {next_player}'s turn that contains "
                                         f"\"{next_player}\" and \"turn\" substrings.")

            if turn not in ['1', '2', '3']:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, your "
                                         f"program should print 5 non-empty lines, third of them is {prev_player}'s "
                                         "turn, so it should be either '1', '2' or '3'.")

            bot_take = (on_table - 1) % 4
            if bot_take != 0 and int(turn) != bot_take:
                return CheckResult.wrong(f"The {next_player}'s move doesn't follow a winning strategy. Example:\n"
                                         f"If there are {on_table} pencils left and it's {next_player}'s turn, they "
                                         f"take {turn} pencils instead of {bot_take}.")
            on_table -= int(turn)

            pencils = [s for s in lines_next if '|' in s]

            if len(pencils) != 1:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, there "
                                         "should be exactly one line in output for each player that contains '|'.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")
            if len(pencils[0]) != on_table:
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, the line "
                                         f"with pencils for {prev_player} should contain as many '|' symbols as there "
                                         f"are pencils left.")

            if not any((prev_player.lower() in s) and ("turn" in s) for s in lines_next):
                return CheckResult.wrong(f"After {prev_player} inputs the number of pencils they will take, there "
                                         f"should be a line in the output for {prev_player}'s turn containing "
                                         f"\"{prev_player}\" and \"turn\" substrings.")


if __name__ == '__main__':
    LastPencilTest().run_tests()
