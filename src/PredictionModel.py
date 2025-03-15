
print("[INFO] loading modules")

from os import path
from random import choice
from pickle import load, dump
from PredictionModelFileStructure import PredictionModelFileStructure

print("[INFO] initializing variables")

model_path = "model-20.pkl"
dataset_path = "Dataset.txt"
train_depth = 20


def preprocess_text(text: str) -> str:
    return (text.lower()
            .replace("\n", " [BREAKPOINT] ")
            .replace(".", " . ")
            .replace("?", " ? ")
            .replace("!", " ! ")
            .replace(",", " , ")
            )


def train(dataset: str, depth: int) -> dict:
    dataset = preprocess_text(dataset)
    computed_data = dict()
    word_list = dataset.split(" ")
    progress = 0
    max_progress = len(word_list) * depth

    print(f"[INFO] progress {progress}/{max_progress}")

    for i in range(depth + 1):
        if i == 0:
            continue
        for j in range(len(word_list) - 1):
            progress += 1
            print(f"[INFO] progress {progress}/{max_progress}")
            try:

                current_phrase = " ".join(word_list[j:j + i])  # ✅ Fix empty phrase issue
                next_phrase = " ".join(word_list[j + 1:j + i + 1])

                if current_phrase in computed_data:
                    computed_data[current_phrase].append(next_phrase)
                else:
                    computed_data[current_phrase] = [next_phrase]
            except IndexError:
                continue


    return computed_data


def guess_next_phrase(phrase: str, word_dict: dict):
    if phrase in word_dict:
        return choice(word_dict[phrase])
    else:
        if len(phrase.split(" ")) == 1:
            print("[INFO] shit, you better make better algorithm for handling unknown phrases")
            return "[FORCE-BREAKPOINT]"
        arrayed_phrase = phrase.split(" ")[1:]
        processed_text = arrayed_phrase[0]
        for i in range(len(arrayed_phrase)):
            if i == 0:
                continue
            processed_text = f"{processed_text} {arrayed_phrase[i]}"
        return guess_next_phrase(processed_text, word_dict)


def load_model(filepath: str):
    with open(filepath, 'rb') as file:
        return load(file)


def save_model(filepath: str, model_to_save: PredictionModelFileStructure):
    with open(filepath, 'wb') as file:
        dump(model_to_save, file)


def initialize():
    global model_path, train_depth, dataset_path

    print("[INFO] initializing")

    dataset: str
    if path.exists(model_path):
        print("[INFO] loading model")
        return load_model(model_path)
    else:
        print("[INFO] model not found, training new one")
        if path.exists(dataset_path):
            with open(dataset_path, 'r', encoding='utf-8') as file:
                dataset = file.read()
        else:
            print("[ERROR] no dataset found")
            return

        model_dict = train(dataset, train_depth)

        onlapusAI_model = PredictionModelFileStructure(model_dict)

        print("[INFO] saving model")
        save_model(model_path, onlapusAI_model)

        return onlapusAI_model

if __name__ == "__main__":
    initialize()
