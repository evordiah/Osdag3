"created by anjali"

from design_type.connection.moment_connection import MomentConnection
from utils.common.component import *
from Common import *
from utils.common.load import Load
from design_report.reportGenerator_latex import CreateLatex
from Report_functions import *
import yaml

import os
from design_report.reportGenerator_latex import CreateLatex
from Report_functions import *
import logging


class BeamCoverPlateWeld(MomentConnection):

    def __init__(self):
        super(BeamCoverPlateWeld, self).__init__()
        self.design_status = False

    ###############################################
    # Design Preference Functions Start
    ###############################################
    def tab_list(self):
        """

        :return: This function returns the list of tuples. Each tuple will create a tab in design preferences, in the
        order they are appended. Format of the Tuple is:
        [Tab Title, Type of Tab, function for tab content)
        Tab Title : Text which is displayed as Title of Tab,
        Type of Tab: There are Three types of tab layouts.
            Type_TAB_1: This have "Add", "Clear", "Download xlsx file" "Import xlsx file"
            TYPE_TAB_2: This contains a Text box for side note.
            TYPE_TAB_3: This is plain layout
        function for tab content: All the values like labels, input widgets can be passed as list of tuples,
        which will be displayed in chosen tab layout

        """
        tabs = []

        t1 = (KEY_DISP_BEAMSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t1)

        t6 = ("Connector", TYPE_TAB_2, self.plate_connector_values)
        tabs.append(t6)

        t3 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t3)

        t4 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t4)

        t5 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t5)

        return tabs

    def tab_value_changed(self):

        """

        :return: This function is used to update the values of the keys in design preferences,
         which are dependent on other inputs.
         It returns list of tuple which contains, tab name, keys whose values will be changed,
         function to change the values and arguments for the function.

         [Tab Name, [Argument list], [list of keys to be updated], input widget type of keys, change_function]

         Here Argument list should have only one element.
         Changing of this element,(either changing index or text depending on widget type),
         will update the list of keys (this can be more than one).

         """

        change_tab = []

        t2 = (KEY_DISP_BEAMSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX, self.get_fu_fy_I_section)
        change_tab.append(t2)

        t3 = ("Connector", [KEY_CONNECTOR_MATERIAL], [KEY_CONNECTOR_FU, KEY_CONNECTOR_FY_20, KEY_CONNECTOR_FY_20_40,
                                                      KEY_CONNECTOR_FY_40], TYPE_TEXTBOX, self.get_fu_fy)
        change_tab.append(t3)

        t5 = (KEY_DISP_BEAMSEC, ['Label_1', 'Label_2', 'Label_3', 'Label_4'],
              ['Label_11', 'Label_12', 'Label_13', 'Label_14', 'Label_15', 'Label_16', 'Label_17', 'Label_18',
               'Label_19', 'Label_20'], TYPE_TEXTBOX, self.get_I_sec_properties)
        change_tab.append(t5)

        return change_tab

    def edit_tabs(self):
        """ This function is required if the tab name changes based on connectivity or profile or any other key.
        Not required for this module but empty list should be passed"""
        return []

    # def list_for_fu_fy_validation(self):
    #     """ This function is no longer required"""
    #     fu_fy_list = []
    #
    #     t2 = (KEY_SEC_MATERIAL, KEY_SEC_FU, KEY_SEC_FY)
    #     fu_fy_list.append(t2)
    #
    #     t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
    #     fu_fy_list.append(t3)
    #
    #     return fu_fy_list

    def input_dictionary_design_pref(self):
        """

        :return: This function is used to choose values of design preferences to be saved to design dictionary.

         It returns list of tuple which contains, tab name, input widget type of keys, keys whose values to be saved,

         [(Tab Name, input widget type of keys, [List of keys to be saved])]

         """
        design_input = []

        t2 = (KEY_DISP_BEAMSEC, TYPE_COMBOBOX, [KEY_SEC_MATERIAL])
        design_input.append(t2)

        # t2 = (KEY_DISP_BEAMSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY])
        # design_input.append(t2)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_TEXTBOX, [KEY_DP_DETAILING_GAP])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD])
        design_input.append(t6)

        t7 = ("Connector", TYPE_COMBOBOX, [KEY_CONNECTOR_MATERIAL])
        design_input.append(t7)

        return design_input

    def input_dictionary_without_design_pref(self):
        """

         :return: This function is used to choose values of design preferences to be saved to
         design dictionary if design preference is never opened by user. It sets are design preference values to default.
         If any design preference value needs to be set to input dock value, tuple shall be written as:

         (Key of input dock, [List of Keys from design preference], 'Input Dock')

         If the values needs to be set to default,

         (None, [List of Design Prefernce Keys], '')

          """
        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (None, [KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_GAP,
                     KEY_DP_DESIGN_METHOD, KEY_CONNECTOR_MATERIAL], '')
        design_input.append(t2)

        return design_input

    def refresh_input_dock(self):
        """

        :return: This function returns list of tuples which has keys that needs to be updated,
         on changing Keys in design preference (ex: adding a new section to database should reflect in input dock)

         [(Tab Name,  Input Dock Key, Input Dock Key type, design preference key, Master key, Value, Database Table Name)]
        """
        add_buttons = []

        t2 = (KEY_DISP_BEAMSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    ####################################
    # Design Preference Functions End
    ####################################
    def set_osdaglogger(key):

        """
        Function to set Logger for Tension Module
        """

        # @author Arsil Zunzunia
        global logger
        logger = logging.getLogger('osdag')

        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.FileHandler('logging_text.log')

        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if key is not None:
            handler = OurLog(key)
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                          datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def input_values(self, existingvalues={}):

        options_list = []

        if KEY_SECSIZE in existingvalues:
            existingvalue_key_secsize = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_secsize = ''

        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_MOMENT in existingvalues:
            existingvalues_key_moment = existingvalues[KEY_MOMENT]
        else:
            existingvalues_key_moment = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_DP_WELD_TYPE in existingvalues:
            existingvalue_key_weld_type = existingvalues[KEY_DP_WELD_TYPE]
        else:
            existingvalue_key_weld_type = ''

        if KEY_FLANGEPLATE_PREFERENCES in existingvalues:
            existingvalue_key_fplate_pref = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_pref = ''

        if KEY_FLANGEPLATE_THICKNESS in existingvalues:
            existingvalue_key_fplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_fplate_thk = ''

        if KEY_WEBPLATE_THICKNESS in existingvalues:
            existingvalue_key_wplate_thk = existingvalues[KEY_PLATETHK]
        else:
            existingvalue_key_wplate_thk = ''

        t16 = (KEY_MODULE, KEY_DISP_BEAMCOVERPLATEWELD, TYPE_MODULE, None, None, True, 'No Validator')
        options_list.append(t16)

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t1)

        t4 = (KEY_SECSIZE, KEY_DISP_SECSIZE, TYPE_COMBOBOX, existingvalue_key_secsize, connectdb("Beams"), True, 'No Validator')
        options_list.append(t4)

        t15 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, True, 'No Validator')
        options_list.append(t15)

        t5 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t5)

        t19 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, existingvalue_key_weld_type,
            VALUES_WELD_TYPE, True, 'No Validator')
        options_list.append(t19)

        t6 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t6)

        t17 = (KEY_MOMENT, KEY_DISP_MOMENT, TYPE_TEXTBOX,existingvalues_key_moment, None, True, 'No Validator')
        options_list.append(t17)

        t7 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None, True, 'No Validator')
        options_list.append(t7)

        t8 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None, True, 'No Validator')
        options_list.append(t8)

        t18 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t18)

        t19 = (KEY_FLANGEPLATE_PREFERENCES, KEY_DISP_FLANGESPLATE_PREFERENCES, TYPE_COMBOBOX, existingvalue_key_fplate_pref, VALUES_FLANGEPLATE_PREFERENCES, True, 'No Validator')
        options_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_fplate_thk, VALUES_FLANGEPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t20)

        t21 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t21)

        t22 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_wplate_thk, VALUES_WEBPLATE_THICKNESS, True, 'No Validator')
        options_list.append(t22)

        return options_list

    def flangecapacity(self, flag):

        flangecapacity = []

        t30 =(KEY_FLANGE_TEN_CAPACITY,KEY_DISP_FLANGE_TEN_CAPACITY,TYPE_TEXTBOX,
               round(self.section.tension_capacity_flange/1000, 2) if flag else '')
        flangecapacity.append(t30)
        t30 = (KEY_FLANGE_PLATE_TEN_CAP, KEY_DISP_FLANGE_PLATE_TEN_CAP, TYPE_TEXTBOX,
               round(self.flange_plate.tension_capacity_flange_plate / 1000, 2) if flag else '')
        flangecapacity.append(t30)

        return flangecapacity

    def customized_input(self):

        list1 = []
        t4 = (KEY_WEBPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t4)
        t5 = (KEY_FLANGEPLATE_THICKNESS, self.plate_thick_customized)
        list1.append(t5)

        return list1

    def webcapacity(self, flag):

        webcapacity = []
        t30 = (KEY_WEB_TEN_CAPACITY, KEY_DISP_WEB_TEN_CAPACITY, TYPE_TEXTBOX,
               round(self.section.tension_capacity_web / 1000,2) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_TEN_CAP_WEB_PLATE, KEY_DISP_TEN_CAP_WEB_PLATE, TYPE_TEXTBOX,
               round(self.web_plate.tension_capacity_web_plate/ 1000, 2) if flag else '')
        webcapacity.append(t30)
        t30 = (KEY_WEBPLATE_SHEAR_CAPACITY, KEY_DISP_WEBPLATE_SHEAR_CAPACITY, TYPE_TEXTBOX,
               round(self.web_plate.shear_capacity_web_plate / 1000, 2) if flag else '')
        webcapacity.append(t30)
        return webcapacity

    def web_weld_details(self,flag):
        web_weld_details = []
        # t15 = (KEY_WEB_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,(self.l_req_weblength) if flag else '')
        # web_weld_details.append(t15)
        t14 = (KEY_WEB_WELD_SIZE, KEY_WEB_DISP_WELD_SIZE, TYPE_TEXTBOX, self.web_weld.size if flag else '')
        web_weld_details.append(t14)

        t15 = (KEY_WEB_WELD_STRENGTH, KEY_WEB_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
           self.web_weld.strength if flag else '')
        web_weld_details.append(t15) #in N/mm

        t16 = (KEY_WEB_WELD_STRESS, KEY_WEB_DISP_WELD_STRESS, TYPE_TEXTBOX, self.web_weld.stress if flag else '')
        web_weld_details.append(t16)

        return web_weld_details

    def flange_weld_details(self, flag):
        flange_weld_details = []
        # t15 = (KEY_FLANGE_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,
        #       (self.l_req_flangelength) if flag else '')
        # flange_weld_details.append(t15)

        # t15 = (KEY_FLANGE_WELD_HEIGHT, KEY_DISP_FLANGE_WELD_HEIGHT, TYPE_TEXTBOX,
        #        (self.flange_weld.height) if flag else '')
        # flange_weld_details.append(t15)

        t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        flange_weld_details.append(t14)

        t15 = (KEY_FLANGE_WELD_STRENGTH, KEY_FLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
            self.flange_weld.strength if flag else '')
        flange_weld_details.append(t15) #in N/mm

        t16 = (KEY_FLANGE_WELD_STRESS, KEY_FLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX,self.flange_weld.stress if flag else '')
        flange_weld_details .append(t16) #in N/mm

        return flange_weld_details


    def Innerflange_weld_details(self, flag):
        Innerflange_weld_details = []
        # t15 = (KEY_INNERFLANGE_WELD_LENGTH, KEY_DISP_INNERFLANGE_WELD_LENGTH, TYPE_TEXTBOX,
        #       ( self.flange_weld.Innerlength ) if flag else '')
        # Innerflange_weld_details.append(t15)
        # t15 = (KEY_FLANGE_WELD_LENGTH, KEY_DISP_WELD_LEN_EFF_OUTSIDE, TYPE_TEXTBOX,
        #        (self.l_req_flangelength) if flag else '')
        # Innerflange_weld_details.append(t15)

        # t15 = (KEY_INNERFLANGE_WELD_HEIGHT, KEY_DISP_INNERFLANGE_WELD_HEIGHT, TYPE_TEXTBOX,
        #        (self.flange_weld.Innerheight) if flag else '')
        # Innerflange_weld_details.append(t15)

        t14 = (KEY_FLANGE_WELD_SIZE, KEY_FLANGE_DISP_WELD_SIZE, TYPE_TEXTBOX, self.flange_weld.size if flag else '')
        Innerflange_weld_details.append(t14)

        t15 = (KEY_INNERFLANGE_WELD_STRENGTH, KEY_INNERFLANGE_DISP_WELD_STRENGTH, TYPE_TEXTBOX,
             self.flange_weld.strength if flag else '')
        Innerflange_weld_details.append(t15) #in N/mm

        t16 = (KEY_INNERFLANGE_WELD_STRESS, KEY_INNERFLANGE_DISP_WELD_STRESS, TYPE_TEXTBOX, self.flange_weld.stress if flag else '')
        Innerflange_weld_details .append(t16) #in N/mm

        return Innerflange_weld_details

    def member_capacityoutput(self,flag):
        member_capacityoutput = []
        t29 = (KEY_MEMBER_MOM_CAPACITY, KEY_OUT_DISP_MOMENT_CAPACITY, TYPE_TEXTBOX,
               round(self.section.moment_capacity  / 1000000, 2) if flag else '')
        member_capacityoutput.append(t29)
        t29 = (KEY_MEMBER_SHEAR_CAPACITY, KEY_OUT_DISP_SHEAR_CAPACITY, TYPE_TEXTBOX,
               round(self.shear_capacity1 / 1000, 2) if flag else '')
        member_capacityoutput.append(t29)
        t29 = (KEY_MEMBER_AXIALCAPACITY, KEY_OUT_DISP_AXIAL_CAPACITY, TYPE_TEXTBOX,
               round(self.axial_capacity/ 1000, 2) if flag else '')
        member_capacityoutput.append(t29)
        return member_capacityoutput



    def output_values(self, flag):

        out_list = []

        t4 = (None, DISP_TITLE_MEMBER_CAPACITY, TYPE_TITLE, None, True)
        out_list.append(t4)
        t21 = (KEY_MEMBER_CAPACITY, KEY_DISP_MEMBER_CAPACITY, TYPE_OUT_BUTTON, ['Member Capacity', self.member_capacityoutput],True)
        out_list.append(t21)

        t1 = (None, DISP_TITLE_WEBSPLICEPLATE, TYPE_TITLE, None, True)

        out_list.append(t1)

        t5 = (KEY_WEB_PLATE_HEIGHT, KEY_DISP_WEB_PLATE_HEIGHT, TYPE_TEXTBOX,
              self.web_plate.height if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_WEB_PLATE_LENGTH, KEY_DISP_WEB_PLATE_LENGTH, TYPE_TEXTBOX,
              self.web_plate.length if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_WEBPLATE_THICKNESS, KEY_DISP_WEBPLATE_THICKNESS, TYPE_TEXTBOX,
              self.web_plate.thickness_provided if flag else '', True)
        out_list.append(t7)

        t21 = (KEY_WEB_CAPACITY, KEY_DISP_WEB_CAPACITY, TYPE_OUT_BUTTON, ['Web Capacity', self.webcapacity], True)
        out_list.append(t21)

        t21 = (KEY_WEB_WELD_DETAILS, KEY_DISP_WEB_WELD_DETAILS, TYPE_OUT_BUTTON, ['Web Plate Weld', self.web_weld_details], True)
        out_list.append(t21)
        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE, TYPE_TITLE, None, True)
        out_list.append(t17)
        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE_OUTER, TYPE_TITLE, None, True)

        out_list.append(t17)

        t18 = (KEY_FLANGE_PLATE_HEIGHT, KEY_DISP_FLANGE_PLATE_HEIGHT, TYPE_TEXTBOX,
               self.flange_plate.height if flag else '', True)
        out_list.append(t18)

        t19 = (
            KEY_FLANGE_PLATE_LENGTH, KEY_DISP_FLANGE_PLATE_LENGTH, TYPE_TEXTBOX,
            self.flange_plate.length if flag else '', True)

        out_list.append(t19)

        t20 = (KEY_FLANGEPLATE_THICKNESS, KEY_DISP_FLANGESPLATE_THICKNESS, TYPE_TEXTBOX,
               self.flange_plate.thickness_provided if flag else '', True)
        out_list.append(t20)

        t21 = (
            KEY_FLANGE_CAPACITY, KEY_DISP_FLANGE_CAPACITY, TYPE_OUT_BUTTON, ['Flange Capacity', self.flangecapacity], True)
        out_list.append(t21)


        t21 = (
        KEY_FLANGE_WELD_DETAILS, KEY_DISP_FLANGE_WELD_DETAILS, TYPE_OUT_BUTTON, ['Flange Plate Weld', self.flange_weld_details], True)
        out_list.append(t21)

        t17 = (None, DISP_TITLE_FLANGESPLICEPLATE_INNER, TYPE_TITLE, None, True)

        out_list.append(t17)

        t18 = (KEY_INNERFLANGE_PLATE_HEIGHT, KEY_DISP_INNERFLANGE_PLATE_HEIGHT, TYPE_TEXTBOX,
               self.flange_plate.Innerheight if flag else '', True)
        out_list.append(t18)

        t19 = (
            KEY_INNERFLANGE_PLATE_LENGTH, KEY_DISP_INNERFLANGE_PLATE_LENGTH, TYPE_TEXTBOX,
            self.flange_plate.Innerlength if flag else '', True)

        out_list.append(t19)

        t20 = (KEY_INNERFLANGEPLATE_THICKNESS, KEY_DISP_INNERFLANGESPLATE_THICKNESS, TYPE_TEXTBOX,
               self.flange_plate.thickness_provided if flag else '', True)
        out_list.append(t20)

        t21 = (KEY_INNERFLANGE_WELD_DETAILS, KEY_DISP_INNERFLANGE_WELD_DETAILS, TYPE_OUT_BUTTON,
               ['Inner plate Weld', self.Innerflange_weld_details], True)
        out_list.append(t21)

        # t17 = (None, DISP_EFF, TYPE_TITLE, None, True)
        # out_list.append(t17)
        #
        # t15 = (KEY_FLANGE_WELD_LENGTH, DISP_EFF, TYPE_TEXTBOX,
        #        (self.l_req_flangelength) if flag else '', True)
        # out_list.append(t15)

        return out_list

    def func_for_validation(self, design_dictionary):

        all_errors = []
        self.design_status = False
        flag = False

        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag:
            self.set_input_values(self, design_dictionary)
        else:
            return all_errors

    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from beams and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.section.designation in red_list or self.section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def generate_missing_fields_error_string(self, missing_fields_list):
        """
        Args:
            missing_fields_list: list of fields that are not selected or entered
        Returns:
            error string that has to be displayed
        """
        # The base string which should be displayed
        information = "Please input the following required field"
        if len(missing_fields_list) > 1:
            # Adds 's' to the above sentence if there are multiple missing input fields
            information += "s"
        information += ": "
        # Loops through the list of the missing fields and adds each field to the above sentence with a comma

        for item in missing_fields_list:
            information = information + item + ", "

        # Removes the last comma
        information = information[:-2]
        information += "."

        return information


    def module_name(self):

        return KEY_DISP_BEAMCOVERPLATEWELD

    def set_input_values(self, design_dictionary):
        super(BeamCoverPlateWeld, self).set_input_values(self, design_dictionary)
        self.module = design_dictionary[KEY_MODULE]
        self.preference = design_dictionary[KEY_FLANGEPLATE_PREFERENCES]


        self.section = Beam(designation=design_dictionary[KEY_SECSIZE],
                              material_grade=design_dictionary[KEY_SEC_MATERIAL])
        # print("anjali",design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])

        self.flange_weld = Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])
        self.web_weld =Weld(material_g_o=design_dictionary[KEY_DP_WELD_MATERIAL_G_O],fabrication = design_dictionary[KEY_DP_WELD_FAB])

        self.flange_plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
                                  material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                                  gap=design_dictionary[KEY_DP_DETAILING_GAP])
        # self.plate = Plate(thickness=design_dictionary.get(KEY_FLANGEPLATE_THICKNESS, None),
        #                           material_grade=design_dictionary[KEY_MATERIAL],
        #                           gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.web_plate = Plate(thickness=design_dictionary.get(KEY_WEBPLATE_THICKNESS, None),
                               material_grade=design_dictionary[KEY_CONNECTOR_MATERIAL],
                               gap=design_dictionary[KEY_DP_DETAILING_GAP])
        self.member_capacity_status = False
        self.initial_pt_thk_status= False
        self.web_plate_weld_status= False
        self.flange_plate_weld_status= False
        self.flange_plate_capacity_axial_status= False
        self.recheck_flange_capacity_axial_status= False
        self.web_plate_capacity_axial_status= False
        self.web_plate_capacity_shear_status= False
        self.cap_blockcheck_web_axial_status = False

        self.member_capacity(self)
        #self.hard_values(self)
    #

    def hard_values(self):
        # Select Selection  WPB 240* 240 * 60.3 (inside Ouside)- material E 250 fe 450A, bearing

        #load
        self.load.axial_force = 481.745 #KN
        self.load.shear_force = 111.906 #KN
        self.load.moment = 8.318420 #KNM
        self.section.fy = 230
        self.section.fu = 410
        #  Flange Weld
        self.flange_weld.size = 8 #mm
        # self.flangespace = 15 #mm
        self.flange_weld.length = 490
        self.flange_weld.height = 190
        #  Flange plate
        self.flange_plate.thickness_provided = 10
        self.flange_plate.height =  210
        self.flange_plate.length = 510
        #  Web Weld
        self.web_weld.size = 6  # mm
        # self.webspace = 15  # mm
        self.web_weld.length = 350
        self.web_weld.height = 155
        #  Web plate
        self.web_plate.thickness_provided =8
        self.web_plate.length = 365
        self.web_plate.height = 170
        #  Inner Flange weld
        self.flange_weld.size = 8  # mm
        self.flange_plate.thickness_provided = 10
        self.flange_weld.Innerheight=60
        self.flange_weld.Innerlength = 490
        #  Inner Flange plate
        self.flange_plate.thickness_provided = 10
        self.flange_plate.Innerheight = 80
        self.flange_plate.Innerlength = 510
        self.flange_plate.gap =10
        self.web_plate.gap = 10
        self.design_status = True

    def member_capacity(self):
        self.member_capacity_status = False
        if self.section.type == "Rolled":
            length = self.section.depth
        else:
            length = self.section.depth - (
                    2 * self.section.flange_thickness)  # -(2*self.supported_section.root_radius)
        gamma_m0 = 1.1
        ############################# Axial Capacity N ############################
        self.axial_capacity = round((self.section.area * self.section.fy) / gamma_m0 ,2)  # N
        self.min_axial_load = 0.3 * self.axial_capacity
        self.factored_axial_load = round(max(self.load.axial_force * 1000, self.min_axial_load),2 ) # N
        print("self.factored_axial_load", self.factored_axial_load)

        ############################# Shear Capacity  # N############################
        self.shear_capacity1 = round(((self.section.depth - (2 * self.section.flange_thickness)) *
                                self.section.web_thickness * self.section.fy) / (math.sqrt(3) * gamma_m0)  ,2) # N # A_v: Total cross sectional area in shear in mm^2 (float)
        self.shear_load1 = 0.6 * self.shear_capacity1  # N
        self.fact_shear_load = round(max(self.shear_load1, self.load.shear_force * 1000) ,2) # N
        print('shear_force', self.load.shear_force)

        # ###########################################################
        self.Z_p = round(((self.section.web_thickness * (
                self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 4),2 )  # mm3
        self.Z_e = round(((self.section.web_thickness * (
                self.section.depth - 2 * (self.section.flange_thickness)) ** 2) / 6), 2)  # mm3

        if self.section.type == "Rolled":
            self.limitwidththkratio_flange = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                           column_t_w=self.section.web_thickness,
                                                                           D=self.section.depth,
                                                                           column_b=self.section.flange_width,
                                                                           column_fy=self.section.fy,
                                                                           factored_axial_force=self.factored_axial_load,
                                                                           column_area=self.section.area,
                                                                           compression_element="External",
                                                                           section="Rolled")
        else:
            pass

        if self.section.type2 == "generally":
            self.limitwidththkratio_web = self.limiting_width_thk_ratio(column_f_t=self.section.flange_thickness,
                                                                        column_t_w=self.section.web_thickness,
                                                                        D=self.section.depth,
                                                                        column_b=self.section.flange_width,
                                                                        column_fy=self.section.fy,
                                                                        factored_axial_force=self.factored_axial_load,
                                                                        column_area=self.section.area,
                                                                        compression_element="Web of an I-H",
                                                                        section="generally")
        else:
            pass

        self.class_of_section = int(max(self.limitwidththkratio_flange, self.limitwidththkratio_web))
        if self.class_of_section == 1 or self.class_of_section == 2:
            Z_w = self.Z_p
        elif self.class_of_section == 3:
            Z_w = self.Z_e

        if self.class_of_section == 1 or self.class_of_section == 2:
            self.beta_b = 1
        elif self.class_of_section == 3:
            self.beta_b = self.Z_e / self.Z_p
        ############################ moment_capacty ############################
        self.section.plastic_moment_capacty(beta_b=self.beta_b, Z_p=self.Z_p,fy=self.section.fy)  # N # for section
        self.section.moment_d_deformation_criteria(fy=self.section.fy, Z_e=self.section.elast_sec_mod_z)
        self.Pmc = self.section.plastic_moment_capactiy
        self.Mdc = self.section.moment_d_def_criteria
        self.section.moment_capacity = round(min(self.section.plastic_moment_capactiy, self.section.moment_d_def_criteria) ,2)
        self.load_moment_min = 0.5 * self.section.moment_capacity
        self.load_moment = round(max(self.load_moment_min, self.load.moment * 1000000) ,2)  # N
        self.moment_web = round((Z_w * self.load_moment / (self.section.plast_sec_mod_z)),2)  # Nm todo add in ddcl # z_w of web & z_p  of section
        self.moment_flange = round(((self.load_moment) - self.moment_web),2)
        self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (self.section.area)  # N
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (self.section.area)  # N
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + (self.axial_force_f))

        ###########################################################
        if self.factored_axial_load > self.axial_capacity:
            logger.warning(' : Factored axial load is exceeding axial capacity  %2.2f KN' % self.axial_capacity)
            logger.error(" : Design is not safe. \n ")
            logger.debug(" :=========End Of design===========")
            self.member_capacity_status = False
        else:
            if self.fact_shear_load > self.shear_capacity1:
                logger.warning(' : Factored shear load is exceeding shear capacity  %2.2f KN' % self.shear_capacity1)
                logger.error(" : Design is not safe. \n ")
                logger.debug(" :=========End Of design===========")
                self.member_capacity_status = False
            else:
                if self.load_moment > self.section.moment_capacity:
                    self.member_capacity_status = False
                    logger.warning(' : Moment load is exceeding moment capacity  %2.2f KN-m' % self.section.moment_capacity)
                    logger.error(" : Design is not safe. \n ")
                    logger.debug(" :=========End Of design===========")
                else:
                    self.member_capacity_status = True
                    self.initial_pt_thk(self)

    def initial_pt_thk(self):
        ############################### WEB MENBER CAPACITY CHECK ############################
        ###### # capacity Check for web in axial = min(block, yielding, rupture)
        self.initial_pt_thk_status = False
        self.initial_pt_thk_status_web =False
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(A_v=A_v_web,fy=self.section.fy)

        if self.section.tension_yielding_capacity_web> self.axial_force_w:

        ################################# FLANGE MEMBER CAPACITY CHECK##############################
            A_v_flange = self.section.flange_thickness * self.section.flange_width
            self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(A_v=A_v_flange,fy=self.flange_plate.fy)
            if self.section.tension_yielding_capacity > self.flange_force:
                self.web_plate_thickness_possible = [i for i in self.web_plate.thickness if i >= (self.section.web_thickness / 2)]
                if self.preference == "Outside":
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if i >= self.section.flange_thickness]
                else:
                    self.flange_plate_thickness_possible = [i for i in self.flange_plate.thickness if i >= (self.section.flange_thickness / 2)]
                if len(self.flange_plate_thickness_possible) == 0:
                    logger.error(" : Flange Plate thickness should be greater than section thicknesss.")
                    self.initial_pt_thk_status =False
                else:
                    self.flange_plate.thickness_provided = self.min_thick_based_on_area(self,
                                                                                        tk=self.section.flange_thickness,
                                                                                        width=self.section.flange_width,
                                                                                        list_of_pt_tk=self.flange_plate_thickness_possible,
                                                                                        t_w=self.section.web_thickness,
                                                                                        r_1=self.section.root_radius,
                                                                                        D=self.section.depth,
                                                                                        preference=self.preference)
                    if self.preference =="Outside":
                        if self.outerwidth < 50:
                            logger.error(" : Outer Height of flange plate should be greater 50 mm.")
                            logger.info(" : Select the wider section.")
                            self.initial_pt_thk_status = False
                            self.design_status = False
                        else:
                            if self.flange_plate.thickness_provided != 0:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area  * 1.05):
                                    logger.error(" : Area of flange plate should be greater than 1.05 times area of flange.")
                                    logger.info(" : Increase the thickness of the plate.")
                                    self.initial_pt_thk_status = False
                                else:
                                    self.initial_pt_thk_status = True
                                    pass
                            else:
                                logger.error(" : Provided flange plate thickness is not sufficient.")
                                logger.error(" : Area of flange plate should be greater than 1.05 times area of flange.")
                                logger.info(" : Increase the thickness of the plate.")
                                self.initial_pt_thk_status = False
                                self.design_status = False

                    else:
                        if self.outerwidth < 50 or self.innerwidth < 50:
                            logger.error(" : Height of flange plate should be greater 50 mm.")
                            logger.info(" : Select the wider section.")
                            self.initial_pt_thk_status = False
                            self.design_status =False

                        else:
                            if self.flange_plate.thickness_provided != 0:
                                if self.flange_plate_crs_sec_area < (self.flange_crs_sec_area * 1.05):
                                    logger.error(" : Area of flange plates should be greater than 1.05 times area of flange.")
                                    logger.info(" : Increase the thickness of the flange plate.")
                                    self.initial_pt_thk_status = False
                                else:
                                    self.initial_pt_thk_status =True
                            else:
                                logger.error(" : Provided flange plate thickness is not sufficient.")
                                logger.error(" : Area of flange plate should be greater than 1.05 times area of flange.")
                                logger.info(" : Increase the thickness of the plate.")
                                self.initial_pt_thk_status = False
                                self.design_status = False

                self.initial_pt_thk_status_web = False
                if  len(self.web_plate_thickness_possible) == 0:
                    logger.error(" : Web Plate thickness should be greater than section  thicknesss.")
                    self.initial_pt_thk_status_web = False
                else:
                    self.web_plate.thickness_provided = self.min_thick_based_on_area(self,
                                                                                     tk=self.section.flange_thickness,
                                                                                     width=self.section.flange_width,
                                                                                     list_of_pt_tk=self.web_plate_thickness_possible,
                                                                                     t_w=self.section.web_thickness,
                                                                                     r_1=self.section.root_radius, D=self.section.depth, )

                    if self.web_plate.thickness_provided != 0:
                        if self.web_plate_crs_sec_area < (self.web_crs_area * 1.05):
                            logger.error(" : Area of web plate should be greater than 1.05 times area of web.")
                            logger.info(" : Increase the thickness of the web plate.")
                            self.initial_pt_thk_status_web = False
                        else:
                            self.initial_pt_thk_status_web = True
                    else:
                        logger.error(" : Provided web plate thickness is not sufficient.")
                        logger.error(" : Area of web plate should be greater than 1.05 times area of web.")
                        logger.info(" : Increase the thickness of the plate.")
                        self.initial_pt_thk_status_web = False
                        self.design_status = False


                if len(self.flange_plate_thickness_possible) == 0:
                    if len(self.flange_plate.thickness) >= 2:
                        self.max_thick_f = max(self.flange_plate.thickness)
                    else:
                        self.max_thick_f = self.flange_plate.thickness[0]
                else:
                    if self.flange_plate.thickness_provided ==0:
                        if len(self.flange_plate.thickness) >= 2:
                            self.max_thick_f = max(self.flange_plate.thickness)
                        else:
                            self.max_thick_f = self.flange_plate.thickness[0]
                    else:
                        self.max_thick_f = self.flange_plate.thickness_provided

                if len(self.web_plate_thickness_possible) == 0:
                    if len(self.web_plate.thickness) >= 2:
                        self.max_thick_w = max(self.web_plate.thickness)
                    else:
                        self.max_thick_w = self.web_plate.thickness[0]
                else:
                    if self.web_plate.thickness_provided == 0:
                        if len(self.web_plate.thickness) >= 2:
                            self.max_thick_w = max(self.web_plate.thickness)
                        else:
                            self.max_thick_w = self.web_plate.thickness[0]
                    else:
                        self.max_thick_w = self.web_plate.thickness_provided

                    if self.initial_pt_thk_status == True and self.initial_pt_thk_status_web == True:
                        self.design_status = True
                        self.web_plate_weld(self)
                    else:
                        self.initial_pt_thk_status = False and self.initial_pt_thk_status_web == False
                        self.design_status = False
                        logger.warning(" : Plate is not possible")
                        logger.error(" : Design is not safe. \n ")
                        logger.debug(" : =========End Of design===========")

            else:
                self.initial_pt_thk_status = False
                logger.warning(" : Tension_yielding_capacity  of flange is less than applied loads, Please select larger sections or decrease loads")
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")
        else:
            self.initial_pt_thk_status_web = False
            logger.warning(" : Tension_yielding_capacity of web  is less than applied loads, Please select larger sections or decrease loads")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design===========")

    def web_plate_weld(self):
        self.web_plate_weld_status = False
        self.min_web_platethk = min(self.web_plate.thickness_provided, self.section.web_thickness)
        self.web_weld.size = int(round_down(self.min_web_platethk - 1.5))
        if self.web_weld.size > self.min_web_platethk:
            self.web_weld.size = self.min_web_platethk
        else:
            pass
        if self.web_weld.size < 3:
            self.web_weld.size = 3
        else:
            pass
        if self.web_weld.size > 16:
            self.web_weld.size = 16
        else:
            pass
        self.webspace = max(15, (self.web_weld.size + 5))
        self.web_weld.get_weld_strength(connecting_fu=[self.web_weld.fu, self.section.fu, self.web_plate.fu],
                                        weld_fabrication=KEY_DP_WELD_FAB_SHOP,
                                        t_weld=self.web_weld.size, weld_angle=90)  # in N/mm
        self.web_plate.height = round_down((self.section.depth - (2 * self.section.flange_thickness)
                                            - (2 * self.section.root_radius) - (2 * self.webspace)), 5)
        self.available_long_web_length = self.web_plate.height

        self.web_plate_weld_status = False
        while self.web_plate_weld_status == False:
            self.weld_stress(self, d=self.available_long_web_length,
                             b=(self.web_plate.height - (2 * self.web_weld.size)),
                             shear_force=self.fact_shear_load, moment_web=self.moment_web,
                             plate_height=(self.web_plate.height - (2 * self.web_weld.size)),
                             weld_size=self.web_weld.size, axial_force_w=self.axial_force_w)

            if self.web_weld.strength > self.web_weld.stress:
                break
            else:
                self.available_long_web_length = self.available_long_web_length + 50
                self.web_plate.length = 2 * (self.available_long_web_length + (2*self.web_weld.size)) + self.web_plate.gap
                if self.web_plate.length >= 150 * self.web_weld.throat_tk:
                    Reduction_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.web_plate.length,
                                                                              t_t=self.web_weld.throat_tk)
                    self.web_weld.strength = self.web_weld.strength * Reduction_factor
                    self.weld_stress(self, d=self.available_long_web_length,
                                     b=(self.web_plate.height - (2 * self.web_weld.size)),
                                     shear_force=self.fact_shear_load, moment_web=self.moment_web,
                                     plate_height=(self.web_plate.height - (2 * self.web_weld.size)), weld_size=self.web_weld.size,
                                     axial_force_w=self.axial_force_w)
                    if self.web_weld.strength > self.web_weld.stress:
                        self.web_plate_weld_status = True
                        break
                    else:
                        self.available_long_web_length = self.available_long_web_length + 50

        if self.web_weld.strength > self.web_weld.stress:
            self.web_plate_weld_status = True
            self.web_weld.length = round_up(self.available_long_web_length, 5)
            self.web_plate.length = round_up(2 * (self.available_long_web_length + (2*self.web_weld.size)) + self.web_plate.gap ,5)
            self.web_plate.height = round_down((self.section.depth - (2 * self.section.flange_thickness) -
                                                (2 * self.section.root_radius) - (2 * self.webspace)), 5)
            self.web_weld.height = round_down((self.web_plate.height - (2 * self.web_weld.size)), 5)
            self.l_req_weblength = round_up(self.l_req_weblength ,5)
            self.flange_plate_weld(self)
            pass
        else:
            logger.error(" : Strength of web is less than stress, Please select larger sections or decrease loads")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design===========")

    def flange_plate_weld(self):
        self.flange_plate_weld_status = False
        self.min_flange_platethk = min(self.flange_plate.thickness_provided, self.section.flange_thickness)
        self.flange_weld.size = int(round_down(self.min_flange_platethk - 1.5))

        if self.flange_weld.size < 3:
            self.flange_weld.size = 3
        else:
            pass
        if self.flange_weld.size > 16:
            self.flange_weld.size = 16
        else:
            pass
        self.flangespace = max(15, (self.flange_weld.size + 5))
        print("space", self.flangespace)
        self.axial_force_f = self.factored_axial_load * self.section.flange_width * self.section.flange_thickness / (self.section.area)
        self.flange_force = (((self.moment_flange) / (self.section.depth - self.section.flange_thickness)) + (self.axial_force_f))

        self.flange_weld.get_weld_strength(connecting_fu=[self.flange_weld.fu, self.section.fu, self.flange_plate.fu],
                                           weld_fabrication=KEY_DP_WELD_FAB_SHOP,
                                           t_weld=self.flange_weld.size,
                                           weld_angle=90)

        ########### ONLY OUTSIDE ##################################################3
        if self.preference == "Outside":
            self.Required_weld_flange_length = round(self.flange_force / self.flange_weld.strength,2)
            self.Required_weld_flange_length_round = round_up(self.flange_force / self.flange_weld.strength,
                                                              5)  # c shape half of the splice  plate

            self.flange_plate.height = (self.section.flange_width - (2 * self.flangespace))  # width of the flange plate
            self.available_long_flange_length = round_up(int((self.Required_weld_flange_length_round - self.flange_plate.height - (
                        2 * self.flange_weld.size)) / 2),5,self.flange_plate.height)  # half of the one side of the flange plate

            self.l_req_flangelength = ((2 * self.available_long_flange_length) + self.flange_plate.height -
                                       (2 * self.flange_weld.size))
            self.flange_weld.stress = self.flange_force / self.l_req_flangelength
            self.flange_plate.length = 2 * (self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap

            while self.flange_plate.length >= 150 * self.flange_weld.throat_tk:
                Reduction_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.web_plate.length,
                                                                          t_t=self.web_weld.throat_tk)
                self.flange_weld.strength = self.flange_weld.strength * Reduction_factor
                self.flange_weld.stress = self.flange_force / self.l_req_flangelength
                if self.flange_weld.strength > self.flange_weld.stress:
                    break
                else:
                    self.available_long_flange_length = self.available_long_flange_length + 50
                    self.l_req_flangelength = ((2 * self.available_long_flange_length) + self.flange_plate.height - (
                            2 * self.flange_weld.size))
                    self.flange_plate.length = 2 * (
                                self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap

            if self.flange_weld.strength > self.flange_weld.stress:
                self.flange_plate_weld_status = True
                self.flange_weld.length = round_up(self.available_long_flange_length, 5)
                print("self.flange_weld.length" ,self.flange_weld.length)
                self.flange_plate.length = round_up(2 * (self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap, 5)
                self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
                self.flange_weld.height = (self.flange_plate.height - (2 * self.flange_weld.size))
                self.l_req_flangelength = round_up(((2 * self.available_long_flange_length) + self.flange_plate.height -
                                                    (2 * self.flange_weld.size)), 5)
                self.flange_weld.strength = round(self.flange_weld.strength,2)
                self.flange_weld.stress = round(self.flange_weld.stress,2)
                self.flange_plate_capacity_axial(self)
            else:
                self.flange_plate_weld_status = False
                logger.error(" : Strength of weld is less than height of the weld stress")  # todo
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")
        else:
            ################ OUTSIDE + INSIDE ###############################
            self.Required_weld_flange_length = round(self.flange_force / self.flange_weld.strength,2)
            self.total_height_of_inner_plate = (self.section.flange_width - (4 * self.flangespace) - self.section.web_thickness - (
                    2 * self.section.root_radius))  # total width of the inner flange plate
            if self.total_height_of_inner_plate > 0:
                self.flange_plate.Innerheight = (self.total_height_of_inner_plate / 2)
                if self.flange_plate.Innerheight < 50:
                    self.flange_plate_weld_status = False
                    logger.warning(" : Inner plate is not possible, select preference outside")
                else:
                    pass
            else:
                self.flange_plate_weld_status = False
            self.flange_plate.height = (self.section.flange_width - (2 * self.flangespace))
            self.Area_flange_plates = ((2 * self.flange_plate.Innerheight) + self.flange_plate.height) * self.flange_plate.thickness_provided
            self.Outside_plate_area = self.flange_plate.height* self.flange_plate.thickness_provided
            self.Area_ratio = self.Outside_plate_area /self.Area_flange_plates
            self.weld_eff_length_outer = round_up(self.Required_weld_flange_length *self.Area_ratio ,5)
            self.available_long_flange_length = round_up(int((self.weld_eff_length_outer - self.flange_plate.height - (
                        2 * self.flange_weld.size)) / 2),5,(self.flange_plate.height/2)) # half of the one side of the flange plate
            self.flange_plate.length = ((2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                                + self.flange_plate.gap))
            self.l_req_flangelength =((6 * self.available_long_flange_length) + self.flange_plate.height +
                                                2 * self.flange_plate.Innerheight - (6 * self.flange_weld.size))
            self.flange_weld.stress = self.flange_force / self.l_req_flangelength

            while self.flange_plate.length >= 150 * self.flange_weld.throat_tk:
                self.flange_weld.stress = self.flange_force / self.l_req_flangelength
                Reduction_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.web_plate.length,
                                                                          t_t=self.web_weld.throat_tk)
                self.flange_weld.strength = self.flange_weld.strength * Reduction_factor
                if self.flange_weld.strength > self.flange_weld.stress:
                    break
                else:
                    self.available_long_flange_length = self.available_long_flange_length + 50
                    self.l_req_flangelength = (6 * self.available_long_flange_length) + self.flange_plate.height \
                                              +(2 * self.flange_plate.Innerheight) - (6 * self.flange_weld.size)
                    self.flange_plate.length = ((2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                                 + self.flange_plate.gap), 5, self.flange_plate.height)

            if self.flange_weld.strength > self.flange_weld.stress:
                self.flange_plate_weld_status = True
                # Outer Plate Details
                self.flange_weld.length = round_up((self.available_long_flange_length), 5)
                self.flange_plate.length = round_up((2 * (self.available_long_flange_length + (2 * self.flange_weld.size))
                                                + self.flange_plate.gap),5,self.flange_plate.height)
                self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
                self.flange_weld.height = round_down((self.flange_plate.height - (2 * self.flange_weld.size)), 5)
                self.l_req_flangelength = round_up(((6 * self.available_long_flange_length) + self.flange_plate.height +
                                                2 * self.flange_plate.Innerheight - (6 * self.flange_weld.size)),5)
                # Inner Plate Details
                self.flange_weld.Innerlength =  self.flange_weld.length
                self.available_long_flange_length = self.available_long_flange_length
                self.flange_plate.Innerlength = self.flange_plate.length
                self.flange_plate.Innerheight = round_down( self.flange_plate.Innerheight , 5)
                self.flange_weld.Innerheight = (self.flange_plate.Innerheight - 2 * self.flange_weld.size)
                self.flange_weld.strength = round(self.flange_weld.strength, 2)
                self.flange_weld.stress = round(self.flange_weld.stress, 2)
                self.flange_plate_capacity_axial(self)
                pass
            else:
                self.flange_plate_weld_status = False
                logger.error(" : Strength of weld is less than height of the weld stress")
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")

    def flange_plate_capacity_axial(self):  # flange plate capacity check in axial
        self.flange_plate_capacity_axial_status = False
        if self.preference == "Outside":
            A_v_flange = self.flange_plate.thickness_provided * self.flange_plate.height

            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                A_v=A_v_flange, fy=self.flange_plate.fy)
            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                A_vn=A_v_flange, fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = min(self.flange_plate.tension_yielding_capacity,
                                                                  self.flange_plate.tension_rupture_capacity)
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                self.flange_plate_capacity_axial_status = False
                logger.error(" : Tension capacity flange plate is less than applied loads, Please select larger sections or decrease loads")
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")
            else:
                self.flange_plate_capacity_axial_status = True
                self.recheck_flange_capacity_axial(self)
        else:
            #  yielding,rupture  for  Oustide + Inside flange plate

            A_v_flange = ((2 * self.flange_plate.Innerheight) + self.flange_plate.height) * self.flange_plate.thickness_provided

            self.flange_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                                                                                                A_v=A_v_flange,
                                                                                                fy=self.flange_plate.fy)

            self.flange_plate.tension_rupture_capacity = self.tension_member_design_due_to_rupture_of_critical_section(
                                                                                                A_vn=A_v_flange,
                                                                                                fu=self.flange_plate.fu)
            self.flange_plate.tension_capacity_flange_plate = round(min(self.flange_plate.tension_yielding_capacity,
                                                                  self.flange_plate.tension_rupture_capacity),2)
            if self.flange_plate.tension_capacity_flange_plate < self.flange_force:
                self.flange_plate_capacity_axial_status = False
                logger.error(" : Tension capacity flange plate is less than applied loads, Please select larger sections or decrease loads")
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")
            else:
                self.flange_plate_capacity_axial_status = True
                self.recheck_flange_capacity_axial(self)

    def recheck_flange_capacity_axial(self):
        self.recheck_flange_capacity_axial_status = False
        A_v_flange = self.section.flange_thickness* self.section.flange_width

        self.section.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
                                                                            A_v=A_v_flange, fy=self.section.fy)
        self.section.tension_rupture_capacity  = self.tension_member_design_due_to_rupture_of_critical_section(
                                                                            A_vn=A_v_flange, fu=self.section.fu)
        self.section.tension_capacity_flange = round(min(self.section.tension_yielding_capacity ,
                                                   self.section.tension_rupture_capacity) ,2)

        if self.section.tension_capacity_flange < self.flange_force:
            self.recheck_flange_capacity_axial_status = False
            logger.error(" : Tension capacity flange is less than applied loads, Please select larger sections or decrease loads")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design===========")
        else:
            self.recheck_flange_capacity_axial_status = True
            self.web_plate_capacity_axial(self)


    def web_plate_capacity_axial(self):
        self.web_plate_capacity_axial_status = False
        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.tension_yielding_capacity = self.tension_member_design_due_to_yielding_of_gross_section(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.web_plate.tension_rupture_capacity= self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.web_plate.fu)
        self.web_plate.tension_capacity_web_plate = round(min(self.web_plate.tension_yielding_capacity,
                                                        self.web_plate.tension_rupture_capacity),2)
        if self.web_plate.tension_capacity_web_plate < self.axial_force_w:
            self.web_plate_capacity_axial_status = False
            logger.error(" : Tension capacity web plate in axial is less than applied loads, Please select larger sections or decrease loads")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design===========")

        else:
            self.web_plate_capacity_axial_status = True
            self.web_plate_capacity_shear(self)

    def web_plate_capacity_shear(self):
        self.web_plate_capacity_shear_status = False
        A_v_web = 2 * self.web_plate.height * self.web_plate.thickness_provided
        self.web_plate.shear_yielding_capacity = self.shear_yielding(
            A_v=A_v_web, fy=self.web_plate.fy)
        self.web_plate.shear_rupture_capacity = self.shear_rupture_(
            A_vn=A_v_web, fu=self.web_plate.fu)
        self.web_plate.shear_capacity_web_plate = round(min(self.web_plate.shear_yielding_capacity,
                                                      self.web_plate.shear_rupture_capacity),2)
        if self.web_plate.shear_capacity_web_plate < self.fact_shear_load:
            self.web_plate_capacity_shear_status = False
            logger.error(" : Shear capacity web plate is less than applied loads, Please select larger sections or decrease loads")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design===========")
        else:
            self.web_plate_capacity_shear_status = True
            self.cap_blockcheck_web_axial(self)

    def cap_blockcheck_web_axial(self):

        self.axial_force_w = ((self.section.depth - (2 * self.section.flange_thickness)) * self.section.web_thickness * self.factored_axial_load) / (
                                                                                                                                    self.section.area)
        A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
        self.section.tension_yielding_capacity_web = self.tension_member_design_due_to_yielding_of_gross_section(
                                                                                A_v=A_v_web, fy=self.section.fy)
        self.section.tension_rupture_capacity_web = self.tension_member_design_due_to_rupture_of_critical_section(
            A_vn=A_v_web, fu=self.section.fu)
        available_web_thickness = list( [x for x in self.web_plate.thickness if ((self.web_plate.thickness_provided) <= x)])

        for self.web_plate.thickness_provided in available_web_thickness:
            design_status_block_shear = False
            while design_status_block_shear == False:
                Avg = 2 * (self.available_long_web_length) * self.section.web_thickness
                Avn = 2 * (self.available_long_web_length) * self.section.web_thickness
                Atg = self.web_plate.height * self.section.web_thickness
                Atn = self.web_plate.height * self.section.web_thickness
                self.section.block_shear_capacity_web = self.block_shear_strength_section(A_vg=Avg, A_vn=Avn,
                                                                                      A_tg=Atg,
                                                                                      A_tn=Atn,
                                                                                      f_u=self.web_plate.fu,
                                                                                      f_y=self.web_plate.fy)
                if self.section.block_shear_capacity_web < self.axial_force_w:
                    self.available_long_web_length = self.available_long_web_length + 50
                else:
                    design_status_block_shear = True
                    break
            if design_status_block_shear == True:
                break
        if design_status_block_shear == True:
            self.section.tension_capacity_web = round(min(self.section.tension_yielding_capacity_web,
                                                    self.section.tension_rupture_capacity_web,
                                                    self.section.block_shear_capacity_web) ,2)
            if self.section.tension_capacity_web < self.axial_force_w:
                self.design_status = False
                logger.error(" : Tension capacity web is less than applied loads, Please select larger sections or decrease the loads")
                logger.error(" : Design is not safe. \n ")
                logger.debug(" : =========End Of design===========")
            else:
                self.design_status = True
                logger.info(" : Overall Beam cover plate welded member design is safe. \n")
                logger.debug(" : =========End Of design===========")
        else:
            logger.error(" : Block Shear is less than applied loads, Increase the thickness of plate")
            logger.error(" : Design is not safe. \n ")
            logger.debug(" : =========End Of design1===========")

        print(self.section)
        print(self.load)
        print("Outside Flange PLate")
        print(self.flange_weld)
        print(self.flange_plate)
        print("Web  PLate")
        print(self.web_weld)
        print(self.web_plate)
        print("flangegap", self.flange_plate.gap)
        print("webgap", self.web_plate.gap)
        print("A",self.load.axial_force)
        print("min_ac", self.min_axial_load / 1000)
        print("axial_capacity",self.axial_capacity / 1000)
        print("app_axial_load",self.factored_axial_load / 1000)
        # print(self.web_plate.thickness_provided)
        # print(self.flange_plate.thickness_provided)
        print("Inside PLate")


        ################################ Extra Functions  #####################################################################################

    @staticmethod
    def block_shear_strength_plate(A_vg, A_vn, A_tg, A_tn, f_u, f_y):  # for flange plate
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1
        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)
        Return:
            block shear strength of bolted connection in N (float)
        Note:
            Reference:
            IS 800:2007, cl. 6.4.1
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb, 3)
        return Tdb

        # Function for block shear capacity calculation

    @staticmethod
    def block_shear_strength_section(A_vg, A_vn, A_tg, A_tn, f_u, f_y):
        """Calculate the block shear strength of bolted connections as per cl. 6.4.1
        Args:
            A_vg: Minimum gross area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_vn: Minimum net area in shear along bolt line parallel to external force [in sq. mm] (float)
            A_tg: Minimum gross area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            A_tn: Minimum net area in tension from the bolt hole to the toe of the angle,
                           end bolt line, perpendicular to the line of force, respectively [in sq. mm] (float)
            f_u: Ultimate stress of the plate material in MPa (float)
            f_y: Yield stress of the plate material in MPa (float)
        Return:
            block shear strength of bolted connection in N (float)
        Note:
            Reference:
            IS 800:2007, cl. 6.4.1
        """
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        T_db1 = A_vg * f_y / (math.sqrt(3) * gamma_m0) + 0.9 * A_tn * f_u / gamma_m1
        T_db2 = 0.9 * A_vn * f_u / (math.sqrt(3) * gamma_m1) + A_tg * f_y / gamma_m0
        Tdb = min(T_db1, T_db2)
        Tdb = round(Tdb, 3)
        return Tdb
        # cl 6.2 Design Strength Due to Yielding of Gross Section

    @staticmethod
    def tension_member_design_due_to_yielding_of_gross_section(A_v, fy):
        '''
             Args:
                 A_v (float) Area under shear
                 Column_fy (float) Yield stress of Column material
             Returns:
                 Capacity of Column web in shear yielding
             '''
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        # A_v = height * thickness
        tdg = (A_v * fy) / (gamma_m0)
        return tdg

    @staticmethod
    def tension_member_design_due_to_rupture_of_critical_section(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Column_fu (float) Ultimate stress of Column material
               Returns:
                   Capacity of Column web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (gamma_m1)
        return T_dn

    @staticmethod
    def shear_yielding(A_v, fy):
        '''
        Args:
            length (float) length of member in direction of shear load
            thickness(float) thickness of member resisting shear
            Column_fy (float) Yield stress of section material
        Returns:
            Capacity of section in shear yeiding
        '''

        # A_v = length * thickness
        gamma_m0 = 1.1
        # print(length, thickness, fy, gamma_m0)
        # V_p = (0.6 * A_v * fy) / (math.sqrt(3) * gamma_m0 * 1000)  # kN
        V_p = (A_v * fy) / (math.sqrt(3) * gamma_m0)  # N
        return V_p

    @staticmethod
    def shear_rupture_(A_vn, fu):
        '''
               Args:
                   A_vn (float) Net area under shear
                   Column_fu (float) Ultimate stress of Column material
               Returns:
                   Capacity of Column web in shear rupture
               '''

        gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
        # A_vn = (height- bolts_one_line * dia_hole) * thickness
        T_dn = 0.9 * A_vn * fu / (math.sqrt(3) * gamma_m1)
        return T_dn


    @staticmethod
    def limiting_width_thk_ratio(column_f_t, column_t_w, D, column_b, column_fy, factored_axial_force,
                                 column_area, compression_element, section):
        column_d = D - (2 *column_f_t)
        epsilon = float(math.sqrt(250 / column_fy))
        axial_force_w = int(((D - 2 * (column_f_t)) * column_t_w * factored_axial_force) / (column_area))  # N

        des_comp_stress_web = column_fy
        des_comp_stress_section = column_fy
        avg_axial_comp_stress = axial_force_w / ((D - (2 * column_f_t)) * column_t_w)
        r1 = avg_axial_comp_stress / des_comp_stress_web
        r2 = avg_axial_comp_stress / des_comp_stress_section
        a = column_b / column_f_t
        # column_d = D - 2(column_f_t)
        # compression_element=["External","Internal","Web of an I-H" ,"box section" ]
        # section=["rolled","welded","compression due to bending","generally", "Axial compression" ]
        # section = "rolled"
        if compression_element == "External" or compression_element == "Internal":
            if section == "Rolled":
                if column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 10.5 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 15.7 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
                # print("class_of_section", class_of_section )
            elif section == "welded":
                if column_b * 0.5 / column_f_t <= 8.4 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 9.4 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 13.6 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            elif section == "compression due to bending":
                if column_b * 0.5 / column_f_t <= 29.3 * epsilon:
                    class_of_section1 = "plastic"
                elif column_b * 0.5 / column_f_t <= 33.5 * epsilon:
                    class_of_section1 = "compact"
                elif column_b * 0.5 / column_f_t <= 42 * epsilon:
                    class_of_section1 = "semi-compact"
                # else:
                #     print('fail')
            # else:
            #     pass

        elif compression_element == "Web of an I-H" or compression_element == "box section":
            if section == "generally":
                if r1 < 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= (max(105 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r2)), (42 * epsilon)):
                    #     class_of_section1 = "semi-compact"
                    # else:
                    #     print('fail')
                    # print("class_of_section3", class_of_section)
                elif r1 > 0:
                    if column_d / column_t_w <= max((84 * epsilon / (1 + r1)), (42 * epsilon)):
                        class_of_section1 = "plastic"
                    elif column_d / column_t_w <= max((105 * epsilon / (1 + (r1 * 1.5))), (
                            42 * epsilon)):
                        class_of_section1 = "compact"
                    else:
                        class_of_section1 = "semi-compact"
                    # elif column_d / column_t_w <= max((126 * epsilon / (1 + 2 * r2)), (
                    #         42 * epsilon)):
                    #     class_of_section1 = "semi-compact"

            elif section == "Axial compression":
                if column_d / column_t_w <= (42 * epsilon):
                    class_of_section1 = "semi-compact"
                else:
                    class_of_section1 = "N/A"

        print("class_of_section", class_of_section1)
        if class_of_section1 == "plastic":
            class_of_section1 = 1
        elif class_of_section1 == "compact":
            class_of_section1 = 2
        elif class_of_section1 == "semi-compact":
            class_of_section1 = 3
        # else:
        #     print('fail')
        print("class_of_section2", class_of_section1)

        return class_of_section1

        print("class_of_section1", class_of_section1)

    def min_thick_based_on_area(self, tk, width, list_of_pt_tk, t_w, r_1, D,
                                preference=None):  # area of flange plate should be greater than 1.05 times area of flange
        # 20 is the maximum spacing either side of the plate
        self.flange_crs_sec_area = tk * width
        self.design_status = True
        for y in list_of_pt_tk:

            if preference != None:
                if preference == "Outside":
                    self.outerwidth = width - (2 * 20)
                    if self.outerwidth < 50:
                        thickness = 0
                        self.design_status = False
                    else:
                        self.design_status = True
                    self.flange_plate_crs_sec_area = y * self.outerwidth
                    self.Ap =self.flange_crs_sec_area * 1.05
                    if self.flange_plate_crs_sec_area >= self.Ap:
                        thickness = y
                        self.design_status = True
                        break
                    else:
                        thickness = 0
                        self.design_status = False
                elif preference == "Outside + Inside":
                    self.outerwidth = width - (2 * 20)
                    self.innerwidth = (width - t_w - (2 * r_1) - (4 * 20)) / 2
                    self.Ap = self.flange_crs_sec_area * 1.05
                    if self.innerwidth < 50:
                        thickness = 0
                        self.design_status = False

                    else:
                        self.design_status = True
                        self.flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * y

                        if self.flange_plate_crs_sec_area >= self.Ap:
                            thickness = y
                            self.design_status = True
                            break
                        else:
                            thickness = 0
                            self.design_status = False


            else:
                self.webwidth = D - (2 * tk) - (2 * r_1) - (2 * 20)
                self.web_crs_area = t_w * (D - (2 * tk) - (2 * r_1))
                self.web_plate_crs_sec_area = (2 * self.webwidth) * y
                self.Wp =self.web_crs_area * 1.05
                if self.web_plate_crs_sec_area >= self.Wp:
                    thickness = y
                    self.design_status = True
                    break
                else:
                    thickness = 0
                    self.design_status = False

        return thickness

    def weld_stress(self, d, b, shear_force, moment_web, plate_height, weld_size, axial_force_w):
        '''
        # while calling take the shearforce in KN and moment KNM and axial foce in N
        # d = self.available_long_web_length
        # b = self.web_plate.height - (2 * self.web_weld.size)
        # self.design_status = False
        '''
        # while self.design_status == False:
        cgy = d ** 2 / (2 * d + b)
        cgx = b / 2
        self.y_max = (d ** 2 / (2 * d + b))
        self.x_max = b / 2
        # print("dfdbjfk", y_max, x_max)
        self.ecc = d - (d ** 2 / (2 * d + b))
        self.Ip_weld = ((8 * (d ** 3)) + (6 * d * (b ** 2)) + (b ** 3)) / 12 - ((d ** 4) / (2 * d + b))  # mm4
        self.weld_twist = (shear_force/2 * self.ecc) + (moment_web/2)  # Nmm
        # print("self.web_weld_length",self.web_weld_length )
        self.l_req_weblength =(2 * d) + plate_height
        self.web_weld.get_weld_stress(weld_shear=shear_force/2, weld_axial=axial_force_w/2,
                                      weld_twist=  self.weld_twist, Ip_weld=self.Ip_weld, y_max=self.y_max , x_max= self.x_max ,
                                      l_weld=self.l_req_weblength)

    # def call_3DModel(self,ui,bgcolor):
    #     # Call to calculate/create the BB Cover Plate Bolted CAD model
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.createBBCoverPlateBoltedCAD()
    #     #     self.ui.btn3D.setChecked(Qt.Checked)
    #     if ui.btn3D.isChecked():
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.chkBxFinplate.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #
    #     # Call to display the BB Cover Plate Bolted CAD model
    #     #     ui.Commondisplay_3DModel("Model", bgcolor)  # "gradient_bg")
    #     ui.commLogicObj.display_3DModel("Model",bgcolor)
    #
    #     # else:
    #     #     self.display.EraseAll()
    #
    # def call_3DBeam(self, ui, bgcolor):
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.ui.chkBx_beamSec1.setChecked(Qt.Checked)
    #     if ui.chkBxBeam.isChecked():
    #         ui.btn3D.setChecked(Qt.Unchecked)
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #     # self.display_3DModel("Beam", bgcolor)
    #     ui.commLogicObj.display_3DModel("Beam",bgcolor)
    #
    #
    # def call_3DConnector(self, ui, bgcolor):
    #     # status = self.resultObj['Bolt']['status']
    #     # if status is True:
    #     #     self.ui.chkBx_extndPlate.setChecked(Qt.Checked)
    #     if ui.chkBxFinplate.isChecked():
    #         ui.btn3D.setChecked(Qt.Unchecked)
    #         ui.chkBxBeam.setChecked(Qt.Unchecked)
    #         ui.mytabWidget.setCurrentIndex(0)
    #     # self.display_3DModel("Connector", bgcolor)
    #     ui.commLogicObj.display_3DModel("Connector", bgcolor)

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t2 = ('Beam', self.call_3DBeam)
        components.append(t2)

        t4 = ('Cover Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Cover Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)



    ################################ Design Report #####################################################################################


    def save_design(self, popup_summary):
        self.gamma_mw_flange = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.flange_weld.fabrication]
        self.gamma_mw_web = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.web_weld.fabrication]
        self.report_supporting = {KEY_DISP_SEC_PROFILE: "ISection",
                                  KEY_DISP_BEAMSEC: self.section.designation,
                                  KEY_DISP_FLANGESPLATE_PREFERENCES: self.preference,
                                  KEY_DISP_MATERIAL: self.section.material,
                                  KEY_DISP_FU: self.section.fu,
                                  KEY_DISP_FY: self.section.fy,
                                  'Mass': self.section.mass,
                                  'Area(mm2) - A': round(self.section.area, 2),
                                  'D(mm)': self.section.depth,
                                  'B(mm)': self.section.flange_width,
                                  't(mm)': self.section.web_thickness,
                                  'T(mm)': self.section.flange_thickness,
                                  'FlangeSlope': self.section.flange_slope,
                                  'R1(mm)': self.section.root_radius,
                                  'R2(mm)': self.section.toe_radius,
                                  'Iz(mm4)': round(self.section.mom_inertia_z, 2),
                                  'Iy(mm4)': round(self.section.mom_inertia_y, 2),
                                  'rz(mm)': round(self.section.rad_of_gy_z, 2),
                                  'ry(mm)': round(self.section.rad_of_gy_y, 2),
                                  'Zz(mm3)': round(self.section.elast_sec_mod_z, 2),
                                  'Zy(mm3)': round(self.section.elast_sec_mod_y, 2),
                                  'Zpz(mm3)': round(self.section.plast_sec_mod_z, 2),
                                  'Zpy(mm3)': round(self.section.elast_sec_mod_y, 2)}

        self.report_input = \
            {KEY_MODULE: self.module,

             KEY_MAIN_MODULE: self.mainmodule ,
             # KEY_CONN: self.connectivity,
             KEY_DISP_MOMENT: self.load.moment,
             KEY_DISP_SHEAR: self.load.shear_force ,
             KEY_DISP_AXIAL: self.load.axial_force,

             "Section": "TITLE",
             "Section Details": self.report_supporting,

             "Weld Details": "TITLE",
             KEY_DISP_DP_WELD_TYPE: "Fillet",
             KEY_DISP_DP_WELD_FAB: self.flange_weld.fabrication,
             KEY_DISP_DP_WELD_MATERIAL_G_O: self.flange_weld.fu,
             # KEY_WEBPLATE_THICKNESS:str(self.plate_thick_customized()),
             # KEY_FLANGEPLATE_THICKNESS:str(self.plate_thick_customized()),
             "Safety Factors - IS 800:2007 Table 5 (Clause 5.4.1) ": "TITLE",
             KEY_DISP_GAMMA_M0: gamma(1.1, "m0"),
             KEY_DISP_GAMMA_M1: gamma(1.25, "m1"),
             KEY_DISP_GAMMA_MW: gamma(self.gamma_mw_flange, "mw")}


        self.report_check = []

        flange_weld_conn_plates_fu = [self.section.fu, self.flange_plate.fu]
        self.flange_weld_connecting_plates = [self.section.flange_thickness, self.flange_plate.thickness_provided]
        self.flange_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(self.section.flange_thickness,self.flange_plate.thickness_provided)
        self.gamma_mw_flange = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.flange_weld.fabrication]
        if self.member_capacity_status ==True and self.initial_pt_thk_status== True:
            self.thick_f = self.flange_plate.thickness_provided
            self.thick_w =self.web_plate.thickness_provided
        else:
            self.thick_f = self.max_thick_f
            self.thick_w = self.max_thick_w

        self.Kt = IS800_2007.cl_10_5_3_2_fillet_weld_effective_throat_thickness_constant()
        h = round(self.section.depth - (2 * self.section.flange_thickness) ,2)
        self.Pmc = self.section.plastic_moment_capactiy
        self.Mdc = self.section.moment_d_def_criteria

        t1 = ('SubSection', 'Member Capacity', '|p{4cm}|p{5cm}|p{5.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
        t1 = (KEY_OUT_DISP_AXIAL_CAPACITY, '', axial_capacity(area=round(self.section.area,2),
                                                              fy=self.section.fy,
                                                              gamma_m0=gamma_m0,
                                                              axial_capacity=round(self.axial_capacity / 1000, 2)), '')
        self.report_check.append(t1)

        self.shear_capacity1 = round(((self.section.depth - (2 * self.section.flange_thickness)) *
                                      self.section.web_thickness * self.section.fy) / (math.sqrt(3) * gamma_m0), 2)

        t1 = (KEY_OUT_DISP_SHEAR_CAPACITY, '', shear_capacity(h=h, t=self.section.web_thickness,
                                                              f_y=self.section.fy, gamma_m0=gamma_m0,
                                                              shear_capacity=round(self.shear_capacity1 / 1000 ,2)), '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_PLASTIC_MOMENT_CAPACITY, '', plastic_moment_capacty(beta_b=round(self.beta_b,2),
                                                                               Z_p=self.Z_p, f_y=self.section.fy,
                                                                               gamma_m0=gamma_m0,
                                                                               Pmc=round(self.Pmc / 1000000, 2)), '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_D_DEFORMATION, '', moment_d_deformation_criteria(fy=self.section.fy,
                                                                                   Z_e=self.section.elast_sec_mod_z,
                                                                                   Mdc=round(self.Mdc / 1000000, 2)), '')
        self.report_check.append(t1)
        t1 = (KEY_OUT_DISP_MOMENT_CAPACITY, '', moment_capacity(Pmc=round(self.Pmc / 1000000, 2),
                                                                Mdc=round(self.Mdc / 1000000, 2),
                                                                M_c=round(self.section.moment_capacity / 1000000, 2)), '')
        self.report_check.append(t1)
        t1 = ('SubSection', 'Load Consideration', '|p{4cm}|p{3.5cm}|p{6.5cm}|p{1.5cm}|')
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_AXIAL_FORCE,
              min_max_axial_capacity(axial_capacity = round(self.axial_capacity / 1000, 2),
                                     min_ac=round(self.min_axial_load / 1000, 2)),
              display_prov( round(self.factored_axial_load / 1000, 2),"A_u"),
              # prov_axial_load(axial_input=self.load.axial_force,min_ac=round(self.min_axial_load / 1000, 2),
              #                 app_axial_load=round(self.factored_axial_load / 1000, 2)),
              get_pass_fail2(round(self.min_axial_load / 1000, 2),round(self.factored_axial_load / 1000, 2),round(self.axial_capacity / 1000, 2)))
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_SHEAR_LOAD,
              min_max_shear_capacity(shear_capacity = round(self.shear_capacity1 / 1000, 2),
                                     min_sc =round(self.shear_load1 / 1000, 2)),
              display_prov(round(self.fact_shear_load / 1000, 2), "V_u"),
              # prov_shear_load(shear_input=self.load.shear_force,min_sc=round(self.shear_load1 / 1000, 2),
              #                 app_shear_load=round(self.fact_shear_load / 1000, 2)),
              get_pass_fail2(round(self.shear_load1 / 1000,2),round(self.fact_shear_load / 1000,2), round(self.shear_capacity1 / 1000, 2)))
        self.report_check.append(t1)
        t1 = (KEY_DISP_APPLIED_MOMENT_LOAD,
              min_max_moment_capacity(moment_capacity = round(self.section.moment_capacity / 1000000, 2),
                                      min_mc =round(self.load_moment_min / 1000000, 2)),
              display_prov(round(self.load_moment / 1000000, 2), "M_u"),
              # prov_moment_load(moment_input=self.load.moment,min_mc=round(self.load_moment_min / 1000000, 2),
              #                  app_moment_load=round(self.load_moment / 1000000, 2)),
              get_pass_fail2(round(self.load_moment_min / 1000000, 2),round(self.load_moment / 1000000, 2), round(self.section.moment_capacity / 1000000, 2)))
        self.report_check.append(t1)
        t23 = (KEY_OUT_DISP_FORCES_WEB, '', forces_in_web(Au=round(self.factored_axial_load / 1000, 2),
                                                          T=self.section.flange_thickness, A=round(self.section.area,2),
                                                          t=self.section.web_thickness, D=self.section.depth,
                                                          Zw=self.Z_p, Mu=round(self.load_moment / 1000000, 2),
                                                          Z=self.section.plast_sec_mod_z,
                                                          Mw=round(self.moment_web / 1000000, 2),
                                                          Aw=round(self.axial_force_w / 1000, 2)), '')
        self.report_check.append(t23)
        t23 = (KEY_OUT_DISP_FORCES_FLANGE, '', forces_in_flange(Au=round(self.factored_axial_load / 1000, 2),
                                                                B=self.section.flange_width,
                                                                T=self.section.flange_thickness, A=round(self.section.area,2),
                                                                D=self.section.depth,
                                                                Mu=round(self.load_moment / 1000000, 2),
                                                                Mw=round(self.moment_web / 1000000, 2),
                                                                Mf=round(self.moment_flange / 1000000, 2),
                                                                Af=round(self.axial_force_f / 1000, 2),
                                                                ff=round(self.flange_force / 1000, 2), ), '')
        self.report_check.append(t23)
        if self.member_capacity_status == True:
            t2 =('SubSection', 'Initial Member Check', '|p{3cm}|p{4.5cm}|p{6.5cm}|p{1.5cm}|' )
            self.report_check.append(t2)
            t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, display_prov( round(self.flange_force / 1000, 2),"F_f"), tension_yield_prov(self.section.flange_width,
                                                                             self.section.flange_thickness,
                                                                             self.section.fy, gamma_m0,
                                                                             round(self.section.tension_yielding_capacity / 1000,2), 1),
                  get_pass_fail(round(self.flange_force / 1000, 2), round(self.section.tension_yielding_capacity / 1000,2), relation="leq"))
            self.report_check.append(t1)
            if self.section.tension_yielding_capacity > self.flange_force :
                webheight = round((self.section.depth - 2 * self.section.flange_thickness) ,2)
                t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, display_prov( round(self.axial_force_w / 1000, 2),"A_w"), tension_yield_prov(webheight,
                                                                              self.section.web_thickness,
                                                                              self.section.fy, gamma_m0,
                                                                              round(self.section.tension_yielding_capacity_web / 1000,), 1),
                      get_pass_fail(round(self.axial_force_w / 1000, 2),round(self.section.tension_yielding_capacity_web / 1000,), relation="leq"))
                self.report_check.append(t1)
        if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force) and (len(self.flange_plate_thickness_possible) != 0):
            t1 = ('SubSection', 'Initial flange plate height check', '|p{4.5cm}|p{2.5cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            if self.preference == "Outside":
                t1 = (KEY_FLANGE_PLATE_HEIGHT , 'Outer.b >= 50',
                      width_pt_chk( B=self.section.flange_width,
                                        t=self.section.web_thickness, r_1=self.section.root_radius,pref= "Outside"),
                      get_pass_fail(50, round(self.outerwidth,2), relation="leq"))
                self.report_check.append(t1)
            else:
                t1 = (KEY_FLANGE_PLATE_HEIGHT , 'Outer.b >= 50',
                      width_pt_chk(B=self.section.flange_width,
                                   t=self.section.web_thickness, r_1=self.section.root_radius, pref="Outside"),
                      get_pass_fail(50, round(self.outerwidth,2), relation="leq"))
                self.report_check.append(t1)

                t1 = (KEY_INNERFLANGE_PLATE_HEIGHT, 'Inner.b >= 50' ,
                      width_pt_chk(B=self.section.flange_width,
                      t=self.section.web_thickness, r_1=self.section.root_radius, pref= "Outside +Inside"),
                     get_pass_fail(50, round(self.innerwidth,2), relation="leq"))
                self.report_check.append(t1)


        if self.member_capacity_status == True and (self.section.tension_yielding_capacity > self.flange_force):
            t1 = ('SubSection', 'Flange plate thickness', '|p{2.5cm}|p{4.5cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            if  self.preference == "Outside":
                t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness, "T"),display_prov(self.thick_f, "t_f"),
                      get_pass_fail(self.section.flange_thickness, self.thick_f, relation="lesser"))
                self.report_check.append(t2)
                if(len(self.flange_plate_thickness_possible) != 0) and self.outerwidth >= 50:
                    t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area,2),flange_web_area = round(self.Ap,2)),
                          flange_plate_area_prov(B=self.section.flange_width,pref = "Outside",y = self.thick_f,outerwidth= round(self.outerwidth,2),fp_area =round(self.flange_plate_crs_sec_area,2),t = self.section.web_thickness,r_1 = self.section.root_radius,),get_pass_fail(self.Ap , self.flange_plate_crs_sec_area, relation="leq"))
                    self.report_check.append(t2)
            else:
                t2 = (KEY_DISP_FLANGESPLATE_THICKNESS, display_prov(self.section.flange_thickness/2, "T"),display_prov(self.thick_f, "t_f"),get_pass_fail(self.section.flange_thickness/2, self.thick_f, relation="lesser"))
                self.report_check.append(t2)
                # flange_plate_crs_sec_area = (self.outerwidth + (2 * self.innerwidth)) * self.thick_f
                if len(self.flange_plate_thickness_possible) != 0 and self.innerwidth >= 50 :
                    t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.flange_crs_sec_area, 2),flange_web_area =round( self.Ap,2)),
                          flange_plate_area_prov(B=self.section.flange_width, pref="Outside+Inside",
                                                 y=self.thick_f,
                                                 outerwidth=round(self.outerwidth,2), fp_area=round(self.flange_plate_crs_sec_area,2),
                                                 t=self.section.web_thickness, r_1=self.section.root_radius,
                                                 innerwidth=round(self.innerwidth,2) ),get_pass_fail(self.Ap, self.flange_plate_crs_sec_area, relation="leq"))
                    self.report_check.append(t2)
            # if (self.flange_plate_crs_sec_area >= (1.05 * self.flange_crs_sec_area)) and len(self.flange_plate_thickness_possible) != 0 and len(self.web_plate_thickness_possible) != 0 :
            t1 = ('SubSection', 'Web plate thickness', '|p{2.5cm}|p{4.5cm}|p{7cm}|p{1.5cm}|')
            self.report_check.append(t1)
            t2 = (KEY_DISP_WEBPLATE_THICKNESS, display_prov(self.section.web_thickness/2, "t"),display_prov(self.thick_w, "t_w"),get_pass_fail(self.section.web_thickness/2, self.thick_w, relation="lesser"))
            self.report_check.append(t2)
            if len(self.web_plate_thickness_possible) != 0:
                # if (self.flange_plate_crs_sec_area >= 1.05 * self.flange_crs_sec_area):
                t2 = (KEY_DISP_AREA_CHECK, plate_area_req(crs_area=round(self.web_crs_area, 2),flange_web_area = round( self.Wp,)),web_plate_area_prov(D=self.section.depth, y = self.thick_w,webwidth = round(self.webwidth,2), wp_area =round(self.web_plate_crs_sec_area,2),T = self.section.flange_thickness, r_1 = self.section.root_radius),
                                            get_pass_fail(self.Wp, self.web_plate_crs_sec_area, relation="leq"))
                self.report_check.append(t2)

