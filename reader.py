import sys
import csv
import json
import pickle


class FileReader:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def read(self):
        raise NotImplementedError("Subclasses should implement this method")

    def write(self, output_file):
        raise NotImplementedError("Subclasses should implement this method")

    def modify(self, changes):
        for change in changes:
            x, y, value = change.split(',')
            x, y = int(x), int(y)
            if y < len(self.data) and x < len(self.data[y]):
                self.data[y][x] = value

    def display(self):
        for row in self.data:
            print(','.join(map(str, row)))


class CSVReader(FileReader):
    def read(self):
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            self.data = [row for row in reader]
        # Ensure all rows have the same length by padding with empty strings if needed
        max_length = max(len(row) for row in self.data)
        self.data = [row + [''] * (max_length - len(row)) for row in self.data]

    def write(self, output_file):
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)


class JSONReader(FileReader):
    def read(self):
        with open(self.filename, mode='r') as file:
            try:
                self.data = json.load(file)
            except json.JSONDecodeError:
                print(f"Blad: Plik '{self.filename}' to nie jest prawidlowy plik JSON lub plik jest pusty.")
                sys.exit(1)

    def write(self, output_file):
        with open(output_file, mode='w') as file:
            json.dump(self.data, file, indent=4)


class TXTReader(FileReader):
    def read(self):
        with open(self.filename, mode='r') as file:
            self.data = [line.strip().split(',') for line in file]

    def write(self, output_file):
        with open(output_file, mode='w') as file:
            for row in self.data:
                file.write(','.join(map(str, row)) + '\n')


class PickleReader(FileReader):
    def read(self):
        with open(self.filename, mode='rb') as file:
            self.data = pickle.load(file)

    def write(self, output_file):
        with open(output_file, mode='wb') as file:
            pickle.dump(self.data, file)


def main():
    if len(sys.argv) < 4:
        print("Dzialanie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ... <zmiana_n>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    if input_file.endswith('.csv'):
        reader = CSVReader(input_file)
    elif input_file.endswith('.json'):
        reader = JSONReader(input_file)
    elif input_file.endswith('.txt'):
        reader = TXTReader(input_file)
    elif input_file.endswith('.pickle'):
        reader = PickleReader(input_file)
    else:
        print("Nieprawidlowy format pliku")
        sys.exit(1)

    reader.read()
    reader.modify(changes)
    reader.display()
    reader.write(output_file)


if __name__ == "__main__":
    main()
