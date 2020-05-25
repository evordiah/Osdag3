"""

@Author:    Danish Ansari - Osdag Team, IIT Bombay
@Co-author: Aditya Pawar, Project Intern, MIT College (Aurangabad)


@Module - Base Plate Connection
           - Pinned Base Plate (welded and bolted) [Axial + Shear]
           - Gusseted Base Plate [Moment (major and minor axis) + Axial + Shear]
           - Base Plate for hollow sections [Moment (major and minor axis) + Axial + Shear]


@Reference(s): 1) IS 800: 2007, General construction in steel - Code of practice (Third revision)
               2) IS 808: 1989, Dimensions for hot rolled steel beam, column, channel, and angle sections and
                                it's subsequent revision(s)
               3) IS 2062: 2011, Hot rolled medium and high tensile structural steel - specification
               4) IS 5624: 1993, Foundation bolts
               5) IS 456: 2000, Plain and reinforced concrete - code of practice
               6) Design of Steel Structures by N. Subramanian (Fifth impression, 2019, Chapter 15)
               7) Limit State Design of Steel Structures by S K Duggal (second edition, Chapter 11)

     other     8)  Column Bases - Omer Blodgett (chapter 3)
  references   9) AISC Design Guide 1 - Base Plate and Anchor Rod Design

"""

# Importing modules from the project directory

from design_type.connection.moment_connection import MomentConnection
from utils.common.is800_2007 import IS800_2007
from utils.common.other_standards import IS_5624_1993
from utils.common.component import *
from utils.common.material import *
from utils.common.common_calculation import *
from Common import *
from utils.common.load import Load
from utils.common.other_standards import *
from design_report.reportGenerator import save_html


import logging



