from design_type.connection.connection import Connection
from utils.common.component import Bolt, Weld, Plate, Angle, Beam, Column, Section
from Common import *
from utils.common.load import Load
from utils.common.material import Material
from utils.common.common_calculation import *



class ShearConnection(Connection):
    def __init__(self):
        super(ShearConnection, self).__init__()

    ############################
    # Design Preferences functions
    ############################
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
            axb = ''
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
            axb = str(Angle_attributes.axb)
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

        t6 = ('Label_1', KEY_DISP_AXB, TYPE_TEXTBOX, None, axb)
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

        t15 = ('Label_26', KEY_DISP_MOD_OF_ELAST, TYPE_TEXTBOX, None, m_o_e)
        section.append(t15)

        t16 = ('Label_27', KEY_DISP_MOD_OF_RIGID, TYPE_TEXTBOX, None, m_o_r)
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

        t28 = (None, None, TYPE_BREAK, None, None)
        section.append(t28)

        t29 = ('Label_23', 'Source', TYPE_TEXTBOX, None, source)
        section.append(t29)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t30 = (None, None, TYPE_ENTER, None, None)
        section.append(t30)

        t31 = ('Label_24', KEY_DISP_POISSON_RATIO, TYPE_TEXTBOX, None, p_r)
        section.append(t31)

        t32 = ('Label_25', KEY_DISP_THERMAL_EXP, TYPE_TEXTBOX, None, t_e)
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
        axb = str(Angle_attributes.axb)
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
        d = {
             KEY_ANGLE_SELECTED:designation,
            KEY_CONNECTOR_MATERIAL: material_grade,
             KEY_CONNECTOR_FY:fy,
             KEY_CONNECTOR_FU:fu,
             'Label_1': axb,
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
             'Label_23':source}
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

        return lst

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

