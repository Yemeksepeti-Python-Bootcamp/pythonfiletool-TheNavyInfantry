from pathlib import Path
import csv, json

class FileToolClass(object):

    def __init__(self,file_path,*fields,):
        self.file_path = file_path
        self.fields = fields

    def is_exists(self):
        """This method checks if the given path/file is existing or not"""
        if not Path(self.file_path).is_file():
            with open(self.file_path.split("/")[-1], 'a', newline='') as csv_file: #possible to use w+ instead of a
                    writer = csv.writer(csv_file)
                    writer.writerows(self.fields)
            print("File CREATED and header inputs were written inside the file!")

        else:
            print("File EXISTS and ready to use!")

    def get_header(self):
        """This method returns header lenght of the given csv file"""
        with open(self.file_path, 'r') as csv_file:
            header = []
            reader = csv.reader(csv_file)
            for row in reader:
                header.append(row)

            if header[0] == []: #If its first row is empty as a list
                return len(header[1]) #Returns next line's lenght (which is first one by index number)
            else:
                return len(header[0]) #If not, returns first row


    def read_in_file(self):
        """This method reads file and returns respectively row number and data"""
        with open(self.file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # for row in reader:
            #     print(row)
            for row, display in enumerate(reader, start=0):
                print(f"{row} |", *display)

    def search_in_file(self,to_find):
        """This method searches the given input and returns all possible matches with the line number found"""
        with open(self.file_path, 'r') as csv_file:
            match_list = []
            reader = csv.reader(csv_file)
            for row, search in enumerate(reader):
                for each in search:
                    if to_find in each.strip(): #Strip method was used to improve search accuracy
                        match_list.append(f"Your query was found on row {row} : (as) {each.strip()}")
            print(*match_list, sep='\n')

    def delete_in_file(self, row_to_delete):
        """This method deletes a row based on the given input"""
        safe_lines = []
        with open(self.file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)

            #Enumerate was used to display the row number, in order to make it easier to match with given input
            for row_number, row in enumerate(reader, start=0):
                if row_number != row_to_delete: #If row number doesn't mathces with given input
                    safe_lines.append(row) #Treat that as a safe row (which won't be deleted) and add it to the list

        with open(self.file_path, 'w') as csv_file: #Overwrite file with safe lines except deleted one
            writer = csv.writer(csv_file)
            writer.writerows(safe_lines)

        print(f"Row {row_to_delete} is deleted from your file")

    def append_in_file(self,*value_to_append):
        """This method appends/adds various number of inputs according to the header's length limit"""
        to_append = []
        to_append.append(value_to_append)

        with open(self.file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if len(value_to_append) == self.get_header(): #If inputs length is equal to header length
                writer.writerow(*[i for i in to_append]) #Does the writing process
                print("Append process was successful!")
            else:
                print(f"Too much inputs were given! Try again!") #If not, prints an info message

        self.read_in_file()

    def update_in_file(self,row_to_update: int,*value_to_change):
        """This method updates a row with the given various number of inputs
            (It will be limited by the header length again)"""
        updated_csv = []
        with open(self.file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)


            for row, search in enumerate(reader):
                if row_to_update == row: #If both rows match
                    search = list(value_to_change[:]) #Gets the whole list with :
                updated_csv.append(search)
            print(*updated_csv, sep="\n")


        with open(self.file_path, 'w') as csv_file: #Overwrite file with the updated version
            writer = csv.writer(csv_file)
            writer.writerows(updated_csv)


    def convert_JSON(self,option):
        """This method converts a file to JSON"""
        json_arr = [] #JSON array to store data

        with open(self.file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                json_arr.append(row)

        generate_json_path = (self.file_path.split("/")[-1]).replace("csv","json")

        with open(generate_json_path, 'w') as json_file:
            json_string = json.dumps(json_arr, indent=3)
            json_file.write(json_string)

        """Generates either the all file or a single line according to the user's decision"""
        if option == "all":
            print(json_arr)
        else:
            try:
                single_row = json_arr[int(option)]
                print(single_row)
            except IndexError as e:
                print(f"Invalid index request! : {e}")

    def merge_files(self,from_file,target_file):
        """This method merges two files which has the same extension
        and does merge process from the current file to the target one,
        as overwriting the target file."""
        from_file_path = Path(from_file)
        target_file_path = Path(target_file)

        if from_file_path.suffix and target_file_path.suffix == ".csv": #CSV merge

                headers = []
                data = []

                try:
                    for file_name in [from_file,target_file]:
                        with open(f'{file_name}','r') as f:
                            temp_csv = csv.DictReader(f)
                            headers += temp_csv.fieldnames
                            for row in temp_csv:
                                data.append(row)

                    headers = sorted(set(headers), key=headers.index) #'key=headers.index' maintains header's real order
                    with open(target_file, 'w') as f:
                        writer = csv.DictWriter(f, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(data)

                    print("Successful!")

                except FileNotFoundError as e:
                    print("Failed!",e)


        elif from_file_path.suffix and target_file_path.suffix == ".json": #JSON merge

            result = list()

            try:
                with open(from_file, 'r') as in_from_file, open(target_file, 'r') as in_target_file:
                    result.extend(json.load(in_from_file))
                    result.extend(json.load(in_target_file))

                with open(target_file, 'w') as in_target_file:
                    json.dump(result, in_target_file, indent=3)

                print("Successful!")

            except FileNotFoundError as e:
                print("Failed!", e)


def menu(): #Displays menu and operations
    ask_path = input("Path: ")
    ask_fields_list = []

    while True:
        ask_a_field = input("Field(s) [quit]: ")
        if "quit" == ask_a_field:
            break
        ask_fields_list.append(ask_a_field)

    obj = FileToolClass(str(ask_path),ask_fields_list)

    # obj = FileToolClass("airtravel.csv", "Month", "1958", "1959", "1960")
    while True:
        print(
            """
            1) Create/Open file 
            2) Read file
            3) Search in file
            4) Add to file 
            5) Delete in file
            6) Update in file
            7) Convert to JSON
            8) File merge
            0) Quit
            """
        )
        choice = int(input("Choice: "))

        if choice == 1:
            obj.is_exists()

        elif choice == 2:
            obj.read_in_file()

        elif choice == 3:
            user_input = str(input("Search: "))
            obj.search_in_file(user_input)

        elif choice == 4:
            added = []
            while True:
                if len(added) == obj.get_header():
                    break
                add_data = input("Data to add: ")
                added.append(add_data)

            obj.append_in_file(*added)


        elif choice == 5:
            delete_row = int(input("Delete: "))
            obj.delete_in_file(delete_row)

        elif choice == 6:
            updated = []
            update_row = int(input("Row # to update: "))
            while True:
                if len(updated) == obj.get_header():
                    break
                update_data = input("Data to update: ")
                updated.append(update_data)

            obj.update_in_file(update_row,*updated)


        elif choice == 7:
            convert_option = input("Convert all file (all) OR "
                                   "Convert a specific row (#) : ")

            obj.convert_JSON(convert_option)


        elif choice == 8:
            from_file_name = str(input("Enter the filename you want to get data from (EX: xyz.csv / xyz.json): "))
            target_file_name = str(input("Enter the target file name you want to merge (EX: xyz.csv / xyz.json): "))

            obj.merge_files(from_file_name,target_file_name)

        elif choice == 0:
            break

menu()