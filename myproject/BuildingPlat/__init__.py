#coding:utf8
from django.apps import AppConfig
import os
default_app_config = 'BuildingPlat.BuildingPaltConfig'
def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class BuildingPaltConfig(AppConfig):
    # name = get_current_app_name(__file__)
    name = 'BuildingPlat'
    verbose_name = "建筑信息"