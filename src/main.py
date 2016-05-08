from magVarAdder import MagVarAdder

# Use decimal (2017, 2019.8855) or
# YYYY,MM,DD (2018,4,7)
year = '2016'

adder = MagVarAdder()
adder.scan_rwy_file()
adder.generate_input_file(year)
print('Computing magnetic variation ...')
adder.run_geomag()
adder.import_output_file()
adder.write_to_csv()
print('Output generated: runway_data/runways_with_true_heading.csv')
input("Press Enter to continue...")
