import os
import errno
import yaml
import sys
from design_type.connection.fin_plate_connection import FinPlateConnection
from design_type.connection.cleat_angle_connection import CleatAngleConnection
import unittest

Output_folder_name = 'Output_PDF'


#predefined pop-up summary.
popup_summary = {'ProfileSummary': {'CompanyName': 'LoremIpsum', 'CompanyLogo': '', 'Group/TeamName': 'LoremIpsum', 'Designer': 'LoremIpsum'},
                'ProjectTitle': 'Fossee', 'Subtitle': '', 'JobNumber': '123', 'AdditionalComments': 'No comments', 'Client': 'LoremIpsum'}


input_file_path = os.path.join(os.path.dirname(__file__), 'ResourceFiles', 'design_example')

output_folder_path = os.path.join(os.path.dirname(__file__), Output_folder_name)


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

make_sure_path_exists(output_folder_path)


osi_files = [file for file in os.listdir(input_file_path) if file.endswith(".osi")]


available_module = {'Fin Plate':FinPlateConnection}  # Add more modules if they are ready.


files_data = []

def precompute_data():

    for file in osi_files:

        in_file = input_file_path + '/' + file

        with open(in_file, 'r') as fileObject:
            uiObj = yaml.load(fileObject, yaml.Loader)

        files_data.append((file, uiObj))


class Modules:

    def run_test(self,mainWindow,main,file_name, file_data): # FinPlate test function . Similarly make functions for other Modules.

        pdf_created = False
        main.set_osdaglogger(None)
        error = main.func_for_validation(main,self,file_data)  # validating files and setting inputs (although we know files are valid).

        if error is None:  # if ran successfully and all input values are set without any error. Now create pdf

            '''


            In save_design function second argument is popup summary which user gives as an input.
            For testing purpose we are giving some default values for creating every pdf.
            We are actually not comparing pdf. This is just for testing purpose whether function
            is running fine and creating pdf or not.

            I have made some changes in save_design function. Instead of asking for output file
            location from save_design function it'll ask from 'save_inputSummary' function inside
            ui_summary_popup.py file immediately after getting popup inputs and send it to
            save_design function using the same dictionary in which popup inputs are present
            with key name as 'filename'.


            '''

            duplicate = output_folder_path         # Making duplicate so that original path doesn't change.
            duplicate = duplicate + '/' + file_name  # giving each output file it's corresponding input file name.
            popup_summary['filename'] = duplicate    # adding this key in popup_summary dict.
            main.save_design(main,popup_summary)  # calling the function.
            pdf_created = True   # if pdf created

        return pdf_created


class TestModules(unittest.TestCase):
    def __init__(self, input, output):
        super(TestModules, self).__init__()
        self.input = input
        self.output = output
        self.module = Modules()

    def runTest(self):

        file_name = self.input[0]
        file_data = self.input[1]
        file_class = available_module[file_data['Module']]
        ans = self.module.run_test(self.module,file_class,file_name, file_data)
        self.assertTrue(ans is self.output)



def suite():
    suite = unittest.TestSuite()
    #suite.addTests(TestModules(item, True) for item in files_data )

    ''' Uncomment and add condition according to your need if you want to run tests only for some specific modules. '''
    suite.addTests(TestModules(item, True) for item in files_data if item[1]['Module'] in available_module)

    return suite


if __name__ == '__main__':

    precompute_data()


    log_file = "test_log_file.txt"   # file in which test results will be written.


    test_log = open(log_file,'w')
    result = unittest.TextTestRunner(stream=test_log, verbosity=2).run(suite())
    test_log.close()




    #with open(log_file, 'r') as content_file:
        #content = content_file.read()

    '''
        Reading the log file to see the output on console rather than opening the log file to see the output.
        In actual test environment we won't need it.
    '''
    #print(content)



    #test_exit_code = int(not result.wasSuccessful())
    #print('Exit Status Code is : ',test_exit_code)
