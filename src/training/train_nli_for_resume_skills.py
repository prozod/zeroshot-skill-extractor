import pandas as pd
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from datasets import Dataset
from pathlib import Path
import evaluate

output_path = Path(__file__).parent.resolve() / \
    "./skill_extractor_zsl_model"
output_path = output_path.resolve()

dataset_path = Path(__file__).parent.resolve() / \
    "./data.csv"
dataset_path = dataset_path.resolve()

# === CONFIG ===
MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
DATA_PATH = dataset_path
OUTPUT_DIR = output_path
LABEL2ID = {"entailment": 0, "neutral": 1, "contradiction": 2}
ID2LABEL = {v: k for k, v in LABEL2ID.items()}
BATCH_SIZE = 16
EPOCHS = 8

# === LOAD MODEL + TOKENIZER ===
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME, num_labels=3)
model.config.label2id = LABEL2ID
model.config.id2label = ID2LABEL

# === LOAD AND PREP DATA ===
df = pd.read_csv(DATA_PATH)  # expects 'premise', 'hypothesis', 'label'
df = df[df["label"].isin(LABEL2ID.keys())]  # filter invalid labels
df["label"] = df["label"].map(LABEL2ID)

dataset = Dataset.from_pandas(df)


def tokenize(batch):
    return tokenizer(batch["premise"], batch["hypothesis"], truncation=True)


dataset = dataset.map(tokenize, batched=True)
dataset = dataset.train_test_split(test_size=0.1)

# === DATA COLLATOR ===
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# === METRICS ===
accuracy_metric = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=-1)
    return accuracy_metric.compute(predictions=predictions, references=labels)


# === TRAINING ARGS ===
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy"
)

# === TRAINER ===
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# === TRAIN ===
trainer.train()

# === SAVE ===
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
