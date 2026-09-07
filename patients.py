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

request = input("Enter 'all' for all patient stats or 'specific' for one patient: ")

if request == "all":
    display_stats(*heart_rate_samples.values())

elif request == "specific":
    patient_number = int(input("Enter patient number (1-8): "))

    patients = list(heart_rate_samples.keys())
    patient_name = patients[patient_number - 1]

    print(patient_name)
    print(heart_rate_samples[patient_name])

else:
    print("Invalid request.")
