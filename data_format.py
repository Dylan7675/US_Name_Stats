def txt_to_csv():

    """This is a helper script that adds a header formatting to all files,
and converts them from .txt to .csv"""

    import os

    output = ""
    header = "Name,Sex,Quantity,Year"
    os.chdir("./Year_of_Birth_Data")

    for file in os.listdir("."):
        if file.endswith(".txt"):
            base = os.path.splitext(file)[0]
            year = base[3:]

            with open(file, 'r') as f_in: #line[:-1] because of a carriage return as last value of line
                data = [ line[:-1] + (",%s" %year)) for line in f_in]
            with open(file, 'w') as f_out:
                f_out.write("%s\n" %header)
                for entry in data: f_out.write("%s\n" % entry)
            os.rename(file, base + ".csv")
            print(file + " Formatted")


def main():

    print("Converting all files from .txt to .csv and applying a header")
    txt_to_csv()
    print("All files have been converted and formatted")


if __name__ == "__main__":
    main()

