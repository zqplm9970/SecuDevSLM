import os
from sentence_transformers import SentenceTransformer, util
import json
import torch  

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SentenceTransformer('bert-base-nli-mean-tokens')
model.to(device)


input_dir = "../jailbreak_result"
index = 0

with open("target_samples.json", "r", encoding="utf-8") as f:
    target_data = json.load(f)
target_dict = {(item["class"], item["behavior"]): item["text"] for item in target_data}

for model_category in os.listdir(input_dir):
    model_category_path = os.path.join(input_dir, model_category)


    if os.path.isdir(model_category_path):
        samples_dir = os.path.join(model_category_path, "samples")


        if os.path.isdir(samples_dir):

            for model_file in os.listdir(samples_dir):
                if model_file.endswith("_ans_samples.json"):
                    model_file_path = os.path.join(samples_dir, model_file)


                    with open(model_file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    model_similarity = []
                    model_data = {}


                    for item in data:
                        sample_model = item['model']
                        class_name = item["class"]
                        behavior_name = item["behavior"]
                        template = item['template']

                        key = (sample_model, class_name, behavior_name)

                        if key not in model_data:
                            model_data[key] = {
                                "model": sample_model,
                                "class": class_name,
                                "behavior": behavior_name,
                                "template": [],
                                "similarity": []
                            }


                        model_data[key]["template"].append(template)
                        sample_answer = item["text"]
                        target_text = target_dict.get((class_name, behavior_name), None)

                        if sample_answer and target_text:
                            target_embedding = model.encode(target_text, device=device)
                            sample_embedding = model.encode(sample_answer, device=device)
                            similarity_score = float(util.pytorch_cos_sim(torch.tensor(target_embedding), torch.tensor(sample_embedding)))

                        else:
                            similarity_score = None

                        model_data[key]["similarity"].append(similarity_score)

                    model_output_file = os.path.join(model_category_path + "/similarity_results", f"{sample_model}_similarity_results.json")

                    all_sample_results = list(model_data.values())

                    index += 1
                    print(f"Now is ------ {index}: {model_category_path}/{sample_model} ------")
                    os.makedirs(os.path.dirname(model_output_file), exist_ok=True)
                    with open(model_output_file, "w", encoding="utf-8") as out_file:
                        json.dump(all_sample_results, out_file, ensure_ascii=False, indent=2)

