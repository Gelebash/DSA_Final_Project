import pygame
import sys
from warehouse import Warehouse
import time
import random


def first_fit(weights, capacity, max_weight):
    warehouse = Warehouse()
    full = 0
    # Place items one by one
    bins = warehouse.get_bins()
    for weight in weights:
        if weight == capacity:
            full += 1
            continue
        # Find the first bin that can aclcommodate the weight
        placed = False
        for bin in bins:
            placed = False
            current_weight = bin.get_contents()
            if capacity - current_weight >= weight:
                placed = True
                bin.add_item(weight)

                # Check if the bin is almost full and remove it if so
                if current_weight + weight >= capacity - (max_weight / 8):
                    bins.remove(bin)
                    full += 1
                break

        # If no bin could accommodate the weight, create a new bi
        if placed is False:
            new_bin = warehouse.add_bin(capacity)
            new_bin.add_item(weight)
            bins = warehouse.get_bins()
    return len(warehouse.get_bins()) + full


def next_fit(weights, capacity):
    warehouse = Warehouse()
    # Add the first bin
    current_bin = warehouse.add_bin(capacity)

    for weight in weights:
        current_weight = current_bin.get_contents()
        # Check if the current bin can accommodate the weight
        if capacity - current_weight >= weight:
            current_bin.add_item(weight)

        else:
            # Create a new bin and use it
            current_bin = warehouse.add_bin(capacity)
            current_bin.add_item(weight)

    return len(warehouse.get_bins())


def main():
    print("Hello World")


if __name__ == "__main__":
    main()