##################################weld design check remains same for outside and " outside +inside" ########################################
            if self.initial_pt_thk_status == True and self.web_plate_weld_status == True:
                t1 = ('SubSection', 'Flange Weld Design Check ', '|p{4cm}|p{5cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                # Flange Weld size#
                t2 = (DISP_MIN_WELD_SIZE, min_weld_size_req(conn_plates_weld=self.flange_weld_connecting_plates,min_weld_size=self.flange_weld_size_min),display_prov(self.flange_weld.size, "t_w"),get_pass_fail(self.flange_weld_size_min, self.flange_weld.size, relation="lesser"))
                self.report_check.append(t2)
                t2 = (DISP_MAX_WELD_SIZE, max_weld_size_req(conn_plates_weld=self.flange_weld_connecting_plates,max_weld_size=self.min_flange_platethk),display_prov(self.flange_weld.size, "t_w"),get_pass_fail(self.min_flange_platethk, self.flange_weld.size, relation="geq"))
                self.report_check.append(t2)
                t2 = (KEY_DISP_CLEARANCE, spacing (sp = self.flangespace,t_w = self.flange_weld.size),display_prov(self.flangespace, "sp"),get_pass_fail(self.min_flange_platethk, self.flange_weld.size, relation="geq"))
                self.report_check.append(t2)
                # Throat thickness #
                t1 = (DISP_THROAT, throat_req(), throat_prov(self.flange_weld.size, self.Kt),get_pass_fail(3.0, self.flange_weld.size, relation="leq"))
                self.report_check.append(t1)
                #####Strength of the weld ####
                if self.preference == "Outside":
                    t1 = (DISP_EFF,' ',eff_len_prov(l_w=self.flange_weld.length,b_fp= self.flange_plate.height,t_w=self.flange_weld.size, l_eff =self.l_req_flangelength), "")
                    self.report_check.append(t1)
                    t2 = (KEY_FLANGE_DISP_WELD_STRENGTH,flange_weld_stress(F_f=round(self.flange_force/1000,2), l_eff=self.l_req_flangelength,F_ws=round(self.flange_weld.stress,2)),weld_strength_prov(conn_plates_weld_fu =  flange_weld_conn_plates_fu,gamma_mw =self.gamma_mw_flange ,t_t =self.flange_weld.throat_tk,f_w =self.flange_weld.strength),get_pass_fail(self.flange_weld.stress, self.flange_weld.strength, relation="lesser"))
                    self.report_check.append(t2)
                    # Outside +Inside#
                else:
                    #Outside
                    t1 = (KEY_DISP_WELD_LEN_EFF_OUTSIDE ,'', eff_len_prov_out_in(l_w=self.flange_weld.length,b_fp=self.flange_plate.height,b_ifp=self.flange_plate.Innerheight,t_w=self.flange_weld.size, l_eff=self.l_req_flangelength), "")
                    self.report_check.append(t1)
                    t2 = (KEY_FLANGE_DISP_WELD_STRENGTH,flange_weld_stress(F_f=round(self.flange_force / 1000, 2), l_eff=self.l_req_flangelength,F_ws=round(self.flange_weld.stress, 2)),weld_strength_prov(conn_plates_weld_fu=flange_weld_conn_plates_fu, gamma_mw=self.gamma_mw_flange,t_t=self.flange_weld.throat_tk,f_w=self.flange_weld.strength),get_pass_fail(self.flange_weld.stress, self.flange_weld.strength, relation="lesser"))
                    self.report_check.append(t2)

                if  self.preference == "Outside":
                    self.min_height_required = 50
                    self.min_length_required = self.flange_plate.height
                    t1 = ('SubSection', 'Flange Plate Check', '|p{3.5cm}|p{6cm}|p{6cm}|p{1.5cm}|')
                    self.report_check.append(t1)
                    t1 = (DISP_MIN_PLATE_HEIGHT,self.min_height_required, height_of_flange_cover_plate(B=self.section.flange_width,sp=self.flangespace,b_fp=self.flange_plate.height),get_pass_fail(self.min_height_required, self.flange_plate.height, relation="lesser"))
                    self.report_check.append(t1)
                    t1 = (DISP_MAX_PLATE_HEIGHT,height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,b_fp=self.flange_plate.height),self.flange_plate.height,get_pass_fail(self.flange_plate.height, self.flange_plate.height, relation="lesser"))
                    self.report_check.append(t1)
                    t1 = (DISP_MIN_PLATE_LENGTH, self.min_length_required,plate_Length_req(l_w=self.flange_weld.length, t_w=self.flange_weld.size,g=self.flange_plate.gap, l_fp=self.flange_plate.length),get_pass_fail(self.min_length_required, self.flange_plate.length, relation="lesser"))
                    self.report_check.append(t1)
                else:
                    t1 = ('SubSection', 'Flange Plate Check-Outside/Inside', '|p{3.5cm}|p{6cm}|p{6cm}|p{1.5cm}|')
                    self.report_check.append(t1)
                    self.min_height_required = 50
                    self.min_length_required = self.flange_plate.height
                    ###Outside####
                    t1 = (DISP_MIN_PLATE_HEIGHT, self.min_height_required,height_of_flange_cover_plate(B=self.section.flange_width, sp=self.flangespace,b_fp=self.flange_plate.height),get_pass_fail(self.min_height_required, self.flange_plate.height, relation="lesser"))
                    self.report_check.append(t1)
                    t1 = (DISP_MIN_PLATE_LENGTH, self.min_length_required,plate_Length_req(l_w=self.flange_weld.length, t_w=self.flange_weld.size,g=self.flange_plate.gap, l_fp=self.flange_plate.length),get_pass_fail(self.min_length_required, self.flange_plate.length, relation="lesser"))
                    self.report_check.append(t1)
                    ####Inside###
                    t1 = (DISP_MIN_PLATE_INNERHEIGHT, self.min_height_required,inner_plate_height_weld(B=self.section.flange_width, sp=self.flangespace,t=self.section.web_thickness, r_1=self.section.root_radius,b_ifp=self.flange_plate.Innerheight),get_pass_fail(self.min_height_required, self.flange_plate.Innerheight, relation="lesser"))
                    self.report_check.append(t1)
                    t1 = (DISP_MAX_PLATE_INNERHEIGHT,inner_plate_height_weld(B = self.section.flange_width, sp =self.flangespace,t= self.section.web_thickness, r_1 = self.section.root_radius ,b_ifp =self.flange_plate.Innerheight),self.flange_plate.Innerheight,get_pass_fail(self.flange_plate.Innerheight, self.flange_plate.Innerheight, relation="lesser"))
                    self.report_check.append(t1)
                    t1 = (DISP_MIN_PLATE_INNERLENGTH, self.min_length_required,plate_Length_req(l_w=self.flange_weld.Innerlength, t_w=self.flange_weld.size,g=self.flange_plate.gap, l_fp=self.flange_plate.Innerlength),get_pass_fail(self.min_length_required, self.flange_plate.Innerlength, relation="lesser"))
                    self.report_check.append(t1)


