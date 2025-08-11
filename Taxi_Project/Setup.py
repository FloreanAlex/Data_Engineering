# Databricks notebook source
# MAGIC %sql
# MAGIC Create Volume workspace.raw.rawvolume

# COMMAND ----------

dbutils.fs.mkdirs("/Volumes/workspace/raw/rawvolume/taxidata")

# COMMAND ----------

# MAGIC %sql
# MAGIC Create Schema workspace.gold
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC Create Volume workspace.gold.goldvolume
