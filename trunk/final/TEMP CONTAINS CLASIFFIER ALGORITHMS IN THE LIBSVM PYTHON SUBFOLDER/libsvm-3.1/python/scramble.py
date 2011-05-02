#!/usr/bin/python

import random

def main():
    f = open("train.out")
    o = open("train_new.out", "w")
    entire_file = f.read()
    file_in_a_list = entire_file.split("\n")
    num_lines = len(file_in_a_list)
    random_nums = random.sample(xrange(num_lines), num_lines)
    for i in random_nums:
        o.write(file_in_a_list[i] + "\n")

    o.close()
    f.close()

if __name__ == "__main__":
  main()