#######################################################Web design###########################################################
                self.web_weld_connecting_plates = [self.section.web_thickness, self.web_plate.thickness_provided]
                self.web_weld_size_min = IS800_2007.cl_10_5_2_3_min_weld_size(self.section.web_thickness,self.web_plate.thickness_provided)
                self.web_weld_conn_plates_fu = [self.section.fu, self.web_plate.fu]
                self.gamma_mw_web = IS800_2007.cl_5_4_1_Table_5['gamma_mw'][self.web_weld.fabrication]
            if self.initial_pt_thk_status == True:
                t1 = ('SubSection', 'Web Weld  Design Check ', '|p{3.5cm}|p{6cm}|p{6cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t2 = (DISP_MIN_WELD_SIZE, min_weld_size_req(conn_plates_weld=self.web_weld_connecting_plates,min_weld_size=self.web_weld_size_min),display_prov(self.web_weld.size, "t_w"),get_pass_fail(self.web_weld_size_min, self.web_weld.size, relation="lesser"))
                self.report_check.append(t2)
                t2 = (DISP_MAX_WELD_SIZE, max_weld_size_req(conn_plates_weld=self.web_weld_connecting_plates,max_weld_size=self.min_web_platethk),display_prov(self.web_weld.size, "t_w"),get_pass_fail(self.min_web_platethk, self.web_weld.size, relation="geq"))
                self.report_check.append(t2)
                t1 = (DISP_EFF, "", eff_len_prov(l_w=self.web_weld.length, b_fp=self.web_plate.height,t_w=self.web_weld.size, l_eff=self.l_req_weblength), "")
                self.report_check.append(t1)
                t2 = (KEY_DISP_CLEARANCE, spacing(sp=self.webspace, t_w=self.web_weld.size),display_prov(self.webspace, "sp"),get_pass_fail(self.min_web_platethk, self.web_weld.size, relation="geq"))
                self.report_check.append(t2)
                t1 = (DISP_THROAT, throat_req(), throat_prov(self.web_weld.size, self.Kt),get_pass_fail(3.0, self.web_weld.size, relation="leq"))
                self.report_check.append(t1)
                t10 = (KEY_OUT_REQ_MOMENT_DEMAND_BOLT, '',moment_demand_req_bolt_force(shear_load=round((self.fact_shear_load / 1000)/2, 2),web_moment=round((self.moment_web / 1000000)/2, 2), ecc=round(self.ecc,2),moment_demand=round(self.weld_twist / 1000000, 2)), '')
                self.report_check.append(t10)
                t2 = (KEY_WEB_DISP_WELD_STRENGTH,weld_strength_stress(V_u=round((self.fact_shear_load/2),2),A_w=round((self.axial_force_w/2),2),
                                                                        M_d=round(self.weld_twist, 2),
                                                                        Ip_w= round(self.Ip_weld,2),
                                                                        y_max=round(self.y_max,2),
                                                                        x_max=round(self.x_max,2),
                                                                        l_eff=self.l_req_weblength,
                                                                        R_w=round(self.web_weld.stress,2)),
                    weld_strength_prov(conn_plates_weld_fu =  self.web_weld_conn_plates_fu,gamma_mw =self.gamma_mw_web ,t_t =self.web_weld.throat_tk,f_w =self.web_weld.strength),get_pass_fail(self.web_weld.stress, self.web_weld.strength, relation="lesser"))
                self.report_check.append(t2)

                t1 = ('SubSection', 'Web Plate Check', '|p{4cm}|p{4cm}|p{6.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t1 = (DISP_MIN_PLATE_HEIGHT, self.min_height_required,height_of_web_cover_plate(D=self.section.depth, sp=self.webspace,b_wp=self.web_plate.height,T=self.section.flange_thickness, R_1 = self.section.root_radius),get_pass_fail(self.min_height_required, self.web_plate.height, relation="lesser"))
                self.report_check.append(t1)
                t1 = (DISP_MIN_PLATE_LENGTH, self.min_length_required,plate_Length_req(l_w=self.web_weld.length, t_w=self.web_weld.size,g=self.web_plate.gap, l_fp=self.web_plate.length),get_pass_fail(self.min_length_required, self.web_plate.length, relation="lesser"))
                self.report_check.append(t1)

####################################### Member Capacities##############################################################
            ###################
            ### Flange Check ###
            if self.flange_plate_weld_status == True and self.flange_plate_capacity_axial_status == True:
                t1 = ('SubSection', 'Member Checks', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                t1 = (KEY_DISP_TENSIONYIELDINGCAP_FLANGE, '', tension_yield_prov(self.section.flange_width,
                                                                             self.section.flange_thickness,
                                                                             self.section.fy, gamma_m0,
                                                                             round(self.section.tension_yielding_capacity / 1000, 2),1), '')
                self.report_check.append(t1)
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                t1 = (KEY_DISP_TENSIONRUPTURECAP_FLANGE, '', tension_rupture_welded_prov(w_p=self.section.flange_width,
                                                                                     t_p=self.section.flange_thickness,
                                                                                     fu=self.section.fu, gamma_m1=gamma_m1,T_dn=round((self.section.tension_rupture_capacity / 1000),2),multiple =1), '')

                self.report_check.append(t1)
                t1 = (KEY_DISP_FLANGE_TEN_CAPACITY, display_prov(round(self.flange_force / 1000, 2), "f_f") ,tensile_capacity_prov(round(self.section.tension_yielding_capacity / 1000, 2),round(self.section.tension_rupture_capacity / 1000, 2)),get_pass_fail(round(self.flange_force / 1000, 2), round(self.section.tension_capacity_flange / 1000, 2),relation="lesser"))
                self.report_check.append(t1)

            ### web Check ###
            if self.web_plate_capacity_axial_status == True and self.web_plate_capacity_shear_status == True:
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                # A_v_web = (self.section.depth - 2 * self.section.flange_thickness) * self.section.web_thickness
                webheight = round((self.section.depth - 2 * self.section.flange_thickness) ,2)
                t1 = (KEY_DISP_TENSIONYIELDINGCAP_WEB, '', tension_yield_prov(webheight,
                                                                          self.section.web_thickness,
                                                                          self.section.fy, gamma_m0,
                                                                          round(self.section.tension_yielding_capacity_web / 1000,2),1), '')
                self.report_check.append(t1)
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
                t1 = (KEY_DISP_TENSIONRUPTURECAP_WEB, '', tension_rupture_welded_prov(w_p=webheight,
                                                                                  t_p=self.section.web_thickness,
                                                                                  fu=self.section.fu, gamma_m1=gamma_m1,
                                                                                  T_dn=round(self.section.tension_rupture_capacity_web / 1000,2),multiple =1), '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_BLOCKSHEARCAP_WEB, '',blockshear_prov(Tdb = round(self.section.block_shear_capacity_web / 1000, 2)), '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_WEB_TEN_CAPACITY,display_prov( round(self.axial_force_w / 1000, 2),"A_w"), tensile_capacity_prov(round(self.section.tension_yielding_capacity_web / 1000, 2),
                                        round(self.section.tension_rupture_capacity_web / 1000, 2),
                                        round(self.section.block_shear_capacity_web / 1000, 2)),get_pass_fail(round(self.axial_force_w / 1000, 2), round(self.section.tension_capacity_web / 1000, 2),relation="lesser"))
                self.report_check.append(t1)

####################### Flange plate Capacities check########################
            ###################
            # if self.flange_plate_capacity_axial == True:
            if self.flange_plate_weld_status == True:
                if self.preference == "Outside":
                   t1 = ('SubSection', 'Flange Plate Capacity Checks in axial-Outside ', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
                   self.report_check.append(t1)
                   gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']

                   t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '', tension_yield_prov(self.flange_plate.height,
                                                                                 self.flange_plate.thickness_provided,
                                                                                 self.flange_plate.fy, gamma_m0,
                                                                                 round(self.flange_plate.tension_yielding_capacity / 1000,
                                                                                     2),1), '')
                   self.report_check.append(t1)
                   gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                   t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_welded_prov(w_p=self.flange_plate.height,
                                                                                            t_p=self.flange_plate.thickness_provided,
                                                                                            fu=self.flange_plate.fu,
                                                                                            gamma_m1=gamma_m1,
                                                                                            T_dn=round(self.flange_plate.tension_rupture_capacity / 1000,
                                                                                                2),multiple =1), '')
                   self.report_check.append(t1)
                   t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "f_f") ,
                      tensile_capacity_prov(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                            round(self.flange_plate.tension_rupture_capacity / 1000, 2)),
                      get_pass_fail(round(self.flange_force / 1000, 2),
                                    round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                    relation="lesser"))
                   self.report_check.append(t1)
                else:
                   t1 = ('SubSection', 'Flange Plate Capacity Checks in axial-Outside/Inside ', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
                   self.report_check.append(t1)
                   gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                   total_height = self.flange_plate.height + (2 * self.flange_plate.Innerheight)

                   t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '', tension_yield_prov(total_height,
                                                                             self.flange_plate.thickness_provided,
                                                                             self.flange_plate.fy, gamma_m0,
                                                                             round(self.flange_plate.tension_yielding_capacity / 1000,
                                                                                 2),1), '')
                   self.report_check.append(t1)

                   gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']

                   t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_welded_prov(w_p=total_height,
                                                                                        t_p=self.flange_plate.thickness_provided,
                                                                                        fu=self.flange_plate.fu,
                                                                                        gamma_m1=gamma_m1,
                                                                                        T_dn=round(
                                                                                            self.flange_plate.tension_rupture_capacity / 1000,
                                                                                            2),multiple =1), '')
                   self.report_check.append(t1)

                   t1 = (KEY_DISP_FLANGE_PLATE_TEN_CAP, display_prov(round(self.flange_force / 1000, 2), "f_f") ,
                      tensile_capacity_prov(round(self.flange_plate.tension_yielding_capacity / 1000, 2),
                                            round(self.flange_plate.tension_rupture_capacity / 1000, 2)),
                                            get_pass_fail(round(self.flange_force / 1000, 2),
                                       round(self.flange_plate.tension_capacity_flange_plate / 1000, 2),
                                       relation="lesser"))
                   self.report_check.append(t1)

               # Web plate Capacities check axial
               ###################
            if self.recheck_flange_capacity_axial_status == True:
                t1 = ('SubSection', 'Web Plate Capacity Checks in Axial', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                gamma_m0 = IS800_2007.cl_5_4_1_Table_5["gamma_m0"]['yielding']
                t1 = (KEY_DISP_TENSION_YIELDCAPACITY, '', tension_yield_prov(self.web_plate.height,
                                                                            self.web_plate.thickness_provided,
                                                                            self.web_plate.fy,
                                                                            gamma_m0,
                                                                            round(self.web_plate.tension_yielding_capacity / 1000,2) , 2), '')
                self.report_check.append(t1)
                gamma_m1 = IS800_2007.cl_5_4_1_Table_5["gamma_m1"]['ultimate_stress']
                t1 = (KEY_DISP_TENSION_RUPTURECAPACITY, '', tension_rupture_welded_prov(self.web_plate.height,
                                                                                       self.web_plate.thickness_provided,
                                                                                       self.web_plate.fu,
                                                                                       gamma_m1,
                                                                                       round(self.web_plate.tension_rupture_capacity / 1000, 2),2), '')
                self.report_check.append(t1)
                t1 = (KEY_DISP_TEN_CAP_WEB_PLATE, display_prov( round(self.axial_force_w / 1000, 2),"A_w"),tensile_capacity_prov(round(self.web_plate.tension_yielding_capacity / 1000, 2),round(self.web_plate.tension_rupture_capacity / 1000, 2)),get_pass_fail(round(self.axial_force_w / 1000, 2), round(self.web_plate.tension_capacity_web_plate / 1000, 2),relation="lesser"))
                self.report_check.append(t1)

               # Web plate Capacities check Shear
               ###################
            if self.web_plate_capacity_axial_status == True:
                t1 = ('SubSection', 'Web Plate Capacity Checks in Shear', '|p{4cm}|p{6cm}|p{5.5cm}|p{1.5cm}|')
                self.report_check.append(t1)
                t1 = (KEY_DISP_SHEAR_YLD, '', shear_yield_prov(self.web_plate.height, self.web_plate.thickness_provided,
                                                              self.web_plate.fy, gamma_m0,
                                                              round(self.web_plate.shear_yielding_capacity / 1000, 2),2), '')
                self.report_check.append(t1)

                t1 = (KEY_DISP_SHEAR_RUP, '', shear_Rupture_prov_weld(self.web_plate.height, self.web_plate.thickness_provided,
                                                                     self.web_plate.fu,
                                                                     round(self.web_plate.shear_rupture_capacity / 1000, 2),gamma_m1, 2),'')
                self.report_check.append(t1)
                t1 = (KEY_DISP_WEBPLATE_SHEAR_CAPACITY, display_prov( round(self.fact_shear_load / 1000, 2),"V_u"),
                   shear_capacity_prov(V_dy=round(self.web_plate.shear_yielding_capacity / 1000, 2),
                                  V_dn= round(self.web_plate.shear_rupture_capacity / 1000, 2),
                                  V_db= 00 ),
                   get_pass_fail(round(self.fact_shear_load / 1000, 2),
                            round(self.web_plate.shear_capacity_web_plate / 1000, 2), relation="lesser"))
                self.report_check.append(t1)

        Disp_3D_image = "/ResourceFiles/images/3d.png"
        rel_path = str(sys.path[0])
        rel_path = rel_path.replace("\\", "/")
        fname_no_ext = popup_summary['filename']
        CreateLatex.save_latex(CreateLatex(), self.report_input, self.report_check, popup_summary, fname_no_ext, rel_path, Disp_3D_image)















        ##############outside#######
        # if self.flange_weld.strength > self.flange_weld.stress:
        #     if self.available_long_flange_length > self.flange_plate.height:
        #         self.design_status = True
        #         break
        #     else:
        #         self.available_long_flange_length = self.available_long_flange_length + 50
        # else:
        #     self.available_long_flange_length = self.available_long_flange_length + 50
        #     self.flange_plate.length = 2 * (self.available_long_flange_length + (2*self.flange_weld.size)) + self.flange_plate.gap
        #     self.l_req_flangelength = round_up((2 * self.available_long_flange_length) + self.flange_plate.height - (
        #                 2 * self.flange_weld.size))
    ##############outside#######
        # if self.flange_weld.stress < self.flange_weld.strength:
        # if self.available_long_flange_length > self.flange_plate.height:
        #     self.design_status = True
        #     break
        # else:
        #     self.available_long_flange_length = int(self.available_long_flange_length + 50)
        # else:
        #     self.available_long_flange_length = int(self.available_long_flange_length + 50)
        #
        #     self.flange_plate.length = 2 * (
        #             self.available_long_flange_length + (2* self.flange_weld.size)) + self.flange_plate.gap
        #     self.l_req_flangelength = round_up(
        #         (2 * self.available_long_flange_length) + self.flange_plate.height -(
        #                 2 * self.flange_weld.size))
        #     if self.flange_plate.length >= 150 * self.flange_weld.throat_tk:
        #         Reduction_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(l_j=self.web_plate.length,
        #                                                                   t_t=self.web_weld.throat_tk)
        #         self.flange_weld.strength = self.flange_weld.strength * Reduction_factor
        #         self.flange_weld.stress = self.flange_force / self.l_req_flangelength
        #         if self.flange_weld.strength > self.flange_weld.stress:
        #             self.design_status = True
        #             break
        #         else:
        #             self.available_long_flange_length = self.available_long_flange_length + 50
        #
        #     else:
        #         self.available_long_flange_length = int(self.available_long_flange_length + 50)

    # print("length", self.available_long_flange_length)
    # if  self.flange_weld.strength > self.flange_weld.stress:
    #     self.design_status = True
    #     self.flange_weld.length = round_up((self.available_long_flange_length), 5)
    #     self.flange_plate.length = round_up(2 * (self.available_long_flange_length + (2* self.flange_weld.size)) + self.flange_plate.gap, 5)
    #     self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
    #     self.flange_weld.height = round_down((self.flange_plate.height - (2 * self.flange_weld.size)), 5)
    #     self.l_req_flangelength = self.l_req_flangelength
    #     # Inner Plate Details
    #     self.flange_weld.Innerlength = round_up((self.available_long_flange_length), 5)
    #     self.flange_plate.Innerlength = round_up(2 * (self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap,
    #         5)
    #     self.flange_plate.Innerheight = round_down(self.total_height_of_inner_plate / 2, 5)
    #     self.flange_weld.Innerheight = round_down((self.flange_plate.Innerheight - 2 * self.flange_weld.size),
    #                                               5)
    #     # self.l_req_innerflangelength = self.l_req_innerflangelength
    #     self.flange_plate_capacity_axial(self)
    #     pass
    # else:
    #     self.design_status = False
    #     logger.error(
    #         ":Length of flange plate is less than height of the flange plate")

    ###########Inside#######################
    # self.design_status =True
    # self.total_height_of_inner_plate = (
    #         self.section.flange_width - (4 * self.flangespace) - self.section.web_thickness - (
    #         2 * self.section.root_radius))  # total width of the inner flange plate
    # if self.total_height_of_inner_plate > 0:
    #
    #     self.flange_plate.Innerheight = round_down((self.total_height_of_inner_plate / 2), 5)
    #     if self.flange_plate.Innerheight < 50:
    #         self.design_status = False
    #         logger.error(
    #             " : Inner plate is not possible, select preference outside")
    #     else:
    #         pass
    #
    #     self.flange_weld.Innerheight = round_down((self.flange_plate.Innerheight - 2 * self.flange_weld.size),
    #                                               5)
    #     if self.flange_weld.Innerheight <= 0:
    #         self.design_status = False
    #         logger.error(
    #             " :Inner plate is not possible, select preference outside")
    #     else:
    #         self.available_long_innerflange_length = self.available_long_flange_length
    #         self.design_status = False
    #         while self.design_status == False:
    #
    #             self.l_req_innerflangelength = (2 * self.available_long_innerflange_length) + self.flange_plate.Innerheight - (
    #                                                    2 * self.flange_weld.size)
    #             self.flange_weld.Innerstress = self.flange_force / self.l_req_innerflangelength
    #             if self.flange_weld.Innerstress < self.flange_weld.strength:
    #                 if self.available_long_innerflange_length > self.flange_plate.Innerheight:
    #                     self.design_status = True
    #                     break
    #
    #                 else:
    #                     self.available_long_innerflange_length = int(
    #                         self.available_long_innerflange_length + 50)
    #             else:
    #                 self.available_long_innerflange_length = int(self.available_long_innerflange_length + 50)
    #                 self.flange_plate.Innerlength = 2 * (self.available_long_innerflange_length + (2*self.flange_weld.size)) + self.flange_plate.gap
    #                 self.l_req_innerflangelength = round_up((2 * self.available_long_innerflange_length) + self.flange_plate.height - (
    #                             2 * self.flange_weld.size))
    #                 if self.flange_plate.Innerlength >= 150 * self.flange_weld.throat_tk:
    #                     Reduction_factor = IS800_2007.cl_10_5_7_3_weld_long_joint(
    #                         l_j=self.flange_plate.Innerlength,
    #                         t_t=self.flange_weld.throat_tk)
    #                     self.flange_weld.strength = self.flange_weld.strength * Reduction_factor
    #                     self.flange_weld.Innerstress = self.flange_force / self.l_req_innerflangelength
    #                     if self.flange_weld.strength > self.flange_weld.Innerstress:
    #                         self.design_status = True
    #                         break
    #                     else:
    #                         self.available_long_flange_length = self.available_long_flange_length + 50
    #
    #                 else:
    #                     self.available_long_flange_length = int(self.available_long_flange_length + 50)
    #
    #     print("self.available_long_length", self.available_long_flange_length)
    # else:
    #     self.flange_plate.Innerheight = 0
    #     self.flange_weld.Innerheight = 0
    #     self.flange_plate.Innerlength = 0
    #     self.flange_weld.Innerlength = 0
    #     self.design_status = False
    #     logger.error(" : Inner plate is not possible, Select outside preference")
    #
    # if self.design_status == True:
    #     # Outer Plate Details
    #     self.flange_weld.length = round_up((self.available_long_flange_length), 5)
    #     self.flange_plate.length = round_up(2*(self.available_long_flange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap, 5)
    #     self.flange_plate.height = round_down((self.section.flange_width - (2 * self.flangespace)), 5)
    #     self.flange_weld.height = round_down((self.flange_plate.height - (2 * self.flange_weld.size)), 5)
    #     self.l_req_flangelength = self.l_req_flangelength
    #     # Inner Plate Details
    #     self.flange_weld.Innerlength = round_up((self.available_long_innerflange_length), 5)
    #     self.flange_plate.Innerlength = round_up(2*(self.available_long_innerflange_length + (2 * self.flange_weld.size)) + self.flange_plate.gap,5)
    #     self.flange_plate.Innerheight = round_down(self.total_height_of_inner_plate / 2, 5)
    #     self.flange_weld.Innerheight = round_down((self.flange_plate.Innerheight - 2 * self.flange_weld.size),5)
    #     self.l_req_innerflangelength = self.l_req_innerflangelength
    #     self.flange_plate_capacity_axial(self)
    # else:
    #     self.design_status = False
#     logger.error(" : Length of flange plate is less than height of the flange plate")