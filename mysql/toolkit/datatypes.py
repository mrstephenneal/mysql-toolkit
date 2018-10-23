import datetime
from operator import itemgetter


DATA_TYPES = {
    # Text Data Types
    'tinytext': {'type': str, 'max': 255},
    'varchar': {'type': str, 'max': 65535},
    'mediumtext': {'type': str, 'max': 16777215},
    'longtext': {'type': str, 'max': 4294967295},

    # Numeric Data Types
    'tinyint': {'type': int, 'min': -128, 'max': 127},
    'smallint': {'type': int, 'min': -32768, 'max': 32767},
    'mediumint': {'type': int, 'min': -8388608, 'max': 8388607},
    'int': {'type': int, 'min': -2147483648, 'max': 2147483647},
    'bigint': {'type': int, 'min': -9223372036854775808, 'max': 9223372036854775807},
    'decimal': {'type': float},

    # Date Data Types
    'date': {'type': datetime.date},
    'datetime': {'type': datetime.datetime},
    'time': {'type': datetime.time},
    'year': {'type': int, 'min': 1901, 'max': 2155},
}

# MySQL accepted datetime ranges
YEARS = list(range(1000, 9999))
MONTHS = list(range(1, 13))
DAYS = list(range(1, 32))
HOURS = list(range(-838, 838))
MINUTES = list(range(1, 60))
SECONDS = list(range(0, 60))


class Text:
    def __init__(self, data):
        self.data = data
        self.type = None
        self.len = None

    def is_varchar(self):
        """Determine if a data record is of the type VARCHAR."""
        dt = DATA_TYPES['varchar']
        if type(self.data) is dt['type'] and len(self.data) < dt['max']:
            self.type = 'VARCHAR'
            self.len = len(self.data)
            return True

    def is_tinytext(self):
        """Determine if a data record is of the type VARCHAR."""
        return self._is_text_data('tinytext')

    def is_mediumtext(self):
        """Determine if a data record is of the type MEDIUMTEXT."""
        return self._is_text_data('mediumtext')

    def is_longtext(self):
        """Determine if a data record is of the type LONGTEXT."""
        return self._is_text_data('longtext')

    def _is_text_data(self, data_type):
        """Private method for testing text data types."""
        dt = DATA_TYPES[data_type]
        if type(self.data) is dt['type'] and len(self.data) < dt['max'] and all(type(char) == str for char in self.data):
            self.type = data_type.upper()
            self.len = len(self.data)
            return True


class Numeric:
    def __init__(self, data):
        self.data = data
        self.type = None
        self.len = len(self.data)

    def is_tinyint(self):
        """Determine if a data record is of the type TINYINT."""
        return self._is_numeric_data('tinyint')

    def is_mediumint(self):
        """Determine if a data record is of the type MEDIUMINT."""
        return self._is_numeric_data('mediumint')

    def is_int(self):
        """Determine if a data record is of the type INT."""
        return self._is_numeric_data('int')

    def is_bigint(self):
        """Determine if a data record is of the type BIGINT."""
        return self._is_numeric_data('bigint')

    def is_decimal(self):
        """Determine if a data record is of the type float."""
        dt = DATA_TYPES['decimal']
        if type(self.data) is dt['type']:
            self.type = 'DECIMAL'
            num_split = str(self.data).split('.', 1)
            self.len = '{0}, {1}'.format(len(num_split[0]), len(num_split[1]))
            return True

    def _is_numeric_data(self, data_type):
        """Private method for testing text data types."""
        dt = DATA_TYPES[data_type]
        if dt['min'] and dt['max']:
            if type(self.data) is dt['type'] and dt['min'] < self.data < dt['max']:
                self.type = data_type.upper()
                self.len = len(str(self.data))
                return True


