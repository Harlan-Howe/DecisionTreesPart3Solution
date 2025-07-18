import unittest
from typing import List

from ConditionFile import NumericCondition
from DecisionTree import DecisionTree, MAX_DIVISIONS_PER_RANGE


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.decision_tree = DecisionTree()

    def test_a_build_conditions_1(self):
        print("Starting test_a.")
        condition_list = self.decision_tree.build_conditions_for_range([200, 500, 400, 600])

        x_conditions:List[NumericCondition] = []

        y_conditions:List[NumericCondition] = []
        for condition in condition_list:
            if condition.attribute_name == "x":
                x_conditions.append(condition)
            if condition.attribute_name == "y":
                y_conditions.append(condition)

        # testing x conditions.
        # I am assuming you've added the conditions in order.
        x_diff = x_conditions[0].threshold_value - 200
        self.assertGreater(x_diff, 0, "The first division should be after the left margin.")
        for i in range(1,len(x_conditions)):
            self.assertLessEqual(abs(x_conditions[i].threshold_value - x_conditions[i-1].threshold_value - x_diff),
                                 1,
                                 "Conditions should be evenly spaced in x.")
        self.assertLess(x_conditions[-1].threshold_value, 400, "last condition in x should be less than right margin.")
        print ("  passed equal spacing in x.")

        self.assertEqual(MAX_DIVISIONS_PER_RANGE,
                         len(x_conditions),
                         f"There should be {MAX_DIVISIONS_PER_RANGE} conditions for x.")
        print("  passed x count.")

        # testing y conditions.
        # I am assuming you've added the conditions in order.
        y_diff = y_conditions[0].threshold_value - 500
        self.assertGreater(y_diff, 0, "The first division should be after the left margin.")
        for i in range(1,len(y_conditions)):
            self.assertLessEqual(abs(y_conditions[i].threshold_value - y_conditions[i-1].threshold_value-y_diff),
                                 1,
                                 "Conditions should be evenly spaced in y.")
        self.assertLess(y_conditions[-1].threshold_value, 600, "last condition in y should be less than right margin.")
        print ("  passed equal spacing in y.")
        self.assertEqual(MAX_DIVISIONS_PER_RANGE,
                         len(y_conditions),
                         f"There should be {MAX_DIVISIONS_PER_RANGE} conditions for y.")
        print("  passed y count.")
        print("Test_a completed.")

    def test_b_build_conditions_2(self):
        print("Starting test_b.")
        condition_list = self.decision_tree.build_conditions_for_range([200, 100, 205, 500])

        x_conditions: List[NumericCondition] = []
        y_conditions: List[NumericCondition] = []

        for condition in condition_list:
            if condition.attribute_name == "x":
                x_conditions.append(condition)
            if condition.attribute_name == "y":
                y_conditions.append(condition)

        # testing x conditions.
        # I am assuming you've added the conditions in order.

        self.assertEqual(x_conditions[0].threshold_value,
                         201,
                         f"The first division should be 201 but it was {x_conditions[0].threshold_value}.")
        for i in range(1, len(x_conditions)):
            self.assertEqual(
                abs(x_conditions[i].threshold_value - x_conditions[i - 1].threshold_value),
                1,
                "Conditions should be evenly spaced in x.")
        self.assertLess(x_conditions[-1].threshold_value, 205,
                        "last condition in x should be less than right margin.")
        print("  passed equal spacing in x.")

        self.assertEqual(4,
                         len(x_conditions),
                         f"There should be 4 conditions for x.")
        print("  passed x count.")

        # testing y conditions.
        # I am assuming you've added the conditions in order.
        y_diff = y_conditions[0].threshold_value - 100
        self.assertGreater(y_diff, 0, "The first division should be after the left margin.")
        for i in range(1, len(y_conditions)):
            self.assertLessEqual(
                abs(y_conditions[i].threshold_value - y_conditions[i - 1].threshold_value - y_diff),
                1,
                "Conditions should be evenly spaced in y.")
        self.assertLess(y_conditions[-1].threshold_value, 500,
                        "last condition in y should be less than right margin.")
        print("  passed equal spacing in y.")
        self.assertEqual(MAX_DIVISIONS_PER_RANGE,
                         len(y_conditions),
                         f"There should be {MAX_DIVISIONS_PER_RANGE} conditions for y.")
        print("  passed y count.")
        print("Test_b completed.")


if __name__ == '__main__':
    unittest.main()
