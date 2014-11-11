import urllib2
import json
import locale
import base64

locale.setlocale(locale.LC_ALL, '')

# Request an api key at http://api.census.gov/data/key_signup.html
key = open("key.txt", "r").read().strip()
# Global variable QUERY_CATEGORIES to keep track of index of categories in JSON result
QUERY_CATEGORIES = []

###### Constants ######

### States ###
# Reference: http://api.census.gov/data/2010/sf1?key=%s&get=NAME&for=state:*
STATES = {
        1: 'Alabama',
        2: 'Alaska',
        3: '',
        4: 'Arizona',
        5: 'Arkansas',
        6: 'California',
        7: '',
        8: 'Colorado',
        9: 'Connecticut',
        10: 'Delaware',
        11: 'District of Columbia',
        12: 'Florida',
        13: 'Georgia',
        14: '',
        15: 'Hawaii',
        16: 'Idaho',
        17: 'Illinois',
        18: 'Indiana',
        19: 'Iowa',
        20: 'Kansas',
        21: 'Kentucky',
        22: 'Louisiana',
        23: 'Maine',
        24: 'Maryland',
        25: 'Massachusetts',
        26: 'Michigan',
        27: 'Minnesota',
        28: 'Mississippi',
        29: 'Missouri',
        30: 'Montana',
        31: 'Nebraska',
        32: 'Nevada',
        33: 'New Hampshire',
        34: 'New Jersey',
        35: 'New Mexico',
        36: 'New York',
        37: 'North Carolina',
        38: 'North Dakota',
        39: 'Ohio',
        40: 'Oklahoma',
        41: 'Oregon',
        42: 'Pennsylvania',
        43: '',
        44: 'Rhode Island',
        45: 'South Carolina',
        46: 'South Dakota',
        47: 'Tennessee',
        48: 'Texas',
        49: 'Utah',
        50: 'Vermont',
        51: 'Virginia',
        53: 'Washington',
        54: 'West Virginia',
        55: 'Wisconsin',
        56: 'Wyoming',
        57: '',
        58: '',
        59: '',
        60: '',
        61: '',
        62: '',
        63: '',
        64: '',
        65: '',
        66: '',
        67: '',
        68: '',
        69: '',
        70: '',
        71: '',
        72: 'Puerto Rico'
}

