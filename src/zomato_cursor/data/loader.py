"""Dataset loader from Hugging Face."""

import datasets

def load_raw_dataset(dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation", split: str = "train") -> datasets.Dataset:
    """Load the raw dataset from Hugging Face."""
    dataset = datasets.load_dataset(dataset_name, split=split)
    return dataset
