#Global variables
Dataset = list()  # Dataset list
Successful_files = [] # Track the status of each file
Failed_files = [] # Track the status of each file
Failed_images = [] # Track which images don't start with a 4C/ID component
WIP_files = [] # Track the files that contain Work-in-progress items
Verbose = False # Verbose output flag
Testing = False # Testing output flag
Taxonomie_pattern = r'^[a-z]{2}-\d{1,3}\.[123]\.[^\s\.]+(\.[^\s\.]+)*\.(?:OI|DT|PI|LT)$' # Taxonomie pattern
ValidDynamicLinkPrefixes = ['https://', 'http://', 'tags/'] # List of valid dynamic links
Rapport_1 = {} # Rapport 1 data
Rapport_2 = {} # Rapport 2 data
ToDo_pattern = r'-=[A-Z]+=-' # To-Do pattern
test_dir = "./.github/tests/test_cases" # Directory of the test cases

# Dataset columns
TC1_COL = 1
TC2_COL = 2
TC3_COL = 5
PROCES_COL = 3
PROCESSTAP_COL = 4
LT_COL = 7
OI_COL = 8
PI_COL = 9
DT_COL = 10

# 4CID
LT = "Leertaken"
OI = "Ondersteunende-informatie" 
PI = "Procedurele-informatie"
DT = "Deeltaken"

#Error message for not including any taxonomy code
ERROR_MISSING_TAXCO = "No taxonomie found in file."

# Icons
SUCCESS = "✅"
FAIL_CIRCLE = "⛔️"
FAIL_CROSS = "❌"
NOT_NECESSARY = "🏳️"
WRONG_TAXONOMY_CODE = "⚠️"
NOT_NEEDED = "🟠"
TODO_ITEMS = "🔨"