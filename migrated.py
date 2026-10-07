#!/usr/bin/env python2

def calculate_total(numbers):
    total = 0

    for number in numbers:
        total += number

    return total


def greet(name):
    print("Hello, " + name)


if __name__ == "__main__":
    values = input("Enter numbers: ")
    numbers = [int(x) for x in values.split()]

    print(calculate_total(numbers))
    greet("Legacy Loom")