class BasePlateConnection(MomentConnection, IS800_2007, IS_5624_1993, IS1367_Part3_2002, Column):
    """
    Perform stress analyses --> design base plate and anchor bolt--> provide connection detailing.

    Attributes:
                connectivity (str): type of base plate connection (pinned - welded, pinned - bolted,
                                    gusseted, hollow section).
                end_condition (str): assume end condition based on base plate type.
                    Assumption(s):
                                1) End condition is 'Pinned' for welded and bolted base plate.
                                2) End condition is 'Fixed' for gusseted and hollow section type base plate.

                column_section (str): column section [Ref: IS 808: 1989, and it's subsequent revision(s),
                                any new section data added by the user using the 'add section' feature from Osdag GUI.
                material (str): material grade of the column section [Ref: IS 2062: 2011, table 2].

                load_axial (float): Axial compressive load (concentric to column axis).
                load_shear (float): Shear/horizontal load.
                load_moment_major (float): Bending moment acting along the major (z-z) axis of the column.
                load_moment_minor (float): Bending moment acting along the minor (y-y) axis of the column.

                anchor_dia (str): diameter of the anchor bolt [Ref: IS 5624: 1993, page 5].
                anchor_type (str): type of the anchor bolt [Ref: IS 5624: 1993, Annex A, clause 4].

                footing_grade (str): grade of footing material (concrete) [Ref: IS 456: 2000, table 2].

                dp_column_designation (str): designation of the column as per IS 808.
                dp_column_type (str): type of manufacturing of the coulmn section (rolled, built-up, welded etc.).
                dp_column_source (str): source of the database of the column section.
                                        [Osdag/ResourceFiles/Database/Intg_osdag.sqite].
                dp_column_material (str): material grade of the column section [Ref: IS 2062: 2011].
                dp_column_fu (float): ultimate strength of the column section (default if not overwritten).
                dp_column_fy (float): yield strength of the column section (default if not overwritten).

                dp_bp_material (str): material grade of the base plate [Ref: IS 2062: 2011].
                dp_bp_fu (float): ultimate strength of the base plate (default if not overwritten).
                dp_bp_fy (float): yield strength of the base plate (default if not overwritten).
                    Assumption: The ultimate and yield strength values of base plare are assumed to be same as the
                                parent (column) material unless and untill overwritten in the design preferences,
                                with suitable validation.

                dp_anchor_designation (str): designation of the anchor bolt as per IS 5624: 1993, clause 5.
                dp_anchor_type (str): type of the anchor bolt [Ref: IS 5624: 1993, Annex A, clause 4].
                dp_anchor_hole (str): type of hole 'Standard' or 'Over-sized'.
                dp_anchor_fu_overwrite (float): ultimate strength of the anchor bolt corresponding to its grade.
                dp_anchor_friction (float): coefficient of friction between the anchor bolt and the footing material.

                dp_weld_fab (str): type of weld fabrication, 'Shop Weld' or 'Field Weld'.
                dp_weld_fu_overwrite (float): ultimate strength of the weld material.

                dp_detail_edge_type (str): type of edge preparation, 'a - hand flame cut' or 'b - Machine flame cut'.
                dp_detail_is_corrosive (str): is environment corrosive, 'Yes' or 'No'.

                dp_design_method (str): design philosophy used 'Limit State Design'.
                dp_bp_method (str): analysis method used for base plate 'Effective Area Method'

                gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling.
                gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress.
                gamma_mb (float): partial safety factor for material - resistance of connection - bolts.
                gamma_mw (float): partial safety factor for material - resistance of connection - weld.

                bearing_strength_concrete (float)

    """

    def __init__(self):
        """Initialize all attributes."""
        super(BasePlateConnection, self).__init__()

        # attributes for input dock UI
        self.connectivity = ""
        self.end_condition = ""
        self.column_section = ""
        self.material = ""

        self.load_axial = 0.0
        self.load_shear = 0.0
        self.load_moment_major = 0.0
        self.load_moment_minor = 0.0

        self.anchor_dia = []
        self.anchor_type = ""
        self.anchor_grade = []
        self.anchor_fu_fy = []

        self.footing_grade = 0.0

        if self.connectivity == 'Welded-Slab Base':
            self.weld_type = self.weld_type
        else:
            self.weld_type = 'Butt Weld'

        # attributes for design preferences
        self.dp_column_designation = ""  # dp for column
        self.dp_column_type = ""
        self.dp_column_source = ""
        self.dp_column_material = ""
        self.dp_column_fu = 0.0
        self.dp_column_fy = 0.0

        self.dp_bp_material = ""  # dp for base plate
        self.dp_bp_fu = 0.0
        self.dp_bp_fy = 0.0

        self.dp_anchor_designation = ""  # dp for anchor bolt
        self.dp_anchor_type = ""
        self.dp_anchor_hole = "Standard"
        self.dp_anchor_length = 0
        self.dp_anchor_fu_overwrite = 0.0
        self.dp_anchor_friction = 0.0

        self.dp_weld_fab = "Shop Weld"  # dp for weld
        self.dp_weld_fu_overwrite = 0.0

        self.dp_detail_edge_type = "b - Machine flame cut"  # dp for detailing
        self.dp_detail_is_corrosive = "No"

        self.dp_design_method = "Limit State Design"  # dp for design
        self.dp_bp_method = "Effective Area Method"

        # other attributes
        self.gamma_m0 = 0.0
        self.gamma_m1 = 0.0
        self.gamma_mb = 0.0
        self.gamma_mw = 0.0

        # self.column_properties = Column(designation=self.dp_column_designation, material_grade=self.dp_column_material)
        self.column_D = 0.0
        self.column_bf = 0.0
        self.column_tf = 0.0
        self.column_tw = 0.0
        self.column_r1 = 0.0
        self.column_r2 = 0.0

        self.bearing_strength_concrete = 0.0
        self.w = 0.0
        self.min_area_req = 0.0
        self.effective_bearing_area = 0.0
        self.projection = 0.0
        self.plate_thk = 0.0
        self.standard_plate_thk = []
        self.neglect_anchor_dia = []
        self.anchor_bolt = ''
        self.anchor_dia_provided = 'M8'
        self.anchor_length_min = 1
        self.anchor_length_max = 1
        self.anchor_length_provided = 1
        self.anchor_nos_provided = 0
        self.anchor_hole_dia = 0.0
        self.bp_length_min = 0.0
        self.bp_width_min = 0.0
        self.bp_length_provided = 0.0
        self.bp_width_provided = 0.0
        self.end_distance = 0.0
        self.end_distance_max = 0.0
        self.edge_distance = 0.0
        self.edge_distance_max = 0.0
        self.pitch_distance = 0.0
        self.gauge_distance = 0.0
        self.bp_area_provided = 0.0
        self.anchor_area = self.bolt_area(self.table1(self.anchor_dia_provided)[0])  # TODO check if this works
        self.shear_capacity_anchor = 0.0
        self.bearing_capacity_anchor = 0.0
        self.anchor_capacity = 0.0
        self.combined_capacity_anchor = 0.0

        self.length_available_total = 0.0
        self.effective_length_flange = 0.0
        self.total_eff_len_available = 0.0
        self.effective_length_web = 0.0
        self.load_axial_flange = 0.0
        self.load_axial_web = 0.0
        self.strength_unit_len = 0.0
        self.weld_size = 0.0
        self.weld_size_flange = 0.0
        self.weld_size_web = 0.0
        self.gusset_along_flange = 'No'
        self.gusset_along_web = 'No'
        self.gusset_plate_length = 0.0
        self.stiffener_plate_length = 0.0
        self.total_eff_len_gusset_available = 0.0
        self.gusset_outstand_length = 0.0
        self.stiffener_outstand_length = 0.0
        self.gusset_fy = self.dp_column_fy
        self.stiffener_fy = self.dp_column_fy
        self.epsilon = 1
        self.gusset_plate_thick = 0.0
        self.stiffener_plate_thick = 0.0
        self.gusset_plate_height = 0.0
        self.stiffener_plate_height = 0.0

        self.shear_on_gusset = 0.0
        self.moment_on_gusset = 0.0
        self.shear_capacity_gusset = 0.0
        self.z_e_gusset = 0.0
        self.moment_capacity_gusset = 0.0

        self.shear_on_stiffener = 0.0
        self.moment_on_stiffener = 0.0
        self.shear_capacity_stiffener = 0.0
        self.z_e_stiffener = 0.0
        self.moment_capacity_stiffener = 0.0

        self.weld_size_gusset = 0.0
        self.weld_size_gusset_vertical = 0.0
        self.weld_size_stiffener = 0.0

        self.eccentricity_zz = 0.0
        self.sigma_max_zz = 0.0
        self.sigma_min_zz = 0.0
        self.critical_xx = 0.0
        self.sigma_xx = 0.0
        self.ze_zz = 0.0
        self.critical_M_xx = 0.0
        self.n = 1
        self.anchor_area_tension = 0.0
        self.f = 0.0
        self.y = 0.0
        self.tension_demand_anchor = 0.0
        self.tension_capacity_anchor = 0.0
        self.tension_bolts_req = 1

        self.safe = True

    def set_osdaglogger(key):
        """
        Set logger for Base Plate Module.
        """
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
            formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    def module_name(self):
        """
        Call the Base Plate Module key for displaying the module name.
        """
        return KEY_DISP_BASE_PLATE

    def input_values(self, existingvalues={}):
        """
        Return a-list of tuple, used to create the Base Plate input dock U.I in Osdag design window.
        """

        self.module = KEY_DISP_BASE_PLATE

        options_list = []

        if KEY_DISP_CONN in existingvalues:
            existingvalue_key_conn = existingvalues[KEY_DISP_CONN]
        else:
            existingvalue_key_conn = ''

        if KEY_SECSIZE in existingvalues:  # this might not be required
            existingvalue_key_suptngsec = existingvalues[KEY_SECSIZE]
        else:
            existingvalue_key_suptngsec = ''


        if KEY_MATERIAL in existingvalues:
            existingvalue_key_mtrl = existingvalues[KEY_MATERIAL]
        else:
            existingvalue_key_mtrl = ''

        if KEY_AXIAL in existingvalues:
            existingvalue_key_axial = existingvalues[KEY_AXIAL]
        else:
            existingvalue_key_axial = ''

        if KEY_MOMENT in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_MOMENT]
        else:
            existingvalue_key_versh = ''

        if KEY_SHEAR in existingvalues:
            existingvalue_key_versh = existingvalues[KEY_SHEAR]
        else:
            existingvalue_key_versh = ''

        if KEY_DIA_ANCHOR in existingvalues:
            existingvalue_key_d = existingvalues[KEY_DIA_ANCHOR]
        else:
            existingvalue_key_d = ''

        # if KEY_TYP in existingvalues:
        #     existingvalue_key_typ = existingvalues[KEY_TYP]
        # else:
        #     existingvalue_key_typ = ''

        # if KEY_GRD in existingvalues:
        #     existingvalue_key_grd = existingvalues[KEY_GRD]
        # else:
        #     existingvalue_key_grd = ''

        t1 = (None, DISP_TITLE_CM, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t1)

        t2 = (KEY_MODULE, KEY_DISP_BASE_PLATE, TYPE_MODULE, None, None, True, 'No Validator')
        options_list.append(t2)

        t3 = (KEY_CONN, KEY_DISP_CONN, TYPE_COMBOBOX, existingvalue_key_conn, VALUES_CONN_BP, True, 'No Validator')
        options_list.append(t3)

        t4 = (KEY_IMAGE, None, TYPE_IMAGE, None, "./ResourceFiles/images/base_plate.png", True, 'No Validator')
        options_list.append(t4)

        t5 = (KEY_END_CONDITION, KEY_DISP_END_CONDITION, TYPE_NOTE, existingvalue_key_conn, 'Pinned', True, 'No Validator')
        options_list.append(t5)

        t6 = (KEY_SECSIZE, KEY_DISP_COLSEC, TYPE_COMBOBOX, existingvalue_key_suptngsec,
              connectdb("Columns"), True, 'No Validator')  # this might not be required
        options_list.append(t6)

        # t4 = (KEY_SUPTDSEC, KEY_DISP_BEAMSEC, TYPE_COMBOBOX, existingvalue_key_suptdsec, connectdb("Columns"))
        # options_list.append(t4)

        t7 = (KEY_MATERIAL, KEY_DISP_MATERIAL, TYPE_COMBOBOX, existingvalue_key_mtrl, VALUES_MATERIAL, True, 'No Validator')
        options_list.append(t7)

        t8 = (None, DISP_TITLE_FSL, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t8)

        t9 = (KEY_AXIAL, KEY_DISP_AXIAL, TYPE_TEXTBOX, existingvalue_key_axial, None, True, 'No Validator')
        options_list.append(t9)

        t10 = (KEY_SHEAR, KEY_DISP_SHEAR, TYPE_TEXTBOX, existingvalue_key_versh, None, True, 'No Validator')
        options_list.append(t10)

        t11 = (KEY_MOMENT, KEY_DISP_MOMENT, '', existingvalue_key_axial, None, True, 'No Validator')
        options_list.append(t11)

        t12 = (KEY_MOMENT_MAJOR, KEY_DISP_MOMENT_MAJOR, TYPE_TEXTBOX, existingvalue_key_conn, None, False, 'No Validator')
        options_list.append(t12)

        t13 = (KEY_MOMENT_MINOR, KEY_DISP_MOMENT_MINOR, TYPE_TEXTBOX, existingvalue_key_conn, None, False, 'No Validator')
        options_list.append(t13)

        t14 = (None, DISP_TITLE_ANCHOR_BOLT, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t14)

        t15 = (KEY_DIA_ANCHOR, KEY_DISP_DIA_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_DIA_ANCHOR, True, 'No Validator')
        options_list.append(t15)

        t16 = (KEY_TYP_ANCHOR, KEY_DISP_TYP_ANCHOR, TYPE_COMBOBOX, existingvalue_key_d, VALUES_TYP_ANCHOR, True, 'No Validator')
        options_list.append(t16)

        t17 = (KEY_GRD_ANCHOR, KEY_DISP_GRD_ANCHOR, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_d, VALUES_GRD_ANCHOR, True, 'No Validator')
        options_list.append(t17)

        t18 = (None, DISP_TITLE_FOOTING, TYPE_TITLE, None, None, True, 'No Validator')
        options_list.append(t18)

        t19 = (KEY_GRD_FOOTING, KEY_DISP_GRD_FOOTING, TYPE_COMBOBOX, existingvalue_key_d, VALUES_GRD_FOOTING, True, 'No Validator')
        options_list.append(t19)

        t20 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True, 'No Validator')
        options_list.append(t20)

        t21 = (KEY_WELD_TYPE, KEY_DISP_WELD_TYPE, TYPE_COMBOBOX, existingvalue_key_d, VALUES_WELD_TYPE, True, 'No Validator')
        options_list.append(t21)

        # t11 = (KEY_TYP, KEY_DISP_TYP, TYPE_COMBOBOX, existingvalue_key_typ, VALUES_TYP)
        # options_list.append(t11)

        # t12 = (KEY_GRD, KEY_DISP_GRD, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_grd, VALUES_GRD)
        # options_list.append(t12)

        # t13 = (None, DISP_TITLE_PLATE, TYPE_TITLE, None, None)
        # options_list.append(t13)

        # t14 = (KEY_PLATETHK, KEY_DISP_PLATETHK, TYPE_COMBOBOX_CUSTOMIZED, existingvalue_key_platethk, VALUES_PLATETHK)
        # options_list.append(t14)

        return options_list

    def output_values(self, flag):
        out_list = []

        t1 = (None, DISP_TITLE_ANCHOR_BOLT, TYPE_TITLE, None, True)
        out_list.append(t1)

        t2 = (KEY_DIA_ANCHOR, KEY_DISP_DIA_ANCHOR, TYPE_TEXTBOX, self.anchor_dia_provided if flag else '', True)
        out_list.append(t2)

        t3 = (KEY_GRD_ANCHOR, KEY_DISP_GRD_ANCHOR, TYPE_TEXTBOX, self.anchor_grade if flag else '', True)
        out_list.append(t3)

        t4 = (KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DISP_DP_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX,
              self.anchor_length_provided if flag else '', True)
        out_list.append(t4)

        t5 = (KEY_OUT_ANCHOR_BOLT_SHEAR, KEY_OUT_DISP_ANCHOR_BOLT_SHEAR, TYPE_TEXTBOX,
              self.shear_capacity_anchor if flag else '', True)
        out_list.append(t5)

        t6 = (KEY_OUT_ANCHOR_BOLT_BEARING, KEY_OUT_DISP_ANCHOR_BOLT_BEARING, TYPE_TEXTBOX,
              self.bearing_capacity_anchor if flag else '', True)
        out_list.append(t6)

        t7 = (KEY_OUT_ANCHOR_BOLT_CAPACITY, KEY_OUT_DISP_ANCHOR_BOLT_CAPACITY, TYPE_TEXTBOX,
              self.anchor_capacity if flag else '', True)
        out_list.append(t7)

        t8 = (KEY_OUT_ANCHOR_BOLT_COMBINED, KEY_OUT_DISP_ANCHOR_BOLT_COMBINED, TYPE_TEXTBOX,
              self.combined_capacity_anchor if flag else '', True)
        out_list.append(t8)

        t20 = (KEY_OUT_ANCHOR_BOLT_TENSION, KEY_OUT_DISP_ANCHOR_BOLT_TENSION, TYPE_TEXTBOX,
               self.tension_capacity_anchor if flag and self.connectivity == 'Gusseted Base Plate' else '', True)
        out_list.append(t20)

        t9 = (None, KEY_DISP_BASE_PLATE, TYPE_TITLE, None, True)
        out_list.append(t9)

        t10 = (KEY_OUT_BASEPLATE_THICKNNESS, KEY_OUT_DISP_BASEPLATE_THICKNNESS, TYPE_TEXTBOX,
               self.plate_thk if flag else '', True)
        out_list.append(t10)

        t11 = (KEY_OUT_BASEPLATE_LENGTH, KEY_OUT_DISP_BASEPLATE_LENGTH, TYPE_TEXTBOX,
               self.bp_length_provided if flag else '', True)
        out_list.append(t11)

        t12 = (KEY_OUT_BASEPLATE_WIDTH, KEY_OUT_DISP_BASEPLATE_WIDTH, TYPE_TEXTBOX,
               self.bp_width_provided if flag else '', True)
        out_list.append(t12)

        t13 = (None, DISP_TITLE_DETAILING, TYPE_TITLE, None, True)
        out_list.append(t13)

        t14 = (KEY_OUT_DETAILING_NO_OF_ANCHOR_BOLT, KEY_OUT_DISP_DETAILING_NO_OF_ANCHOR_BOLT, TYPE_TEXTBOX,
               self.anchor_nos_provided if flag else '', True)
        out_list.append(t14)

        t21 = (KEY_OUT_DETAILING_PITCH_DISTANCE, KEY_OUT_DISP_DETAILING_PITCH_DISTANCE, TYPE_TEXTBOX,
               self.end_distance if flag else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_DETAILING_GAUGE_DISTANCE, KEY_OUT_DISP_DETAILING_GAUGE_DISTANCE, TYPE_TEXTBOX,
               self.end_distance if flag else '', True)
        out_list.append(t22)

        t15 = (KEY_OUT_DETAILING_END_DISTANCE, KEY_OUT_DISP_DETAILING_END_DISTANCE, TYPE_TEXTBOX,
               self.end_distance if flag else '', True)
        out_list.append(t15)

        t16 = (KEY_OUT_DETAILING_EDGE_DISTANCE, KEY_OUT_DISP_DETAILING_EDGE_DISTANCE, TYPE_TEXTBOX,
               self.edge_distance if flag else '', True)
        out_list.append(t16)

        t17 = (KEY_OUT_DETAILING_PROJECTION, KEY_OUT_DISP_DETAILING_PROJECTION, TYPE_TEXTBOX,
               self.projection if flag and self.connectivity == 'Welded-Slab Base' else '', True)
        out_list.append(t17)

        t23 = (None, DISP_TITLE_GUSSET_PLATE, TYPE_TITLE, None, True)
        out_list.append(t23)

        t24 = (KEY_OUT_GUSSET_PLATE_THICKNNESS, KEY_OUT_DISP_GUSSET_PLATE_THICKNESS, TYPE_TEXTBOX,
               self.gusset_plate_thick if flag else '', True)
        out_list.append(t24)

        t25 = (KEY_OUT_GUSSET_PLATE_SHEAR_DEMAND, KEY_OUT_DISP_GUSSET_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_gusset if flag else '', True)
        out_list.append(t25)

        t26 = (KEY_OUT_GUSSET_PLATE_SHEAR, KEY_OUT_DISP_GUSSET_PLATE_SHEAR, TYPE_TEXTBOX,
               self.shear_capacity_gusset if flag else '', True)
        out_list.append(t26)

        t27 = (KEY_OUT_GUSSET_PLATE_MOMENT_DEMAND, KEY_OUT_DISP_GUSSET_PLATE_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_gusset if flag else '', True)
        out_list.append(t27)

        t28 = (KEY_OUT_GUSSET_PLATE_MOMENT, KEY_OUT_DISP_GUSSET_PLATE_MOMENT, TYPE_TEXTBOX,
               self.moment_capacity_gusset if flag else '', True)
        out_list.append(t28)

        t29 = (None, DISP_TITLE_STIFFENER_PLATE, TYPE_TITLE, None, True)
        out_list.append(t29)

        t30 = (KEY_OUT_STIFFENER_PLATE_THICKNNESS, KEY_OUT_DISP_STIFFENER_PLATE_THICKNESS, TYPE_TEXTBOX,
               self.stiffener_plate_thick if flag else '', True)
        out_list.append(t30)

        t31 = (KEY_OUT_STIFFENER_PLATE_SHEAR_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_SHEAR_DEMAND, TYPE_TEXTBOX,
               self.shear_on_stiffener if flag else '', True)
        out_list.append(t31)

        t32 = (KEY_OUT_STIFFENER_PLATE_SHEAR, KEY_OUT_DISP_STIFFENER_PLATE_SHEAR, TYPE_TEXTBOX,
               self.shear_capacity_stiffener if flag else '', True)
        out_list.append(t32)

        t33 = (KEY_OUT_STIFFENER_PLATE_MOMENT_DEMAND, KEY_OUT_DISP_STIFFENER_PLATE_MOMENT_DEMAND, TYPE_TEXTBOX,
               self.moment_on_stiffener if flag else '', True)
        out_list.append(t33)

        t34 = (KEY_OUT_STIFFENER_PLATE_MOMENT, KEY_OUT_DISP_STIFFENER_PLATE_MOMENT, TYPE_TEXTBOX,
               self.moment_capacity_stiffener if flag else '', True)
        out_list.append(t34)

        t18 = (None, DISP_TITLE_WELD, TYPE_TITLE, None, True)
        out_list.append(t18)

        # t19 = (KEY_OUT_WELD_SIZE, KEY_OUT_DISP_WELD_SIZE, TYPE_TEXTBOX,
        #        self.weld_size if flag and self.weld_type != 'Butt Weld' else '')
        # out_list.append(t19)

        t20 = (KEY_OUT_WELD_SIZE_FLANGE, KEY_OUT_DISP_WELD_SIZE_FLANGE, TYPE_TEXTBOX,
               self.weld_size_flange if flag and self.weld_type != 'Butt Weld' else '', True)
        out_list.append(t20)

        t21 = (KEY_OUT_WELD_SIZE_WEB, KEY_OUT_DISP_WELD_SIZE_WEB, TYPE_TEXTBOX,
               self.weld_size_web if flag and self.weld_type != 'Butt Weld' else '', True)
        out_list.append(t21)

        t22 = (KEY_OUT_WELD_SIZE_STIFFENER, KEY_OUT_DISP_WELD_SIZE_STIFFENER, TYPE_TEXTBOX,
               self.weld_size_stiffener if flag and self.weld_type != 'Butt Weld' else '', True)
        out_list.append(t22)

        return out_list

    def major_minor(self):

        conn = self[0]
        if conn in ['Bolted-Slab Base', 'Gusseted Base Plate', 'Hollow Section']:
            return True
        else:
            return False

    def label_end_condition(self):

        conn = self[0]
        if conn in ['Gusseted Base Plate', 'Hollow Section']:
            return 'Fixed'
        else:
            return 'Pinned'

    def out_weld(self):

        conn = self[0]
        if conn == 'Butt Weld':
            return True
        else:
            return False

    def out_anchor_tension(self):

        conn = self[0]
        if conn != 'Gusseted Base Plate':
            return True
        else:
            return False

    def out_detail_projection(self):

        conn = self[0]
        if conn != 'Welded-Slab Base':
            return True
        else:
            return False

    def out_anchor_combined(self):

        conn = self[0]
        if conn != 'Welded-Slab Base':
            return True
        else:
            return False

    def input_value_changed(self):

        lst = []

        t1 = ([KEY_CONN], KEY_MOMENT_MAJOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t1)

        t2 = ([KEY_CONN], KEY_MOMENT_MINOR, TYPE_TEXTBOX, self.major_minor)
        lst.append(t2)

        t3 = ([KEY_CONN], KEY_END_CONDITION, TYPE_NOTE, self.label_end_condition)
        lst.append(t3)

        # t4 = (KEY_WELD_TYPE, KEY_OUT_WELD_SIZE, TYPE_OUT_DOCK, self.out_weld)
        # lst.append(t4)
        #
        # t5 = (KEY_WELD_TYPE, KEY_OUT_WELD_SIZE, TYPE_OUT_LABEL, self.out_weld)
        # lst.append(t5)

        t12 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_FLANGE, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t12)

        t13 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_FLANGE, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t13)

        t14 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_WEB, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t14)

        t15 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_WEB, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t15)

        t16 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_STIFFENER, TYPE_OUT_DOCK, self.out_weld)
        lst.append(t16)

        t17 = ([KEY_WELD_TYPE], KEY_OUT_WELD_SIZE_STIFFENER, TYPE_OUT_LABEL, self.out_weld)
        lst.append(t17)

        t6 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION, TYPE_OUT_DOCK, self.out_anchor_tension)
        lst.append(t6)

        t7 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_TENSION, TYPE_OUT_LABEL, self.out_anchor_tension)
        lst.append(t7)

        t8 = ([KEY_CONN], KEY_OUT_DETAILING_PROJECTION, TYPE_OUT_DOCK, self.out_detail_projection)
        lst.append(t8)

        t9 = ([KEY_CONN], KEY_OUT_DETAILING_PROJECTION, TYPE_OUT_LABEL, self.out_detail_projection)
        lst.append(t9)

        t10 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_COMBINED, TYPE_OUT_DOCK, self.out_anchor_combined)
        lst.append(t10)

        t11 = ([KEY_CONN], KEY_OUT_ANCHOR_BOLT_COMBINED, TYPE_OUT_LABEL, self.out_anchor_combined)
        lst.append(t11)

        return lst

    @staticmethod
    def diam_bolt_customized():
        c = connectdb2()
        return c

    @staticmethod
    def grdval_customized():
        b = VALUES_GRD_CUSTOMIZED
        return b

    def customized_input(self):

        list1 = []
        t1 = (KEY_DIA_ANCHOR, self.diam_bolt_customized)
        list1.append(t1)
        t2 = (KEY_GRD_ANCHOR, self.grdval_customized)
        list1.append(t2)

        return list1

    def func_for_validation(self, design_dictionary):
        all_errors = []
        self.design_status = False
        flag = False
        option_list = self.input_values(self)
        missing_fields_list = []
        if design_dictionary[KEY_CONN] == 'Welded-Slab Base':
            design_dictionary[KEY_MOMENT_MAJOR] = 'Disabled'
            design_dictionary[KEY_MOMENT_MINOR] = 'Disabled'
        for option in option_list:
            if option[2] == TYPE_TEXTBOX:
                if design_dictionary[option[0]] == '':
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX and option[0] != KEY_CONN:
                val = option[4]
                if design_dictionary[option[0]] == val[0]:
                    missing_fields_list.append(option[1])
            elif option[2] == TYPE_COMBOBOX_CUSTOMIZED:
                if design_dictionary[option[0]] == []:
                    missing_fields_list.append(option[1])

        if len(missing_fields_list) > 0:
            error = self.generate_missing_fields_error_string(self,missing_fields_list)
            all_errors.append(error)
            # flag = False
        else:
            flag = True

        if flag:
            print(design_dictionary)

            # self.set_input_values(self, design_dictionary)
            self.bp_parameters(self, design_dictionary)
        else:
            return all_errors

    def input_dictionary_design_pref(self):

        design_input = []
        t1 = (KEY_DISP_COLSEC, TYPE_COMBOBOX, ['Label_8', KEY_SEC_MATERIAL])
        design_input.append(t1)

        t1 = (KEY_DISP_COLSEC, TYPE_TEXTBOX, [KEY_SEC_FU, KEY_SEC_FY, 'Label_21'])
        design_input.append(t1)

        t2 = ("Base Plate", TYPE_COMBOBOX, [KEY_BASE_PLATE_MATERIAL])
        design_input.append(t2)

        t2 = ("Base Plate", TYPE_TEXTBOX, [KEY_BASE_PLATE_FU, KEY_BASE_PLATE_FY])
        design_input.append(t2)

        t3 = ("Anchor Bolt", TYPE_TEXTBOX,
              [KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DP_ANCHOR_BOLT_DESIGNATION, KEY_DP_ANCHOR_BOLT_MATERIAL_G_O,
               KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DP_ANCHOR_BOLT_TYPE])
        design_input.append(t3)

        t3 = ("Anchor Bolt", TYPE_COMBOBOX, [KEY_DP_ANCHOR_BOLT_HOLE_TYPE])
        design_input.append(t3)

        t4 = ("Weld", TYPE_COMBOBOX, [KEY_DP_WELD_FAB])
        design_input.append(t4)

        t4 = ("Weld", TYPE_TEXTBOX, [KEY_DP_WELD_MATERIAL_G_O])
        design_input.append(t4)

        t5 = ("Detailing", TYPE_COMBOBOX, [KEY_DP_DETAILING_EDGE_TYPE, KEY_DP_DETAILING_CORROSIVE_INFLUENCES])
        design_input.append(t5)

        t6 = ("Design", TYPE_COMBOBOX, [KEY_DP_DESIGN_METHOD, KEY_DP_DESIGN_BASE_PLATE])
        design_input.append(t6)

        return design_input

    def input_dictionary_without_design_pref(self):

        design_input = []
        t1 = (KEY_MATERIAL, [KEY_SEC_MATERIAL, KEY_BASE_PLATE_MATERIAL], 'Input Dock')
        design_input.append(t1)

        t2 = (KEY_TYP_ANCHOR, [KEY_DP_ANCHOR_BOLT_TYPE], 'Input Dock')
        design_input.append(t2)

        t3 = (None, ['Label_8', 'Label_21', KEY_SEC_FU, KEY_BASE_PLATE_FU,
                     KEY_DP_ANCHOR_BOLT_MATERIAL_G_O, KEY_SEC_FY, KEY_BASE_PLATE_FY,
                     KEY_DP_ANCHOR_BOLT_DESIGNATION, KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DP_ANCHOR_BOLT_HOLE_TYPE,
                     KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DP_WELD_FAB, KEY_DP_WELD_MATERIAL_G_O, KEY_DP_DETAILING_EDGE_TYPE,
                     KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DP_DESIGN_METHOD, KEY_DP_DESIGN_BASE_PLATE], '')
        design_input.append(t3)

        return design_input

    def get_values_for_design_pref(self, key, design_dictionary):

        section = Column(design_dictionary[KEY_SECSIZE], design_dictionary[KEY_SEC_MATERIAL])
        length = str(self.anchor_length_provided if self.design_button_status else 0)
        fu = Material(design_dictionary[KEY_MATERIAL]).fu

        val = {'Label_8': "Rolled",
               'Label_21': str(section.source),
               KEY_SEC_FU: str(section.fu),
               KEY_BASE_PLATE_FU: str(section.fu),
               KEY_DP_ANCHOR_BOLT_MATERIAL_G_O: str(section.fu),
               KEY_SEC_FY: str(section.fy),
               KEY_BASE_PLATE_FY: str(section.fy),
               KEY_DP_ANCHOR_BOLT_DESIGNATION:
                   str(str(design_dictionary[KEY_DIA_ANCHOR][0]) + "X" + length + " IS5624 GALV"),
               KEY_DP_ANCHOR_BOLT_LENGTH: str(length),
               KEY_DP_ANCHOR_BOLT_HOLE_TYPE: "Standard",
               KEY_DP_ANCHOR_BOLT_FRICTION: str(0.30),
               KEY_DP_WELD_FAB: KEY_DP_WELD_FAB_SHOP,
               KEY_DP_WELD_MATERIAL_G_O: str(fu),
               KEY_DP_DETAILING_EDGE_TYPE: "a - Sheared or hand flame cut",
               KEY_DP_DETAILING_CORROSIVE_INFLUENCES: "No",
               KEY_DP_DESIGN_METHOD: "Limit State Design",
               KEY_DP_DESIGN_BASE_PLATE: "Effective Area Method"
               }[key]

        return val

    def refresh_input_dock(self):

        add_buttons = []

        t1 = (KEY_DISP_COLSEC, KEY_SECSIZE, TYPE_COMBOBOX, KEY_SECSIZE, None, None, "Columns")
        add_buttons.append(t1)

        return add_buttons

    def edit_tabs(self):
        return []

    def tab_value_changed(self):

        change_tab = []

        t1 = (KEY_DISP_COLSEC, [KEY_SEC_MATERIAL], [KEY_SEC_FU, KEY_SEC_FY], TYPE_TEXTBOX,
              self.get_fu_fy_I_section)
        change_tab.append(t1)

        t2 = ("Base Plate", [KEY_BASE_PLATE_MATERIAL], [KEY_BASE_PLATE_FU, KEY_BASE_PLATE_FY], TYPE_TEXTBOX,
              self.get_fu_fy)

        t3 = ("Anchor Bolt", [KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DP_ANCHOR_BOLT_GALVANIZED],
              [KEY_DP_ANCHOR_BOLT_DESIGNATION], TYPE_TEXTBOX, self.anchor_bolt_designation)
        change_tab.append(t3)

        change_tab.append(t2)

        return change_tab

    def anchor_bolt_designation(self):

        length = str(self[0])
        galvanized = str(self[1])
        input_dictionary = self[2]
        if not input_dictionary:
            d = ''
        else:
            d = input_dictionary[KEY_DIA_ANCHOR][0]
        new_des = str(d)+'X'

        if galvanized == 'Yes':
            new_des = str(new_des)+str(length)+' IS5624 '+'GALV'
        elif galvanized == 'No':
            new_des = str(new_des)+str(length)+' IS5624'
        else:
            new_des = ''

        d = {KEY_DP_ANCHOR_BOLT_DESIGNATION: str(new_des)}
        return d

    def list_for_fu_fy_validation(self):

        fu_fy_list = []

        t1 = (KEY_SEC_MATERIAL, KEY_SEC_FU, KEY_SEC_FY)
        fu_fy_list.append(t1)

        t2 = (KEY_BASE_PLATE_MATERIAL, KEY_BASE_PLATE_FU, KEY_BASE_PLATE_FY)
        fu_fy_list.append(t2)

        return fu_fy_list

    def tab_list(self):

        self.design_button_status = False

        tabs = []

        t0 = (KEY_DISP_COLSEC, TYPE_TAB_1, self.tab_section)
        tabs.append(t0)

        t5 = ("Base Plate", TYPE_TAB_2, self.tab_bp)
        tabs.append(t5)

        t1 = ("Anchor Bolt", TYPE_TAB_2, self.anchor_bolt_values)
        tabs.append(t1)

        t2 = ("Weld", TYPE_TAB_2, self.weld_values)
        tabs.append(t2)

        t3 = ("Detailing", TYPE_TAB_2, self.detailing_values)
        tabs.append(t3)

        t4 = ("Design", TYPE_TAB_2, self.design_values)
        tabs.append(t4)

        # t5 = ("Connector", TYPE_TAB_2, self.connector_values)
        # tabs.append(t5)

        return tabs

    def anchor_bolt_values(self, input_dictionary):

        self.input_dictionary = input_dictionary
        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_SECSIZE], input_dictionary[KEY_MATERIAL]]:
            length = ''
            designation = ''
            anchor_type = ''
            fu = ''
        else:
            length = str(self.anchor_length_provided if self.design_button_status else 0)
            designation = str(input_dictionary[KEY_DIA_ANCHOR][0]) + "X" + length + " IS5624 GALV"
            anchor_type = input_dictionary[KEY_TYP_ANCHOR]
            fu = Material(input_dictionary[KEY_MATERIAL]).fu

        anchor_bolt = []

        t1 = (KEY_DP_ANCHOR_BOLT_DESIGNATION, KEY_DISP_DESIGNATION, TYPE_TEXTBOX, None, str(designation))
        anchor_bolt.append(t1)

        t2 = (KEY_DP_ANCHOR_BOLT_TYPE, KEY_DISP_DP_ANCHOR_BOLT_TYPE, TYPE_TEXTBOX, None, str(anchor_type))
        anchor_bolt.append(t2)

        t3 = (KEY_DP_ANCHOR_BOLT_GALVANIZED, KEY_DISP_DP_ANCHOR_BOLT_GALVANIZED, TYPE_COMBOBOX, ['Yes', 'No'], 'Yes')
        anchor_bolt.append(t3)

        t4 = (KEY_DP_ANCHOR_BOLT_HOLE_TYPE, KEY_DISP_DP_ANCHOR_BOLT_HOLE_TYPE, TYPE_COMBOBOX,
              ['Standard', 'Over-sized'], 'Standard')
        anchor_bolt.append(t4)

        t5 = (KEY_DP_ANCHOR_BOLT_LENGTH, KEY_DISP_DP_ANCHOR_BOLT_LENGTH, TYPE_TEXTBOX, None, length)
        anchor_bolt.append(t5)

        t6 = (KEY_DP_ANCHOR_BOLT_MATERIAL_G_O, KEY_DISP_DP_ANCHOR_BOLT_MATERIAL_G_O, TYPE_TEXTBOX, None, str(fu))
        anchor_bolt.append(t6)

        t7 = (KEY_DP_ANCHOR_BOLT_FRICTION, KEY_DISP_DP_ANCHOR_BOLT_FRICTION, TYPE_TEXTBOX, None, str(0.30))
        anchor_bolt.append(t7)

        return anchor_bolt

    def tab_bp(self, input_dictionary):

        if not input_dictionary or 'Select Section' in [input_dictionary[KEY_MATERIAL]]:
            material_grade = ''
            fu = ''
            fy = ''
        else:
            material_grade = input_dictionary[KEY_MATERIAL]
            material_attributes = Material(material_grade)
            fu = material_attributes.fu
            fy = material_attributes.fy

        tab_bp = []
        material = connectdb("Material", call_type="popup")
        t1 = (KEY_BASE_PLATE_MATERIAL, KEY_DISP_BASE_PLATE_MATERIAL, TYPE_COMBOBOX, material, material_grade)
        tab_bp.append(t1)

        t2 = (KEY_BASE_PLATE_FU, KEY_DISP_BASE_PLATE_FU, TYPE_TEXTBOX, None, fu)
        tab_bp.append(t2)

        t3 = (KEY_BASE_PLATE_FY, KEY_DSIP_BASE_PLATE_FY, TYPE_TEXTBOX, None, fy)
        tab_bp.append(t3)

        return tab_bp

    def detailing_values(self, input_dictionary):

        detailing = []

        t1 = (KEY_DP_DETAILING_EDGE_TYPE, KEY_DISP_DP_DETAILING_EDGE_TYPE, TYPE_COMBOBOX, [
            'a - Sheared or hand flame cut', 'b - Rolled, machine-flame cut, sawn and planed'],
              'a - Sheared or hand flame cut')
        detailing.append(t1)

        t3 = (KEY_DP_DETAILING_CORROSIVE_INFLUENCES, KEY_DISP_DP_DETAILING_CORROSIVE_INFLUENCES, TYPE_COMBOBOX,
              ['No', 'Yes'], 'No')
        detailing.append(t3)

        t4 = ("textBrowser", "", TYPE_TEXT_BROWSER, DETAILING_DESCRIPTION)
        detailing.append(t4)

        return detailing

    def design_values(self, input_dictionary):

        design = []

        t1 = (KEY_DP_DESIGN_METHOD, KEY_DISP_DP_DESIGN_METHOD, TYPE_COMBOBOX, [
            'Limit State Design', 'Limit State (Capacity based) Design', 'Working Stress Design'],
              'Limit State Design')
        design.append(t1)

        t2 = (KEY_DP_DESIGN_BASE_PLATE, KEY_DISP_DP_DESIGN_BASE_PLATE, TYPE_COMBOBOX, ['Effective Area Method'],
              'Effective Area Method')
        design.append(t2)

        return design

    def get_3d_components(self):
        components = []

        t1 = ('Model', self.call_3DModel)
        components.append(t1)

        t3 = ('Column', self.call_3DColumn)
        components.append(t3)

        t4 = ('Base Plate', self.call_3DPlate)
        components.append(t4)

        return components

    def call_3DPlate(self, ui, bgcolor):
        from PyQt5.QtWidgets import QCheckBox
        from PyQt5.QtCore import Qt
        for chkbox in ui.frame.children():
            if chkbox.objectName() == 'Base Plate':
                continue
            if isinstance(chkbox, QCheckBox):
                chkbox.setChecked(Qt.Unchecked)
        ui.commLogicObj.display_3DModel("Connector", bgcolor)


    # def dia_to_len(self, d):
    #
    #     ob = IS_5624_1993()
    #     l = ob.table1(d)
    #     return l

    # Start of calculation

    def bp_parameters(self, design_dictionary):
        """ Initialize variables to use in calculation from input dock and design preference UI.

        Args: design dictionary based on the user inputs from the GUI

        Returns: None
        """
        # attributes of input dock
        self.mainmodule = "Moment Connection"
        self.connectivity = str(design_dictionary[KEY_CONN])
        self.end_condition = str(design_dictionary[KEY_END_CONDITION])
        self.column_section = str(design_dictionary[KEY_SECSIZE])
        self.material = str(design_dictionary[KEY_MATERIAL])

        self.load_axial = float(design_dictionary[KEY_AXIAL])
        self.load_axial = self.load_axial * 10 ** 3  # N

        self.load_shear = float(design_dictionary[KEY_SHEAR])
        self.load_shear = self.load_shear * 10 ** 3  # N

        self.load_moment_major = float(design_dictionary[KEY_MOMENT_MAJOR] if design_dictionary[KEY_MOMENT_MAJOR] != 'Disabled' else 0)
        self.load_moment_major = self.load_moment_major * 10 ** 6  # N-mm

        self.load_moment_minor = float(design_dictionary[KEY_MOMENT_MINOR] if design_dictionary[KEY_MOMENT_MINOR] != 'Disabled' else 0)
        self.load_moment_minor = self.load_moment_minor * 10 ** 6  # N-mm

        self.anchor_dia = design_dictionary[KEY_DIA_ANCHOR]
        self.anchor_type = str(design_dictionary[KEY_TYP_ANCHOR])
        self.anchor_grade = design_dictionary[KEY_GRD_ANCHOR]

        self.footing_grade = str(design_dictionary[KEY_GRD_FOOTING])

        self.weld_type = str(design_dictionary[KEY_WELD_TYPE])

        # attributes of design preferences
        self.dp_column_designation = str(design_dictionary[KEY_SECSIZE])
        self.dp_column_type = str(design_dictionary['Label_8'])
        self.dp_column_source = str(design_dictionary['Label_21'])
        self.dp_column_material = str(design_dictionary[KEY_SEC_MATERIAL])
        self.dp_column_fu = float(design_dictionary[KEY_SEC_FU])
        self.dp_column_fy = float(design_dictionary[KEY_SEC_FY])

        self.dp_bp_material = str(design_dictionary[KEY_BASE_PLATE_MATERIAL])
        self.dp_bp_fu = float(design_dictionary[KEY_BASE_PLATE_FU])
        self.dp_bp_fy = float(design_dictionary[KEY_BASE_PLATE_FY])

        self.dp_anchor_designation = str(design_dictionary[KEY_DP_ANCHOR_BOLT_DESIGNATION])
        self.dp_anchor_type = str(design_dictionary[KEY_DP_ANCHOR_BOLT_TYPE])
        self.dp_anchor_hole = str(design_dictionary[KEY_DP_ANCHOR_BOLT_HOLE_TYPE])
        self.dp_anchor_length = int(design_dictionary[KEY_DP_ANCHOR_BOLT_LENGTH])
        self.dp_anchor_fu_overwrite = float(design_dictionary[KEY_DP_ANCHOR_BOLT_MATERIAL_G_O])
        self.dp_anchor_friction = float(design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] if
                                        design_dictionary[KEY_DP_ANCHOR_BOLT_FRICTION] != "" else 0.30)

        self.dp_weld_fab = str(design_dictionary[KEY_DP_WELD_FAB])
        self.dp_weld_fu_overwrite = float(design_dictionary[KEY_DP_WELD_MATERIAL_G_O])

        self.dp_detail_edge_type = str(design_dictionary[KEY_DP_DETAILING_EDGE_TYPE])
        self.dp_detail_is_corrosive = str(design_dictionary[KEY_DP_DETAILING_CORROSIVE_INFLUENCES])

        self.dp_design_method = str(design_dictionary[KEY_DP_DESIGN_METHOD])
        self.dp_bp_method = str(design_dictionary[KEY_DP_DESIGN_BASE_PLATE])

        # properties of the column section

        self.column_properties = Column(designation=self.dp_column_designation, material_grade=self.dp_column_material)
        self.column_D = self.column_properties.depth
        self.column_bf = self.column_properties.flange_width
        self.column_tf = self.column_properties.flange_thickness
        self.column_tw = self.column_properties.web_thickness
        self.column_r1 = self.column_properties.root_radius
        self.column_r2 = self.column_properties.toe_radius

        # other attributes
        self.gamma_m0 = self.cl_5_4_1_Table_5["gamma_m0"]["yielding"]  # gamma_mo = 1.10
        self.gamma_m1 = self.cl_5_4_1_Table_5["gamma_m1"]["ultimate_stress"]  # gamma_m1 = 1.25
        self.gamma_mb = self.cl_5_4_1_Table_5["gamma_mb"][self.dp_weld_fab]  # gamma_mb = 1.25
        self.gamma_mw = self.cl_5_4_1_Table_5["gamma_mw"][self.dp_weld_fab]  # gamma_mw = 1.25 for 'Shop Weld' and 1.50 for 'Field Weld'
        self.safe = True

        self.bp_analyses_parameters(self)
        self.bp_analyses(self)
        self.anchor_bolt_design(self)
        self.design_weld(self)
        self.design_gusset_plate(self)

    def bp_analyses_parameters(self):
        """ initialize detailing parameters like the end/edge/pitch/gauge distances, anchor bolt diameter and grade,
         length and width of the base plate.
        These parameters are used to run the first iteration of the analyses and improvise accordingly.

        Args:

        Returns:
        """
        # select anchor bolt diameter [Reference: based on design experience, field conditions  and sample calculations]
        # the following list of diameters are neglected due its practical non acceptance/unavailability - 'M8', 'M10', 'M12', 'M16'
        # M20 and M24 are the preferred choices for the design

        self.anchor_dia = self.anchor_dia + ['M20', 'M24']  # adding M20 and M24 diameters if the list passed does not include them
        sort_bolt = filter(lambda x: 'M20' <= x <= self.anchor_dia[-1], self.anchor_dia)

        for i in sort_bolt:
            self.anchor_bolt = i  # anchor dia provided (str)
            break

        self.anchor_dia_provided = self.table1(self.anchor_bolt)[0]  # mm anchor dia provided (int)
        self.anchor_area = self.bolt_area(self.anchor_dia_provided)  # list of areas [shank area, thread area] mm^2

        # hole diameter
        self.anchor_hole_dia = self.cl_10_2_1_bolt_hole_size(self.anchor_dia_provided, self.dp_anchor_hole)  # mm

        # assign anchor grade from the selected list
        # trying the design with the highest selected grade
        self.anchor_grade = list(reversed(self.anchor_grade))
        for i in self.anchor_grade:
            self.anchor_grade = i
            break

        self.anchor_fu_fy = self.get_bolt_fu_fy(self.anchor_grade)  # returns a list with strength values - [bolt_fu, bolt_fy]

        # TODO add condition for number of anchor bolts depending on col depth and force
        # number of anchor bolts
        self.anchor_nos_provided = 4

        # perform detailing checks
        # Note: end distance is along the depth, whereas, the edge distance is along the flange, of the column section

        # end distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
        self.end_distance = self.cl_10_2_4_2_min_edge_end_dist(self.anchor_dia_provided, self.dp_anchor_hole, self.dp_detail_edge_type)
        self.end_distance = round_up(self.end_distance, 5) + 15  # mm, adding 15 mm extra

        # TODO: add max end, edge distance check after the plate thk check
        # self.end_distance_max = self.cl_10_2_4_3_max_edge_dist([self.plate_thk], self.dp_bp_fy, self.dp_detail_is_corrosive)

        # edge distance [Reference: Clause 10.2.4.2 and 10.2.4.3, IS 800:2007]
        self.edge_distance = self.end_distance  # mm
        # self.edge_distance_max = self.end_distance_max

        # pitch and gauge distance [Reference: Clause 10.2.2 and 10.2.3.1, IS 800:2007]
        # TODO add pitch and gauge calc for bolts more than 4 nos
        if self.anchor_nos_provided == 4:
            self.pitch_distance = 0.0
            self.gauge_distance = self.pitch_distance
        else:
            pass

        # minimum required dimensions of the base plate [as per the detailing criteria]
        # considering clearance equal to 1.5 times the edge distance (on each side) along the width of the base plate
        if self.connectivity == 'Welded-Slab Base' or 'Gusseted Base Plate':
            self.bp_length_min = round_up(self.column_D + 2 * (2 * self.end_distance), 5)  # mm
            self.bp_width_min = round_up(self.column_bf + 1.5 * self.edge_distance + 1.5 * self.edge_distance, 5)  # mm

        elif self.connectivity == 'Bolted-Slab Base':
            pass
        else:
            pass

    def bp_analyses(self):
        """ perform analyses of the base plate

        Args:

        Returns:

        # TODO: Write algorithm here
        """
        # bearing strength of concrete [Reference: Clause 7.4.1, IS 800:2007]
        self.bearing_strength_concrete = self.cl_7_4_1_bearing_strength_concrete(self.footing_grade)  # N/mm^2 or MPa

        # slab base analyses (pinned connection)
        if self.connectivity == 'Welded-Slab Base':

            # minimum required area for the base plate [bearing stress = axial force / area of the base]
            self.min_area_req = self.load_axial / self.bearing_strength_concrete  # mm^2

            # calculate projection by the 'Effective Area Method' [Reference: Clause 7.4.1.1, IS 800:2007]
            # the calculated projection is added by half times the hole dia on each side to avoid stress concentration near holes
            if self.dp_column_type == 'Rolled' or 'Welded':
                print('proioooooooooooo')

                self.projection = self.calculate_c(self.column_bf, self.column_D, self.column_tw, self.column_tf, self.min_area_req,
                                                   self.anchor_hole_dia)  # mm
                print('fdddddddddddddd', self.projection)
                self.projection = max(self.projection, self.end_distance)  # projection should at-least be equal to the end distance
            else:
                pass
            if self.projection <= 0:
                self.safe = False
                logger.error(": [Analysis Error] The value of the projection (c) as per the Effective Area Method is {} mm. [Reference:"
                             " Clause 7.4.1.1, IS 800: 2007]".format(self.projection))
                logger.warning(": [Analysis Error] The computed value of the projection is not suitable for performing the design.")
                logger.info(": [Analysis Error] Check the column section and its properties.")
                logger.info(": Re-design the connection")
            else:
                pass

            self.bp_length_provided = self.column_D + 2 * self.projection + 2 * self.end_distance  # mm
            self.bp_width_provided = self.column_bf + 2 * self.projection + 2 * self.end_distance  # mm

            # check for the provided area against the minimum required area
            self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2

            # checking if the provided dimensions (length and width) are sufficient
            bp_dimensions = [self.bp_length_provided, self.bp_width_provided]

            n = 1
            while self.bp_area_provided < self.min_area_req:
                bp_update_dimensions = [bp_dimensions[-2], [-1]]

                for i in bp_update_dimensions:
                    i += 25
                    bp_dimensions.append(i)
                    i += 1

                self.bp_area_provided = bp_dimensions[-2] * bp_dimensions[-1]  # mm^2, area according to the desired length and width
                n += 1

            self.bp_length_provided = bp_dimensions[-2]  # mm, updated length if while loop is True
            self.bp_width_provided = bp_dimensions[-1]  # mm, updated width if while loop is True
            self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2, update area if while loop is True

            # actual bearing pressure acting on the provided area of the base plate
            self.w = self.load_axial / self.bp_area_provided  # N/mm^2 (MPa)

            # design of plate thickness
            # thickness of the base plate [Reference: Clause 7.4.3.1, IS 800:2007]
            self.plate_thk = self.projection * (math.sqrt((2.5 * self.w * self.gamma_m0) / self.dp_bp_fy))  # mm

        elif self.connectivity == 'Gusseted Base Plate':

            self.eccentricity_zz = self.load_moment_major / self.load_axial  # mm, eccentricity about major (z-z) axis

            # Defining cases: Case 1: e <= L/6        (compression throughout the BP)
            #                 Case 2: L/6 < e < L/3   (compression throughout + moderate tension/uplift in the anchor bolts)
            #                 Case 3: e >= L/3        (compression + high tension/uplift in the anchor bolts)

            if self.eccentricity_zz <= self.bp_length_min / 6:  # Case 1

                self.gusseted_bp_case = 'Case1'

                # fixing length and width of the base plate
                width_min = 2 * self.load_axial / (self.bp_length_min * self.bearing_strength_concrete)  # mm
                if width_min < self.bp_width_min:
                    width_min = self.bp_width_min
                else:
                    pass

                self.bp_length_provided = max(self.bp_length_min, width_min)  # mm, assigning maximum dimension to length
                self.bp_width_provided = min(self.bp_length_min, width_min)  # mm, assigning minimum dimension to width
                self.bp_area_provided = self.bp_length_provided * self.bp_width_provided  # mm^2

                # calculating the maximum and minimum bending stresses
                self.ze_zz = self.bp_width_provided * self.bp_length_provided ** 2 / 6  # mm^3, elastic section modulus of plate (BL^2/6)

                self.sigma_max_zz = (self.load_axial / self.bp_area_provided) + (self.load_moment_major / self.ze_zz)  # N/mm^2
                self.sigma_min_zz = (self.load_axial / self.bp_area_provided) - (self.load_moment_major / self.ze_zz)  # N/mm^2

                # calculating moment at the critical section

                # Assumption: the critical section (critical_xx) acts at a distance of 0.95 times the column depth, along the depth
                self.critical_xx = (self.bp_length_provided - 0.95 * self.column_D) / 2  # mm
                self.sigma_xx = (self.sigma_max_zz - self.sigma_min_zz) * (self.bp_length_provided - self.critical_xx) / \
                                self.bp_length_provided
                self.sigma_xx = self.sigma_xx + self.sigma_min_zz  # N/mm^2, bending stress at the critical section

                self.critical_M_xx = (self.sigma_xx * self.critical_xx ** 2 / 2) + \
                                     (0.5 * self.critical_xx * (self.sigma_max_zz - self.sigma_xx) * (2 / 3) * self.critical_xx)
                # N-mm, bending moment at critical section

                # equating critical moment with critical moment to compute the required minimum plate thickness
                # Assumption: The bending capacity of the plate is (M_d = 1.5*fy*Z_e/gamma_m0) [Reference: Clause 8.2.1.2, IS 800:2007]
                # Assumption: Z_e of the plate is = b*tp^2 / 6, where b = 1 for a cantilever strip of unit dimension

                self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.dp_bp_fy))  # mm

                self.tension_capacity_anchor = 0

            else:  # Case 2 and Case 3
                self.gusseted_bp_case = 'Case2&3'

                # fixing length and width of the base plate
                self.bp_length_provided = self.bp_length_min
                self.bp_width_provided = self.bp_width_min

                # calculating the distance (y) which lies under compression
                # Reference: Omer Blodgett, Column Bases, section 3.3, equation 13

                self.n = 2 * 10 ** 5 / (5000 * math.sqrt(self.cl_7_4_1_bearing_strength_concrete(self.footing_grade) / 0.45))
                self.anchor_area_tension = self.anchor_area[0] * (self.anchor_nos_provided / 2)  # mm^2, area of anchor under tension
                self.f = (self.bp_length_provided / 2) - self.end_distance  # mm

                k1 = 3 * (self.eccentricity_zz - self.bp_length_provided / 2)
                k2 = (6 * self.n * self.anchor_area_tension / self.bp_width_provided) * (self.f + self.eccentricity_zz)
                k3 = (self.bp_length_provided / 2 + self.f) * -k2

                # equation for finding 'y' is: y^3 + k1*y^2 + k2*y + k3 = 0
                roots = np.roots([1, k1, k2, k3])  # finding roots of the equation
                r_1 = roots[0]
                r_2 = roots[1]
                r_3 = roots[2]
                r = max(r_1, r_2, r_3)
                r = r.real  # separating the imaginary part

                self.y = round(r, 3)  # mm

                # finding maximum tension in the bolts for maximum permissible bearing stress (0.45*f_ck)
                self.tension_demand_anchor = ((self.bearing_strength_concrete * self.anchor_area_tension * self.n) / self.y) * \
                                             ((self.bp_length_provided / 2) + self.f - self.y)  # N
                self.tension_demand_anchor = round(self.tension_demand_anchor / 1000, 2)  # kN

                self.tension_capacity_anchor = self.cl_10_3_5_bearing_bolt_tension_resistance(self.anchor_fu_fy[0], self.anchor_fu_fy[1],
                                                                                              self.anchor_area[0], self.anchor_area[1],
                                                                                              safety_factor_parameter=self.dp_weld_fab)  # N
                self.tension_capacity_anchor = round(self.tension_capacity_anchor / 1000, 2)  # kN

                # design number of anchor bolts required to resist tension
                # Assumption: The minimum number of anchor bolts is 2, for stability purpose
                self.tension_bolts_req = max(self.tension_demand_anchor / self.tension_capacity_anchor, 2)

                if self.tension_bolts_req > 3:
                    self.safe = False
                    # TODO: Add log messages or update the design with more bolts
                else:
                    pass

                # computing the actual bending stress at the compression side
                # TODO: complete this check
                # self.flange_force_axial = self.dp_bp_fy * (self.column_bf * self.column_tf)  # N, load transferred by the flange
                # self.flange_force_moment = self.load_moment_major / (self.column_D - self.column_tf)  # N, tension acting at the flange
                # self.bp_area_compression = self.y * self.bp_width_provided  # mm^2, area of the base plate under compression

                # designing the plate thickness

                # finding the length of the critical section from the edge of the base plate
                self.critical_xx = (self.bp_length_provided - 0.95 * self.column_D) / 2  # mm
                if self.y > self.critical_xx:
                    self.critical_xx = self.critical_xx
                else:
                    self.critical_xx = self.y

                # moment acting at the critical section due to applied loads
                # Assumption: The moment acting at the critical section is taken as 0.45*f_ck*B*critical_xx (plastic moment)
                self.critical_M_xx = (self.critical_xx * self.bearing_strength_concrete * self.bp_width_provided) * \
                                     (self.critical_xx / 2)  # N-mm

                # equating critical moment with critical moment to compute the required minimum plate thickness
                # Assumption: The bending capacity of the plate is (M_d = 1.5*fy*Z_e/gamma_m0) [Reference: Clause 8.2.1.2, IS 800:2007]
                # Assumption: Z_e of the plate is = b*tp^2 / 6, where b = 1 for a cantilever strip of unit dimension

                self.plate_thk = math.sqrt((self.critical_M_xx * self.gamma_m0 * 6) / (1.5 * self.dp_bp_fy * self.bp_width_provided))  # mm

        elif self.connectivity == "Bolted-Slab Base":
            pass
        elif self.connectivity == "Hollow Section":
            pass

        # assign appropriate plate thickness

        self.plate_thk = max(self.plate_thk, self.column_tf)  # base plate thickness should be larger than the flange thickness

        # assigning plate thickness according to the available standard sizes
        # the thicknesses of the flats (in mm) listed below is obtained from SAIL's product brochure
        standard_plate_thk = [8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 75, 80, 90, 100, 110, 120]

        sort_plate = filter(lambda x: self.plate_thk <= x <= 120, standard_plate_thk)

        for i in sort_plate:
            self.plate_thk = i  # plate thickness provided (mm)
            break

    def anchor_bolt_design(self):
        """ Perform design checks for the anchor bolt

        Args:

        Returns:
        """
        # design strength of the anchor bolt [Reference: Clause 10.3.2, IS 800:2007; Section 3, IS 5624:1993]
        # Assumption: number of shear planes passing through - the thread is 1 (n_n) and through the shank is 0 (n_s)

        self.shear_capacity_anchor = self.cl_10_3_3_bolt_shear_capacity(self.dp_anchor_fu_overwrite, self.anchor_area[1],
                                                                        self.anchor_area[0], 1, 0, self.dp_weld_fab)
        self.shear_capacity_anchor = round(self.shear_capacity_anchor / 1000, 2)  # kN

        self.bearing_capacity_anchor = self.cl_10_3_4_bolt_bearing_capacity(self.dp_bp_fu, self.dp_anchor_fu_overwrite, self.plate_thk,
                                                                            self.anchor_dia_provided, self.end_distance,
                                                                            self.pitch_distance, self.dp_anchor_hole, self.dp_weld_fab)
        self.bearing_capacity_anchor = round(self.bearing_capacity_anchor / 1000, 2)  # kN

        self.anchor_capacity = min(self.shear_capacity_anchor, self.bearing_capacity_anchor)  # kN

        # information message to the user
        if self.load_shear > 0:
            logger.info(": [Anchor Bolt] The anchor bolt is not designed to resist any shear force")
        else:
            pass

        # combined shear + tension capacity check of the anchor bolts subjected to tension
        # Assumption: Although the anchor bolt does not carry any shear force, this check is made to ensure its serviceability
        # The anchor bolts under tension might be subjected to shear forces (accidentally) due to incorrect erection practice

        if self.connectivity == 'Gusseted Base Plate':

            if self.eccentricity_zz <= self.bp_length_min / 6:
                self.combined_capacity_anchor = 0

            else:
                v_sb = self.load_shear * 10 ** -3 / self.anchor_nos_provided  # kN
                v_db = self.anchor_capacity  # kN
                t_b = self.tension_demand_anchor / self.tension_bolts_req  # kN
                t_db = self.tension_capacity_anchor  # kN
                self.combined_capacity_anchor = self.cl_10_3_6_bearing_bolt_combined_shear_and_tension(v_sb, v_db, t_b, t_db)
                self.combined_capacity_anchor = round(self.combined_capacity_anchor, 3)

                if self.combined_capacity_anchor > 1.0:
                    self.safe = False
                    logger.error(": [Large Shear Force] The shear force acting on the base plate is large.")
                    logger.info(": [Large Shear Force] Provide shear key to safely transfer the shear force.")
                    logger.error(": [Anchor Bolt] The anchor bolt fails due to combined shear + tension [Reference: Clause 10.3.6, "
                                 "IS 800:2007].")
                else:
                    pass

        else:
            self.combined_capacity_anchor = 0

        if self.safe:
            pass
        else:
            logger.error(": [Anchor Bolt] Unexpected failure occurred.")
            logger.error(": [Anchor Bolt] Cannot compute capacity checks for the anchor bolt.")
            logger.info(": [Anchor Bolt] Check the input values and re-design the connection.")

        # validation of anchor bolt length [Reference: IS 5624:1993, Table 1]
        self.anchor_length_min = self.table1(self.anchor_bolt)[1]
        self.anchor_length_max = self.table1(self.anchor_bolt)[2]

        # design of anchor length [Reference: Design of Steel Structures by N. Subramanian 2nd. edition 2018, Example 15.5]
        if self.connectivity == 'Welded-Slab Base':
            self.anchor_length_provided = self.anchor_length_min  # mm

        # Equation: T_b = k * sqrt(fck) * (anchor_length_req)^1.5
        elif self.connectivity == 'Gusseted Base Plate':

            if self.eccentricity_zz <= self.bp_length_min / 6:
                self.anchor_length_provided = self.anchor_length_min  # mm

            else:
                # length of anchor for cast-in situ anchor bolts (k = 15.5)
                self.anchor_length_provided = (self.tension_capacity_anchor * 1000 /
                                               (15.5 * math.sqrt(self.bearing_strength_concrete / 0.45))) ** (1 / 1.5)  # mm
                self.anchor_length_provided = max(self.anchor_length_provided, self.anchor_length_min)

            logger.info(": [Anchor Bolt Length] The length of the anchor bolt is computed assuming the anchor bolt is casted in-situ"
                        " during the erection of the column.")

        elif self.connectivity == 'Bolted-Slab Base':
            pass
        elif self.connectivity == 'Hollow Section':
            pass

        # calling value of the anchor length from user from design preferences
        if self.dp_anchor_length == 0:
            self.anchor_length_provided = self.anchor_length_provided  # mm
        else:
            self.anchor_length_provided = self.dp_anchor_length

        if self.anchor_length_provided < self.anchor_length_min or self.anchor_length_provided > self.anchor_length_max:
            self.safe = False
            logger.error(": [Anchor Bolt] The length of the anchor bolt provided occurred out of the preferred range.")

        else:
            logger.info(": [Anchor Bolt] The preferred range of length for the anchor bolt of thread size {} is as follows:"
                        .format(self.anchor_dia_provided))
            logger.info(": [Anchor Bolt] Minimum length = {} mm, Maximum length = {} mm."
                        .format(self.anchor_length_min, self.anchor_length_max))
            logger.info(": [Anchor Bolt] The provided length of the anchor bolt is {} mm".format(self.anchor_length_provided))
            logger.info(": [Anchor Bolt] Designer/Erector should provide adequate anchorage depending on the availability "
                        "of standard lengths and sizes, satisfying the suggested range.")
            logger.info(": [Anchor Bolt] Reference: IS 5624:1993, Table 1.")

    def design_weld(self):
        """ design weld for the base plate and stiffeners

        Args:

        Returns:
        """
        # design the weld connecting the column and the stiffeners to the base plate

        self.weld_fu = min(self.dp_weld_fu_overwrite, self.dp_column_fu)

        # design of fillet weld
        if self.weld_type == 'Fillet Weld':

            if self.connectivity == 'Welded-Slab Base':

                if self.dp_column_type == 'Rolled' or 'Welded':

                    # defining the maximum limit of weld size that can be provided, which is equal to/less than the flange/web thickness
                    self.weld_size_flange_max = round_down(self.column_tf, 2)  # mm
                    self.weld_size_web_max = round_down(self.column_tw, 2)  # mm

                    # available length for welding along the flange and web of the column, without the stiffeners
                    length_available_flange = 2 * (self.column_bf + (self.column_bf - self.column_tw - (2 * self.column_r1)))  # mm
                    length_available_web = 2 * (self.column_D - (2 * self.column_tf) - (2 * self.column_r1))  # mm

                    # TODO: check end returns reduction
                    # Note: The effective length of weld is calculated by assuming 1% reduction in length at each end return. Since, the
                    # total number of end returns are 12, a total of 12% reduction (8% at flange and 4% at web) is incorporated into the
                    # respective 'effective' lengths.
                    self.effective_length_flange = length_available_flange - (0.08 * length_available_flange)  # mm
                    self.effective_length_web = length_available_web - (0.04 * length_available_web)  # mm

                    self.strength_unit_len = self.load_axial / (self.effective_length_flange + self.effective_length_web)  # N/mm
                    self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                    [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                    [self.plate_thk, self.column_tf], self.dp_weld_fab)  # mm

                    self.weld_size_flange = self.weld_size  # mm
                    self.weld_size_web = self.weld_size  # mm

                    # check against maximum allowed size
                    # checking if stiffener plates are required for providing extra length of weld

                    if self.weld_size_web > self.weld_size_web_max:
                        # Case 1: Adding stiffeners along the flanges of the column on either sides (total four in number)
                        self.stiffener_along_flange = 'Yes'

                        # length available on each stiffener plate for (fillet) welding on either sides
                        len_stiffener_available_flange = ((self.bp_width_provided - self.column_bf) / 2) * 2  # mm
                        # effective length assuming 2% reduction to incorporate end returns
                        eff_len_stiffener_available_flange = len_stiffener_available_flange - (0.02 * len_stiffener_available_flange)  # mm

                        # total effective len available including four stiffeners
                        self.total_eff_len_available = self.effective_length_flange + self.effective_length_web + \
                                                       (4 * eff_len_stiffener_available_flange)  # mm

                        # relative strength of weld per unit weld length and weld size including stiffeners along the flange
                        self.strength_unit_len = self.load_axial / self.total_eff_len_available  # N/mm
                        self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                               [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                               [self.plate_thk, self.column_tf], self.dp_weld_fab)  # mm

                        self.weld_size_web = self.weld_size  # mm

                    # Second itreation: checking the maximum weld size limit (at web)
                    if self.weld_size_web > self.weld_size_web_max:
                        # Case 2: Adding stiffeners along web of the column (total two in number)
                        self.stiffener_along_web = 'Yes'

                        len_stiffener_available_web = ((self.bp_length_provided - self.column_D) / 2) * 2  # mm  (each)
                        # effective length assuming 2% reduction to incorporate end returns
                        eff_len_stiffener_available_web = len_stiffener_available_web - (0.02 * len_stiffener_available_web)  # mm

                        # TODO: deduce notch size
                        # total effective len available including four stiffeners along flange and two along the web
                        self.total_eff_len_available = self.total_eff_len_available + (2 * eff_len_stiffener_available_web)  # mm

                        # relative strength of weld per unit weld length and weld size, including stiffeners along the flange and the web
                        self.strength_unit_len = self.load_axial / self.total_eff_len_available  # N/mm
                        self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                               [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                               [self.plate_thk, self.column_tf], self.dp_weld_fab)  # mm

                        self.weld_size_web = self.weld_size  # mm

                        # Third iteration: checking the maximum weld size limit (at web)
                        if self.weld_size_web > self.weld_size_web_max:
                            # Case 3: Adding stiffeners across the web of the column, between the depth (total two in number)
                            self.stiffener_across_web = 'Yes'

                            len_required = (self.load_axial * math.sqrt(3) * self.gamma_mw) / (0.7 * self.weld_size_web_max * self.weld_fu)  # mm
                            # Adding 16% of the total length to incorporate end returs (16 ends in this case)
                            len_required = len_required + (0.16 * len_required)  # mm

                            len_stiffener_req_across_web = len_required - self.total_eff_len_available

                            if len_stiffener_req_across_web < ((self.bp_width_provided / 2) - (self.column_tw / 2) - self.edge_distance):
                                len_stiffener_req_across_web = max(len_stiffener_req_across_web, eff_len_stiffener_available_flange,
                                                                   eff_len_stiffener_available_web)  # mm
                                self.total_eff_len_available = self.total_eff_len_available + (2 * len_stiffener_req_across_web)  # mm

                                # relative strength of weld per unit weld length and weld size, including stiffeners along the flange, web and across web
                                self.strength_unit_len = self.load_axial / self.total_eff_len_available  # N/mm
                                self.weld_size = self.calc_weld_size_from_strength_per_unit_len(self.strength_unit_len,
                                                                                                [self.dp_weld_fu_overwrite, self.dp_column_fu],
                                                                                                [self.plate_thk, self.column_tf],
                                                                                                self.dp_weld_fab)  # mm

                                self.weld_size_web = self.weld_size  # mm

                                if self.weld_size_web > self.weld_size_web_max:
                                    self.weld_size_web = self.weld_size_web_max
                            else:
                                self.design_status = False
                                # TODO: add log messages

                            # TODO: add log messages
                        else:
                            pass

                    self.weld_size_flange = self.weld_size  # mm
                    self.weld_size_stiffener = self.weld_size  # mm

                else:  # TODO: add checks for other type(s) of column section here (Example: built-up, star shaped etc.)
                    pass

            elif self.connectivity == 'Hollow Section':  # TODO: add calculations for hollow sections
                pass

        # design of butt/groove weld
        else:

            if self.connectivity == 'Gusseted Base Plate':
                self.stiffener_along_flange = 'Yes'
                self.stiffener_along_web = 'Yes'

            self.weld_size_flange = self.column_tf  # mm
            self.weld_size_web = self.column_tw  # mm

    def design_gusset_plate(self):
        """ design the gusset and the stiffener plate

        Args:

        Returns:
        """
        if self.connectivity == 'Welded-Slab Base' or 'Gusseted Base Plate':

            if self.gusset_along_flange == 'Yes':

                # layout of the gusset and the stiffener plate
                self.gusset_plate_length = self.bp_width_provided  # mm (each), gusset plate is along the flange of the column
                self.stiffener_plate_length = (self.bp_length_provided - self.column_D) / 2  # mm (each), stiffener plate is across the flange of the column

                self.gusset_outstand_length = (self.gusset_plate_length - self.column_bf) / 2  # mm
                self.stiffener_outstand_length = self.stiffener_plate_length  # mm

                self.gusset_fy = self.dp_column_fy  # MPa
                self.stiffener_fy = self.dp_column_fy  # MPa
                self.epsilon = math.sqrt(250 / self.gusset_fy)

                # thickness of the gusset/stiffener plate as per Table 2 of IS 800:2007 [b/t_f <= 13.6 * epsilon]
                # considering the maximum outstanding length to calculate the thickness of the gusset/stiffener
                thk_req = (max(self.gusset_outstand_length, self.stiffener_outstand_length)) / (13.6 * self.epsilon)  # mm

                # gusset/stiffener plate should be at-least equal to the flange thickness
                self.gusset_plate_thick = round_up(thk_req, 2, self.column_tf)  # mm
                self.stiffener_plate_thick = self.gusset_plate_thick  # mm

                # update the length pf the stiffener plate
                self.stiffener_plate_length = self.stiffener_plate_length - self.gusset_plate_thick  # mm

                # height of the gusset/stiffener plate
                # the size of the landing is 100 mm along vertical dimension and 50 mm along horizontal dimension
                # the assumed inclination of the gusset/stiffener plate is 45 degrees
                self.stiffener_plate_height = self.stiffener_plate_length + 50  # mm
                self.gusset_plate_height = max((self.gusset_outstand_length + 50), self.stiffener_plate_height)  # mm

                # defining stresses for the connectivity types
                if self.connectivity == 'Welded-Slab Base':
                    self.sigma_max_zz = self.w
                    self.sigma_xx = self.w
                else:
                    if self.gusseted_bp_case == 'Case1':
                        self.sigma_max_zz = self.sigma_max_zz
                        self.sigma_xx = self.sigma_xx
                    else:
                        self.sigma_max_zz = 0.45 * self.bearing_strength_concrete
                        self.sigma_xx = 0.45 * self.bearing_strength_concrete

                # shear yielding and moment capacity checks for the gusset/stiffener plates

                # gusset plate

                # shear and moment acting on the gusset plate
                self.shear_on_gusset = self.sigma_xx * self.gusset_outstand_length * self.gusset_plate_height  # for each gusset plate
                self.shear_on_gusset = round((self.shear_on_gusset / 1000), 3)  # kN

                self.moment_on_gusset = self.sigma_xx * self.gusset_plate_height * self.gusset_outstand_length ** 2 * 0.5
                self.moment_on_gusset = round((self.moment_on_gusset * 10 ** -6), 3)  # kN-m

                # shear yielding capacity and moment capacity of the gusset plate
                self.shear_capacity_gusset = IS800_2007.cl_8_4_design_shear_strength(self.gusset_plate_height * self.gusset_plate_thick,
                                                                                     self.gusset_fy)
                self.shear_capacity_gusset = round((self.shear_capacity_gusset / 1000), 3)  # kN

                self.z_e_gusset = (self.gusset_plate_thick * self.gusset_plate_height ** 2) / 6  # mm^3

                self.moment_capacity_gusset = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_gusset, 0, self.gusset_fy,
                                                                                           section_class='semi-compact')
                self.moment_capacity_gusset = round((self.moment_capacity_gusset * 10 ** -6), 3)  # kN-m

                # checks
                if self.shear_on_gusset > (0.6 * self.shear_capacity_gusset):
                    self.design_status = False
                else:
                    pass

                if self.moment_on_gusset > self.moment_capacity_gusset:
                    self.design_status = False
                else:
                    pass

                # stiffener plate

                # shear and moment acting on the stiffener plate
                self.shear_on_stiffener = ((self.sigma_max_zz + self.sigma_xx) / 2) * self.stiffener_plate_length * self.stiffener_plate_height
                self.shear_on_stiffener = round((self.shear_on_stiffener / 1000), 3)  # kN

                self.moment_on_stiffener = (self.sigma_xx * self.stiffener_plate_height * self.stiffener_plate_length ** 2 * 0.5) + \
                                           (0.5 * self.stiffener_plate_length * (self.sigma_max_zz - self.sigma_xx) * self.stiffener_plate_height *
                                            (2 / 3) * self.stiffener_plate_length)
                self.moment_on_stiffener = round((self.moment_on_stiffener * 10 ** -6), 3)  # kN-m

                # shear yielding capacity and moment capacity of the stiffener plate
                self.shear_capacity_stiffener = IS800_2007.cl_8_4_design_shear_strength(self.stiffener_plate_height * self.stiffener_plate_thick,
                                                                                        self.stiffener_fy)
                self.shear_capacity_stiffener = round((self.shear_capacity_stiffener / 1000), 3)  # kN

                self.z_e_stiffener = (self.stiffener_plate_thick * self.stiffener_plate_height ** 2) / 6  # mm^3
                self.moment_capacity_stiffener = IS800_2007.cl_8_2_1_2_design_moment_strength(self.z_e_stiffener, 0, self.stiffener_fy,
                                                                                              section_class='semi-compact')
                self.moment_capacity_stiffener = round((self.moment_capacity_stiffener * 10 ** -6), 3)  # kN-m
                # checks
                if self.shear_on_stiffener > (0.6 * self.shear_capacity_stiffener):
                    self.design_status = False
                else:
                    pass

                if self.moment_on_stiffener > self.moment_capacity_stiffener:
                    self.design_status = False
                else:
                    pass

                # weld size on the gusset and the stiffener plates
                self.weld_size_gusset = self.weld_size_flange  # mm
                self.weld_size_gusset_vertical = 6  # mm
                self.weld_size_stiffener = self.weld_size_web  # mm

        else:
            pass

        # end of calculation
        if self.safe:
            self.design_status = True
            logger.info(": Overall base plate connection design is safe")
            logger.debug(": =========End Of design===========")
        else:
            logger.info(": Overall base plate connection design is unsafe")
            logger.debug(": =========End Of design===========")

        # printing values for output dock

        # anchor bolt
        print(self.anchor_dia_provided)
        print(self.anchor_grade)
        print(self.anchor_length_provided)  # Length (mm)
        print(self.shear_capacity_anchor)
        print(self.bearing_capacity_anchor)
        print(self.anchor_capacity)  # Bolt capacity (kN)
        print(self.combined_capacity_anchor)  # Combined capacity (kN)
        if self.connectivity == 'Gusseted Base Plate':
            print(self.tension_capacity_anchor)  # Tension capacity (kN) (show only for 'Gusseted Base Plate' connectivity)
        else:
            pass

        # base plate
        print(self.plate_thk)  # Thickness (mm)
        print(self.bp_length_provided)  # Length (mm)
        print(self.bp_width_provided)  # Width (mm)

        # Gusset Plate (this section and subsection is only for 'Gusseted Base Plate' connectivity)

        # details coming soon...

        # detailing
        print(self.anchor_nos_provided)
        print(self.pitch_distance)  # Pitch Distance (mm) (show only when this value is not 'Null')
        print(self.gauge_distance)  # Gauge Distance (mm) mm (show only when this value is not 'Null')
        print(self.end_distance)  # mm
        print(self.edge_distance)  # mm
        if self.connectivity == 'Welded-Slab Base':
            print(self.projection)  # mm (show only for 'Welded-Slab Base' connectivity)
        else:
            pass

        # Gusset/Stiffener Plate
        # Details tab (this is supposed to be taken from Osdag 2 - details to be given soon)

        # Gusset Plate
        print(self.gusset_plate_thick)  # Thickness (mm)
        print(self.shear_on_gusset)  # Shear Demand (kN)
        print(self.shear_capacity_gusset)  # Shear Capacity (kN)
        print(self.moment_on_gusset)  # Moment Demand (kN-m)
        print(self.moment_capacity_gusset)  # Moment Capacity (kN-m)

        # Stiffener Plate
        print(self.stiffener_plate_thick)  # Thickness (mm)
        print(self.shear_on_stiffener)  # Shear Demand (kN)
        print(self.shear_capacity_stiffener)  # Shear Capacity (kN)
        print(self.moment_on_stiffener)  # Moment Demand (kN-m)
        print(self.moment_capacity_stiffener)  # Moment Capacity (kN-m)


        # Weld

        print(self.weld_size_flange if self.weld_type != 'Butt Weld' else '')  # Size at Flange (mm)
        print(self.weld_size_web if self.weld_type != 'Butt Weld' else '')  # Size at Web (mm)

        if self.gusset_along_flange == 'Yes':
            print(self.weld_size_stiffener if self.weld_type != 'Butt Weld' else '')  # Size at Gusset/Stiffener (mm)

        # this might not be required
        # print(self.weld_size if self.weld_type != 'Butt Weld' else '')  # Weld size (mm)

        # col properties
        print(self.column_D, self.column_bf, self.column_tf, self.column_tw, self.column_r1, self.column_r2)
        # print(self.w)

        print("Here {}".format(self.dp_anchor_fu_overwrite))
