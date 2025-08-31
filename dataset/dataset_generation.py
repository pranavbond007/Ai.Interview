import pandas as pd
import random

# Define fillers and base sentences
fillers = ["uh", "um", "hmm", "you know", "like"]
base_sentences = [
    "I think the project was successful because we followed agile practices.",
    "The main challenge was debugging the memory leak in the code.",
    "I enjoy working in teams and learning new technologies.",
    "My internship taught me valuable lessons about time management.",
    "I believe Python is a very versatile programming language.",
    "Machine learning is exciting because of its real-world applications.",
    "I improved the algorithm to optimize runtime performance.",
    "Working on group projects has helped me develop leadership skills.",
    "I learned C++ during my first year and applied it in projects.",
    "The best way to grow is by constantly practicing and learning."
]

# Function to insert fillers randomly in a sentence
def insert_fillers(sentence, fillers, max_fillers=2):
    words = sentence.split()
    num_fillers = random.randint(1, max_fillers)
    filler_positions = random.sample(range(len(words)), num_fillers)
    for pos in sorted(filler_positions, reverse=True):
        words.insert(pos, random.choice(fillers))
    return " ".join(words)

# Generate dataset
data = []
for i in range(150):  # increased to 150 rows
    base = random.choice(base_sentences)
    if random.random() < 0.7:  # 70% chance sentence will have fillers
        transcript = insert_fillers(base, fillers)
        filler_type = "filler"
    else:  # 30% normal sentences
        transcript = base
        filler_type = "none"

    # Add chance of long pause
    if random.random() < 0.25:  # 25% chance of pause
        transcript += " ... (long pause)"
        if filler_type == "none":
            filler_type = "pause"
        else:
            filler_type = "filler+pause"

    data.append([f"audio_{i+1}", transcript, filler_type])

# Create DataFrame
df = pd.DataFrame(data, columns=["audio_id", "transcript", "filler_type"])

# Save CSV
df.to_csv("filler_pause_dataset_2.csv", index=False)

print("✅ Dataset saved as filler_dataset.csv with", len(df), "rows.")
