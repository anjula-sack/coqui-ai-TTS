import re
import csv

# === MAPPINGS FROM JS FILES ===

ro_specials = [
    ('ඓ', 'ai'), ('ඖ', 'au'), ('ඍ', 'ṛ'), ('ඎ', 'ṝ'), ('ඐ', 'ḹ'),
    ('අ', 'a'), ('ආ', 'ā'), ('ඇ', 'æ'), ('ඈ', 'ǣ'), ('ඉ', 'i'), ('ඊ', 'ī'),
    ('උ', 'u'), ('ඌ', 'ū'), ('එ', 'e'), ('ඒ', 'ē'), ('ඔ', 'o'), ('ඕ', 'ō'),
    ('ඞ්', 'ṅ'), ('ං', 'ṁ'), ('ඃ', 'ḥ')
]

ro_consonants = [
    ('ඛ', 'kh'), ('ඨ', 'ṭh'), ('ඝ', 'gh'), ('ඡ', 'ch'), ('ඣ', 'jh'), ('ඦ', 'ñj'),
    ('ඪ', 'ḍh'), ('ඬ', 'ṇḍ'), ('ථ', 'th'), ('ධ', 'dh'), ('ඵ', 'ph'), ('භ', 'bh'),
    ('ඹ', 'mb'), ('ඳ', 'ṉd'), ('ඟ', 'ṉg'), ('ඥ', 'gn'), ('ක', 'k'), ('ග', 'g'),
    ('ච', 'c'), ('ජ', 'j'), ('ඤ', 'ñ'), ('ට', 'ṭ'), ('ඩ', 'ḍ'), ('ණ', 'ṇ'),
    ('ත', 't'), ('ද', 'd'), ('න', 'n'), ('ප', 'p'), ('බ', 'b'), ('ම', 'm'),
    ('ය', 'y'), ('ර', 'r'), ('ල', 'l'), ('ව', 'v'), ('ශ', 'ś'), ('ෂ', 'ṣ'),
    ('ස', 's'), ('හ', 'h'), ('ළ', 'ḷ'), ('ෆ', 'f')
]

ro_combinations = [
    ('්', ''), ('', 'ā', 'ා'), ('', 'æ', 'ැ'), ('', 'ǣ', 'ෑ'), ('', 'i', 'ි'),
    ('', 'ī', 'ී'), ('', 'u', 'ු'), ('', 'ū', 'ූ'), ('', 'e', 'ෙ'), ('', 'ē', 'ේ'),
    ('', 'ai', 'ෛ'), ('', 'o', 'ො'), ('', 'ō', 'ෝ'), ('', 'ṛ', 'ෘ'), ('', 'ṝ', 'ෲ'),
    ('', 'au', 'ෞ'), ('', 'ḹ', 'ෳ')
]

# === TRANSLITERATION FUNCTIONS ===

def create_conso_combi():
    combi = []
    for comb in ro_combinations:
        for conso in ro_consonants:
            sinh = conso[0] + (comb[2] if len(comb) > 2 else comb[0])
            roman = conso[1] + comb[1]  # Important: consonant first
            combi.append((sinh, roman))
    return sorted(combi, key=lambda x: len(x[0]), reverse=True)

def sinhala_to_roman(text):
    text = text.replace('\u200D', '')  # Remove ZWJ

    # Step 1: consonant + vowel combos (e.g., කා, පි, තු)
    for sinh, rom in create_conso_combi():
        text = text.replace(sinh, rom)

    # Step 2: specials (independent vowels, visarga, anusvara)
    for sinh, rom in sorted(ro_specials, key=lambda x: len(x[0]), reverse=True):
        text = text.replace(sinh, rom)

    # Step 3: base consonants (add § marker to evaluate implicit 'a')
    for sinh, rom in sorted(ro_consonants, key=lambda x: len(x[0]), reverse=True):
        text = text.replace(sinh, rom + "§")

    # Step 4: insert implicit 'a' where appropriate
    text = re.sub(r'§(?=[āæǣiīuūeēaiōṛṝauḹṁḥ]|$)', '', text)  # no a if vowel or end
    text = text.replace('§', 'a')  # default a

    return text

# === MAIN PROCESSING FUNCTION ===

def convert_metadata(input_txt='metadata.txt', output_csv='converted_metadata.csv'):
    with open(input_txt, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        # writer.writerow(['name', 'romanized_text', 'sinhala_text', 'author'])  # header

        for line in infile:
            match = re.match(r'\(\s*(\w+)\s+"(.+?)"\s*\)', line.strip())
            if match:
                name_raw, sinhala_text = match.groups()
                romanized_text = sinhala_to_roman(sinhala_text)
                formatted_name = name_raw
                writer.writerow([formatted_name, romanized_text, sinhala_text, 'mettananda'])

# === RUN SCRIPT ===
if __name__ == '__main__':
    convert_metadata()
