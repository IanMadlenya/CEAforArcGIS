import os
import unittest

import pandas as pd

from cea.demand.occupancy_model import schedule_maker
from cea.demand.thermal_loads import calc_thermal_loads, BuildingProperties
from cea.globalvar import GlobalVariables
from cea.inputlocator import InputLocator
from cea.utilities import epwreader


class TestCalcThermalLoads(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import zipfile
        import tempfile
        import cea.examples
        archive = zipfile.ZipFile(os.path.join(os.path.dirname(cea.examples.__file__), 'reference-case-open.zip'))
        archive.extractall(tempfile.gettempdir())
        reference_case = os.path.join(tempfile.gettempdir(), 'reference-case-open', 'baseline')
        cls.locator = InputLocator(reference_case)
        cls.gv = GlobalVariables()
        weather_path = cls.locator.get_default_weather()
        cls.weather_data = epwreader.epw_reader(weather_path)[
            ['drybulb_C', 'relhum_percent', 'windspd_ms', 'skytemp_C']]

        # run properties script
        import cea.demand.preprocessing.properties
        cea.demand.preprocessing.properties.properties(cls.locator, True, True, True, True)

        cls.building_properties = BuildingProperties(cls.locator, cls.gv)
        cls.date = pd.date_range(cls.gv.date_start, periods=8760, freq='H')
        cls.list_uses = cls.building_properties.list_uses()
        cls.archetype_schedules, cls.archetype_values = schedule_maker(cls.date, cls.locator, cls.list_uses)
        cls.occupancy_densities = cls.archetype_values['people']
        cls.usage_schedules = {'list_uses': cls.list_uses, 'archetype_schedules': cls.archetype_schedules,
                               'occupancy_densities': cls.occupancy_densities, 'archetype_values': cls.archetype_values}

    def test_calc_thermal_loads(self):
        # FIXME: the usage_schedules bit needs to be fixed!!
        bpr = self.building_properties['B01']
        result = calc_thermal_loads('B01', bpr, self.weather_data,
                                    self.usage_schedules, self.date, self.gv, self.locator)
        self.assertIsNone(result)
        self.assertTrue(os.path.exists(self.locator.get_demand_results_file('B01')), 'Building csv not produced')
        self.assertTrue(os.path.exists(self.locator.get_temporary_file('B01T.csv')),
                        'Building temp file not produced')

        # test the building csv file
        df = pd.read_csv(self.locator.get_demand_results_file('B01'))
        #
        # expected_columns = self.gv.demand_building_csv_columns
        # print expected_columns
        # set(expected_columns)
        # self.assertEqual(set(expected_columns), set(df.columns),
        #                  'Column list of building csv does not match: ' + str(
        #                      set(expected_columns).symmetric_difference(set(df.columns))))
        # self.assertEqual(df.shape[0], 8760, 'Expected one row per hour in the year')

        value_columns = [u'Ealf_kWh', u'Eauxf_kWh', u'Edataf_kWh', u'Ef_kWh', u'QCf_kWh', u'QHf_kWh',
                         u'Qcdataf_kWh', u'Qcref_kWh', u'Qcs_kWh', u'Qcsf_kWh', u'Qhs_kWh', u'Qhsf_kWh', u'Qww_kWh',
                         u'Qwwf_kWh', u'Tcsf_re_C', u'Thsf_re_C', u'Twwf_re_C', u'Tcsf_sup_C', u'Thsf_sup_C',
                         u'Twwf_sup_C']
        values = [155102.615999994, 3817.304, 0.0, 158919.92, 8373.964, 235413.775, 0,
                  0, 7888.446, 8373.964, 183389.465, 195411.984, 37198.8870000003, 40001.765,
                  2567.0, 67361.359, 99496.0, 1812.0, 77058.2680000001, 525600]

        for i, column in enumerate(value_columns):
            try:
                self.assertAlmostEqual(values[i], df[column].sum(), msg='Sum of column %s differs, %f != %f' % (
                    column, values[i], df[column].sum()), places=3)
            except:
                print 'values:', [df[column].sum() for column in value_columns]  # make it easier to update changes
                raise

    def test_calc_thermal_loads_other_buildings(self):
        """Test some other buildings just to make sure we have the proper data"""
        # randomly selected except for B302006716, which has `Af == 0`
        buildings = {'B01': (8373.96400, 235413.77500),
                     'B03': (8362.64100, 235053.04400),
                     'B02': (8423.01800, 235556.22800),
                     'B05': (8569.54200, 234874.28400),
                     'B04': (8546.75100, 235917.23100),
                     'B07': (8358.49200, 235153.72100),
                     'B06': (0.00000, 0.00000),
                     'B09': (8436.55700, 234898.39800),
                     'B08': (8401.99800, 236110.17000)}
        if self.gv.multiprocessing:
            import multiprocessing as mp
            pool = mp.Pool()
            joblist = []
            for building in buildings.keys():
                bpr = self.building_properties[building]
                job = pool.apply_async(run_for_single_building,
                                       [building, bpr, self.weather_data, self.usage_schedules, self.date, self.gv,
                                        self.locator])
                joblist.append(job)
            for job in joblist:
                b, qcf_kwh, qhf_kwh = job.get(120)
                b0 = buildings[b][0]
                b1 = buildings[b][1]
                self.assertAlmostEqual(b0, qcf_kwh,
                                       msg="qcf_kwh for %(b)s should be: %(qcf_kwh).5f, was %(b0).5f" % locals(),
                                       places=3)
                self.assertAlmostEqual(b1, qhf_kwh,
                                       msg="qhf_kwh for %(b)s should be: %(qhf_kwh).5f, was %(b1).5f" % locals(),
                                       places=3)
            pool.close()
        else:
            for building in buildings.keys():
                bpr = self.building_properties[building]
                b, qcf_kwh, qhf_kwh = run_for_single_building(building, bpr, self.weather_data, self.usage_schedules,
                                                              self.date, self.gv, self.locator)
                b0 = buildings[b][0]
                b1 = buildings[b][1]
                self.assertAlmostEqual(b0, qcf_kwh,
                                       msg="qcf_kwh for %(b)s should be: %(qcf_kwh).5f, was %(b0).5f" % locals(),
                                       places=3)
                self.assertAlmostEqual(b1, qhf_kwh,
                                       msg="qhf_kwh for %(b)s should be: %(qhf_kwh).5f, was %(b1).5f" % locals(),
                                       places=3)


def run_for_single_building(building, bpr, weather_data, usage_schedules, date, gv, locator):
    calc_thermal_loads(building, bpr, weather_data, usage_schedules, date, gv, locator)
    df = pd.read_csv(locator.get_demand_results_file(building))
    return building, df['QCf_kWh'].sum(), df['QHf_kWh'].sum()


if __name__ == "__main__":
    unittest.main()
