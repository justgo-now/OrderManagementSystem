# coding: UTF-8

from repast.models.database import *
from repast.models import *



if __name__ == '__main__':
    Base.metadata.create_all(engine)