import pytest
import json
from django.db.utils import IntegrityError
from rest_framework.test import APIClient

from tariffs.models import Distributor
from universities.models import University

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

ENDPOINT = '/api/distributors/'

@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])

        self.distributor_for_create = {
            'name': 'Distribuidora',
            'cnpj': '00038174000143',
            'university': self.university.id
        }

    def test_creates_distributor(self):
        response = self.client.post(ENDPOINT, self.distributor_for_create)

        created_distributor = json.loads(response.content)

        assert 'Distribuidora' == created_distributor['name']
    
    def test_can_create_the_same_distributor_for_different_unitversities(self):
        dis_1 = {'name': 'Dis 1', 'cnpj': '00038174000143', 'university_id': self.university.id}
        dis_2 = {'name': 'Dis 2', 'cnpj': '00038174000143', 'university_id': self.university.id}
        univ_2 = {'name': 'Universidade de Brasília', 'cnpj': '00038174000143'}

        University.objects.create(**univ_2)

        Distributor.objects.create(**dis_1)
        with pytest.raises(IntegrityError):
            Distributor.objects.create(**dis_2)

    def test_can_create_distributors_for_different_universities(self):
        university_2 = University.objects.create(name='Universidade de Brasília', cnpj='00038174000143')
        
        dis_1 = {'name': 'Dis 1', 'cnpj': '01083200000118', 'university': self.university}
        dis_2 = {'name': 'Dis 2', 'cnpj': '01083200000118', 'university': university_2}

        Distributor.objects.create(**dis_1)
        Distributor.objects.create(**dis_2)

    def test_name_tamanho_min_e_max(self):
        dis_1 = {'name': '', 'cnpj': '75501604000110', 'university_id': self.university.id}
        dis_2 = {'name': None, 'cnpj': '47457781000101', 'university_id': self.university.id}
        dis_3 = {'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'cnpj': '43509384000185', 'university_id': self.university.id}
        dis_4 = {'name': 'CEB Energia', 'cnpj': '38131740000130', 'university_id': self.university.id}

        Distributor.objects.create(**dis_4)
        with pytest.raises(IntegrityError):
            Distributor.objects.create(**dis_1)
            Distributor.objects.create(**dis_2)
            Distributor.objects.create(**dis_3)
