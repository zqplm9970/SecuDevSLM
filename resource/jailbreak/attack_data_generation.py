# from scenario_template_cn import *
from scenario_template import *
import random
import json


def scenario_selection(harm_action, template_type):

    class_name = f"MultiTurnAttack_{template_type}"

    # print(globals().keys())
    class_object = globals()[class_name]
    mt = class_object()
    # print(mt.system_prompt)

    messages = [
        {"role": "system", "content": mt.system_prompt},
        {"role": "user", "content": mt.sentence_1.format(action=harm_action)},
        {"role": "assistant", "content": mt.response_1},
        {"role": "user", "content": mt.sentence_2},
        {"role": "assistant", "content": mt.response_2},
        {"role": "user", "content": mt.sentence_3},
        {"role": "assistant", "content": mt.response_3},
        {"role": "user", "content": mt.sentence_4},
        {"role": "assistant", "content": mt.response_4},
        {"role": "user", "content": mt.sentence_5},
    ]

    return messages


if __name__ == "__main__":
    # with open('harmful_dict.txt', 'r', encoding='utf-8') as file:
    #     harmful_dict = json.load(file)
    # # print(harmful_dict)
    # print(harmful_dict.keys())
    #
    # for category, behaviors in harmful_dict.items():
    #     print(category)
    #     for behavior in behaviors:
    #         print(behavior)

    # harmful_action = random.choice(list(harmful_dict.keys()))
    # print(harmful_action.values())

    # template_list = ['occupation_teacher', 'occupation_police', 'occupation_detective', 'occupation_lawyer',
    #                  'occupation_priest', 'relation_friend', 'relation_neighbor', 'relation_someone',
    #                  'relation_relative', 'relation_son']
    # for template in template_list:
    #     message = scenario_selection(harmful_action, template)
    #     print(message)

    message = scenario_selection("rob a bank with friends", "relation_friend")
    print(message)
