import argparse
import requests
import csv
import os

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
        elif tag == 'img' and self.in_cell:
            for attr in attrs:
                if attr[0] == 'alt':  # or 'title', depending on how the content is labeled
                    self.current_data.append(attr[1])

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
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'alt':  # Extract the 'alt' text if available
                    self.text.append(attr[1])

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)

#Page parser - copy and save the hole page
def save_full_page(full_text, output_target, debugMode):
    """
    Saves the full HTML content to a specified file.

    Parameters:
    full_text (str): The HTML content to be saved.
    output_target (str): The file path where the content will be saved.
    debugMode (bool): Flag to enable/disable debug messages.

    Returns:
    None
    """
    if debugMode: #sending debug info    
        print(f"DEBUG:: Entered Full page subroutine, starting to save output file at {output_target}.")
    with open(output_target, "w", encoding="utf-8") as text_file:
        text_file.write(full_text)
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"DEBUG:: Full text content saved successfully in {output_target}!")
    
#Table parser - copy and save a page based on parameters pre-set
def save_table_data(table_data, output_target, rowAmount, debugMode):
    """
    Saves the Table HTML content to a specified file.

    Parameters:
    table_data (list): The HTML content to be saved.
    output_target (str): The file path where the table data will be saved.
    rowAmount (int): The expected number of columns in each row to be saved.
    debugMode (bool): Flag to enable or disable debug messages.

    Returns:
    None
    """
    with open(output_target, "w", encoding="utf-8") as text_file:
        row_count = 0
        for row in table_data:
            if len(row) == rowAmount:  # Ensure that we are fetching the correct table
                if debugMode: # Debugging: Print each row
                    print(f"DEBUG:: Processing row {row_count}: {row}")  
                line = " - ".join(row)  # Join the row data with a "-"
                text_file.write(line + "\n")  # Write the line to the file
            else:
                if debugMode: # Debugging: Print each row
                    print(f"DEBUG:: Row {row_count}: params are wrong, ignoring content {row}")  # Content doens't align with the format, ignoring it.
            row_count += 1
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"DEBUG:: Full text content saved successfully in {output_target}!")

#Xml parser - save moves tags into a xml config file
def save_into_xml(table_data, output_folder, rowAmount, debugMode):
    """
    Saves the Table HTML content to a specified file.

    Parameters:
    table_data (list): The HTML content to be saved.
    output_target (str): The file path where the table data will be saved.
    rowAmount (int): The expected number of columns in each row to be saved.
    debugMode (bool): Flag to enable or disable debug messages.

    Returns:
    None
    """
    output_file = "moves.xml"
    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        if debugMode:
            print(f"DEBUG:: Created directory {output_folder}")

    # Full path to the output file
    output_path = os.path.join(output_folder, output_file)
    with open(output_path, "w", encoding="utf-8") as file:
        # Start the XML structure
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<moves>\n')
        for row in table_data:
            if len(row) == rowAmount: # Ensure that we are fetching the correct table
                if debugMode: # Debugging: Print each row
                    print(f"DEBUG:: Processing row {row_count}: {row}")  
                move_name = row[0]
                move_type = row[1]
                # Construct the XML content for each move
                xml_content = f'    <move name="{move_name}" words="{move_name.lower()}" control="revision" script="{move_type}/{move_name}.lua"/>\n'
                file.write(xml_content)
                if debugMode:
                    print(f"DEBUG:: Added {move_name} to XML file")
        # End the XML structure
        file.write('</moves>\n')  
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"DEBUG:: All moves saved successfully in {output_file}!")
        
