CSV File utilizing a ~ delimiter that stores a pandas dataframe containing data regarding NJ real estate.
File Format
0,           1,     2,       3,      4, ......... 58,                      59
photo links, price, address, features ........... zillow link to property, zillow link to initial search (debugging reasons)

(note that feature columns contain a string representing a several features under a specific category)
(note that each feature in the string is separated by '||')
(example of a feature value in the csv. bedrooms & bathrooms||bedrooms: 1||bathrooms: 1||full bathrooms: 1)
