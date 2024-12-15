# Variables
from config import Rapport_1, Rapport_2

# Constants
from config import NOT_NECESSARY, LT, DT, OI, PI

"""
Update the Rapport 1 data with the new values.
Args:
    tc_1 (str): TC1 code.
    tc_2 (str): TC2 code.
"""
def updateProcessReportData(tc_1, tc_2):
    Rapport_1[tc_1]['TC2'] = ['v' if tc_2 == '1' and Rapport_1[tc_1]['TC2'][0] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][0], 'v' if tc_2 == '2' and Rapport_1[tc_1]['TC2'][1] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][1], 'v' if tc_2 == '3' and Rapport_1[tc_1]['TC2'][2] != NOT_NECESSARY else Rapport_1[tc_1]['TC2'][2]]

"""
Update the Rapport 2 data with the new values.
Args:
    file_type (str): File type.
    tc_1 (str): TC1 code.
    tc_2 (str): TC2 code.
    tc_3 (str): TC3 code.
"""
def updateSubjectReportData(file_type, tc_1, tc_2, tc_3):
    # Update the record with the new values
    def updateRapport2Row(tc_3, tc_1, tc_2, file_type, searchType):
        Rapport_2[tc_3][tc_1][searchType] = [
            'v' if file_type == searchType and tc_2 == '1' and Rapport_2[tc_3][tc_1][searchType][0] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][0], 
            'v' if file_type == searchType and tc_2 == '2' and Rapport_2[tc_3][tc_1][searchType][1] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][1], 
            'v' if file_type == searchType and tc_2 == '3' and Rapport_2[tc_3][tc_1][searchType][2] != NOT_NECESSARY else Rapport_2[tc_3][tc_1][searchType][2]
        ]

    Rapport_2[tc_3][tc_1]['TC2'] = ['v' if tc_2 == '1' and Rapport_2[tc_3][tc_1]['TC2'][0] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][0], 'v' if tc_2 == '2' and Rapport_2[tc_3][tc_1]['TC2'][1] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][1], 'v' if tc_2 == '3' and Rapport_2[tc_3][tc_1]['TC2'][2] != NOT_NECESSARY else Rapport_2[tc_3][tc_1]['TC2'][2]]
    updateRapport2Row(tc_3, tc_1, tc_2, file_type, LT)
    updateRapport2Row(tc_3, tc_1, tc_2, file_type, OI)
    updateRapport2Row(tc_3, tc_1, tc_2, file_type, PI)
    updateRapport2Row(tc_3, tc_1, tc_2, file_type, DT)

