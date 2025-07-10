import time
from typing import Optional, List, Tuple, Dict

from AnswerGroupFile import AnswerGroup
from ConditionFile import NumericCondition
from NodeFile import GenericNode, BranchNode, LeafNode

MAX_DIVISIONS_PER_RANGE = 9
MAX_DEPTH = 4
MIN_ITEMS_PER_BRANCH_NODE = 5
VERBOSE = True

class DecisionTree:

    def __init__(self):
        self.decision_tree_root: Optional[GenericNode] = None

    def build_tree(self, training_data: List[AnswerGroup], bounds: List[int]|Tuple[int, int, int, int]):
        print(f"I am about to build a tree with {len(training_data)} data points.")
        start_time = time.perf_counter()
        self.decision_tree_root = self.make_node_for_instances_at_depth(answergroup_list=training_data,
                                                                        depth = 0,
                                                                        range=bounds,
                                                                        verbose = VERBOSE)
        end_time = time.perf_counter()
        print(f"Tree built in {(end_time-start_time):0.6f} seconds.")

    def build_conditions_for_range(self, range: List[int]|Tuple[int, int, int, int]) -> List[NumericCondition]:
        """
        builds a collection of "Condition" objects to split this range into up to MAX_DIVISIONS_PER_RANGE slices in the
        x and y dimensions.
        :param range: (x_min, y_min, x_max, y_max) - max is assumed to be >= min.
        :return: a list of x and y conditions for this range.
        """
        x_division_size = max(1, int((range[2] - range[0]) / (MAX_DIVISIONS_PER_RANGE)))
        y_division_size = max(1, int((range[3] - range[1]) / (MAX_DIVISIONS_PER_RANGE)))

        conditions_out: List[NumericCondition] = []
        x = range[0]+x_division_size
        while x < range[1]:
            conditions_out.append(NumericCondition("x", x))
            x+= x_division_size

        y = range[1]+y_division_size
        while y < range[3]:
            conditions_out.append(NumericCondition("y", y))
            y+= y_division_size

        return conditions_out

    def split_answer_groups_by_condition(self, groups: List[AnswerGroup], condition: NumericCondition) -> Tuple[List[AnswerGroup], List[AnswerGroup]]:
        """
        loops through all the AnswerGroup instances in groups and copies each one into either "yes" or "no" lists based
        on whether they meet the given Condition. The original group is unchanged.
        :param groups: a list of answergroups
        :param condition: a condition to apply to each of the answergroups
        :return: a list of the ag's that meet the condition, and a list of the ag's that don't meet the condition.

        note: these conditions are spatial (x/y), NOT labels (land vs. water).
        """
        yes_list: List[AnswerGroup] = []
        no_list: List[AnswerGroup] = []

        # TODO: You write this.

        return yes_list, no_list

    def counts_per_label(self, groups: List[AnswerGroup]) -> Dict[str,int]:
        """
        counts up the number of "land" and "water" labels in the training groups given
        :param groups: AnswerGroups, each with a label of "land" or "water"
        :return: a dictionary with the number of land labels and the number of water labels.
        """
        counts = {"land":0, "water":0}

        for ag in groups:
            counts[ag.get_label()] += 1
        return counts

    def all_labels_in_group_match(self, groups: List[AnswerGroup]) -> bool:
        """
        determines whether these groups are all "land" or all "water"
        :param groups: a list of labeled answer groups
        :return: whether they all have the same label.
        """
        # Note: we could have called counts_per_label to see whether either count was zero, but this is faster.
        previous = None
        for ag in groups:
            if previous is not None and previous != ag.get_label():
                return False
            previous = ag.get_label()
        return True

    def get_most_frequent_label_in_list(self, groups: List[AnswerGroup]) -> str:
        """
        returns the label that appears most often in this collection of labeled AnswerGroups. If it is a tie, selects
        "land."
        :param groups: a list of AnswerGroups, each labeled "land" or "water".
        :return: either "land" or "water".
        """
        counts = self.counts_per_label(groups)
        if counts["water"] > counts["land"]:
            return "water"
        return "land"

    def gini_coefficient_for_list(self, answergroup_list: List[AnswerGroup]) -> float:
        """
        Find the gini coefficient for the given list of AnswerGroups, based on their labels.
        1 - Pa**2 + Pb**2 + Pc**2 +...   where Pa = Num "a" labels/total number of labels.
        (Note: "**2" means "Squared" in python.)
        :param answergroup_list: the list to consider
        :return: the gini coefficient of that list.
        """
        N = len(answergroup_list)  # total number of labels

        if N == 0:  # if this is an empty list, bail out now so we don't divide by zero later.
            return 0

        # get the dictionary of label_names --> number of that label found...
        # e.g., {"land": 12, "water": 4}
        label_counts = self.counts_per_label(groups=answergroup_list)

        # TODO: Start with gini = 1, and then loop through self.category_names and find P for each category.
        #  Subtract P**2 from gini each time.
        # Note, since we only have two labels in this program, this may reduce to something simple and may not need a
        # loop.
        gini = 1

        return gini

    def make_node_for_instances_at_depth(self,
                                         answergroup_list: List[AnswerGroup],
                                         depth: int,
                                         range: List[int]|Tuple[int, int, int, int],
                                         verbose=False) -> GenericNode:
        """
        creates a Node (either a LeafNode or a BranchNode) based on the collection of answergroups given.
        A leafnode will be created if the size of the answergroup is small, if the depth is at the max depth, or if
        all the answergroups given have the same label.

        If this is going to be a LeafNode, then it will base it on the majority of labels in the answergroup_list.
        If this is going to be a BranchNode, then it will be one that generates its own "children" (yes/no) Nodes.
        :param answergroup_list: a list of answergroups to consider when making this Node.
        :param depth: the depth in the tree where this node will go. Used to keep track of when to stop!
        :return: The Node we are creating!
        """
        N = len(answergroup_list)
        if verbose:
            print(f"I've been asked to make a node at depth {depth}, using {N} AnswerGroups.")

        # checks whether this is one of the three conditions to make a leaf node.
        if depth == MAX_DEPTH or N < MIN_ITEMS_PER_BRANCH_NODE or self.all_labels_in_group_match(answergroup_list):
            most_frequent_label = self.get_most_frequent_label_in_list(answergroup_list)
            if verbose:
                print(f"I'll make a LeafNode: [[{most_frequent_label}]]")
            return LeafNode(most_frequent_label, depth=depth)

        min_gini_index = 1000  # a ridiculously high number to start; we're likely to find values less than one.
        best_condition = None
        best_yes_group = None
        best_no_group = None

        condition_list = self.build_conditions_for_range(range)

        # loop through all the conditions in our list of possible conditions.
        for condition in condition_list:
            # use this condition to split our list of AnswerGroups in two
            (yes_choices, no_choices) = self.split_answer_groups_by_condition(answergroup_list, condition)

            # get some statistics about the two sublists we just made:
            yes_count = len(yes_choices)
            no_count = len(no_choices)
            p_yes = yes_count / N
            p_no = no_count / N
            gini_yes: float = self.gini_coefficient_for_list(yes_choices)
            gini_no: float = self.gini_coefficient_for_list(no_choices)

            # TODO #5: based on "p_yes," "p_no," "gini_yes," and "gini_no," calculate the gini index for this choice.
            #   if this gini_index is better than the others we've seen so far, update "best_condition," "best_yes_group,"
            #   "best_no_group" and "min_gini_index"

        if verbose:
            print(f"\tThe best condition was: {best_condition}, which had a low gini Index of {min_gini_index:3.3}.")
            print(f"\tThis split the dataset into {len(best_yes_group)} 'yes' values with a gini coefficient of ",
                  end="")
            print(
                f"{self.gini_coefficient_for_list(best_yes_group):3.3} and {len(best_no_group)} 'no' values with a gini ",
                end="")
            print(f"coefficient of {self.gini_coefficient_for_list(best_no_group):3.3}.")

        # make the node we're about to return, based on the favorite condition we just found.
        result = BranchNode(best_condition, depth=depth)

        # build subranges - how have we just split the rectangle on the map into two?
        # reminder: we have been asking whether points are greater than the threshold_value.
        if best_condition.attribute_name == "x":
            no_range = (range[0],range[1],best_condition.threshold_value, range[3])  # left
            yes_range = (best_condition.threshold_value, range[1], range[2], range[3]) # right
        else:
            no_range = (range[0],range[1], range[2], best_condition.threshold_value) # top
            yes_range = (range[0], best_condition.threshold_value, range[2], range[3]) # bottom

        # but before we return it, have it create and connect the sub nodes for yes and no. (recursive)
        result.set_yes_node(self.make_node_for_instances_at_depth(answergroup_list=best_yes_group,
                                                                  depth=depth + 1,
                                                                  range=yes_range,
                                                                  verbose=verbose))
        result.set_no_node(self.make_node_for_instances_at_depth(answergroup_list=best_no_group,
                                                                 depth=depth + 1,
                                                                 range=no_range,
                                                                 verbose=verbose))

        # now that we have a fully-formed node and its children, give it back to the method that called this one.
        return result

    def predict(self, answer_group: AnswerGroup) -> str:
        return self.decision_tree_root.predict(answer_group)