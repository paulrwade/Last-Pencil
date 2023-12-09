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

    test_data = [
        [5, True, [2, 1, 2]],
        [20, True, [3, 2, 3, 1, 2, 3, 3, 3]],
        [30, True, [3, 2, 3, 1, 2, 3, 3, 3, 2, 1, 2, 3, 2]],
        [15, True, [8, 7]],
        [5, False, [2, 1, 2]],
        [20, False, [3, 2, 3, 1, 2, 3, 3, 3]],
        [30, False, [3, 2, 3, 1, 2, 3, 3, 3, 2, 1, 2, 3, 2]],
        [15, False, [8, 7]]
    ]

    @dynamic_test(data=test_data)
    def CheckGame(self, number, first_starts, moves):
        main = TestedProgram()
        main.start()
        output = main.execute(str(number)).replace(" ", "")

        left_name = output[output.rfind('(') + 1:output.rfind(',')]
        right_name = output[output.rfind(',') + 1:output.rfind(')')]

        prev_player, next_player = (left_name, right_name) if first_starts else (right_name, left_name)

        output = main.execute(prev_player).lower()

        lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

        if len(lines) != 2:
            return CheckResult.wrong("When the player provides the initial game conditions"
                                     ", your program should print 2 non-empty lines:\n"
                                     "one with with vertical bar symbols representing the number of pencils, "
                                     "the other with the \"*NameX* turn\" string.\n"
                                     f"{len(lines)} lines were found in the output.")

        pencils = [s.strip() for s in lines if '|' in s]
        if len(pencils) != 1:
            return CheckResult.wrong("When the player provides the initial game conditions, "
                                     "your program should print only one line with several vertical bar "
                                     "symbols ('|') representing pencils.")
        if len(list(set(pencils[0]))) != 1:
            return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|' symbol.")

        if len(pencils[0]) != int(number):
            return CheckResult.wrong("The line with pencils should contain as many '|' symbols as the player provided.")

        if not any((prev_player.lower() in s) and ("turn" in s) for s in lines):
            return CheckResult.wrong(f"When the player provides the initial game conditions"
                                     f" there should be a line in output that contains the \"{prev_player}\'s turn\""
                                     f" string if {prev_player} is the first player.")

        on_table = number
        for i in moves:
            on_table -= i
            output = main.execute(str(i)).lower()
            lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

            if on_table <= 0:
                if len(lines) != 0:
                    return CheckResult.wrong("After the last pencil is taken, there should be no output.")
                else:
                    break

            if len(lines) != 2:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "your program should print 2 non-empty lines.")

            pencils = [s.strip() for s in lines if '|' in s]
            if len(pencils) != 1:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "your program should print only one line with vertical bar symbols ('|') "
                                         "representing pencils.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")
            if len(pencils[0]) != on_table:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "the line with pencils should contain as many '|' symbols as there are "
                                         "pencils left.")

            if not any((next_player.lower() in s) and ("turn" in s) for s in lines):
                return CheckResult.wrong(f"When {prev_player} enters the number of pencils they want to remove, "
                                         f"there should be a line in the output that contains \"{next_player} turn\".")
            prev_player, next_player = next_player, prev_player
        if not main.is_finished():
            return CheckResult.wrong("Your program should not request anything when there are no pencils left.")

        return CheckResult.correct()


if __name__ == '__main__':
    LastPencilTest().run_tests()
