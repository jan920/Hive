import sys

sys.path.append('../Hive/')

from board.stones import Stone

from board.globals import FREE_SPACE


class TestMoves:
    should_pass = []
    should_fail = []
    cases = []

    pass_case0 = [0]
    fail_case0 = []
    circle_stones_case0 = []
    for c in range(1):
        circle_stones_case0 += [Stone(colour="B", index=c, kind="Q")]
    should_pass += [pass_case0]
    should_fail += [fail_case0]
    cases += [circle_stones_case0]



    pass_case1 = []
    fail_case1 = [1]
    circle_stones_case1 = []
    for c in range(3):
        circle_stones_case1 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case1[0].connections[2] = circle_stones_case1[1]
    circle_stones_case1[1].connections[5] = circle_stones_case1[0]
    circle_stones_case1[1].connections[2] = circle_stones_case1[2]
    circle_stones_case1[2].connections[5] = circle_stones_case1[1]
    should_pass += [pass_case1]
    should_fail += [fail_case1]
    cases += [circle_stones_case1]

    pass_case2 = [0, 1, 2]
    fail_case2 = []
    circle_stones_case2 = []
    for c in range(3):
        circle_stones_case2 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case2[0].connections[2] = circle_stones_case2[1]
    circle_stones_case2[1].connections[5] = circle_stones_case2[0]
    circle_stones_case2[0].connections[1] = circle_stones_case2[2]
    circle_stones_case2[2].connections[4] = circle_stones_case2[0]
    circle_stones_case2[1].connections[0] = circle_stones_case2[2]
    circle_stones_case2[2].connections[3] = circle_stones_case2[1]
    should_pass += [pass_case2]
    should_fail += [fail_case2]
    cases += [circle_stones_case2]

    pass_case3 = [0, 1, 2, 3, 4, 5]
    fail_case3 = []
    circle_stones_case3 = []
    for c in range(6):
        circle_stones_case3 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case3[0].connections[2] = circle_stones_case3[1]
    circle_stones_case3[1].connections[5] = circle_stones_case3[0]
    circle_stones_case3[1].connections[3] = circle_stones_case3[2]
    circle_stones_case3[2].connections[0] = circle_stones_case3[1]
    circle_stones_case3[2].connections[4] = circle_stones_case3[3]
    circle_stones_case3[3].connections[1] = circle_stones_case3[2]
    circle_stones_case3[3].connections[5] = circle_stones_case3[4]
    circle_stones_case3[4].connections[2] = circle_stones_case3[3]
    circle_stones_case3[4].connections[0] = circle_stones_case3[5]
    circle_stones_case3[5].connections[3] = circle_stones_case3[4]
    circle_stones_case3[5].connections[1] = circle_stones_case3[0]
    circle_stones_case3[0].connections[4] = circle_stones_case3[5]
    should_pass += [pass_case3]
    should_fail += [fail_case3]
    cases += [circle_stones_case3]

    pass_case4 = [0,2,3,4]
    fail_case4 = [1]
    circle_stones_case4 = []
    for c in range(5):
        circle_stones_case4 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case4[0].connections[2] = circle_stones_case4[1]
    circle_stones_case4[1].connections[5] = circle_stones_case4[0]
    circle_stones_case4[0].connections[1] = circle_stones_case4[2]
    circle_stones_case4[2].connections[4] = circle_stones_case4[0]
    circle_stones_case4[1].connections[0] = circle_stones_case4[2]
    circle_stones_case4[2].connections[3] = circle_stones_case4[1]
    circle_stones_case4[1].connections[2] = circle_stones_case4[3]
    circle_stones_case4[3].connections[5] = circle_stones_case4[1]
    circle_stones_case4[3].connections[4] = circle_stones_case4[4]
    circle_stones_case4[4].connections[1] = circle_stones_case4[3]
    circle_stones_case4[4].connections[0] = circle_stones_case4[1]
    circle_stones_case4[1].connections[3] = circle_stones_case4[4]
    should_pass += [pass_case4]
    should_fail += [fail_case4]
    cases += [circle_stones_case4]

    pass_case5 = []
    fail_case5 = [1]
    circle_stones_case5 = []
    for c in range(4):
        circle_stones_case5 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case5[0].connections[2] = circle_stones_case5[1]
    circle_stones_case5[1].connections[5] = circle_stones_case5[0]
    circle_stones_case5[1].connections[1] = circle_stones_case5[2]
    circle_stones_case5[2].connections[4] = circle_stones_case5[1]
    circle_stones_case5[1].connections[3] = circle_stones_case5[3]
    circle_stones_case5[3].connections[0] = circle_stones_case5[1]
    should_pass += [pass_case5]
    should_fail += [fail_case5]
    cases += [circle_stones_case5]

    pass_case6 = [1,2,3,4,5]
    fail_case6 = [0]
    circle_stones_case6 = []
    for c in range(7):
        circle_stones_case6 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case6[0].connections[2] = circle_stones_case6[1]
    circle_stones_case6[1].connections[5] = circle_stones_case6[0]
    circle_stones_case6[1].connections[3] = circle_stones_case6[2]
    circle_stones_case6[2].connections[0] = circle_stones_case6[1]
    circle_stones_case6[2].connections[4] = circle_stones_case6[3]
    circle_stones_case6[3].connections[1] = circle_stones_case6[2]
    circle_stones_case6[3].connections[5] = circle_stones_case6[4]
    circle_stones_case6[4].connections[2] = circle_stones_case6[3]
    circle_stones_case6[4].connections[0] = circle_stones_case6[5]
    circle_stones_case6[5].connections[3] = circle_stones_case6[4]
    circle_stones_case6[5].connections[1] = circle_stones_case6[0]
    circle_stones_case6[0].connections[4] = circle_stones_case6[5]
    circle_stones_case6[0].connections[0] = circle_stones_case6[6]
    circle_stones_case6[6].connections[3] = circle_stones_case6[0]
    should_pass += [pass_case6]
    should_fail += [fail_case6]
    cases += [circle_stones_case6]

    pass_case7 = [0,1,2,3,4,5,6,7,8,9]
    fail_case7 = []
    circle_stones_case7 = []
    for c in range(10):
        circle_stones_case7 += [Stone(colour="B", index=c, kind="Q")]
    circle_stones_case7[0].connections[2] = circle_stones_case7[1]
    circle_stones_case7[1].connections[5] = circle_stones_case7[0]
    circle_stones_case7[1].connections[3] = circle_stones_case7[2]
    circle_stones_case7[2].connections[0] = circle_stones_case7[1]
    circle_stones_case7[2].connections[4] = circle_stones_case7[3]
    circle_stones_case7[3].connections[1] = circle_stones_case7[2]
    circle_stones_case7[3].connections[5] = circle_stones_case7[4]
    circle_stones_case7[4].connections[2] = circle_stones_case7[3]
    circle_stones_case7[4].connections[0] = circle_stones_case7[5]
    circle_stones_case7[5].connections[3] = circle_stones_case7[4]
    circle_stones_case7[5].connections[1] = circle_stones_case7[0]
    circle_stones_case7[0].connections[4] = circle_stones_case7[5]
    circle_stones_case7[0].connections[0] = circle_stones_case7[6]
    circle_stones_case7[6].connections[3] = circle_stones_case7[0]
    circle_stones_case7[6].connections[5] = circle_stones_case7[7]
    circle_stones_case7[7].connections[2] = circle_stones_case7[6]
    circle_stones_case7[7].connections[4] = circle_stones_case7[8]
    circle_stones_case7[8].connections[1] = circle_stones_case7[7]
    circle_stones_case7[8].connections[3] = circle_stones_case7[9]
    circle_stones_case7[9].connections[0] = circle_stones_case7[8]
    circle_stones_case7[9].connections[2] = circle_stones_case7[5]
    circle_stones_case7[5].connections[5] = circle_stones_case7[9]
    should_pass += [pass_case7]
    should_fail += [fail_case7]
    cases += [circle_stones_case7]

    """
    def test_count_holes(self):
        stone1 = Stone("B", 1, "Q")
        stone1.connections = [1, 1, 1, 1, 1, 1]
        stone2 = Stone("B", 1, "Q")
        stone2.connection = [FREE_SPACE, 1, FREE_SPACE, 1, FREE_SPACE, 1]
        stone3 = Stone("B", 1, "Q")
        stone3.connections = [FREE_SPACE, 1, 1, 1, 1, 1]
        stone4 = Stone("B", 1, "Q")
        stone4.connection = [FREE_SPACE, 1, FREE_SPACE, 1, 1, 1]
        assert
    """
    def test_is_movable(self):
        for case_number, case in enumerate(self.cases):
            if case_number in []:
                pass
            else:
                for stone_number, stone in enumerate(case):
                    print("case: %r, stone: %r" % (case_number, stone_number))
                    if stone_number in self.should_pass[case_number]:
                        assert stone.is_movable() is True
                    elif stone_number in self.should_fail[case_number]:
                        assert stone.is_movable() is False
                    else:
                        pass