#Lua parser - create a parser for lua files
def save_into_lua(table_data, output_folder, rowAmount, debugMode):
    """
    Generates and saves Lua scripts based on table data for each move.

    Parameters:
    table_data (list): A list of lists, where each sublist contains data for a specific move.
    output_folder (str): The folder where the Lua scripts will be saved.
    rowAmount (int): The expected number of columns in each row to ensure correct data parsing.
    debugMode (bool): Flag to enable or disable debug messages.

    Returns:
    None
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        if debugMode:
            print(f"DEBUG:: Created directory {output_folder}")
            
    for row in table_data:
        if len(row) == rowAmount:  # Ensure that we are fetching the correct table
            if debugMode:  # Debugging: Print each row
                print(f"DEBUG:: Processing row: {row}")        
            move_name = row[0]
            move_type = row[1]
            move_category = row[2]
            move_power = row[3]
            move_accuracy = row[4]
            move_PP = row[5]
            move_Effect = row[6]
                
            # Create a unique file name based on the move name (row[0])
            output_file = f"{move_name}.lua"
            output_path = os.path.join(output_folder, output_file)
            
            # Define the Lua script content
            lua_content = f'''
    
-- This move type is '{move_type}'
-- This move category is '{move_category}' ( put into XML file? )
-- This move PP is {move_PP} (evaluate if this is necessary, usage? conversion?)
-- This move EFFECT/DESCRIPTION is '{move_Effect}' this shoud be reflected in the spell routing

local power = {move_power}
local name = "{move_name}"
local accuracy = {move_accuracy}
local eff = 1 -- change magic effect

-- adapt area of spell
local area = {{ 
    {{0, 0, 0, 0, 0}},
    {{0, 1, 1, 1, 0}},
    {{0, 1, 2, 1, 0}},
    {{0, 1, 1, 1, 0}},
    {{0, 0, 0, 0, 0}}
}}

local combat = Combat()
-- Spell Damage
combat:setMove(power, accuracy, name)
combat:setParameter(COMBAT_PARAM_MAGICAL, FALSE)
-- Spell Animation
combat:setParameter(COMBAT_PARAM_TYPE, COMBAT_NORMALDAMAGE)
combat:setArea(createCombatArea(area))
-- Condition to apply?
combat:setParameter(COMBAT_PARAM_CONDITION, CONDITION_ATTRIBUTES) -- REVIEW CONDITION
combat:setParameter(COMBAT_PARAM_CONDITIONCHANCE, 100)
combat:setParameter(COMBAT_PARAM_CONDITIONVALUE, 13)
combat:setParameter(COMBAT_PARAM_CONDITIONTIME, 30)
combat:setParameter(COMBAT_PARAM_CONDITIONSKILL, STAT_DEFENSE)

function onCastSpell(creature, variant, isHotkey)
    creature:say(string.upper(name), TALKTYPE_MONSTER_SAY)
    
    -- remove if not using area
    local pos = creature:getPosition()
    pos.x = pos.x + 1
    pos.y = pos.y + 1
    Position(pos):sendMagicEffect(eff)
    
    return combat:execute(creature, variant)
end
'''
            output_file = f"{move_name}.lua"
            output_path = os.path.join(output_folder, output_file)
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(lua_content) 
                
                if debugMode:
                    print(f"DEBUG:: Lua script saved successfully in {output_path}")       
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(lua_content)       
                if debugMode:
                    print(f"DEBUG:: Lua script saved successfully in {output_path}")
                    
    if debugMode: # Debugging: Print the sucessfull save on output_target       
        print(f"DEBUG:: All moves saved successfully in {output_file}!")

# Step 0: Setup 'Arguments' parser
Arguments = argparse.ArgumentParser(description="Save webpage content or table data.")
ExclusiveArguments = Arguments.add_mutually_exclusive_group() #create a mutually exclusive group of arguments ensuring the user wont choose multiple data methods
ExclusiveArguments.add_argument('-xml', action='store_true', help="This will parse the info as XMl files over multiple files accoding to the setted up method.")
ExclusiveArguments.add_argument('-table', action='store_true', help="This will parse into a .TXT file a table of data lined per row and separated by '-'.")
ExclusiveArguments.add_argument('-page', action='store_true', help="(DEFAULT) This will parse into a .TXT file the hole page as plain text.")
ExclusiveArguments.add_argument('-lua', action='store_true', help="This will parse the info as Lua files over multiple files accoding to the setted up method.")
Arguments.add_argument('-c', '--cols', type=int, default=7, help="(DEFAULT = 7) Number of columns to consider in the table. this is used on XML and TABLE options.")
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
    save_into_xml(parser.table_data, args.dir, args.cols,args.debug)
    
# Step 3.4 -> user wants to save in Lua files
if args.lua:
    save_into_lua(parser.table_data, args.dir, args.cols,args.debug)
    
    
# Step 4: code finished successfully, execution terminated, informing user
print("Code execution finished successfully.")