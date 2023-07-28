# coding: utf-8

import os
import glob
import logging

from datetime import date, datetime

# create logger
logger = logging.getLogger('renamer')

class Renamer:

    # ***************** #
    # Private variables #
    # ***************** #
    __path_directory = '.'
    __element_type_selected = 'FILE'
    __filter_name = '*'
    __format_name = '%N%'
    __increment_start = 1
    __sort_type = 'NAME'
    __show_preview = False


    # ************ #
    # Constructors #
    # ************ #
    def __init__(self):
        logger.debug("Default constructor")

    
    def __init__(self, args):
        logger.debug("Constructor taking input options as parameters")
        logger.debug(args)
        self.__path_directory = args.path
        self.__element_type_selected = args.element
        self.__filter_name = args.filter
        self.__format_name = args.new_name
        self.__increment_start = args.increment_start
        self.determines_the_sort_type(args.sort, args.reverse)
        self.__show_preview = args.preview


    # ***************** #
    # Getters & Setters #
    # ***************** #
    def get_path_directory(self):
        return self.__path_directory
    

    def set_path_directory(self, path):
        self.__path_directory = path
    

    def rename_files(self):
        return self.__element_type_selected == 'FILE'
    

    def set_element_type_selected(self, element_selected):
        self.__element_type_selected = element_selected
    

    def get_sort_type(self):
        return self.__sort_type


    def determines_the_sort_type(self, sort_type, reverse_sort_type):
        """
        Function used to define the type of sort desired by the user,
        in the case of reverse sorting, a lowercase r is added as a prefix to the sort type.
        By default, sorting will be based on element name and in ascending order.
        """
        logger.debug("Defining element sorting")
        if sort_type != None and reverse_sort_type == None:
            self.__sort_type = sort_type
        elif sort_type == None and reverse_sort_type != None:
            self.__sort_type = 'r' + reverse_sort_type
        else:
            self.__sort_type = 'NAME'


    def get_filter_name(self):
        return self.__filter_name


    def set_filter_name(self, filter):
        self.__filter_name = filter


    def get_format_name(self):
        return self.__format_name


    def set_format_name(self, format):
        self.__format_name = format


    def get_increment_start(self):
        return self.__increment_start


    def set_increment_start(self, increment_start):
        self.__increment_start = increment_start


    def show_preview(self):
        return self.__show_preview
    

    def determines_whether_a_preview_is_requested(self, preview):
        self.__show_preview = preview

    
    # ********* #
    # Functions #
    # ********* #
    def get_elements_from_repository(self):
        """
        Function using -p, -e and -f parameters to list items in selected directory (-p, default = current repository) according to item type (-e, default = FILE) and defined filter (-f, default = ALL element)

        return : list of selected elements
        """
        path = self.get_path_directory()
        list_of_elements = []

        if not os.path.exists(path):
            logger.error('The directory specified as script input does not exist')
            return None

        for filter in self.get_filter_name().split(';'):
            files = glob.glob(os.path.join(path, filter))

            for elem in files:
                if self.rename_files() == True and os.path.isfile(elem):
                    list_of_elements.append(elem)
                elif self.rename_files() == False and os.path.isdir(elem):
                    list_of_elements.append(elem)

        return list_of_elements
    

    def sort_elements(self, list_of_elements):
        """
        Function for sorting selected items according to the sort type passed as an application parameter.

        Parameters :
            list_of_elements : list of selected elements
        """
        reverse_sort = self.get_sort_type().startswith('r')

        if 'NAME' in self.get_sort_type():
            return sorted(list_of_elements, reverse=reverse_sort)
        elif 'DATE' in self.get_sort_type():
            return sorted(list_of_elements, key= lambda elem: self.__get_element_create_date(elem), reverse=reverse_sort)
        elif 'TYPE' in self.get_sort_type():
            return sorted(list_of_elements, key= lambda elem: self.__get_element_extension(elem), reverse=reverse_sort)

        return list_of_elements
    

    def __get_element_create_date(self, element):
        """
        Function that returns the creation date of the element passed in parameter.
        For Linux systems, this is the last modification date.

        Parameters :
            element : corresponds to a file or folder currently being processed
        
        return : element creation date
        """
        return datetime.fromtimestamp(os.stat(element).st_ctime)
    

    def __get_element_extension(self, element):
        """
        Function that returns the extension of the element passed in parameter, returns an empty string if there is none.

        Parameters :
            element : corresponds to a file or folder currently being processed
        
        return : element extension
        """
        return os.path.splitext(element)[1]
    

    def generate_new_name(self, list_of_elements):
        """
        Function used to generate new names for selected elements.

        Parameters :
            list_of_elements : list of selected elements
        
        return : tuple list containing the original element and the new name to be assigned to it
        """
        logger.debug('Generates new names for selected items according to the format specified in the program options')
        renamed_list = []
        today = str(date.today().strftime("%y%m%d"))
        increment_format = self.__generate_pattern_format_for_increment(len(list_of_elements))
        increment = self.get_increment_start()

        for i in range(0, len(list_of_elements)):
            element = list_of_elements[i]
            new_name = self.get_format_name() + self.__get_element_extension(element)
            if new_name != None and '%N%' in new_name:
                logger.debug('generate_new_name - increment insertion')
                new_name = new_name.replace('%N%', increment_format.format(increment), 1)
                increment += 1
            if '%NA%' in new_name:
                logger.debug('generate_new_name - automatic increment insertion')
                new_name = new_name.replace('%NA%', increment_format.format(increment), 1)
                increment += 1
            if '%D%' in new_name:
                logger.debug('generate_new_name - date insertion')
                new_name= new_name.replace('%D%', today)
            renamed_list.append((element, new_name))

        return renamed_list
    

    def __generate_pattern_format_for_increment(self, nb_element):
        """
        Function for generating the increment format, which defaults to 4 characters.
        For example, for a format corresponding to {:04}, an increment with a value of 24 would be written as '0024'.

        Parameters :
            nb_element : number of elements selected

        return : pattern format for increment
        """
        nb_carac_for_increment = 4
        if '%NA%' in self.get_format_name():
            i = 1
            is_ok = False
            while i < 10 and is_ok == False:
                max_elements = (10 ** i) - 1
                logger.debug(f'generate_pattern_format_for_increment - The maximum number of elements for a {i}-character format is {max_elements}.')
                if nb_element < max_elements:
                    logger.debug(f'generate_pattern_format_for_increment - the number of elements to be processed corresponds to a {i}-character format')
                    is_ok = True
                    nb_carac_for_increment = i
                i += 1
        return '{:0' + str(nb_carac_for_increment) + '}'

    
    def print_preview_or_rename_elements(self, renamed_list):
        """
        Function which, if preview is requested, displays in the console the correspondence between the old and new names of selected elements
        or rename them.

        Parameters :
            renamed_list : tuple list containing the original element and the new name to be assigned to it
        """
        arrow = '\033[1m\033[1;34m->\033[0m'
        if self.show_preview():
            logger.info('print_preview_or_rename_elements - Displaying transformations')
            for elem in renamed_list:
                old_name = os.path.basename(elem[0])
                logger.info(f'{old_name} (create date : {str(self.__get_element_create_date(elem[0]))}) -> {elem[1]}')
                print(f'{old_name} {arrow} {elem[1]}')
        else:
            logger.info('print_preview_or_rename_elements - The selected elements will be renamed according to the new format')
            for elem in renamed_list:
                old_name = elem[0]
                new_name = os.path.join(self.get_path_directory(), elem[1])
                os.rename(old_name, new_name)
                logger.info(f'{old_name} {arrow} {new_name}')
                print(f'{old_name} {arrow} {new_name}')