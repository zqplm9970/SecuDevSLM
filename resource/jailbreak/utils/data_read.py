import os
import json


def read_and_transform_data(root_dir, output_dir):
    index = 0
    for model_category in os.listdir(root_dir):
        model_category_path = os.path.join(root_dir, model_category)
        print(f"Processing category: {model_category_path}")
        if os.path.isdir(model_category_path):
            for model in os.listdir(model_category_path):
                model_path = os.path.join(model_category_path, model)
                print(f"Processing model: {model_path}")
                if os.path.isdir(model_path) and model.endswith("_result"):
                    model_name = model.replace("_result", "")
                    final_result_path = os.path.join(output_dir, model_category + "/samples", model_name + "_ans_samples.json")
                    os.makedirs(os.path.dirname(final_result_path), exist_ok=True)

                    all_data = []

                    for category in os.listdir(model_path):
                        category_path = os.path.join(model_path, category)

                        if os.path.isdir(category_path):
                            for behavior_file in os.listdir(category_path):
                                if behavior_file.endswith(".json"):
                                    behavior_path = os.path.join(category_path, behavior_file)



                                    with open(behavior_path, "r", encoding="utf-8") as f:
                                        data = json.load(f)
                                        for template, text in data.items():
                                            all_data.append({
                                                "model": model_name,
                                                "class": category,
                                                "behavior": behavior_file.replace(".json", ""),
                                                "template": template,
                                                "text": text
                                            })

                    if not all_data:
                        print(f"Warning: No data to save for {model_category}/{model_name}.")
                    else:
                        index += 1
                        print(f"Now is ------ {index}: {model_category}/{model_name} ------")

                        try:
                            if not os.path.exists(os.path.dirname(final_result_path)):
                                print(f"Error: Directory {os.path.dirname(final_result_path)} does not exist.")
                            else:
                                with open(final_result_path, "w", encoding="utf-8") as out_file:
                                    json.dump(all_data, out_file, ensure_ascii=False, indent=4)
                                print(f"Successfully saved: {final_result_path}")
                        except Exception as e:
                            print(f"Error saving file {final_result_path}: {e}")


root_dir = "../model_result"
output_dir = "../jailbreak_result"

read_and_transform_data(root_dir, output_dir)
