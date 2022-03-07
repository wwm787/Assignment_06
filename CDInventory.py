#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Bill McG..., 2022-Mar-06, Modified File to add functionality
#------------------------------------------#

import sys

# -- DATA -- #
strChoice = "" # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = "CDInventory.txt"  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def myAddProcCode(myID, myTitle, myArtist):
        """ Function to process ID, Title and Artist
        
        Args:
            myID (string): ID of CD.
            myTitle (string): Title of CD.
            myArtist (string): Artist name.

        Returns:
            None.

        """
        # Add item to the table
        intID = int(myID)
        dicRow = {"ID": intID, "Title": myTitle, "Artist": myArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
    def myDeleteDataProcFunc(intIDDelReceived):
        """ Function to delete CD based on ID passed to function

        Args:
            intIDDelReceived (int): ID of CD to delete.

        Returns:
            None.

        """
        # search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row["ID"] == intIDDelReceived:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print("The CD was removed")
        else:
            print("Could not find this CD!")
        IO.show_inventory(lstTbl) # display inventory
        return

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, startTbl):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dictionary): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            startTbl.clear()  # this clears existing data and allows to load data from file
            objFile = open(file_name, "r")
            for line in objFile:
                data = line.strip().split(",")
                dicRow = {"ID": int(data[0]), "Title": data[1], "Artist": data[2]}
                startTbl.append(dicRow)
            objFile.close()
        except Exception as e:
            print("\nYou need to create a CDInventory.txt file first. \n")
            print(e)
            print("Exiting Program\n")
            sys.exit()
            
    @staticmethod
    def write_file(file_name, recTbl): #save data
        """ Function to save table data to text file
        
        Args:
            file_name (string): name of the file used to write data to.
            recTbl (list of dictionary): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        # Save to text file
        objFile = open(file_name, "w")
        for row in recTbl: # Parse each row
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(",".join(lstValues) + "\n")
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print("Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory")
        print("[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n")

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = " "
        while choice not in ["l", "a", "i", "d", "s", "x"]:
            choice = input("Which operation would you like to perform? [l, a, i, d, s or x]: ").lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(invTbl):
        """Displays current inventory of table invTbl


        Args:
            invTbl (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print("======= The Current Inventory: =======")
        print("ID\tCD Title (by: Artist)\n")
        for row in invTbl:
            print("{}\t{} (by:{})".format(*row.values()))
        print("======================================")
    @staticmethod
    def myAddIOFunc():
        """ Function for input / ouput
            Ask the user CD ID, Title and Artist
    
        Returns:
            strID1 (string): User inputted CD ID.
            strTitle1 (string): User inputted CD Title.
            strArtist1 (string): User inputted CD Artist.
    
        """
        strID1 = input("Enter ID: ").strip()
        strTitle1 = input("What is the CD\"s title? ").strip()
        strArtist1 = input("What is the Artist\"s name? ").strip()
        return strID1, strTitle1, strArtist1

# When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# Start main loop
while True:
    # Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # Process menu selection
    # Process exit first
    if strChoice == "x":
        break
    # Process load inventory
    if strChoice == "l":
        print("WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.")
        strYesNo = input("type \"yes\" to continue and reload from file. otherwise reload will be canceled: ")
        if strYesNo.lower() == "yes":
            print("reloading...")
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input("canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.")
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # Process add a CD
    elif strChoice == "a":
        # Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.myAddIOFunc()
        DataProcessor.myAddProcCode(strID, strTitle, strArtist)
        continue  # start loop back at top.
    # Process display current inventory
    elif strChoice == "i":
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    elif strChoice == "d": # process delete a CD
        IO.show_inventory(lstTbl) # display inventory
        # Get Userinput for which CD to delete
        intIDDelInput = int(input("Which ID would you like to delete? ").strip())
        DataProcessor.myDeleteDataProcFunc(intIDDelInput)
        continue  # start loop back at top.
    elif strChoice == "s": # process save inventory to file
        # Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input("Save this inventory to file? [y/n] ").strip().lower()
        # Process choice
        if strYesNo == "y":
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input("The inventory was NOT saved to file. Press [ENTER] to return to the menu.")
        continue  # start loop back at top.
    # Catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print("General Error")
