import re
from words import words

# normalize dictionaries
english_to_minionese = {k.lower(): v for k, v in words.items()}
minionese_to_english = {v.lower(): k for k, v in words.items()}

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def apply_case(original, translated):
    if not original:
        return translated
    if original.isupper():
        return translated.upper()
    if original[0].isupper():
        return translated.capitalize()
    return translated


def rebuild_text(tokens):
    result = ""
    for i, token in enumerate(tokens):
        if i == 0:
            result += token
        elif re.fullmatch(r"[^\w\s]", token):
            result += token
        elif tokens[i - 1] in "([{\"'":
            result += token
        else:
            result += " " + token
    return result


def translate(sentence, minionese=False):
    dictionary = minionese_to_english if minionese else english_to_minionese

    # first try full sentence match
    stripped = sentence.strip()
    lower_sentence = stripped.lower()
    if lower_sentence in dictionary:
        translated = dictionary[lower_sentence]
        return apply_case(stripped, translated)

    # otherwise do token/phrase matching
    tokens = TOKEN_RE.findall(sentence)
    lowered = [t.lower() if re.fullmatch(r"\w+", t) else t for t in tokens]

    result = []
    i = 0

    # longest phrase first
    phrase_keys = sorted(dictionary.keys(), key=lambda x: len(x.split()), reverse=True)

    while i < len(tokens):
        matched = False

        if re.fullmatch(r"\w+", tokens[i]):
            for phrase in phrase_keys:
                phrase_parts = phrase.split()
                n = len(phrase_parts)

                if i + n <= len(tokens):
                    chunk = lowered[i:i + n]

                    # only compare if all are word tokens
                    if all(re.fullmatch(r"\w+", t) for t in tokens[i:i + n]) and chunk == phrase_parts:
                        original_chunk = " ".join(tokens[i:i + n])
                        translated = apply_case(original_chunk, dictionary[phrase])
                        result.append(translated)
                        i += n
                        matched = True
                        break

        if not matched:
            token = tokens[i]
            if re.fullmatch(r"\w+", token):
                translated = dictionary.get(token.lower(), token)
                translated = apply_case(token, translated)
                result.append(translated)
            else:
                result.append(token)
            i += 1

    return rebuild_text(result)


def main():
    print("=== English ↔ Minionese Translator ===")
    print("1. English to Minionese")
    print("2. Minionese to English")
    print("Type 'exit' to quit.\n")

    while True:
        choice = input("Choose mode (1/2): ").strip()

        if choice.lower() == "exit":
            print("Goodbye!")
            break

        if choice not in {"1", "2"}:
            print("Invalid choice. Please enter 1 or 2.\n")
            continue

        while True:
            prompt = "English: " if choice == "1" else "Minionese: "
            text = input(prompt).strip()

            if text.lower() == "exit":
                print("Goodbye!")
                return

            if not text:
                print("Please enter some text.\n")
                continue

            if choice == "1":
                print("Minionese:", translate(text, minionese=False))
            else:
                print("English:", translate(text, minionese=True))

            print()


if __name__ == "__main__":
    main()