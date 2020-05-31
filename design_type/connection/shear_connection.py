from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, Section
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common.common_calculation import *
from utils.common.is800_2007 import IS800_2007



class ShearConnection(Connection):
    def __init__(self):
        super(ShearConnection, self).__init__()

    ############################
    # Design Preferences functions
    ############################

    def tab_angle_section(self, input_dictionary):

        "In design preference, it shows other properties of section used "
        "In design preference, it shows other properties of section used "
        if not input_dictionary or input_dictionary[KEY_ANGLE_LIST] == '' or \
                input_dictionary[KEY_MATERIAL] == 'Select Material':
            designation = ''
            material_grade = ''
            fu = ''
            fy = ''
            mass = ''
            area = ''
            a = ''
            b = ''
            thickness = ''
            root_radius = ''
            toe_radius = ''
            Cz = ''
            Cy = ''
            mom_inertia_z = ''
            mom_inertia_y = ''
            mom_inertia_u = ''
            mom_inertia_v = ''
            rad_of_gy_z = ''
            rad_of_gy_y = ''
            rad_of_gy_u = ''
            rad_of_gy_v = ''
            elast_sec_mod_z = ''
            elast_sec_mod_y = ''
            plast_sec_mod_z = ''
            plast_sec_mod_y = ''
            torsion_const=''
            source = ''
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
        else:
            designation = str(input_dictionary[KEY_ANGLE_LIST][0])
            material_grade = str(input_dictionary[KEY_MATERIAL])
            Angle_attributes = Angle(designation,material_grade)
            Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
            source = str(Angle_attributes.source)
            fu = str(Angle_attributes.fu)
            fy = str(Angle_attributes.fy)
            a = str(Angle_attributes.a)
            b = str(Angle_attributes.b)
            thickness = str(Angle_attributes.thickness)
            root_radius = str(Angle_attributes.root_radius)
            toe_radius = str(Angle_attributes.toe_radius)
            m_o_e = "200"
            m_o_r = "76.9"
            p_r = "0.3"
            t_e = "12"
            mass = str(Angle_attributes.mass)
            area = str(Angle_attributes.area)
            Cz = str(Angle_attributes.Cz)
            Cy = str(Angle_attributes.Cy)
            mom_inertia_z = str(Angle_attributes.mom_inertia_z)
            mom_inertia_y = str(Angle_attributes.mom_inertia_y)
            mom_inertia_u = str(Angle_attributes.mom_inertia_u)
            mom_inertia_v = str(Angle_attributes.mom_inertia_v)
            rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
            rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
            rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
            rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
            elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
            elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
            plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
            plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
            torsion_const = str(Angle_attributes.torsion_const)

        if KEY_CONNECTOR_MATERIAL in input_dictionary.keys():
            material_grade = input_dictionary[KEY_CONNECTOR_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        section = []

        if input_dictionary:
            designation_list = input_dictionary[KEY_ANGLE_LIST]
        else:
            designation_list = []

        t0 = (KEY_ANGLE_LIST, KEY_DISP_DESIGNATION, TYPE_COMBOBOX, designation_list, designation)
        section.append(t0)

        t1 = (KEY_ANGLE_SELECTED, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, designation)
        section.append(t1)

        t2 = (None, KEY_DISP_MECH_PROP, TYPE_TITLE, None, None)
        section.append(t2)

        material = connectdb("Material")
        t34 = (KEY_CONNECTOR_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        section.append(t34)

        t3 = (KEY_CONNECTOR_FU, KEY_DISP_FU, TYPE_TEXTBOX, None, fu)
        section.append(t3)

        t4 = (KEY_CONNECTOR_FY, KEY_DISP_FY, TYPE_TEXTBOX, None, fy)
        section.append(t4)

        t5 = (None, KEY_DISP_DIMENSIONS, TYPE_TITLE, None, None)
        section.append(t5)

        t6 = ('Label_1', KEY_DISP_A, TYPE_TEXTBOX, None, a)
        section.append(t6)

        t6 = ('Label_2', KEY_DISP_B, TYPE_TEXTBOX, None, b)
        section.append(t6)

        t8 = ('Label_3', KEY_DISP_LEG_THK, TYPE_TEXTBOX, None, thickness)
        section.append(t8)

        t11 = ('Label_4', KEY_DISP_ROOT_R, TYPE_TEXTBOX, None, root_radius)
        section.append(t11)

        t12 = ('Label_5', KEY_DISP_TOE_R, TYPE_TEXTBOX, None, toe_radius)
        section.append(t12)

        t13 = (None, None, TYPE_BREAK, None, None)
        section.append(t13)

        t14 = ('Label_6', KEY_DISP_TYPE, TYPE_COMBOBOX, ['Rolled', 'Welded'], 'Rolled')
        section.append(t14)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t18 = (None, None, TYPE_ENTER, None, None)
        section.append(t18)

        t15 = ('Label_27', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_28', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
        section.append(t16)

        t17 = (None, KEY_DISP_SEC_PROP, TYPE_TITLE, None, None)
        section.append(t17)

        t18 = ('Label_9', KEY_DISP_MASS, TYPE_TEXTBOX, None, mass)
        section.append(t18)

        t19 = ('Label_10', KEY_DISP_AREA, TYPE_TEXTBOX, None, area)
        section.append(t19)

        t18 = ('Label_7', KEY_DISP_Cz, TYPE_TEXTBOX, None, Cz)
        section.append(t18)

        t19 = ('Label_8', KEY_DISP_Cz, TYPE_TEXTBOX, None, Cy)
        section.append(t19)

        t20 = ('Label_11', KEY_DISP_MOA_IZ, TYPE_TEXTBOX, None, mom_inertia_z)
        section.append(t20)

        t21 = ('Label_12', KEY_DISP_MOA_IY, TYPE_TEXTBOX, None, mom_inertia_y)
        section.append(t21)

        t22 = ('Label_13', KEY_DISP_MOA_IU, TYPE_TEXTBOX, None, mom_inertia_u)
        section.append(t22)

        t23 = ('Label_14', KEY_DISP_MOA_IV, TYPE_TEXTBOX, None, mom_inertia_v)
        section.append(t23)

        t22 = ('Label_15', KEY_DISP_ROG_RZ, TYPE_TEXTBOX, None, rad_of_gy_z)
        section.append(t22)

        t23 = ('Label_16', KEY_DISP_ROG_RY, TYPE_TEXTBOX, None, rad_of_gy_y)
        section.append(t23)

        t22 = ('Label_17', KEY_DISP_ROG_RU, TYPE_TEXTBOX, None, rad_of_gy_u)
        section.append(t22)

        t23 = ('Label_18', KEY_DISP_ROG_RV, TYPE_TEXTBOX, None, rad_of_gy_v)
        section.append(t23)

        t24 = ('Label_19', KEY_DISP_EM_ZZ, TYPE_TEXTBOX, None, elast_sec_mod_z)
        section.append(t24)

        t25 = ('Label_20', KEY_DISP_EM_ZY, TYPE_TEXTBOX, None, elast_sec_mod_y)
        section.append(t25)

        t26 = ('Label_21', KEY_DISP_PM_ZPZ, TYPE_TEXTBOX, None, plast_sec_mod_z)
        section.append(t26)

        t27 = ('Label_22', KEY_DISP_PM_ZPY, TYPE_TEXTBOX, None, plast_sec_mod_y)
        section.append(t27)

        t27 = ('Label_23', KEY_DISP_It, TYPE_TEXTBOX, None, torsion_const)
        section.append(t27)

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t29 = ('Label_24', 'Source', TYPE_TEXTBOX, None, source)
        section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t31 = ('Label_25', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_26', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
        section.append(t32)

        t33 = (KEY_IMAGE, None, TYPE_IMAGE, None, None, None)
        section.append(t33)

        return section

    def get_new_angle_section_properties(self):

        designation = self[0]
        material_grade = self[1]

        Angle_attributes = Angle(designation, material_grade)
        Angle_attributes.connect_to_database_update_other_attributes_angles(designation, material_grade)
        source = str(Angle_attributes.source)
        Type= str(Angle_attributes.Type)
        fu = str(Angle_attributes.fu)
        fy = str(Angle_attributes.fy)
        a = str(Angle_attributes.leg_a_length)
        b = str(Angle_attributes.leg_b_length)
        thickness = str(Angle_attributes.thickness)
        root_radius = str(Angle_attributes.root_radius)
        toe_radius = str(Angle_attributes.toe_radius)
        mass = str(Angle_attributes.mass)
        area = str(Angle_attributes.area)
        Cz = str(Angle_attributes.Cz)
        Cy = str(Angle_attributes.Cy)
        mom_inertia_z = str(Angle_attributes.mom_inertia_z)
        mom_inertia_y = str(Angle_attributes.mom_inertia_y)
        mom_inertia_u = str(Angle_attributes.mom_inertia_u)
        mom_inertia_v = str(Angle_attributes.mom_inertia_v)
        rad_of_gy_z = str(Angle_attributes.rad_of_gy_z)
        rad_of_gy_y = str(Angle_attributes.rad_of_gy_y)
        rad_of_gy_u = str(Angle_attributes.rad_of_gy_u)
        rad_of_gy_v = str(Angle_attributes.rad_of_gy_v)
        elast_sec_mod_z = str(Angle_attributes.elast_sec_mod_z)
        elast_sec_mod_y = str(Angle_attributes.elast_sec_mod_y)
        plast_sec_mod_z = str(Angle_attributes.plast_sec_mod_z)
        plast_sec_mod_y = str(Angle_attributes.plast_sec_mod_y)
        torsion_const = str(Angle_attributes.torsion_const)
        d = {
            KEY_ANGLE_SELECTED:designation,
            KEY_CONNECTOR_MATERIAL: material_grade,
            KEY_CONNECTOR_FY:fy,
            KEY_CONNECTOR_FU:fu,
            'Label_1': a,
            'Label_2': b,
            'Label_3':thickness,
            'Label_4':root_radius,
            'Label_5':toe_radius,
            'Label_6':Type,
            'Label_7': Cz,
            'Label_8': Cy,
            'Label_9':mass,
            'Label_10':area,
            'Label_11':mom_inertia_z,
            'Label_12':mom_inertia_y,
            'Label_13':mom_inertia_u,
            'Label_14':mom_inertia_v,
            'Label_15':rad_of_gy_z,
            'Label_16':rad_of_gy_y,
            'Label_17':rad_of_gy_u,
            'Label_18':rad_of_gy_v,
            'Label_19':elast_sec_mod_z,
            'Label_20':elast_sec_mod_y,
            'Label_21':plast_sec_mod_z,
            'Label_22':plast_sec_mod_y,
            'Label_23':torsion_const,
            'Label_24':source}
        return d

    @staticmethod
    def pltthk_customized():
        a = VALUES_PLATETHK_CUSTOMIZED
        return a

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    @staticmethod
    def diam_bolt_customized():
        c = connectdb1()
        return c

    def customized_input(self):

        list1 = []
        t1 = (KEY_GRD, self.grdval_customized)
        list1.append(t1)
        t2 = (KEY_PLATETHK, self.pltthk_customized)
        list1.append(t2)
        t3 = (KEY_D, self.diam_bolt_customized)
        list1.append(t3)
        return list1

    def fn_conn_suptngsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_COLSEC
        elif conn in VALUES_CONN_2:
            return KEY_DISP_PRIBM
        else:
            return ''

    def fn_conn_suptdsec_lbl(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return KEY_DISP_BEAMSEC
        elif conn in VALUES_CONN_2:
            return KEY_DISP_SECBM
        else:
            return ''

    def fn_conn_suptngsec(self):

        conn = self[0]
        if conn in VALUES_CONN_1:
            return connectdb("Columns")
        elif conn in VALUES_CONN_2:
            return connectdb("Beams")
        else:
            return []

    def fn_conn_suptdsec(self):

        conn = self[0]
        if conn in VALUES_CONN:
            return connectdb("Beams")
        else:
            return []

    def fn_conn_image(self):

        conn = self[0]
        if conn == VALUES_CONN[0]:
            return './ResourceFiles/images/fin_cf_bw.png'
        elif conn == VALUES_CONN[1]:
            return './ResourceFiles/images/fin_cw_bw.png'
        elif conn in VALUES_CONN_2:
            return './ResourceFiles/images/fin_beam_beam.png'
        else:
            return ''

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_LABEL, self.fn_conn_suptngsec_lbl)
        lst.append(t1)

        t2 = ([KEY_CONN], KEY_SUPTNGSEC, TYPE_COMBOBOX, self.fn_conn_suptngsec)
        lst.append(t2)

        t3 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_LABEL, self.fn_conn_suptdsec_lbl)
        lst.append(t3)

        t4 = ([KEY_CONN], KEY_SUPTDSEC, TYPE_COMBOBOX, self.fn_conn_suptdsec)
        lst.append(t4)

        t5 = ([KEY_CONN], KEY_IMAGE, TYPE_IMAGE, self.fn_conn_image)
        lst.append(t5)

        t6 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_DOCK, self.out_bolt_bearing)
        lst.append(t6)

        t7 = ([KEY_TYP], KEY_OUT_BOLT_BEARING, TYPE_OUT_LABEL, self.out_bolt_bearing)
        lst.append(t7)

        return lst

    def out_bolt_bearing(self):

        bolt_type = self[0]
        if bolt_type != TYP_BEARING:
            return True
        else:
            return False

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        flag1 = False
        flag2=False
        option_list = self.input_values(self)
        missing_fields_list = []
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[3]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])
            # elif option[2] == TYPE_MODULE:
            #     if design_dictionary[option[0]] == "Fin Plate":
        if len(missing_fields_list) == 0:
            if design_dictionary[KEY_CONN] == VALUES_CONN_2[0]:
                primary = design_dictionary[KEY_SUPTNGSEC]
                secondary = design_dictionary[KEY_SUPTDSEC]
                conn = sqlite3.connect(PATH_TO_DATABASE)
                cursor = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? ) ", (primary,))
                lst = []
                rows = cursor.fetchall()
                for row in rows:
                    lst.append(row)
                p_val = lst[0][0]
                cursor2 = conn.execute("SELECT D FROM BEAMS WHERE Designation = ( ? )", (secondary,))
                lst1 = []
                rows1 = cursor2.fetchall()
                for row1 in rows1:
                    lst1.append(row1)
                s_val = lst1[0][0]
                if p_val <= s_val:
                    error = "Secondary beam depth is higher than clear depth of primary beam web " + "\n" + "(No provision in Osdag till now)"
                    all_errors.append(error)
                else:
                    flag1 = True

            elif design_dictionary[KEY_CONN] == VALUES_CONN_1[1]:
                primary = design_dictionary[KEY_SUPTNGSEC]
                secondary = design_dictionary[KEY_SUPTDSEC]
                conn = sqlite3.connect(PATH_TO_DATABASE)
                cursor = conn.execute("SELECT D, T, R1, R2 FROM COLUMNS WHERE Designation = ( ? ) ", (primary,))
                p_beam_details = cursor.fetchone()
                p_val = p_beam_details[0] - 2*p_beam_details[1] - p_beam_details[2] - p_beam_details[3]
                cursor2 = conn.execute("SELECT B FROM BEAMS WHERE Designation = ( ? )", (secondary,))

                s_beam_details = cursor2.fetchone()
                s_val = s_beam_details[0]
                #print(p_val,s_val)
                if p_val <= s_val:
                    error = "Secondary beam width is higher than clear depth of primary column web " + "\n" + "(No provision in Osdag till now)"
                    all_errors.append(error)
                else:
                    flag1 = True
            else:
                flag1 = True

            selected_plate_thk = list(np.float_(design_dictionary[KEY_PLATETHK]))
            supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC],material_grade=design_dictionary[KEY_MATERIAL])
            available_plates = [i for i in selected_plate_thk if i >= supported_section.web_thickness]
            if not available_plates:
                error = "Plate thickness should be greater than suppported section web thicknesss."
                all_errors.append(error)
            else:
                flag2=True
            if flag1 and flag2:
                self.set_input_values(self, design_dictionary)
            else:
                return all_errors
        else:
            error = self.generate_missing_fields_error_string(self, missing_fields_list)
            all_errors.append(error)
            return all_errors

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


    def warn_text(self):

        """
        Function to give logger warning when any old value is selected from Column and Beams table.
        """

        # @author Arsil Zunzunia
        global logger
        red_list = red_list_function()
        if self.supported_section.designation in red_list or self.supporting_section.designation in red_list:
            logger.warning(
                " : You are using a section (in red color) that is not available in latest version of IS 808")
            logger.info(
                " : You are using a section (in red color) that is not available in latest version of IS 808")

    def set_input_values(self, design_dictionary):
        self.mainmodule = "Shear Connection"
        self.connectivity = design_dictionary[KEY_CONN]
        self.material = Material(material_grade=design_dictionary[KEY_MATERIAL])

        if self.connectivity in VALUES_CONN_1:
            self.supporting_section = Column(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])
        else:
            self.supporting_section = Beam(designation=design_dictionary[KEY_SUPTNGSEC], material_grade=design_dictionary[KEY_SUPTNGSEC_MATERIAL])

        self.supported_section = Beam(designation=design_dictionary[KEY_SUPTDSEC], material_grade=design_dictionary[KEY_SUPTDSEC_MATERIAL])
        self.supported_section.notch_ht = round_up(self.supporting_section.flange_thickness * 2, 5)
        self.bolt = Bolt(grade=design_dictionary[KEY_GRD], diameter=design_dictionary[KEY_D],
                         bolt_type=design_dictionary[KEY_TYP],
                         bolt_hole_type=design_dictionary[KEY_DP_BOLT_HOLE_TYPE],
                         edge_type=design_dictionary[KEY_DP_DETAILING_EDGE_TYPE],
                         mu_f=design_dictionary.get(KEY_DP_BOLT_SLIP_FACTOR, None),
                         corrosive_influences=design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES],
                         bolt_tensioning=design_dictionary[KEY_DP_BOLT_TYPE])

        self.load = Load(shear_force=design_dictionary[KEY_SHEAR], axial_force=design_dictionary.get(KEY_AXIAL, None))

    def member_capacity(self):
        # print(KEY_CONN,VALUES_CONN_1,self.supported_section.type)
        self.supported_section.notch_ht = round_up(
            max(self.supporting_section.flange_thickness + self.supporting_section.root_radius + 10,
                self.supported_section.flange_thickness + self.supported_section.root_radius + 10), 5)
        if self.connectivity in VALUES_CONN_1:
            if self.supported_section.type == "Rolled":
                self.supported_section.web_height = self.supported_section.depth
            else:
                self.supported_section.web_height = self.supported_section.depth - (
                            2 * self.supported_section.flange_thickness)  # -(2*self.supported_section.root_radius)
        else:

            self.supported_section.web_height = self.supported_section.depth - self.supported_section.notch_ht

        A_g = self.supported_section.web_height * self.supported_section.web_thickness
        # 0.6 is multiplied for shear yielding capacity to keep the section in low shear
        self.supported_section.shear_yielding_capacity = 0.6 * IS800_2007.cl_8_4_design_shear_strength(A_g,
                                                                                                       self.supported_section.fy)
        self.supported_section.tension_yielding_capacity = IS800_2007.cl_6_2_tension_yielding_strength(A_g,
                                                                                                       self.supported_section.fy)

        print(self.supported_section.shear_yielding_capacity, self.load.shear_force,
              self.supported_section.tension_yielding_capacity, self.load.axial_force)

