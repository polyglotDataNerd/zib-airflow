#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'gbartolome'

from datetime import datetime
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

# base DAG
baseDAG = DAG('yelp-DAG',
              description='runs yelp DAG',
              schedule_interval='30 07 * * *',
              start_date=datetime(2020, 3, 23),
              catchup=False)

start = DummyOperator(task_id='yelp-Loader-start',
                      dag=baseDAG)
end = DummyOperator(task_id='yelp-Loader-end',
                    dag=baseDAG)

path = "/usr/local/airflow/bash/yelp_ecs_ETL.sh"
if os.path.exists(path):
    command = BashOperator(
        task_id='yelp',
        bash_command="sh {} ".format(path),
        dag=baseDAG,
    )
else:
    raise Exception("Cannot loacate{}".format(path))

start >> command >> end
