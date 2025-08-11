# Databricks notebook source


# COMMAND ----------

taxi_types = [
    {"type": "yellow"},
    {"type": "green"},
    {"type": "fhv"},
    {"type": "fhvhv"}
]

# COMMAND ----------

dbutils.jobs.taskValues.set(key="types_key", value=taxi_types)
