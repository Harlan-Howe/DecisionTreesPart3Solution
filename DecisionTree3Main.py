import copy
import random
from typing import List, Tuple

import cv2
import numpy as np

from AnswerGroupFile import AnswerGroup
from DecisionTree import DecisionTree

DOT_RADIUS = 10

def load_map_image():
    global source_map
    source_map = cv2.imread("land&water desaturated.png")

def generate_N_data(N:int, label_data:bool = True) -> Tuple[List[AnswerGroup], List[str]]:
    """
    polls the map to create N AnswerGroups, and a matching list of the correct classifications.
    :param N: the number of AnswerGroups to generate
    :param label_data: if True, the AnswerGroups should have a label that matches the correct classification. Otherwise,
    the AnswerGroup should have a label = None.
    :return: A list of AnswerGroups, perhaps labeled, and a matching list of strings indicating land or water.
    """
    result: List[AnswerGroup] = []
    correct_answers: List[str] = []
    width = source_map.shape[1]  # this looks backwards because openCV graphics are row,col
    height = source_map.shape[0]
    AG_categories = ["x","y"]

    for i in range(N):
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)

        if source_map[y,x,0] > 128:
            result.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y]))
            correct_answers.append("water")
        else:
            result.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y]))
            correct_answers.append("land")

        if label_data:
            result[-1].set_label(correct_answers[-1])

    return result, correct_answers


def display_labeled_data(data: List[AnswerGroup]) -> np.ndarray:
    """
    draws a copy of the map with the given data appearing as dots on the map.
    (Note: This graphic is HUGE, so it will appear shrunk on the screen, which is why we are using large radius dots.)
    :param data: a list of AnswerGroups that are labeled "water" or "land".
    :return: a copy of the map, in case we want to draw more stuff on it.
    """
    canvas = copy.deepcopy(source_map)
    for ag in data:
        if ag.get_label()=="water":
            cv2.circle(img=canvas,
                       center= (ag.get_attribute_for_name("x"), ag.get_attribute_for_name("y")),
                       radius= DOT_RADIUS,
                       color=(255,0,0),
                       thickness = -1)
        if ag.get_label()=="land":
            cv2.circle(img=canvas,
                       center= (ag.get_attribute_for_name("x"), ag.get_attribute_for_name("y")),
                       radius= DOT_RADIUS,
                       color=(0,255,0),
                       thickness = -1)
    cv2.imshow("Map",canvas)
    cv2.waitKey(0)
    cv2.destroyWindow("Map")
    return canvas


if __name__ == "__main__":
    # generate labeled training data and show the map with this data.
    SHOW_DEBUG_IMAGE = True
    N_TRAINING = 3000
    N_TESTING = 7500
    load_map_image()
    training_data, training_answers = generate_N_data(N=N_TRAINING, label_data = True)
    training_map:np.ndarray = display_labeled_data(training_data)

    # build the tree.
    tree = DecisionTree()
    tree.build_tree(training_data, [0,0,source_map.shape[1], source_map.shape[0]],debug_canvas=training_map)
    print(f"Tree generated with max depth of {tree.max_depth_used}.")

    if SHOW_DEBUG_IMAGE:
        cv2.imshow("trained",training_map)
        cv2.waitKey()
        cv2.destroyWindow("trained")

    # check how well the tree predicts the data.
    testing_data, testing_correct_answers = generate_N_data(N=N_TESTING, label_data = False)
    num_correct = 0
    for i in range(len(testing_data)):
        prediction_string = tree.predict(testing_data[i])
        if prediction_string == testing_correct_answers[i]:
            num_correct += 1
        testing_data[i].set_label(prediction_string)
    print(f"Tree predicted {num_correct} out of {len(testing_data)} points, for {100*num_correct/len(testing_data):3.2f}%")
    display_labeled_data(testing_data)