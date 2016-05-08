import subprocess


class MagVarAdder:
    __csv_data = []
    __mag_heading_first = None
    __mag_heading_second = None
    __items_to_compute = []

    def __set_list_sizes(self):
        count = len(self.__csv_data)
        self.__mag_heading_first = [None] * count
        self.__mag_heading_second = [None] * count

        for i in range(0, count):
            self.__mag_heading_first[i] = ''
            self.__mag_heading_second[i] = ''

    def scan_rwy_file(self):
        """
        Scans the csv file to get runway lat/lon for
        mag. var computation.
        """
        fo = open("../runway_data/runways.csv", "r")
        lines = fo.readlines()

        for line in lines:
            self.__csv_data.append(line.split(','))

        self.__set_list_sizes()
        self.__set_first_line()

        self.__fill_compute_list()

    def generate_input_file(self, year: str):
        lines = []
        items = self.__items_to_compute

        for entry in items:
            _, (lat, lon, _) = entry
            lines.append(year + " D F0 " + str(lat) + " " + str(lon))

        text_to_write = '\n'.join(lines)

        f = open("../geomag70_windows/in.txt", 'w')
        f.write(text_to_write)

    @staticmethod
    def __latlon_valid(lat, lon):
        return -90 < lat < 90 and -180 <= lon <= 180

    @staticmethod
    def run_geomag():
        output = subprocess.check_output(
            'cd ../geomag70_windows &' +
            'geomag70.exe WMM2015.COF f in.txt out.txt',
            shell=True)
        return output

    def __fill_compute_list(self):
        count = len(self.__csv_data)

        for i in range(1, count):
            """   9  10   12
                 15  16   18
                lat lon heading"""
            line = self.__csv_data[i]
            (first_val, first_avail) = self.__extract_latlon_heading(line, True)
            (second_val, second_avail) = \
                self.__extract_latlon_heading(line, False)

            if first_avail:
                (lat, lon, _) = first_val
                if self.__latlon_valid(lat, lon):
                    self.__items_to_compute.append(((i, 1), first_val))

            if second_avail:
                (lat, lon, _) = second_val
                if self.__latlon_valid(lat, lon):
                    self.__items_to_compute.append(((i, 2), second_val))

    def __set_first_line(self):
        self.__mag_heading_first[0] = '"le_heading_degM"'
        self.__mag_heading_second[0] = '"he_heading_degM"'

    @staticmethod
    def __extract_latlon_heading(line: [str], is_first: bool):
        """ Returns result and whether the conversion succeeds. """

        if is_first:
            lat_index = 9
            lon_index = 10
            heading_index = 12
        else:
            lat_index = 15
            lon_index = 16
            heading_index = 18

        try:
            lat = float(line[lat_index])
            lon = float(line[lon_index])
            heading = float(line[heading_index])
            return (lat, lon, heading), True
        except ValueError:
            return None, False

    def import_output_file(self):
        fo = open('../geomag70_windows/out.txt', 'r')
        lines = fo.readlines()

        for i in range(1, len(self.__items_to_compute)):
            # filter is used to remove empty strings
            words = list(filter(None, lines[i].split(' ')))

            deg = float(words[5].replace('d', ''))
            minute = float(words[6].replace('m', ''))
            is_negative = deg < 0 or minute < 0
            mag_var = abs(deg) + abs(minute) / 60.0
            mag_var *= -1.0 if is_negative else 1.0

            (csv_line_num, pos), (_, _, heading_true) = \
                self.__items_to_compute[i-1]
            heading_mag = str((heading_true - mag_var) % 360.0)

            if pos == 1:
                self.__mag_heading_first[csv_line_num] = heading_mag
            else:
                self.__mag_heading_second[csv_line_num] = heading_mag

    def write_to_csv(self):
        lines = []
        csv_data = self.__csv_data

        for i in range(0, len(csv_data)):
            strs = [s for (i, s) in enumerate(csv_data[i])
                    if i <= 12] + \
                   [self.__mag_heading_first[i]] + \
                   [s for (i, s) in enumerate(csv_data[i])
                    if 13 <= i <= 18] + \
                   [self.__mag_heading_second[i]] + \
                   [s for (i, s) in enumerate(csv_data[i])
                    if i > 18]

            line = ','.join(strs)
            lines.append(line)

        text_to_write = ''.join(lines)

        f = open("../runway_data/runways_with_true_heading.csv", 'w')
        f.write(text_to_write)
