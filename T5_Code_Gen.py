import os
import time
import math
import random
import datetime
from pathlib import Path
import streamlit as st
import tensorflow as tf
from transformers import RobertaTokenizer, TFT5ForConditionalGeneration
from datasets import load_dataset
import logging


# Helper functions
def setup_strategy(xla, fp16, no_cuda):
    if xla:
        tf.config.optimizer.set_jit(True)

    if fp16:
        policy = tf.keras.mixed_precision.experimental.Policy("mixed_float16")
        tf.keras.mixed_precision.experimental.set_policy(policy)

    gpus = tf.config.list_physical_devices("GPU")
    if no_cuda:
        return tf.distribute.OneDeviceStrategy(device="/cpu:0")
    elif len(gpus) == 1:
        return tf.distribute.OneDeviceStrategy(device="/gpu:0")
    elif len(gpus) > 1:
        return tf.distribute.MirroredStrategy()
    else:
        return tf.distribute.get_strategy()


def download_dataset(cache_dir):
    _url = "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/mbpp.jsonl"
    dataset_path = tf.keras.utils.get_file("mbpp.jsonl", origin=_url, cache_dir=cache_dir, cache_subdir=cache_dir)
    return dataset_path


def run_predict(args, text):
    model = TFT5ForConditionalGeneration.from_pretrained(args.save_dir)
    tokenizer = RobertaTokenizer.from_pretrained(args.save_dir)
    query = args.prefix + text
    encoded_text = tokenizer(query, return_tensors="tf", padding="max_length", truncation=True, max_length=args.max_input_length)
    generated_code = model.generate(
        encoded_text["input_ids"], attention_mask=encoded_text["attention_mask"], max_length=args.max_target_length,
        top_p=0.95, top_k=50, repetition_penalty=2, num_return_sequences=1
    )
    decoded_code = tokenizer.decode(generated_code.numpy()[0], skip_special_tokens=True)
    return decoded_code


def run(args):
    st.write("Starting training and evaluation...")
    dataset_path = download_dataset(args.cache_dir)
    dataset = load_dataset("json", data_files=dataset_path)
    dataset = dataset["train"].train_test_split(0.1, shuffle=False)

    tokenizer = RobertaTokenizer.from_pretrained(args.tokenizer_name)

    st.write("Preparing Features...")
    dataset = dataset.map(
        lambda examples: convert_examples_to_features(examples, tokenizer, args),
        batched=True
    )

    train_dataset = dataset["train"]
    validation_dataset = dataset["test"]
    num_train_examples = len(train_dataset)
    num_validation_examples = len(validation_dataset)

    st.write(f"Training model: {args.model_type.upper()}")
    with strategy.scope():
        model = TFT5ForConditionalGeneration.from_pretrained(args.model_name_or_path, from_pt=True)

    st.write("Starting training...")
    trainer = Trainer(model, args, train_dataset, validation_dataset, num_train_examples, num_validation_examples)
    trainer.train()

    st.write("Saving model...")
    model.save_pretrained(args.save_dir)
    tokenizer.save_pretrained(args.save_dir)
    st.success("Training and saving completed successfully!")


# Streamlit UI
def main():
    st.title("Code Generation with T5")
    st.sidebar.header("Configuration")
    mode = st.sidebar.selectbox("Select Mode", ["Train Model", "Generate Code"])
    strategy = setup_strategy(xla=True, fp16=False, no_cuda=False)

    class Args:
        model_type = "t5"
        tokenizer_name = "Salesforce/codet5-base"
        model_name_or_path = "Salesforce/codet5-base"
        train_batch_size = 8
        validation_batch_size = 8
        max_input_length = 48
        max_target_length = 128
        prefix = "Generate Python: "
        learning_rate = 3e-4
        weight_decay = 1e-4
        warmup_ratio = 0.2
        adam_epsilon = 1e-8
        seed = 2022
        epochs = 20
        output_dir = "runs/"
        logging_dir = f"{output_dir}/logs/"
        checkpoint_dir = f"{output_dir}/checkpoint"
        save_dir = f"{output_dir}/saved_model/"
        cache_dir = "../working/"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        Path(logging_dir).mkdir(parents=True, exist_ok=True)
        Path(save_dir).mkdir(parents=True, exist_ok=True)

    args = Args()

    if mode == "Train Model":
        st.header("Train and Evaluate the Model")
        if st.button("Start Training"):
            with st.spinner("Training in progress..."):
                run(args)
    elif mode == "Generate Code":
        st.header("Generate Python Code")
        query = st.text_area("Enter a prompt (e.g., 'Write a Python function to calculate factorial.')")
        if st.button("Generate Code"):
            with st.spinner("Generating code..."):
                output = run_predict(args, query)
                st.code(output, language="python")


if __name__ == "__main__":
    main()
