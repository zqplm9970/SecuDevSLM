from transformers import AutoTokenizer, AutoModelForCausalLM
from attack_data_generation import scenario_selection
import json
import random
import os
import pandas as pd


excel_path = "/home/lizijun/data/model_list.xlsx"
df = pd.read_excel(excel_path)
model_list = df["<=2B"].dropna().tolist()

index = 0      # 当前从哪个模型开始跑
now_index = index
for model_name in model_list[index: ]:


    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    print(f" {now_index}: {model_name}")
    now_index += 1

    class MultiTurnAttackFiveTurn:
        def __init__(self, message):
            self.messages = message

        def format_messages(self):
            """
            Format the messages into a single text input for the model.
            """
            formatted_messages = ""
            for message in self.messages:
                if message["role"] == "system":
                    formatted_messages += f"System: {message['content']}\n"
                elif message["role"] == "user":
                    formatted_messages += f"User: {message['content']}\n"
                elif message["role"] == "assistant":
                    formatted_messages += f"Assistant: {message['content']}\n"
            return formatted_messages

        def run_dialogue(self):
            """
            Inject the messages into the model and generate the next response.
            """
            formatted_messages = self.format_messages()
            inputs = tokenizer(formatted_messages, return_tensors="pt", truncation=True)

            # Generate model response
            outputs = model.generate(inputs["input_ids"], max_length=1024, do_sample=True, temperature=0.7)

            # Decode the last assistant's response
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract the last assistant's response
            last_response = response.split("Assistant:")[-1].strip()

            # print(last_response)
            return last_response


    if __name__ == "__main__":
        # conversation = MultiTurnAttackRelationFriendFiveTurn()    # test

        # Chinese dict
        # with open('/home/lizijun/llm_data_poison/attack_tool/multi_dialogue_jailbreak/harmful_dict_cn.txt', 'r', encoding='utf-8') as file:
        #     harmful_dict = json.load(file)
        # print(harmful_dict)

        # English dict
        with open('/home/lizijun/llm_data_poison/attack_tool/multi_dialogue_jailbreak/harmful_dict_en.txt', 'r', encoding='utf-8') as file:
            harmful_dict = json.load(file)
        # print(harmful_dict)

        scenario_list = ['occupation_teacher', 'occupation_police', 'occupation_detective', 'occupation_lawyer',
                        'occupation_priest', 'relation_friend', 'relation_neighbor', 'relation_someone',
                        'relation_relative', 'relation_son']

        if not os.path.exists(f"/home/lizijun/llm_data_poison/attack_tool/multi_dialogue_jailbreak/{model_name}_result"):
            os.makedirs(f"/home/lizijun/llm_data_poison/attack_tool/multi_dialogue_jailbreak/{model_name}_result")


        for category, actions in harmful_dict.items():
            catagory_path = os.path.join(f"/home/lizijun/llm_data_poison/attack_tool/multi_dialogue_jailbreak/{model_name}_result", category)
            if not os.path.exists(catagory_path):
                os.makedirs(catagory_path)

            for action in actions:
                action_file_path = os.path.join(catagory_path, f"{action}.json")
                action_data = {scenario: [] for scenario in scenario_list}

                for scenario in scenario_list:
                    message = scenario_selection(action, scenario)

                    conversation = MultiTurnAttackFiveTurn(message)
                    final_response = conversation.run_dialogue()
                    if final_response:
                        plan_start = final_response.find("1.")
                        if plan_start != -1:
                            final_response = final_response[plan_start:]
                    print(f"{model_name} Final Response:")
                    print(final_response)

                    action_data[scenario] = final_response

                with open(action_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(action_data, json_file, ensure_ascii=False, indent=4)

