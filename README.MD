# THIS IS A SIMPLE WEBPAGE DOWNLOADER TO MANAGE INFO, IF YOU NEED THE INFO TO BE MANAGED IN A DIFFERENT WAY:

1. Clone this repository using your SSH key: `git clone --recursive git@github.com:ograda/webpageinfo_to_xml.git` (or download it directly from the same link).
2. Open PowerShell or CMD and navigate to the project repository folder
3. This python script only uses basic python libraries so if you have python, you should be able to use it, however you might need to add requests `pip install requests`


# ARGUMENTS AND DEFAULTS

1. you can see all commands available with a -h or --help argument
2. The export method is mutual exclusive, so you can only use one method at a time (Hole page, Table content, XML or Lua file)
3. If using XMl and Lua export, make sure to set code you example parameters correctly
4. The default paramenters will be set to
    * OUTPUT_TYPE 	= FULL PAGE (page, table, lua, xml)
    * OUTPUT_FILE 	= content.txt (full page and table)
    * OUTPUT_FOLDER = Moves (xml and lua)
	* URL_TARGET 	= https://pokemondb.net/move/generation/1
	* #COLLUMS 		= 7
    * DEBUG			= False


## Running

1. python main.py `ARGS[]`


## TODO

1. Lua parsing subroutine
2. Xml parsing subroutine