class Dates:
    def __init__(self, data):
        self.data = data
        self.type = None
        self.len = len(self.data)

    def is_date(self):
        """Determine if a data record is of type DATE."""
        dt = DATA_TYPES['date']
        if type(self.data) is dt['type'] and '-' in str(self.data) and str(self.data).count('-') == 2:
            # Separate year, month and day
            date_split = str(self.data).split('-')
            y, m, d = date_split[0], date_split[1], date_split[2]

            # Validate values
            valid_year, valid_months, valid_days = int(y) in YEARS, int(m) in MONTHS, int(d) in DAYS

            # Check that all validations are True
            if all(i is True for i in (valid_year, valid_months, valid_days)):
                self.type = 'date'.upper()
                self.len = None
                return True

    def is_datetime(self):
        """Determine if a data record is of type DATETIME."""
        return self._is_date_data('datetime')

    def is_time(self):
        """Determine if a data record is of type TIME."""
        dt = DATA_TYPES['time']
        if type(self.data) is dt['type'] and ':' in str(self.data) and str(self.data).count(':') == 2:
            # Separate hour, month, second
            date_split = str(self.data).split(':')
            h, m, s = date_split[0], date_split[1], date_split[2]

            # Validate values
            valid_hour, valid_min, valid_sec = int(h) in HOURS, int(m) in MINUTES, int(float(s)) in SECONDS

            if all(i is True for i in (valid_hour, valid_min, valid_sec)):
                self.type = 'time'.upper()
                self.len = None
                return True

    def is_year(self):
        """Determine if a data record is of type YEAR."""
        dt = DATA_TYPES['year']
        if dt['min'] and dt['max']:
            if type(self.data) is dt['type'] and dt['min'] < self.data < dt['max']:
                self.type = 'year'.upper()
                self.len = None
                return True

    def _is_date_data(self, data_type):
        """Private method for determining if a data record is of type DATE."""
        dt = DATA_TYPES[data_type]
        if isinstance(self.data, dt['type']):
            self.type = data_type.upper()
            self.len = None
            return True


class Record(Text, Numeric, Dates):
    def __init__(self, data):
        super(Record, self).__init__(data)
        self.data = data
        self.type = None
        self.len = None

    @property
    def datatype(self):
        if not self.type:
            self.get_type()

        if self.len:
            return '{0} ({1})'.format(self.type, self.len)
        else:
            return '{0}'.format(self.type)

    def get_type(self):
        """Retrieve the data type for a data record."""
        test_method = [
            self.is_time,
            self.is_date,
            self.is_datetime,
            self.is_decimal,
            self.is_year,
            self.is_tinyint,
            self.is_mediumint,
            self.is_int,
            self.is_bigint,
            self.is_tinytext,
            self.is_varchar,
            self.is_mediumtext,
            self.is_longtext,
        ]
        # Loop through test methods until a test returns True
        for method in test_method:
            if method():
                return self.datatype

    @property
    def get_type_len(self):
        """Retrieve the type and length for a data record."""
        # Check types and set type/len
        self.get_type()
        return self.type, self.len


class DataTypes:
    def __init__(self, data):
        self.record = Record(data)

    def varchar(self):
        """Retrieve the data type of a data record suspected to a VARCHAR."""
        return self.record.datatype if self.record.is_varchar() else False

    def text(self):
        """Retrieve the data type of a data record suspected to a VARCHAR."""
        return self.record.datatype if self.record.is_text() else False


def column_datatype(column_data, prefer_varchar=False, prefer_int=False):
    """
    Retrieve the best fit data type for a column of a MySQL table.

    Accepts a iterable of values ONLY for the column whose data type
    is in question.

    :param column_data: Iterable of values from a MySQL table column
    :param prefer_varchar: Use type VARCHAR if valid
    :param prefer_int: Use type INT if valid
    :return: data type
    """
    # Collect list of type, length tuples
    type_len_pairs = [Record(record).get_type_len for record in column_data]

    # Retrieve frequency counts of each type
    types_count = {t: type_len_pairs.count(t) for t in set([t for t, l in type_len_pairs])}

    # Most frequently occurring datatype
    most_frequent = max(types_count.items(), key=itemgetter(1))[0]

    # Get max length of all rows to determine suitable limit
    try:
        max_len = max([l for t, l in type_len_pairs if t == most_frequent and type(l) is int])
    except ValueError:
        # Current type has no len
        max_len = None

    # Return VARCHAR or INT type if flag is on
    if prefer_varchar and most_frequent != 'VARCHAR' and 'text' in most_frequent.lower():
        most_frequent = 'VARCHAR'
    elif prefer_int and most_frequent != 'INT' and 'int' in most_frequent.lower():
        most_frequent = 'INT'

    # Return MySQL datatype in proper format, only include length if it is set
    return '{0} ({1})'.format(most_frequent, max_len) if max_len else most_frequent
