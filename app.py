#!/usr/bin/env python
# coding: utf-8

import argparse
import renamer

def get_args():
    """
    Functions used to parse appilcation options

    return: the namespace containing the parsed arguments
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('path', type=str, nargs='?', default='.', help='Path of the directory from which to retrieve the items to be renamed')

    parser.add_argument('-e', '--element', choices=['FILE', 'FOLDER'], default='FILE', help='Select the type of item to rename (FILE by default)')
    parser.add_argument('-f', '--filter', action='store', type=str, default='*', help='Entry directory item selection filter (all by default)')
    parser.add_argument('-n', '--new-name', action='store', type=str, default='%N%', 
                        help='New element name format (%%N%% by default)' + 
                        '\nAvailable options :' + 
                        '\n\t%%N%% represents a 4-character numeric increment ' + 
                        '\n\t%%NA%% represents an increment whose format is automatically defined according to the number of elements to be renamed ' + 
                        '\n\t%%D%% represents a date in yymmdd format')
    parser.add_argument('-i', '--increment-start', action='store', type=int, default=1, help='Permet de définir sur quel entier doit démarrer l\'incrémentation du nom si il y en a un')

    group_sort = parser.add_mutually_exclusive_group()
    group_sort.add_argument('-s', '--sort', choices=['NAME', 'DATE', 'TYPE'], help='Sorting type')
    group_sort.add_argument('-r', '--reverse', choices=['NAME', 'DATE', 'TYPE'], help='Reverse sorting type')

    parser.add_argument('-p', '--preview', action='store_true', help='Show preview of renaming')

    return parser.parse_args()


ren = renamer.Renamer(get_args())
list_of_elements = ren.get_elements_from_repository()
if len(list_of_elements) > 0:
    list_of_elements = ren.sort_elements(list_of_elements)
    renamed_list = ren.generate_new_name(list_of_elements)
    ren.print_preview_or_rename_elements(renamed_list)
else:
    print('No elements were found according to the requested criteria.')