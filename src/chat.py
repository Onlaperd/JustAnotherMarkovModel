from PredictionModel import preprocess_text, train_depth, guess_next_phrase, initialize
from PredictionModelFileStructure import PredictionModelFileStructure
from time import sleep
from random import random

onlapusAI_model: PredictionModelFileStructure


def generate(prompt: str, delay: float, limit: int):
    processed_prompt = preprocess_text(prompt)
    processed_prompt = processed_prompt.split(" ")
    processed_prompt = processed_prompt[-train_depth:]

    computed_prompt = ""
    for e in processed_prompt:
        computed_prompt = f"{computed_prompt} {e}"

    next_phrase = computed_prompt


    for i in range(limit):
        next_phrase = guess_next_phrase(next_phrase, onlapusAI_model.phrase_dict)
        if next_phrase == "[BREAKPOINT]":
            for q in range(10):
                next_phrase = guess_next_phrase(next_phrase, onlapusAI_model.phrase_dict)
                if next_phrase != "[BREAKPOINT]":
                    break

        display_phrase = next_phrase.split(" ")


        if display_phrase[-1] == '':
            tmp = display_phrase
            display_phrase = []
            for e in tmp:
                if e == '':
                    continue
                display_phrase.append(e)


        try:
            if display_phrase[-1] == "[BREAKPOINT]":
                chance = random()
                if chance > 0.49:
                    return
                else:
                    print()
                    continue
            elif display_phrase[-1] == "[FORCE-BREAKPOINT]":
                return
            print(display_phrase[-1] + " ", end='')
        except IndexError:
            pass
        sleep(delay)



def run_chat():
    print(f"[INFO] {len(onlapusAI_model.phrase_dict)}")
    while True:
        user_input = input("[you] ")
        print("[OnlapusAI] ", end='')
        generate(user_input, 0.2, 100)
        print()


if __name__ == "__main__":
    onlapusAI_model = initialize()
    run_chat()
