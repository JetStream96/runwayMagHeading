from magVarAdder import *

a = MagVarAdder()
a.scan_rwy_file()
a.generate_input_file('2016')
print('Computing magnetic variation ...')
a.run_geomag()
a.import_output_file()
a.write_to_csv()
print('Output generated: runway_data/runways_with_true_heading.csv')
input("Press Enter to continue...")
