import argparse
import requests
import csv

from html.parser import HTMLParser

# Custom HTMLTableParser to extract text
class HTMLTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_data = []
        self.table_data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.in_row = True
            self.current_data = []
        elif tag == 'td':
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.in_row = False
            if self.current_data:
                self.table_data.append(self.current_data)
        elif tag == 'td':
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_data.append(data.strip())
            
# Custom HTMLPageParser to extract text
class HTMLTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)

#Page parser - copy and save the hole page
def save_full_page(full_text, output_target, debugMode):
    if debugMode: #sending debug info    
        print(f"DEBUG:: Entered Full page subroutine, starting to save output file at {output_target}.")
    with open(output_target, "w", encoding="utf-8") as text_file:
        text_file.write(full_text)
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"Full text content saved successfully in {output_target}!")
    
#Table parser - copy and save a page based on parameters pre-set
def save_table_data(table_data, output_target, rowAmount, debugMode):
    with open(output_target, "w", encoding="utf-8") as text_file:
        row_count = 0
        for row in table_data:
            if len(row) == rowAmount:  # Ensure that we are fetching the correct table
                if debugMode: # Debugging: Print each row
                    print(f"Processing row {row_count}: {row}")  
                line = " - ".join(row)  # Join the row data with a "-"
                text_file.write(line + "\n")  # Write the line to the file
            else:
                if debugMode: # Debugging: Print each row
                    print(f"Row {row_count}: params are wrong, ignoring content {row}")  # Content doens't align with the format, ignoring it.
            row_count += 1
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"Full text content saved successfully in {output_target}!")

#Xml parser - TODO
def save_into_xml(debugMode):
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"File content created successfully in {debugMode}!")
        
#Xml parser - TODO
def save_into_lua(debugMode):
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"File content created successfully in {debugMode}!")

# Step 0: Setup 'Arguments' parser
Arguments = argparse.ArgumentParser(description="Save webpage content or table data.")
ExclusiveArguments = Arguments.add_mutually_exclusive_group() #create a mutually exclusive group of arguments ensuring the user wont choose multiple data methods
ExclusiveArguments.add_argument('-xml', action='store_true', help="This will parse the info as XMl files over multiple files accoding to the setted up method.")
ExclusiveArguments.add_argument('-table', action='store_true', help="This will parse into a .TXT file a table of data lined per row and separated by '-'.")
ExclusiveArguments.add_argument('-page', action='store_true', help="(DEFAULT) This will parse into a .TXT file the hole page as plain text.")
ExclusiveArguments.add_argument('-lua', action='store_true', help="This will parse the info as Lua files over multiple files accoding to the setted up method.")
Arguments.add_argument('-c', '--cols', type=int, default=6, help="(DEFAULT = 6) Number of columns to consider in the table. this is used on XML and TABLE options.")
Arguments.add_argument('-f', '--outfile', type=str, default="content.txt", help="(DEFAULT = web_content.txt) the file that is receiving the text info if we are using PAGE or Table options.")
Arguments.add_argument('-l', '--dir', '-outfolder', type=str, default="Moves", help="(DEFAULT = Moves) the folder that will be receiving the xml files if we are using XML option.")
Arguments.add_argument('-d', '--debug', action='store_true', help="activate console debug messages.")
Arguments.add_argument('-t', '--target', type=str, default="https://pokemondb.net/move/generation/1", help="(DEFAULT = https://pokemondb.net/move/generation/1activate) target website for content extraction.")
args = Arguments.parse_args() #parse arguments

if args.debug: # informing user if DEBUG is being done     
    print("DEBUG:: debug is true, starting routine.")

if not (args.page or args.xml or args.table or args.lua):
    args.page = True
    if args.debug: # informing user that we are assuming default operation     
        print("DEBUG:: Parsing Method was not chosen, using hole page as default.")

# Step 1: Get web information
response = requests.get(args.target)
webpage_content = response.content.decode('utf-8') # decode web information to utf-8 encoding standard
if args.debug: #sending debug info 
    print("DEBUG:: getting website response and content.")

# Step 2: Parse the HTML content
if args.page:
    parser = HTMLTextParser()
    parser.feed(webpage_content)
    if args.debug: #sending debug info    
        print("DEBUG:: parsing website content on HTMLTextParser subroutine to flush the hole text.")
else:
    parser = HTMLTableParser()
    parser.feed(webpage_content)
    if args.debug: #sending debug info    
        print("DEBUG:: parsing website content on HTMLTableParser subroutine to output the table rows.")
    
    

# Step 3: define wich saving method we are using and save the data accoding
# Step 3.1 -> default or user wants to save hole data as plain text to a file
if args.page: 
    save_full_page(parser.get_text(), args.outfile, args.debug)
    
# Step 3.2 -> user wants to save table data to a file
if args.table:
    save_table_data(parser.table_data, args.outfile, args.cols, args.debug)
    
# Step 3.3 -> user wants to save in XML files
if args.xml:
    save_into_xml(args.debug)
    
# Step 3.4 -> user wants to save in Lua files
if args.lua:
    save_into_lua(args.debug)
    
    
# Step #last: code finished successfully, execution terminated, informing user
print("Code execution finished successfully.")