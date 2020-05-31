from utils.common.component import Section,I_sectional_Properties, Material
from design_type.main import Main
from Common import *


class Connection(Main):

    ########################################
    # Design Preference Functions Start
    ########################################

    def tab_supporting_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SUPTNGSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
            source = ''
            fu = ''
            fy = ''
            depth = ''
            flange_width = ''
            flange_thickness = ''
            web_thickness = ''
            flange_slope = ''
            root_radius = ''
            toe_radius = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = ''
            area = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            torsion_const = ''
            warping_const = ''

        else:
            designation = str(input_dictionary[KEY_SUPTNGSEC])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            I_sec_attributes = Section(designation, material_grade)
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
            Section.connect_to_database_update_other_attributes(I_sec_attributes, table, designation,material_grade)
            source = str(I_sec_attributes.source)
            fu = str(I_sec_attributes.fu)
            fy = str(I_sec_attributes.fy)
            depth = str(I_sec_attributes.depth)
            flange_width = str(I_sec_attributes.flange_width)
            flange_thickness = str(I_sec_attributes.flange_thickness)
            web_thickness = str(I_sec_attributes.web_thickness)
            flange_slope = str(I_sec_attributes.flange_slope)
            root_radius = str(I_sec_attributes.root_radius)
            toe_radius = str(I_sec_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(I_sec_attributes.mass)
            area = str(I_sec_attributes.area)
            mom_inertia_z = str(I_sec_attributes.mom_inertia_z)
            mom_inertia_y = str(I_sec_attributes.mom_inertia_y)
            rad_of_gy_z = str(I_sec_attributes.rad_of_gy_z)
            rad_of_gy_y = str(I_sec_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(I_sec_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(I_sec_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(I_sec_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(I_sec_attributes.plast_sec_mod_y)
            torsion_const = str(I_sec_attributes.torsion_const)
            warping_const = str(I_sec_attributes.warping_const)

        if KEY_SUPTNGSEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SUPTNGSEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        supporting_section = []
        t1 = (KEY_SUPTNGSEC, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTNGSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = (KEY_SUPTNGSEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = (KEY_SUPTNGSEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        supporting_section.append(t5)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        supporting_section.append(t5)

        t6 = ('Label_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
        supporting_section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
        supporting_section.append(t7)

        t8 = ('Label_3', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
        supporting_section.append(t8)

        t9 = ('Label_4', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
        supporting_section.append(t9)

        t10 = ('Label_5', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        supporting_section.append(t10)

        t11 = ('Label_6', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        supporting_section.append(t11)

        t12 = ('Label_7', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t13)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t18 = ('Label_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        supporting_section.append(t18)

        t19 = ('Label_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        supporting_section.append(t19)

        t20 = ('Label_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        supporting_section.append(t20)

        t21 = ('Label_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        supporting_section.append(t21)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        supporting_section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        supporting_section.append(t23)

        t24 = ('Label_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        supporting_section.append(t24)

        t25 = ('Label_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        supporting_section.append(t25)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        supporting_section.append(t26)

        t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        t29 = ('Label_23', 'Source', TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        supporting_section.append(t33)

        return supporting_section

    def tab_supported_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "

        if not input_dictionary or input_dictionary[KEY_SUPTDSEC] == 'Select Section' or input_dictionary[
            KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
            source = ''
            fu = ''
            fy = ''
            depth = ''
            flange_width = ''
            flange_thickness = ''
            web_thickness = ''
            flange_slope = ''
            root_radius = ''
            toe_radius = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = ''
            area = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            torsion_const = ''
            warping_const = ''

        else:
            designation = str(input_dictionary[KEY_SUPTDSEC])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            I_sec_attributes = Section(designation)
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"

            I_sec_attributes.connect_to_database_update_other_attributes(table, designation,material_grade)
            source = str(I_sec_attributes.source)
            fu = str(I_sec_attributes.fu)
            fy = str(I_sec_attributes.fy)
            depth = str(I_sec_attributes.depth)
            flange_width = str(I_sec_attributes.flange_width)
            flange_thickness = str(I_sec_attributes.flange_thickness)
            web_thickness = str(I_sec_attributes.web_thickness)
            flange_slope = str(I_sec_attributes.flange_slope)
            root_radius = str(I_sec_attributes.root_radius)
            toe_radius = str(I_sec_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(I_sec_attributes.mass)
            area = str(I_sec_attributes.area)
            mom_inertia_z = str(I_sec_attributes.mom_inertia_z)
            mom_inertia_y = str(I_sec_attributes.mom_inertia_y)
            rad_of_gy_z = str(I_sec_attributes.rad_of_gy_z)
            rad_of_gy_y = str(I_sec_attributes.rad_of_gy_y)
            elast_sec_mod_z = str(I_sec_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(I_sec_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(I_sec_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(I_sec_attributes.plast_sec_mod_y)
            torsion_const = str(I_sec_attributes.torsion_const)
            warping_const = str(I_sec_attributes.warping_const)

        if KEY_SUPTDSEC_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_SUPTDSEC_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        supporting_section = []
        t1 = (KEY_SUPTDSEC, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        supporting_section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t2)

        material = connectdb("Material", call_type="popup")
        t34 = (KEY_SUPTDSEC_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        supporting_section.append(t34)

        t3 = (KEY_SUPTDSEC_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        supporting_section.append(t3)

        t4 = (KEY_SUPTDSEC_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        supporting_section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        supporting_section.append(t5)

        t6 = ('Label_1', KEY_DISP_DEPTH, TYPE_TEXTBOX, None, depth)
        supporting_section.append(t6)

        t7 = ('Label_2', KEY_DISP_FLANGE_W, TYPE_TEXTBOX, None, flange_width)
        supporting_section.append(t7)

        t8 = ('Label_3', KEY_DISP_FLANGE_T, TYPE_TEXTBOX, None, flange_thickness)
        supporting_section.append(t8)

        t9 = ('Label_4', KEY_DISP_WEB_T, TYPE_TEXTBOX, None, web_thickness)
        supporting_section.append(t9)

        t10 = ('Label_5', KEY_DISP_FLANGE_S, TYPE_TEXTBOX, None, flange_slope)
        supporting_section.append(t10)

        t11 = ('Label_6', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        supporting_section.append(t11)

        t12 = ('Label_7', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        supporting_section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t13)

        t14 = ('Label_8', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        supporting_section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t18)

        t15 = ('Label_9', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        supporting_section.append(t15)

        t16 = ('Label_10', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        supporting_section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        supporting_section.append(t17)

        t18 = ('Label_11', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        supporting_section.append(t18)

        t19 = ('Label_12', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        supporting_section.append(t19)

        t20 = ('Label_13', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        supporting_section.append(t20)

        t21 = ('Label_14', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        supporting_section.append(t21)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        supporting_section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        supporting_section.append(t23)

        t24 = ('Label_17', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        supporting_section.append(t24)

        t25 = ('Label_18', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        supporting_section.append(t25)

        t26 = ('Label_19', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        supporting_section.append(t26)

        t27 = ('Label_20', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        supporting_section.append(t27)

        t26 = ('Label_21', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        supporting_section.append(t26)

        t27 = ('Label_22', KEY_DISP_Iw, TYPE_TEXTBOX, None, warping_const)
        supporting_section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        supporting_section.append(t28)

        t29 = ('Label_23', 'Source', TYPE_TEXTBOX, None, source)
        supporting_section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        supporting_section.append(t30)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        supporting_section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        supporting_section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        supporting_section.append(t33)

        return supporting_section

    def get_fu_fy_I_section_suptng(self):
        material_grade = self[0]
        designation = self[1].get(KEY_SUPTNGSEC, None)
        fu = ''
        fy = ''
        if material_grade != "Select Material" and designation != "Select Section":
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
            I_sec_attributes = Section(designation)
            I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
            fu = str(I_sec_attributes.fu)
            fy = str(I_sec_attributes.fy)
        else:
            pass

        d = {KEY_SUPTNGSEC_FU: fu,
             KEY_SUPTNGSEC_FY: fy}

        return d

    def get_fu_fy_I_section_suptd(self):
        material_grade = self[0]
        designation = self[1].get(KEY_SUPTDSEC, None)
        fu = ''
        fy = ''
        if material_grade != "Select Material" and designation != "Select Section":
            table = "Beams" if designation in connectdb("Beams", "popup") else "Columns"
            I_sec_attributes = Section(designation)
            I_sec_attributes.connect_to_database_update_other_attributes(table, designation, material_grade)
            fu = str(I_sec_attributes.fu)
            fy = str(I_sec_attributes.fy)
        else:
            pass

        d = {
             KEY_SUPTDSEC_FU: fu,
             KEY_SUPTDSEC_FY: fy}

        return d


    def get_fu_fy(self):
        material_grade = self[0]
        fu_conn = ''
        fy_20 = ''
        fy_20_40 = ''
        fy_40 = ''
        fu = ''
        fy = ''
        if material_grade != "Select Material":
            m_conn = Material(material_grade)
            fu_conn = m_conn.fu
            fy_20 = m_conn.fy_20
            fy_20_40 = m_conn.fy_20_40
            fy_40 = m_conn.fy_40
        else:
            pass

        d = {KEY_CONNECTOR_FU: fu_conn,
             KEY_CONNECTOR_FY_20: fy_20,
             KEY_CONNECTOR_FY_20_40: fy_20_40,
             KEY_CONNECTOR_FY_40: fy_40,
             KEY_BASE_PLATE_FU: fu,
             KEY_BASE_PLATE_FY: fy}

        return d

    def edit_tabs(self):

        edit_list = []

        t1 = (KEY_DISP_COLSEC, KEY_CONN, TYPE_CHANGE_TAB_NAME, self.get_column_tab_name)
        edit_list.append(t1)

        t1 = (KEY_DISP_BEAMSEC, KEY_CONN, TYPE_CHANGE_TAB_NAME, self.get_beam_tab_name)
        edit_list.append(t1)

        return edit_list

    def get_column_tab_name(self):
        if self in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        else:
            return KEY_DISP_PRIBM

    def get_beam_tab_name(self):
        if self in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        else:
            return KEY_DISP_SECBM

    def list_for_fu_fy_validation(self):

        fu_fy_list = []

        t1 = (KEY_SUPTNGSEC_MATERIAL, KEY_SUPTNGSEC_FU, KEY_SUPTNGSEC_FY)
        fu_fy_list.append(t1)

        t2 = (KEY_SUPTDSEC_MATERIAL, KEY_SUPTDSEC_FU, KEY_SUPTDSEC_FY)
        fu_fy_list.append(t2)

        t3 = (KEY_CONNECTOR_MATERIAL, KEY_CONNECTOR_FU, KEY_CONNECTOR_FY)
        fu_fy_list.append(t3)

        return fu_fy_list


    def get_values_for_design_pref(self, key, design_dictionary):

        if design_dictionary[KEY_MATERIAL] != 'Select Material':
            fu = Material(design_dictionary[KEY_MATERIAL],41).fu
        else:
            fu = ''

        val = {KEY_DP_BOLT_TYPE: "Pretensioned",
               KEY_DP_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_BOLT_MATERIAL_G_O: str(fu),
               KEY_DP_BOLT_SLIP_FACTOR: str(0.3),
               KEY_DP_WELD_FAB: KEY_DP_WELD_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "a - Sheared or hand flame cut",
               KEY_DP_DETAILING_GAP: '10',
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: 'No',
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_CONNECTOR_MATERIAL: str(design_dictionary[KEY_MATERIAL])
               }[key]

        return val

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_1, "Columns")
        add_buttons.append(t1)

        t1 = (KEY_DISP_COLSEC, KEY_SUPTNGSEC, TYPE_COMBOBOX, KEY_SUPTNGSEC, KEY_CONN, VALUES_CONN_2, "Beams")
        add_buttons.append(t1)

        t2 = (KEY_DISP_BEAMSEC, KEY_SUPTDSEC, TYPE_COMBOBOX, KEY_SUPTDSEC, None, None, "Beams")
        add_buttons.append(t2)

        return add_buttons

    ########################################
    # Design Preference Functions End
    ########################################


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

    def call_3DModel(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Model':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Model", bgcolor)

    def call_3DColumn(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Column':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Column", bgcolor)

    def call_3DBeam(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Beam':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Beam", bgcolor)

if __name__ == "__main__":
    connection = Connection()
    connection.test()
    connection.design()
