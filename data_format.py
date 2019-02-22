"""This is a helper script that adds a header formatting to all files,
and converts all files from .txt to .csv"""

def txt_to_csv():
    import os

    header = "Name,Sex,Quantity"
    os.chdir("./Year_of_Birth_Data")
    for file in os.listdir("."):
        if file.endswith(".txt"):
            base = os.path.splitext(file)[0]
            with open(file, 'r') as f_in: data = f_in.read()
            with open(file, 'w') as f_out:
                f_out.write("%s\n%s" %(header, data))
            os.rename(file, base + ".csv")
            print(file + " Formatted")


def main():

    print("Converting all files from .txt to .csv and applying a header")
    txt_to_csv()
    print("All files have been converted and formatted")


if __name__ == "__main__":
    main()

