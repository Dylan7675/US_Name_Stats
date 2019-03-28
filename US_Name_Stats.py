"""This is the main script for my US_Name_Stats data anylysis project"""
import os
import pandas as pd
import numpy as np


def main():

    name_dic = csv_to_name_dic()


def csv_to_name_dic():

    name_dic = {}

    for file in os.listdir("./Year_of_Birth_Data"):
        print("loading data from {}".format(file))
        with open("./Year_of_Birth_Data/{}".format(file), 'r') as f_in:
            for line in f_in:
                data = line.split(',')
                key = data[0]
                data[3] = data[3][:-1] #carraige return at the end of each line
                values = data[1:]

                if key not in name_dic.keys():
                    name_dic[key] = values

                else:
                    name_dic[key].append(values)

    return(name_dic)





if __name__ == "__main__":
    main()
