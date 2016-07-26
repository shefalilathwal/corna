import numpy as np


def zero_if_negative(num):
    """
    This function replaces negative numbers by zero_if_negative

    Args:
        num : any int value

    Return:
        1. zero if num is negative
        2. number itself if num is non negative
    """
    if num < 0:
        return 0
    return num


def replace_negative_to_zero(corrected_dict, replace_negative=True):
    """
    This function replaces negative intensity values by zero from list of intensity
    in the standardised model dictionary

    Args:
        corrected_dict : nested dictionary (std model) with NA corrected intensity values
        replace_negative :
                          1. if True, replaces negative values and updates the dictionary
                          2. if False, return the nested dictionary with corrected values
                             as it is
    Returns:
        post_proc_dict : returns nested dictionary with negative values replaced

    """
    if replace_negative == True:
        post_proc_dict = {}

        for frag_key, frag_info in corrected_dict.iteritems():
            sample_int_dict = frag_info[1]
            dict_replaced_vals = replace_vals(sample_int_dict)
            post_proc_dict[frag_key] = [
            frag_info[0], dict_replaced_vals, frag_info[2], frag_info[3]]

        return post_proc_dict

    elif replace_negative == False:
        return corrected_dict


def enrichment(fragments_dict, decimals):
    """
    This function calculates the fractional enrichment for each label
    Fractional enrichment[sample1] = Corrected Intensity/ Sum of corrected intensities of all labels

    Args:
        fragments_dict : dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']

        decimals : number of significant digits to keep

    Returns:
        fragments_fractional : fragment dictionary model of fractional enrichment values
    """
    fragments_fractional = {}
    sum_dict = sum_intensities(fragments_dict)

    for key, value in fragments_dict.iteritems():
        data = value[1]
        fractional_data = {}
        for sample_name, intensity in data.iteritems():
            if not sum_dict[sample_name] == 0:
                fractional_data[sample_name] = np.around(
                    intensity/sum_dict[sample_name], decimals)
            else:
                raise ValueError('sum of labels is zero for sample' + sample_name)
        fragments_fractional[key] = [value[0], fractional_data, value[2], value[3]]

    return fragments_fractional



def sum_intensities(fragments_dict):
    """
    This function calculates the sum of corrected intensities for a given sample

    Args:
        fragments_dict : dictionary of the form, example : {'Aceticacid_C13_1': [C2H4O2,
                         {'sample_1': array([ 0.0164])}, False, 'Aceticacid']
    Returns:
        sum_dict :  dictionary of sum of all corrected intensities for each sample
    """
    all_values = fragments_dict.values()
    sample_names = all_values[1][1].keys()
    sum_dict = {}

    for sample_name in sample_names:
        curr_arr = np.zeros(len(all_values[1][1][sample_name]))
        for value in all_values:
            curr_arr = curr_arr + value[1][sample_name]
        sum_dict[sample_name] = curr_arr

    return sum_dict


def replace_vals(sample_int_dict):
    """
    This function replace negatives by zero in sample intensity dictionary
    Args:
        sample_int_dict : dictionary with keys as samples and values as corrected intensities

    Returns:
        dict_replaced_vals : sample_int_dict with negative intensities replaced by zeroes
    """
    dict_replaced_vals = {}

    for sample, intensity_list in sample_int_dict.iteritems():
        intensity_list = map(zero_if_negative, intensity_list)
        dict_replaced_vals[sample] = np.array(intensity_list)

    return dict_replaced_vals





