'''
Script done by:
Bruno Lopes 202000210
Gonçalo Cachado 202000190
Ioana Chichirita 202000180
Rodrigo Silva 202000193
Samuel Correia 202000094
Turma: Binf21
'''
import sys
import glob

file_identifier = sys.argv[1]
file_extension = sys.argv[2]
pattern = file_identifier + ('*' + file_extension)

Peninsula = {
    'KITs' : ['1','Wauna','Joemma','PortTownsend'],
    'PUGn' : ['2', 'TulareBeach', 'CamanoIsland', 'Chuckanut','SpeeBiDah'],
    'KITw' : ['3', 'Belfair', 'Tahuya', 'Dewatto', 'Holly'],
    'OLY' : ['4', 'Duckabush', 'BeckettPoint', 'AndersonIsland', 'KetronIsland'],
    'PUGs' : ['5', 'CambersCreek', 'Burien', 'MauryIslandS', 'MauryIslandN','PointDefiance'] 

}


def find_files(pattern):
    '''
    Gets the pattern of the files through the parameter pattern.
    Searches for the all files containing the pattern (the file identifier and the file extension)
    and saves them in list files.
    The list containing all the files with a certain pattern (files) is returned
    '''
    files = glob.glob(pattern)
    return(files)

def get_seq_name_location(files):
    '''
    Gets the files list through the parameter files.
    The list files is iterated for each file. During the
    interation the file is split by the character '_'. The list
    seq_names appends the name of the sequence, seq_locations
    appends the locations.
    The list of names and locations are returned by the respective:
    seq_names and seq_locations
    '''
    seq_names = []
    seq_locations = []
    for file in files:
        file = file.replace('.fastq','')
        file  = file.split('_')
        seq_names.append(file[3] + '_' + file[4])
        seq_locations.append(file[2] + '_' + file[0])
    return(seq_names,seq_locations)

def line_count_normalizer(seq_names, seq_locations):
    '''
    Gets the lists of names and locations through the respective
    paramenters: seq_names, seq_locations.
    Creation of two lists using seq_names and seq_locations: 
    seq_names_length and seq_locations_length, containing the size of each name and location.
    Creation of two lists using seq_names_length and seq_locations_length:
    seq_names_normalize_length, seq_locations_normalize_length, containing the
    values necessary to make each name and location equal to the largest 
    name and location in seq_names_length and seq_locations_length.
    The lists of values to reach max size of names and locations are returned by
    seq_names_normalize_length and seq_locations_normalize_length.
    '''
    seq_names_length = [len(x) for x in seq_names]
    seq_locations_length = [len(x) for x in seq_locations]
    max_seq_names_length = max(seq_names_length)
    max_seq_locations_length = max(seq_locations_length)
    seq_names_normalize_length = [(max_seq_names_length - x) for x in seq_names_length]
    seq_locations_normalize_length = [(max_seq_locations_length - x) for x in seq_locations_length]
    return(seq_names_normalize_length, seq_locations_normalize_length)

def localization(seq_location, seq_locations_normalize_length, count_name):
    '''
    Gets a location, its value to reach the largest location size and
    the index of seq_locations_normalize_length corresponding to the seq_location
    through the paramenters: seq_location, seq_locations_normalize_length, count_name.
    The dict Peninsula is iterated by its keys.
    The list of values of the key is saved in the variable location_list. 
    If seq_location.replace('_WA','') is a value in location_list, seq_location is 
    changed to the size of the largest location in seq_locations using white space(' '). 
    seq_location also receives the id (value of the first element of location_list) of the 
    corresponding key.
    The normalized and transformed seq_location is returned.
    '''
    for key in Peninsula.keys():
        location_list = Peninsula[key]
        if(seq_location.replace('_WA','') in location_list):
            seq_location = seq_location + ' ' + ' ' * seq_locations_normalize_length[count_name] + location_list[0]
    return(seq_location)

def indfile_transformer(seq_names,seq_locations,seq_names_normalize_length, seq_locations_normalize_length):
    '''
    Receives the list of names, locations, values to make names size
    equal to the largest name and values to make locations size equal to
    the largest location through the parameters: seq_names, seq_locations,
    seq_names_normalize_length, seq_locations_normalize_length.
    seq_names is iterated by its names (seq_name).
    seq_name is changed to the size of the largest name in seq_names using 
    white space(' ').
    The location of the name is acquired by the respective index in 
    seq_locations.
    the location (seq_location) is transformed.
    The seq_name and location is grouped to form a line saved in the variable
    line.
    All the lines are added together in the variable all_lines.
    The string containing all the lines (all_lines) is returned
    '''
    count_name = 0
    all_lines = ''
    for seq_name in seq_names:
        seq_name = seq_name + ' ' * seq_names_normalize_length[count_name]
        seq_location = seq_locations[count_name]
        seq_location = localization(seq_location,  seq_locations_normalize_length, count_name)
        line = seq_name + ' ' + seq_location + '\n'
        all_lines = all_lines + line
        count_name += 1
    return(all_lines)

def create_indfile (all_lines):
    '''
    The content to write in the .indfile is passed through 
    the parameter all_lines.
    The Sceloporus occidentalis.indfile is created and opened.
    The content (all_lines) is written in the file and then
    the file closes.
    '''
    indfile = open("Sceloporus occidentalis.indfile","w+")
    indfile.write(all_lines)
    indfile.close


files = find_files(pattern)

seq_names, seq_locations = get_seq_name_location(files)
seq_names_normalize_length, seq_locations_normalize_length = line_count_normalizer(seq_names, seq_locations)
all_lines = indfile_transformer(seq_names, seq_locations, seq_names_normalize_length, seq_locations_normalize_length)

create_indfile(all_lines)





