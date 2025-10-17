import json
import os
import random
import argparse
import sys

def load_mapping(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "test.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("mapping", {})

def homoglyph_random_replace(text, mapping):
    if not text:
        return text

    chars = list(text)
    # find indices that can be replaced (character present in mapping)
    candidate_indices = [i for i, ch in enumerate(chars) if ch in mapping]
    if not candidate_indices:
        return text

    # Choose a random number of replacements:
    # - if there is more than one candidate, pick between 1 and len-1 (so not all)
    # - if exactly one candidate, replace it (can't avoid replacing "all" in that case)
    if len(candidate_indices) > 1:
        k = random.randint(1, len(candidate_indices) - 1)
    else:
        k = 1

    # shuffle candidate indices (absolute random offset)
    random.shuffle(candidate_indices)
    chosen = set(candidate_indices[:k])

    for i in chosen:
        orig = chars[i]
        chars[i] = mapping.get(orig, orig)

    return "".join(chars)

def main():
    parser = argparse.ArgumentParser(description="Randomly replace characters with homoglyphs from test.json")
    parser.add_argument("text", nargs="?", help="Text to transform. If omitted, reads from stdin.")
    parser.add_argument("--mapping", "-m", help="Path to JSON mapping file (defaults to ./test.json)", default=None)
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        if sys.stdin.isatty():
            text = input("Enter text: ")
        else:
            text = sys.stdin.read().rstrip("\n")

    mapping = load_mapping(args.mapping)
    out = homoglyph_random_replace(text, mapping)
    print(out)

if __name__ == "__main__":
    main()