### Categories ###
# Reference http://api.census.gov/data/2010/sf1/variables.html
NAME = 'NAME'
TOTAL_POPULATION = 'P0010001'
TOTAL_POPULATION_WHITES = 'P0080003'
TOTAL_POPULATION_BLACKS = 'P0080004'
TOTAL_POPULATION_ASIANS = 'P0080006'
TOTAL_POPULATION_18_OR_OVER = 'P0100001'
MALE = 'P0120002'
HOUSEHOLDS = 'PCT0140001'
HOUSEHOLD_THREE_OR_MORE_GENERATIONS = 'PCT0140002'
HOUSEHOLD_NOT_THREE_OR_MORE_GENERATIONS = 'PCT0140003'
HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE = 'PCT014A001'
HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014A002'
HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014A003'
HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE = 'PCT014B001'
HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014B002'
HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014B003'
HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE = 'PCT014C001'
HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014C002'
HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014C003'
HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE = 'PCT014D001'
HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014D002'
HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014D003'
HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE = 'PCT014E001'
HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014E002'
HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014E003'
HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE = 'PCT014F001'
HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014F002'
HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014F003'
HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES = 'PCT014G001'
HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES_THREE_OR_MORE_GENERATIONS = 'PCT014G002'
HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014G003'
HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE = 'PCT014H001'
HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE_THREE_OR_MORE_GENERATIONS = 'PCT014H002'
HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE_NOT_THREE_OR_MORE_GENERATIONS = 'PCT014H003'
HOUSEHOLDS_HUSBAND_WIFE = 'PCT0150002'
HOUSEHOLDS_HUSBAND_WIFE_MALE_HOUSEHOLDER = 'PCT0150003'
HOUSEHOLDS_FAMILY = 'PCT0160002'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE = 'PCT0160003'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE_NO_CHILDREN_UNDER_18 = 'PCT0160004'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE_ONE_CHILD_UNDER_18 = 'PCT0160005'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE_TWO_CHILDREN_UNDER_18 = 'PCT0160006'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE_THREE_CHILDREN_UNDER_18 = 'PCT0160007'
HOUSEHOLDS_FAMILY_HUSBAND_WIFE_FOUR_OR_MORE_CHILDREN_UNDER_18 = 'PCT0160008'
HOUSING_UNITS = 'H00010001'
HOUSING_UNITS_OCCUPIED = 'H0030002'
HOUSING_UNITS_VACANT = 'H0030003'
HOUSING_UNITS_FOR_RENT = 'H0050002'
HOUSING_UNITS_FOR_SALE = 'H0050004'
HOUSING_UNITS_FOR_SEASONAL_RECREATIONAL_OR_OCCASIONAL_USE = 'H0050006'
HOUSING_UNITS_FOR_MIGRANT_WORKERS = 'H0050007'
HOUSING_UNITS_OCCUPIED_POPULATION = 'H0100001'
MALE_UNDER_5_YEARS = 'P0120003'
MALE_5_TO_9_YEARS = 'P0120004'
MALE_10_TO_14_YEARS = 'P0120005'
MALE_15_TO_17_YEARS = 'P0120006'
MALE_18_TO_19_YEARS = 'P0120007'
MALE_20_YEARS = 'P0120008'
MALE_21_YEARS = 'P0120009'
MALE_22_TO_24_YEARS = 'P0120010'
MALE_25_TO_29_YEARS = 'P0120011'
MALE_30_TO_34_YEARS = 'P0120012'
MALE_35_TO_39_YEARS = 'P0120013'
MALE_40_TO_44_YEARS = 'P0120014'
MALE_45_TO_49_YEARS = 'P0120015'
MALE_50_TO_54_YEARS = 'P0120016'
MALE_55_TO_59_YEARS = 'P0120017'
MALE_60_TO_61_YEARS = 'P0120018'
MALE_62_TO_64_YEARS = 'P0120019'
MALE_65_TO_66_YEARS = 'P0120020'
MALE_67_TO_69_YEARS = 'P0120021'
MALE_70_TO_74_YEARS = 'P0120022'
MALE_75_TO_79_YEARS = 'P0120023'
MALE_80_TO_84_YEARS = 'P0120024'
MALE_85_YEARS_AND_OVER = 'P0120025'
FEMALE_UNDER_5_YEARS = 'P0120027'
FEMALE_5_TO_9_YEARS = 'P0120028'
FEMALE_10_TO_14_YEARS = 'P0120029'
FEMALE_15_TO_17_YEARS = 'P0120030'
FEMALE_18_TO_19_YEARS = 'P0120031'
FEMALE_20_YEARS = 'P0120032'
FEMALE_21_YEARS = 'P0120033'
FEMALE_22_TO_24_YEARS = 'P0120034'
FEMALE_25_TO_29_YEARS = 'P0120035'
FEMALE_30_TO_34_YEARS = 'P0120036'
FEMALE_35_TO_39_YEARS = 'P0120037'
FEMALE_40_TO_44_YEARS = 'P0120038'
FEMALE_45_TO_49_YEARS = 'P0120039'
FEMALE_50_TO_54_YEARS = 'P0120040'
FEMALE_55_TO_59_YEARS = 'P0120041'
FEMALE_60_TO_61_YEARS = 'P0120042'
FEMALE_62_TO_64_YEARS = 'P0120043'
FEMALE_65_TO_66_YEARS = 'P0120044'
FEMALE_67_TO_69_YEARS = 'P0120045'
FEMALE_70_TO_74_YEARS = 'P0120046'
FEMALE_75_TO_79_YEARS = 'P0120047'
FEMALE_80_TO_84_YEARS = 'P0120048'
FEMALE_85_YEARS_AND_OVER = 'P0120049'


