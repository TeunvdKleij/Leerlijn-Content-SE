# Variables
from config import VERBOSE, Rapport_1, Rapport_2, WIPFiles, failedFiles, failedImages, parsedFiles, REPORT_PATH

# Constants
from config import LT, DT, OI, PI, FAIL_CIRCLE, SUCCESS, NOT_NECESSARY

# Functions
from files.markdown_utils import format_file_report_table
from files.images import format_image_report_table
from report.table import generate_markdown_table

"""
Generate the report based on the taxonomie report, success, and failed reports.
"""
def generate_report(REPORT_PATH):
    if VERBOSE: print("Generating report...")
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write('---\ndraft: true\n---\n')
        
        f.write('## Rapport 1 - Processtappen\n')
        f.write('*Doel: achterhalen welke processtappen nog helemaal niet zijn geïmplementeerd*\n\n')
        f.write('- ✅ Er bestaat een bestand met deze taxonomiecode op dit niveau \n')
        f.write('- ⛔️ Er is geen enkel bestand met deze taxonomiecode op dit niveau \n')
        f.write('- 🏳️ De taxonomiecode wordt niet aangeboden op dit niveau (X in de Dataset) \n')
        f.write('\n')
        f.write(generate_rapport_1())

        f.write('\n\n')

        f.write('## Rapport 2 - Onderwerpen Catalogus\n')
        f.write('*Doel: Lijst met onderwerpen + gekoppelde taxonomie code voor inzicht in aangeboden onderwerpen.*\n')
        f.write('Bij kolom *TC2*, *Leertaken*, *Ondersteunende informatie*, *Procedurele informatie* en *Deeltaken* zijn drie tekens aanwezig om de drie HBO-i niveaus weer te geven\n\n')
        f.write('- ✅ Het onderwerp met taxonomie code wordt aangeboden op het aangegeven niveau \n')
        f.write('- ⛔️ Het onderwerp met taxonomie code wordt **niet** aangeboden op het aangegeven niveau \n')
        f.write('- 🏳️ Het onderwerp hoeft met deze taxonomie code niet aangeboden te worden op het aangegeven niveau \n')
        f.write('\n')
        f.write(generate_rapport_2())

        f.write('\n\n')

        f.write("## Work-in-progress bestanden\n")
        f.write('Doel: De onderstaande bestanden hebben nog todo items in de markdown staan.\n')
        f.write('Deze todo items moeten nog worden afgehandeld.\n')
        f.write('\n')
        f.write(format_file_report_table(sorted(WIPFiles, key=lambda x: x['file'])))

        f.write('\n\n')

        f.write("## Gefaalde bestanden\n")
        f.write("*Doel: De onderstaande bestanden zijn niet succesvol verwerkt.*\n\n")
        f.write('❌ Dit bestand bevat nog geen taxonomie code\n')
        f.write('⚠️ Dit bestand bevat een foute taxonomie code. Zie de *Errors* kolom om te weten wat er mis is\n')
        f.write('🟠 Dit bestand bevat een taxonomie code die niet toegevoegd hoeft te zijn\n')
        f.write('\n')
        f.write(format_file_report_table(sorted(failedFiles, key=lambda x: x['file'])))

        f.write('\n\n')

        f.write("## Gefaalde images\n")
        f.write("*Doel: De onderstaande images missen een 4C/ID component.*\n\n")
        f.write('Als een image de error heeft over het niet gebruikt worden, betekent dit dat de image niet in build staat, maar nog wel in content.\n\n')
        f.write(format_image_report_table(sorted(failedImages, key=lambda x: x['image'])))

        f.write('\n\n')

        f.write("## Geslaagde bestanden\n")
        f.write("De onderstaande bestanden zijn succesvol verwerkt.\n")
        f.write('\n')
        f.write(format_file_report_table(sorted(parsedFiles, key=lambda x: x['file'])))

        f.write('\n\n')

    if VERBOSE:
        print("Rapport 1:")
        print(generate_rapport_1())
        print("Rapport 2:")
        print(generate_rapport_2())
        print("Geslaagde bestanden:")
        print(format_file_report_table(sorted(parsedFiles, key=lambda x: x['file'])))
        print("Gefaalde bestanden:")
        print(format_file_report_table(sorted(failedFiles, key=lambda x: x['file'])))
        print("Gefaalde images:")
        print(format_image_report_table(sorted(failedImages, key=lambda x: x['image'])))
        print("Report generated.")


"""
Format the report table for table 1
Returns:
    table (str): Markdown table string.
"""
def generate_rapport_1():
    if VERBOSE: print("Generating Rapport 1 table...")

    headers = ["TC1", "Proces", "Processtap", "Niveau 1", "Niveau 2", "Niveau 3"]
    rows = []
    for tc, details in Rapport_1.items():
        proces = details.get('Proces', '')
        processtap = details.get('Processtap', '')
        tc2_levels = details.get('TC2', {})
        niveau_1 = FAIL_CIRCLE if tc2_levels[0] == 'x' else SUCCESS if tc2_levels[0] == 'v' or tc2_levels[0] == 'g' else NOT_NECESSARY
        niveau_2 = FAIL_CIRCLE if tc2_levels[1] == 'x' else SUCCESS if tc2_levels[1] == 'v' or tc2_levels[1] == 'g' else NOT_NECESSARY        
        niveau_3 = FAIL_CIRCLE if tc2_levels[2] == 'x' else SUCCESS if tc2_levels[2] == 'v' or tc2_levels[2] == 'g' else NOT_NECESSARY
        rows.append([tc, proces, processtap, niveau_1, niveau_2, niveau_3])

    table = generate_markdown_table(headers, rows)
    if VERBOSE: print("Rapport 1 table generated.")
    return table

"""
Format the report for table 2
Returns:
    table (str): Markdown table string.
"""
def generate_rapport_2():
    if VERBOSE: print("Generating Rapport 2 table...")

    headers = ["TC3", "TC1", "TC2", LT, OI, PI, DT]
    rows = []

    def get_status(value):
        if value == 'v' or value == 'g':
            return SUCCESS
        elif value != NOT_NECESSARY:
            return FAIL_CIRCLE
        else:
            return NOT_NECESSARY

    for tc3, details in Rapport_2.items():
        for tc1, other in details.items():
            tc2_levels = other.get('TC2', [''] * 3)
            tc2 = ' '.join([get_status(level) for level in tc2_levels])

            leertaak_levels = other.get(LT, [''] * 3)
            leertaak = ' '.join([get_status(level) for level in leertaak_levels])

            ondersteunende_informatie_levels = other.get(OI, [''] * 3)
            ondersteunende_informatie = ' '.join([get_status(level) for level in ondersteunende_informatie_levels])
            
            procedurele_informatie_levels = other.get(PI, [''] * 3)
            procedurele_informatie = ' '.join([get_status(level) for level in procedurele_informatie_levels])
            
            deeltaak_levels = other.get(DT, [''] * 3)
            deeltaak = ' '.join([get_status(level) for level in deeltaak_levels])

            rows.append([tc3, tc1, tc2, leertaak, ondersteunende_informatie, procedurele_informatie, deeltaak])

    table = generate_markdown_table(headers, rows)
    if VERBOSE: print("Rapport 2 table generated.")
    return table