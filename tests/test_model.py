from __future__ import print_function
import pytest

from corna.model import Ion
from corna.model import Label
from corna.model import Fragment
from corna.model import LabelmetabIon

class TestIonClass:

    @classmethod
    def setup_class(cls):
        cls.ion = Ion('Glucose', 'C6H12O6', -1)
        cls.ion_err = Ion('OrganicCompund', 'CH2R', 0)

    @classmethod
    def teardown_class(cls):
        del cls.ion

    def test_get_formula(self):
        assert self.ion.get_formula() == {'C':6, 'H':12, 'O':6}

    def test_number_of_atoms(self):
        assert self.ion.number_of_atoms('C') == 6

    def test_number_of_atoms_wildcard(self):
        with pytest.raises(KeyError):
            self.ion.number_of_atoms('N')

    def test_molecular_weight(self):
        assert self.ion.get_mol_weight() == 180.15588

    def test_molecular_weight_wildcard(self):
        with pytest.raises(KeyError):
            self.ion_err.get_mol_weight()

class TestLabelClass:

    @classmethod
    def setup_class(cls):
        cls.label = Label()

    @classmethod
    def teardown_class(cls):
        del cls.label

    def test_validity_of_isotopes(self):
        assert self.label.check_if_valid_isotope(['C13', 'N15']) == True

    def test_validity_of_isotopes_wildcard(self):
        with pytest.raises(KeyError):
            self.label.check_if_valid_isotope(['C13', 'N15', 'K10'])

    def test_get_number_of_labeled_atoms(self):
        assert self.label.get_num_labeled_atoms('C13', {'C13':3, 'N15':3}) == 3

    def test_get_number_of_labeled_atoms_wildcard(self):
        with pytest.raises(KeyError) as err:
            self.label.get_num_labeled_atoms('C14', {'C13':2, 'N15':3})
        assert err.value.message == 'Isotope not present in label dictionary'

    def test_check_for_number_atoms_zero(self):
        assert self.label.get_num_labeled_atoms('C12', {'C12':2}) == 0

    def test_number_of_label_from_mass(self):
        assert self.label.get_label_from_mass('C13', 192.124, 198) == 6

    def test_number_of_label_from_mass_natural_form(self):
        assert self.label.get_label_from_mass('C12', 192, 192) == 0

class TestFragmentClass:
    @classmethod
    def setup_class(cls):
        cls.glu = LabelmetabIon()
        cls.fragment = Fragment('Glucose', 'C6H12O6', -1, {'C':2}, cls.glu)
        cls.fragment_err_lab_ele = Fragment('Glucose', 'C6H12O6', -1, {'C':2, 'N':3}, cls.glu)
        cls.fragment_err_lab_number = Fragment('Glucose', 'C6H12O6', -1, {'C':7}, cls.glu)

    @classmethod
    def teardown_class(cls):
        del cls.fragment
        del cls.fragment_err_lab_ele
        del cls.fragment_err_lab_number

    def test_fragment_sensible_label(self):
        assert self.fragment.sensible_label() == True

    def test_fragment_sensible_label_wildcard(self):
        with pytest.raises(KeyError) as err:
            self.fragment_err_lab_ele.sensible_label()
        assert err.value.message == 'Labeled element not in formula'

    def test_fragment_sensible_label_number(self):
        with pytest.raises(OverflowError) as err:
            self.fragment_err_lab_number.sensible_label()
        assert err.value.message == 'Number of labeled atoms must be' \
                                    ' less than total number of atoms' \
                                    ' and greater than zero'