CATEGORY_FULLNAMES = {
        NAME : "State Name",
        TOTAL_POPULATION : "Total Population",
        TOTAL_POPULATION_WHITES : "Total Population (Whites)",
        TOTAL_POPULATION_BLACKS : "Total Population (Blacks)",
        TOTAL_POPULATION_ASIANS : "Total Population (Asians)",
        TOTAL_POPULATION_18_OR_OVER : "Total Population (18+)",
        MALE : "Male",
        HOUSEHOLDS : "Households",
        HOUSEHOLD_THREE_OR_MORE_GENERATIONS : "Households(3+ Generations)",
        HOUSEHOLD_NOT_THREE_OR_MORE_GENERATIONS : "Households(NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE : "Households(Householder White ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder White ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_WHITE_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder White ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE : "Households(Householder Black/African American ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder Black/African American ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_BLACK_OR_AFRICAN_AMERICAN_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Black/African American ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE : "Households(Householder American Indian/Alaska Native ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder American Indian/Alaska Native ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_AMERICAN_INDIAN_AND_ALASKA_NATIVE_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder American Indian/Alaska Native ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE : "Households(Householder Asian ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder Asian ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_ASIAN_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Asian ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE : "Households(Householder Native Hawaiian/Other Pacific Islander ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder Native Hawaiian/Other Pacific Islander ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_NATIVE_HAWAIIAN_AND_OTHER_PACIFIC_ISLANDER_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Native Hawaiian/Other Pacific Islander ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE : "Households(Householder Other Race ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder Other Race ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_OTHER_RACE_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Other Race ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES : "Households(Householder Two or More Races ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES_THREE_OR_MORE_GENERATIONS : "Households(Householder Two or More Races ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_TWO_OR_MORE_RACES_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Two or More Races ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE : "Households(Householder Hispanic/Latino ALONE)",
        HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE_THREE_OR_MORE_GENERATIONS : "Households(Householder Hispanic/Latino ALONE, 3+ Generations)",
        HOUSEHOLDS_HOUSEHOLDER_HISPANIC_OR_LATINO_ALONE_NOT_THREE_OR_MORE_GENERATIONS : "Households(Householder Hispanic/Latino ALONE, NOT 3+ Generations)",
        HOUSEHOLDS_HUSBAND_WIFE : "Households(Husband-Wife)",
        HOUSEHOLDS_HUSBAND_WIFE_MALE_HOUSEHOLDER : "Households(Husband-Wife, Male Householder)",
        HOUSEHOLDS_FAMILY : "Households(Family)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE : "Households(Family, Husband-Wife)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE_NO_CHILDREN_UNDER_18 : "Households(Family, Husband-Wife, No children under 18)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE_ONE_CHILD_UNDER_18 : "Households(Family, Husband-Wife, One child under 18)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE_TWO_CHILDREN_UNDER_18 : "Households(Family, Husband-Wife, Two children under 18)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE_THREE_CHILDREN_UNDER_18 : "Households(Family, Husband-Wife, Three children under 18)",
        HOUSEHOLDS_FAMILY_HUSBAND_WIFE_FOUR_OR_MORE_CHILDREN_UNDER_18 : "Households(Family, Husband-Wife, Four or more children under 18)",
        HOUSING_UNITS : "Total Housing Units",
        HOUSING_UNITS_OCCUPIED : "Total Housing Units (Occupied)",
        HOUSING_UNITS_VACANT : "Total Housing Units (Vacant)",
        HOUSING_UNITS_FOR_RENT : "Total Housing Units (For Rent)",
        HOUSING_UNITS_FOR_SALE : "Total Housing Units (For Sale)" ,
        HOUSING_UNITS_FOR_SEASONAL_RECREATIONAL_OR_OCCASIONAL_USE : "Total Housing Units (For Seasonal, Recreational, or Occasional Use)",
        HOUSING_UNITS_FOR_MIGRANT_WORKERS : "Total Housing Units (For Migrant Workers)",
        HOUSING_UNITS_OCCUPIED_POPULATION : "Total Occupied Population of Housing Units",
        MALE_UNDER_5_YEARS : "Male (Under 5 Years)",
        MALE_5_TO_9_YEARS : "Male (5 to 9 Years)",
        MALE_10_TO_14_YEARS : "Male (10 to 14 Years)",
        MALE_15_TO_17_YEARS : "Male (15 to 17 Years)",
        MALE_18_TO_19_YEARS : "Male (18 to 19 Years)",
        MALE_20_YEARS : "Male (20 Years)",
        MALE_21_YEARS : "Male (21 Years)",
        MALE_22_TO_24_YEARS : "Male (22 to 24 Years)",
        MALE_25_TO_29_YEARS : "Male (25 to 29 Years)",
        MALE_30_TO_34_YEARS : "Male (30 to 34 Years)",
        MALE_35_TO_39_YEARS : "Male (35 to 39 Years)",
        MALE_40_TO_44_YEARS : "Male (40 to 44 Years)",
        MALE_45_TO_49_YEARS : "Male (45 to 49 Years)",
        MALE_50_TO_54_YEARS : "Male (50 to 54 Years)",
        MALE_55_TO_59_YEARS : "Male (55 to 59 Years)",
        MALE_60_TO_61_YEARS : "Male (60 to 61 Years)",
        MALE_62_TO_64_YEARS : "Male (62 to 64 Years)",
        MALE_65_TO_66_YEARS : "Male (65 to 66 Years)",
        MALE_67_TO_69_YEARS : "Male (67 to 69 Years)",
        MALE_70_TO_74_YEARS : "Male (70 to 74 Years)",
        MALE_75_TO_79_YEARS : "Male (75 to 79 Years)",
        MALE_80_TO_84_YEARS : "Male (80 to 84 Years)",
        MALE_85_YEARS_AND_OVER : "Male (85+ Years)",
        FEMALE_UNDER_5_YEARS : "Female (Under 5 Years)",
        FEMALE_5_TO_9_YEARS : "Female (5 to 9 Years)",
        FEMALE_10_TO_14_YEARS : "Female (10 to 14 Years)",
        FEMALE_15_TO_17_YEARS : "Female (15 to 17 Years)",
        FEMALE_18_TO_19_YEARS : "Female (18 to 19 Years)",
        FEMALE_20_YEARS : "Female (20 Years)",
        FEMALE_21_YEARS : "Female (21 Years)",
        FEMALE_22_TO_24_YEARS : "Female (22 to 24 Years)",
        FEMALE_25_TO_29_YEARS : "Female (25 to 29 Years)",
        FEMALE_30_TO_34_YEARS : "Female (30 to 34 Years)",
        FEMALE_35_TO_39_YEARS : "Female (35 to 39 Years)",
        FEMALE_40_TO_44_YEARS : "Female (40 to 44 Years)",
        FEMALE_45_TO_49_YEARS : "Female (45 to 49 Years)",
        FEMALE_50_TO_54_YEARS : "Female (50 to 54 Years)",
        FEMALE_55_TO_59_YEARS : "Female (55 to 59 Years)",
        FEMALE_60_TO_61_YEARS : "Female (60 to 61 Years)",
        FEMALE_62_TO_64_YEARS : "Female (62 to 64 Years)",
        FEMALE_65_TO_66_YEARS : "Female (65 to 66 Years)",
        FEMALE_67_TO_69_YEARS : "Female (67 to 69 Years)",
        FEMALE_70_TO_74_YEARS : "Female (70 to 74 Years)",
        FEMALE_75_TO_79_YEARS : "Female (75 to 79 Years)",
        FEMALE_80_TO_84_YEARS : "Female (80 to 84 Years)",
        FEMALE_85_YEARS_AND_OVER : "Female (85+ Years)"
}

def sortBy(data, category):
    ''' Sort data by a category '''
    index = QUERY_CATEGORIES.index(category)
    isInt = False
    try:
        i = int(data[0][index])
        isInt = True
        print "Category is int"
    except ValueError:
        print "Category is not int"

    if isInt:
        # Reverse sort to sort descending
        return sorted(data, key=lambda state:int(state[index]), reverse=True)
    else:
        # No reverse sort to sort alphabetically
        return sorted(data, key=lambda state:state[index])

def top10(data, category):
    ''' Get top 10 states/values in a category '''
    data = sortBy(data, category)
    return data[:10]

def categoryValueForState(data, category, stateIndex):
    ''' Get value of category for state '''
    index = QUERY_CATEGORIES.index(category)
    for row in data:
        # row[-1] should always be the state index
        if (int(row[-1]) == stateIndex):
            return row[index]
    return None

def average(data, category):
    ''' Get average(arithmetic mean) for category '''
    index = QUERY_CATEGORIES.index(category)
    runningSum = 0
    for row in data:
        try:
            runningSum += int(row[index])
        except ValueError:
            return None
    return runningSum / len(data)

def median(data, category):
    ''' Get median for category '''
    index = QUERY_CATEGORIES.index(category)
    data = sortBy(data, category)
    try:
        if len(data) % 2 == 0:
            return 0.5 * int(data[len(data) / 2 - 1][index]) + int(data[len(data) / 2][index])
        else:
            return (data[len(data) / 2 - 1][index])
    except ValueError:
        return None

'''
# Commification to be done in front-end after generating bars
def commify(data):
    try:
        return format(int(data), "n")
    except ValueError:
        return None
'''

def indexForState(s):
    ''' Get state index given state name '''
    return STATES.values().index(s) + 1

def getJSON(categories):
    ''' Get JSON data '''
    if type(categories) != list: 
        raise Exception("getJSON(categories): List expected for argument categories. Got %s instead." % type(categories))
    global QUERY_CATEGORIES
    QUERY_CATEGORIES = categories
    url_base = "http://api.census.gov/data/2010/sf1?key=%s" % key
    url_query = "&get=%s&for=state:*" % ','.join(QUERY_CATEGORIES)
    # index 0 contains the query categories metadata, so we can ignore it
    return json.loads(urllib2.urlopen(url_base + url_query).read())[1:]

def getSummary(state, categories):
    ''' Get summary of data for categories '''
    if type(categories) != list: 
        raise Exception("getSummary(state, categories): List expected for argument categories. Got %s instead." % type(categories))
    data_dict = getJSON(categories) 
    stateIndex = indexForState(state)
    summary = {}
    summary['STATE'] = state
    summary['STATE_VALUES'] = []
    summary['CATEGORIES'] = []
    summary['AVERAGE_VALUES'] = []
    summary['MEDIAN_VALUES'] = []
    summary['TOP_10_VALUES'] = []
    summary['JS_BAR_GRAPH_COMPARE_WITH_AVERAGE_MEDIAN'] = []
    summary['JS_BAR_GRAPH_TOP_10'] = []
    chart_id_prefix_average_median = "a" 
    chart_id_prefix_top_10 = "b"
    iteration = 0
    for category in categories:
        iteration += 1
        category_name = CATEGORY_FULLNAMES[category]
        category_value = categoryValueForState(data_dict, category, stateIndex)
        average_value = average(data_dict, category)
        median_value = median(data_dict, category)
        top_10_values = top10(data_dict, category)
        states_names = []
        states_values = []
        category_index = QUERY_CATEGORIES.index(category)
        for state in top_10_values:
            states_names.append(STATES[int(state[-1])])
            states_values.append(state[category_index])
        summary['CATEGORIES'].append(category_name)
        summary['STATE_VALUES'].append(category_value)
        summary['AVERAGE_VALUES'].append(average_value)
        summary['MEDIAN_VALUES'].append(median_value)
        summary['TOP_10_VALUES'].append(top_10_values)
        summary['JS_BAR_GRAPH_COMPARE_WITH_AVERAGE_MEDIAN'].append(generateBarGraphJS_compare_average_median(chart_id_prefix_average_median + str(iteration), category_name, category_value, average_value, median_value))
        summary['JS_BAR_GRAPH_TOP_10'].append(generateBarGraphJS_top_10(chart_id_prefix_top_10+ str(iteration), category_name, states_names, states_values))
    substituteStateNames(summary)
    return summary

def substituteStateNames(summary):
    ''' Replace state indices with state names '''
    for i, category_values in enumerate(summary['TOP_10_VALUES']):
        for u, values in enumerate(category_values):
            try:
                category_values[u][-1] = STATES[int(values[-1])]
            except ValueError:
                pass

def generateBarGraphJS_compare_average_median(chart_id, category, category_value_for_this_state, average_value, median_value):
    script = """
    <canvas id="{chart_id}" width="500" height="500"></canvas>
    <script>
        var ctx = document.getElementById("{chart_id}").getContext("2d");
        var data = {{
            labels: [\"{label}\", "Average", "Median"],
            datasets: [
                {{
                    label: "",
                    fillColor: "rgba(220,220,220,0.5)",
                    strokeColor: "rgba(200,200,200,0.5)",
                    highlightFill: "rgba(26, 188, 156, 1)",
                    highlightStroke: "rgba(26, 188, 156, 0.7)",
                    data: [{this_state}, {average_value}, {median_value}]
                }}
            ]
        }};
        var {chart_id} = new Chart(ctx).Bar(data);
    </script>
    """
    return script.format(chart_id=chart_id,\
                         label=category,\
                         this_state=category_value_for_this_state,\
                         average_value=average_value,\
                         median_value=median_value)

def generateBarGraphJS_top_10(chart_id, category, states, states_values):
    script = """
    <canvas id="{chart_id}" width="500" height="500"></canvas>
    <script>
        var ctx = document.getElementById("{chart_id}").getContext("2d");
        var data = {{
            labels: [\"{labels}\"],
            datasets: [
                {{
                    label: "{category}",
                    fillColor: "rgba(220,220,220,0.5)",
                    strokeColor: "rgba(220,220,220,0.3)",
                    highlightFill: "rgba(52, 152, 219, 1)",
                    highlightStroke: "rgba(52, 152, 219, 0.6)",
                    data: [\"{states_values}\"]
                }}
            ]
        }};
        var {chart_id} = new Chart(ctx).Bar(data);
    </script>
    """
    return script.format(chart_id=chart_id,\
                         category=category,\
                         labels="\", \"".join(states),\
                         states_values="\", \"".join(states_values))


if __name__ == "__main__":
    dict = getSummary("New York", [TOTAL_POPULATION, HOUSEHOLDS])
    print dict

