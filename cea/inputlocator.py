"""
inputlocator.py - locate input files by name based on the reference folder structure.
"""
import os
import tempfile

__author__ = "Daren Thomas"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Daren Thomas", "Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "thomas@arch.ethz.ch"
__status__ = "Production"

class InputLocator(object):
    """The InputLocator locates files and folders for input to the scripts. This works, because we
    have a convention for the folder structure of a scenario.
    It also provides locations of other files, such as those in the databases folder (e.g. archetypes).
    """
    # SCENARIO
    def __init__(self, scenario_path):
        self.scenario_path = scenario_path
        self.db_path = os.path.join(os.path.dirname(__file__), 'databases', 'CH')

        if scenario_path:
            self.get_geothermal_potential = os.path.join(self.get_potentials_results_folder(), "geothermal.csv")
            self.get_sewageheat_potential = os.path.join(self.get_potentials_results_folder(), "SWP.csv")

            self.pathSubsRes = os.path.join(self.get_optimization_results_folder(), "substations")  # Substation results for disconnected buildings
            self.pathClustRes = os.path.join(self.get_optimization_results_folder(), "clustering") # Clustering results for disconnected buildings
            self.pathDiscRes = os.path.join(self.get_optimization_results_folder(), "disconnected") # Operation pattern for disconnected buildings
            self.pathNtwRes = os.path.join(self.get_optimization_results_folder(), "network")  # Ntw summary results
            self.pathMasterRes = os.path.join(self.get_optimization_results_folder(), "master") # Master checkpoints
            self.pathSlaveRes = os.path.join(self.get_optimization_results_folder(), "slave") # Slave results (storage + operation pattern)

            self.pathTotalNtw = os.path.join(self.pathNtwRes, "totals") # Total files (inputs to substation + ntw in master)
            self.pathNtwLayout = os.path.join(self.pathNtwRes, "layout") # Ntw layout files
            self.get_pipes_DH_network = os.path.join(self.pathNtwLayout, "PipesData_DH.csv")
            self.pathSolarRaw = os.path.join(self.get_potentials_results_folder(), "solar") # Raw solar files

    # optimization
    def get_optimization_results_folder(self):
        """scenario/outputs/data/demand"""
        folder = os.path.join(self.scenario_path, 'outputs', 'data', 'optimization')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    # resource potential assessment
    def get_potentials_results_folder(self):
        """scenario/outputs/data/demand"""
        folder = os.path.join(self.scenario_path, 'outputs', 'data', 'potentials')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder

    # DATABASES
    def get_default_weather(self):
        """db/Weather/Zurich.epw
        path to database of archetypes file Archetypes_properties.xlsx"""
        return os.path.join(self.db_path, 'Weather', 'Zug-2010.epw')

    def get_weather(self, name):
        """db/Weather/{name}.epw"""
        weather_path = os.path.join(self.db_path, 'Weather', name + '.epw')
        if not os.path.exists(weather_path):
            return self.get_default_weather()
        return weather_path

    def get_weather_names(self):
        """Return a list of all installed epw files in the system"""
        weather_names = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(self.db_path, 'Weather'))]
        return weather_names

    def get_archetypes_properties(self):
        """db/Archetypes/Archetypes_properties.xlsx
        path to database of archetypes file Archetypes_properties.xlsx"""
        return os.path.join(self.db_path, 'Archetypes', 'Archetypes_properties.xlsx')

    def get_archetypes_schedules(self):
        """db/Archetypes/Archetypes_schedules.xlsx
        path to database of archetypes file Archetypes_HVAC_properties.xlsx"""
        return os.path.join(self.db_path, 'Archetypes', 'Archetypes_schedules.xlsx')

    def get_life_cycle_inventory_supply_systems(self):
        """db/Systems/supply_systems.csv"""
        return os.path.join(self.db_path, 'Systems', 'supply_systems.xls')

    def get_technical_emission_systems(self):
        """db/Systems/emission_systems.csv"""
        return os.path.join(self.db_path, 'Systems',  'emission_systems.xls')

    def get_envelope_systems(self):
        """db/Systemsl/emission_systems.csv"""
        return os.path.join(self.db_path, 'Systems',  'envelope_systems.xls')

    def get_data_benchmark(self):
        """db/Benchmarks/benchmark_targets.xls"""
        return os.path.join(self.db_path, 'Benchmarks', 'benchmark_targets.xls')
    def get_data_benchmark_today(self):
        """db/Benchmarks/benchmark_today.xls"""
        return os.path.join(self.db_path, 'Benchmarks', 'benchmark_today.xls')

    def get_data_mobility(self):
        """db/Benchmarks/mobility.xls"""
        return os.path.join(self.db_path, 'Benchmarks', 'mobility.xls')

    def get_uncertainty_db(self):
        """db/Uncertainty/uncertainty_distributions.xls"""
        return os.path.join(self.db_path, 'Uncertainty', 'uncertainty_distributions.xls')

    # INPUTS
    def get_building_geometry(self):
        """scenario/inputs/building-geometry/zone.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-geometry', 'zone.shp')

    def get_district(self):
        """scenario/inputs/building-geometry/district.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-geometry', 'district.shp')

    def get_building_age(self):
        """scenario/inputs/building-properties/age.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'age.shp')

    def get_building_occupancy(self):
        """scenario/inputs/building-properties/building_occupancy.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'occupancy.shp')

    def get_building_supply(self):
        """scenario/inputs/building-properties/building_supply.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'supply_systems.shp')

    def get_building_thermal(self):
        """scenario/inputs/building-properties/thermal_properties.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'thermal_properties.shp')

    def get_building_internal(self):
        """scenario/inputs/building-properties/internal_loads.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'internal_loads.shp')

    def get_building_comfort(self):
        """scenario/inputs/building-properties/indoor_comfort.shp'"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'indoor_comfort.shp')

    def get_building_hvac(self):
        """scenario/inputs/building-properties/technical_systems.shp"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'technical_systems.shp')

    def get_building_architecture(self):
        """scenario/inputs/building-properties/architecture.shp
        This file is generated by the properties script.
        This file is used in the embodied energy script (cea/embodied.py)
        and the demand script (cea/demand_main.py)"""
        return os.path.join(self.scenario_path, 'inputs', 'building-properties', 'architecture.shp')

    def get_terrain(self):
        """scenario/inputs/topography/terrain.tif"""
        return os.path.join(self.scenario_path, 'inputs', 'topography', 'terrain.tif')

    # OUTPUTS

    ##SOLAR-RADIATION
    def get_radiation(self):
        """scenario/outputs/data/solar-radiation/radiation.csv"""
        solar_radiation_folder = os.path.join(self.scenario_path, 'outputs', 'data', 'solar-radiation')
        if not os.path.exists(solar_radiation_folder):
            os.makedirs(solar_radiation_folder)
        return os.path.join(solar_radiation_folder, 'radiation.csv')

    def get_surface_properties(self):
        """scenario/outputs/data/solar-radiation/properties_surfaces.csv"""
        solar_radiation_folder = os.path.join(self.scenario_path, 'outputs', 'data', 'solar-radiation')
        if not os.path.exists(solar_radiation_folder):
            os.makedirs(solar_radiation_folder)
        return os.path.join(solar_radiation_folder, 'properties_surfaces.csv')


    def get_radiation_metadata(self, building_name):
        """scenario/2-results/2-demand/1-timeseries/{building_name}.csv"""
        radiation_results_folder = self.get_radiation_folder()
        return os.path.join(radiation_results_folder, '%s_id_df.csv' % building_name)

    def get_radiation_building(self, building_name):
        """scenario/2-results/2-demand/1-timeseries/{building_name}.csv"""
        radiation_results_folder = self.get_radiation_folder()
        return os.path.join(radiation_results_folder, '%s.csv' % building_name)

    def get_building_list(self, name):
        """scenario/2-results/2-demand/1-timeseries/{building_name}.csv"""
        radiation_results_folder = self.get_radiation_folder()
        return os.path.join(radiation_results_folder, '%s.csv' % name)

    def get_radiation_folder(self):
        """scenario/outputs/data/solar-radiation/radiation.csv"""
        return os.path.join(self.scenario_path, 'outputs', 'data', 'solar-radiation')


    ## POTENTIALS
    def get_solar_potential_folder(self):
        """scenario/outputs/data/potentials/solar"""
        return os.path.join(self.scenario_path, 'outputs', 'data', 'potentials', 'solar')

    def PV_results(self, building_name):
        """scenario/outputs/data/potentials/solar/{building_name}_PV.csv"""
        solar_potential_folder = self.get_solar_potential_folder()
        return os.path.join(solar_potential_folder, '%s_PV.csv' % building_name)

    def metadata_results(self, building_name):
        """scenario/outputs/data/potentials/solar/{building_name}_PV.csv"""
        solar_potential_folder = self.get_solar_potential_folder()
        return os.path.join(solar_potential_folder, '%s_sensors.csv' % building_name)

    def get_sensitivity_output(self, method, samples):
        """scenario/outputs/data/sensitivity-analysis/sensitivity_${METHOD}_${SAMPLES}.xls"""
        return os.path.join(self.scenario_path, 'outputs', 'data', 'sensitivity-analysis', 'sensitivity_'+ method + '_%s.xls' % samples)

    def get_sensitivity_plots_file(self, parameter):
        """scenario/outputs/plots/sensitivity/${PARAMETER}.pdf"""
        return os.path.join(self.scenario_path, 'outputs', 'plots', 'sensitivity', '%s.pdf' % parameter)



    ##DEMAND
    def get_demand_results_folder(self):
        """scenario/outputs/data/demand"""
        demand_results_folder = os.path.join(self.scenario_path, 'outputs', 'data', 'demand')
        if not os.path.exists(demand_results_folder):
            os.makedirs(demand_results_folder)
        return demand_results_folder

    def get_total_demand(self):
        """scenario/outputs/data/demand/Total_demand.csv"""
        return os.path.join(self.get_demand_results_folder(), 'Total_demand.csv')

    def get_demand_results_file(self, building_name):
        """scenario/outputs/data/demand/{building_name}.csv"""
        demand_results_folder = self.get_demand_results_folder()
        return os.path.join(demand_results_folder, '%s.csv' % building_name)

    ##EMISSIONS
    def get_lca_emissions_results_folder(self):
        """scenario/outputs/data/emissions"""
        lca_emissions_results_folder = os.path.join(self.scenario_path, 'outputs', 'data', 'emissions')
        if not os.path.exists(lca_emissions_results_folder):
            os.makedirs(lca_emissions_results_folder)
        return lca_emissions_results_folder

    def get_lca_embodied(self):
        """cenario/outputs/data/emissions/Total_LCA_embodied.csv"""
        return os.path.join(self.get_lca_emissions_results_folder(), 'Total_LCA_embodied.csv')

    def get_lca_operation(self):
        """cenario/outputs/data/emissions/Total_LCA_operation.csv"""
        return os.path.join(self.get_lca_emissions_results_folder(), 'Total_LCA_operation.csv')

    def get_lca_mobility(self):
        """scenario/outputs/data/emissions/Total_LCA_mobility.csv"""
        return os.path.join(self.get_lca_emissions_results_folder(), 'Total_LCA_mobility.csv')

    ##GRAPHS
    def get_demand_plots_folder(self):
        """scenario/outputs/plots/timeseries"""
        demand_plots_folder = os.path.join(self.scenario_path, 'outputs', 'plots', 'timeseries')
        if not os.path.exists(demand_plots_folder):
            os.makedirs(demand_plots_folder)
        return demand_plots_folder

    def get_demand_plots_file(self, building_name):
        """scenario/outputs/plots/timeseries/{building_name}.pdf"""
        demand_plots_folder = self.get_demand_plots_folder()
        return os.path.join(demand_plots_folder, '%s.pdf' % building_name)

    def get_timeseries_plots_file(self, building_name):
        """scenario/outputs/plots/timeseries/{building_name}.pdf"""
        demand_plots_folder = self.get_demand_plots_folder()
        return os.path.join(demand_plots_folder, '%s.html' % building_name)

    def get_benchmark_plots_file(self):
        """scenario/outputs/plots/graphs/{building_name}.pdf"""
        benchmark_plots_folder = os.path.join(self.scenario_path, 'outputs', 'plots', 'graphs')
        if not os.path.exists(benchmark_plots_folder):
            os.makedirs(benchmark_plots_folder)
        return os.path.join(benchmark_plots_folder, 'Benchmark_scenarios.pdf')

    ##HEATMAPS
    def get_heatmaps_demand_folder(self):
        """scenario/outputs/plots/heatmaps"""
        heatmaps_demand_folder = os.path.join(self.scenario_path, 'outputs', 'plots', 'heatmaps')
        if not os.path.exists(heatmaps_demand_folder):
            os.makedirs(heatmaps_demand_folder)
        return heatmaps_demand_folder

    def get_heatmaps_emission_folder(self):
        """scenario/outputs/plots/heatmaps"""
        heatmaps_emissions_folder = os.path.join(self.scenario_path, 'outputs', 'plots', 'heatmaps')
        if not os.path.exists(heatmaps_emissions_folder):
            os.makedirs(heatmaps_emissions_folder)
        return heatmaps_emissions_folder

    #OTHER
    def get_temporary_folder(self):
        """Temporary folder as returned by `tempfile`."""
        return tempfile.gettempdir()

    def get_temporary_file(self, filename):
        """Returns the path to a file in the temporary folder with the name `filename`"""
        return os.path.join(self.get_temporary_folder(), filename)


    # Optimizaton
