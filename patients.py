heart_rate_samples = {
"J. Alvarez": [72, 75, 78],
"M. Chen": [80, 82],
"R. Okafor": [65, 68, 70, 66],
"S. Patel": [90, 95, 92, 88, 91],
"T. Nguyen": [77, 79],
"L. Kowalski": [68, 70, 69],
"D. Osei": [98, 101, 95, 99],
"A. Whitfield": [74, 76, 75, 73],
}

def get_all_stats(patient_name, dataset):
    if patient_name in dataset:
        return dataset[patient_name]
    else:
        return "Patient not found."

def get_specific_stat(patient_name, dataset, index):
    if patient_name in dataset:
        return dataset[patient_name][index]
    else:
        return "Patient not found"

def display_stats(*args):
    for stat in args:
        print(stat)

patient_name = input("Enter patient name:")

request = input("Enter 'all' for all patient stats or 'specific' for a specific patient stat:")

if request == "all":
    all_stats = get_all_stats(patient_name, heart_rate_samples)
    display_stats(*all_stats)

elif request == "specific":
    patient_number = int(input("Enter patient number (1-8):"))
    get_specific_stat(patient_name, heart_rate_samples, patient_number)

else:
    print("Invalid request.")
