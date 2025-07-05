import os
import json


# base_path = '../jailbreak_result'
base_path = '../jailbreak_result_do_not_process'


for model_category in os.listdir(base_path):
    model_category_path = os.path.join(base_path, model_category)

    if not os.path.isdir(model_category_path):
        continue

    sentiment_dir = os.path.join(model_category_path, 'sentiment_results')
    similarity_dir = os.path.join(model_category_path, 'similarity_results')

    if not os.path.isdir(sentiment_dir) or not os.path.isdir(similarity_dir):
        continue


    sentiment_files = [f for f in os.listdir(sentiment_dir) if f.endswith('_sentiment_results.json')]
    similarity_files = [f for f in os.listdir(similarity_dir) if f.endswith('_similarity_results.json')]


    for sentiment_file in sentiment_files:

        base_name = sentiment_file.replace('_sentiment_results.json', '')
        similarity_file = f"{base_name}_similarity_results.json"

        if similarity_file not in similarity_files:
            continue


        with open(os.path.join(sentiment_dir, sentiment_file), 'r') as f:
            sentiment_data = json.load(f)

        with open(os.path.join(similarity_dir, similarity_file), 'r') as f:
            similarity_data = json.load(f)


        for entry in sentiment_data:
            if 'judgement' in entry:
                del entry['judgement']

        for sentiment_entry, similarity_entry in zip(sentiment_data, similarity_data):
            sentiment_entry['similarity'] = similarity_entry.get('similarity', [])


        model_output_file = os.path.join(model_category_path + "/final_results", f"{base_name}_final_results.json")
        os.makedirs(os.path.dirname(model_output_file), exist_ok=True)
        with open(model_output_file, 'w', encoding="utf-8") as f:
            json.dump(sentiment_data, f, indent=4)

