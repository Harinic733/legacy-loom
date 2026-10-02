#!/usr/bin/env python2

def calculate_total(numbers):
    total = 0

    for number in numbers:
        total += number

    return total


def greet(name):
    print("Hello, " + name)


if __name__ == "__main__":
    values = [10, 20, 30]
    print(calculate_total(values))
    greet("Legacy Loom")
    