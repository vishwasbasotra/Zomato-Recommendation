import datasets
from pprint import pprint

dataset = datasets.load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
print(f"Total rows: {len(dataset)}")
print("First row:")
pprint(dataset[0])
