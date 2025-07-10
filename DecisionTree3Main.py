import copy
import random
from typing import List, Tuple

import cv2

from AnswerGroupFile import AnswerGroup
from DecisionTree import DecisionTree

DOT_RADIUS = 10

def load_map_image():
    global source_map
    source_map = cv2.imread("land&water desaturated.png")

def generate_N_training_data(N:int) -> List[AnswerGroup]:
    result: List[AnswerGroup] = []
    width = source_map.shape[1]  # this looks backwards because openCV graphics are row,col
    height = source_map.shape[0]
    AG_categories = ["x","y"]

    for i in range(N):
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)

        if source_map[y,x,0] > 128:
            result.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y],label="water"))
        else:
            result.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y], label="land"))

    return result

def generate_N_testing_data(N:int) -> Tuple[List[AnswerGroup], List[str]]:
    points: List[AnswerGroup] = []
    correct_answers: List[str] = []
    width = source_map.shape[1]  # this looks backwards because openCV graphics are row,col
    height = source_map.shape[0]
    AG_categories = ["x","y"]

    for i in range(N):
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)

        if source_map[y,x,0] > 128:
            points.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y]))
            correct_answers.append("water")
        else:
            points.append(AnswerGroup(question_name_list=AG_categories, answer_list=[x, y]))
            correct_answers.append("land")
    return points, correct_answers

def display_labeled_data(data: List[AnswerGroup]):
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



if __name__ == "__main__":
    load_map_image()
    training_data = generate_N_training_data(2000)
    # display_labeled_data(training_data)
    testing_data, testing_correct_answers = generate_N_testing_data(5000)
    tree = DecisionTree()
    tree.build_tree(training_data, [0,0,source_map.shape[1], source_map.shape[0]])

    num_correct = 0
    for i in range(len(testing_data)):
        prediction_string = tree.predict(testing_data[i])
        if prediction_string == testing_correct_answers[i]:
            num_correct += 1
        testing_data[i].set_label(prediction_string)

    print(f"Tree predicted {num_correct} out of {len(testing_data)} points, for {100*num_correct/testing_data:3.2f}%")
    display_labeled_data(testing_data)