# get API translations (GPT-4o) (Experiment 1 and 3)

from openai import OpenAI
from string import digits

client = OpenAI(
    api_key='INSERT_KEY_HERE'
)

def condition_b(original, model="gpt-4o-mini"):
    prompt = f"Please translate the following poem to German. Please make sure that your translation reproduces the form of the original (rhyme and meter): \n\n{original}"
    messages = [{"role": "user", "content": prompt}]
    chat = client.chat.completions.create(model=model, messages=messages)
    translation = chat.choices[0].message.content
    return translation

def condition_d(original, attempt, model="gpt-4o-mini"):
    prompt = f"You are provided with an English poem and an attempt at a German translation. Please suggest a translation to German that reproduces the form of the original (rhyme and meter) better.\n\nOriginal:\n\n{original}\n\nAttempt at translation:\n\n{attempt}"
    messages = [{"role": "user", "content": prompt}]
    chat = client.chat.completions.create(model=model, messages=messages)
    translation = chat.choices[0].message.content
    return translation

def condition_h(original, candidate_translation, model="gpt-4o-mini"):
    prompt1 = f"Please tell me the meter and rhyme of the following poem (in the format: \"Meter: [meter]; Rhyme scheme: [rhyme scheme]\").\n\nPoem:\n{original}\n\n"
    messages = [{"role": "user", "content": prompt1}]
    chat = client.chat.completions.create(model=model, messages=messages)
    description = chat.choices[0].message.content
    prompt2 = f"Please translate the following to German:\n\n{description}"
    messages = [{"role": "user", "content": prompt2}]
    chat = client.chat.completions.create(model=model, messages=messages)
    german_description = chat.choices[0].message.content
    prompt3 = f"Bitte schreiben Sie den folgenden Text in ein Gedicht mit den folgenden Eigenschaften um:\n\n{german_description}\n\nText:\n{candidate_translation}\n\n"
    messages = [{"role": "user", "content": prompt3}]
    chat = client.chat.completions.create(model=model, messages=messages)
    translation = chat.choices[0].message.content
    return translation

def condition_i(original, model="gpt-4o-mini"):
    prompt1 = f"Please tell me the meter and rhyme of the following poem (in the format: \"Meter: [meter]; Rhyme scheme: [rhyme scheme]\").\n\nPoem:\n{original}\n\n"
    messages = [{"role": "user", "content": prompt1}]
    chat = client.chat.completions.create(model=model, messages=messages)
    description = chat.choices[0].message.content
    prompt2 = f"Please translate the poem below to German. Please make sure to reproduce the meter and rhyme scheme of the original, making use of the given additional information.\n\nInformation on meter and rhyme scheme:\n{description}\n\nPoem:\n{original}\n\n"
    messages = [{"role": "user", "content": prompt2}]
    chat = client.chat.completions.create(model=model, messages=messages)
    translation = chat.choices[0].message.content
    return translation

if __name__ == "__main__":
    remove_digits = str.maketrans('', '', digits)

    # original texts and (if applicable) input translation attempts, in the format <number>text<number>…<end>
    originals = "".join(open("ORIGINAL_POEMS.txt", "r").readlines()).replace("END", "").translate(
        remove_digits).split("<>")[1:-1]
    candidate_translations = "".join(open("TRANSLATION_ATTEMPT.txt", "r").readlines()).replace("END","").translate(
        remove_digits).split("<>")[1:-1]

    paired = [(originals[i], candidate_translations[i]) for i in range(len(originals))]
    translations = []

    for p in paired:
        t = condition_d(p[0], p[1], model="gpt-4o")
        translations.append(t)
        continue

    # write output translations to file
    with open("OUTPUT_TRANSLATION.txt", "w") as outfile:
        for c in range(len(translations)):
            outfile.write("<" + str(c + 1) + ">\n" + str(translations[c]) + "\n")