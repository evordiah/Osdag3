
from Threading import FinPlateConnection
import unittest
class test:

    def Finplate_test(self,mainWindow,main,d):

        main.set_osdaglogger(None)
        error = main.func_for_validation(main,self,d)
        return error

class TestClass(unittest.TestCase):

    def test_one(self):

        finplate = test()

        uiObj = uiObj = {'Module': 'Fin Plate', 'Connectivity': 'Column flange-Beam web', 'Member.Supporting_Section': 'PBP 300X222.9', 'Member.Supported_Section': 'UB 406 x 178 x 74', 'Member.Material': 'E 250 (Fe 410 W)B', 'Load.Shear': '150', 'Load.Axial': '300', 'Bolt.Diameter': ['12', '16', '20', '24', '30', '36'], 'Bolt.Type': 'Bearing Bolt', 'Bolt.Grade': ['3.6', '4.6', '4.8', '5.6', '5.8', '6.8', '8.8', '9.8', '10.9', '12.9'], 'Plate.Thickness': ['3', '4', '5', '6', '8', '10', '12', '14', '16', '18', '20'], 'Member.Supporting_Section.Material': 'E 250 (Fe 410 W)B', 'Member.Supported_Section.Material': 'E 250 (Fe 410 W)B', 'DesignPreferences.Bolt.Bolt_Hole_Type': 'Standard', 'DesignPreferences.Bolt.Material_Grade_OverWrite': '410', 'DesignPreferences.Bolt.Slip_Factor': '0.3', 'DesignPreferences.Weld.Fab': 'Shop Weld', 'DesignPreferences.Weld.Material_Grade_OverWrite': '410', 'DesignPreferences.Detailing.Edge_type': 'a - Sheared or hand flame cut', 'DesignPreferences.Detailing.Gap': '10', 'DesignPreferences.Detailing.Corrosive_Influences': 'No', 'DesignPreferences.Design.Design_Method': 'Limit State Design', 'Plate.Material': 'E 165 (Fe 290)'}

        ans = finplate.Finplate_test(finplate,FinPlateConnection,uiObj)
        self.assertTrue(ans is None)


if __name__ == '__main__':
    
    unittest.main()
