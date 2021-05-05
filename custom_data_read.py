import pickle

with open("730_all_item_names.docx", "rb") as file:
    all_items_names = pickle.load(file)
    print(all_items_names)
    print(len(all_items_names))
