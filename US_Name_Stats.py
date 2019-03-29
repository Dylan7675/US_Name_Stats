"""This is the main script for my US_Name_Stats data anylysis project"""
import os
import pandas as pd
import numpy as np
import time

def main():

    name_dic = csv_to_name_dic()
    print(name_dic['Dylan'])


def csv_to_name_dic():

    name_dic = {}
    header = ['Sex', 'Qty', 'Year']

    for file in os.listdir("./Year_of_Birth_Data"):
        #print("loading data from {}".format(file))
        with open("./Year_of_Birth_Data/{}".format(file), 'r') as f_in:
            for line in f_in:
                data = line.split(',')
                key = data[0]
                data[3] = data[3][:-1] #carraige return at the end of each line
                values = data[1:]
                tempdf = pd.DataFrame([values], columns = header)

                if key not in name_dic.keys():
                    name_dic[key] = tempdf
                    print(name_dic[key])
                    #time.sleep(2)
                else:
                    name_dic[key] = pd.concat([name_dic[key], tempdf], ignore_index = True)
                    print(name_dic[key])
                    #time.sleep(2)

    return(name_dic)





if __name__ == "__main__":
    main()
