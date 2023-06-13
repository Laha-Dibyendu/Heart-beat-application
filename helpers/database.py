from pymongo import MongoClient
import configuration

connection_params = configuration.connection_params

#connect to mongodb
mongoconnection = MongoClient(
    'mongodb://{host}:'
    '{port}/?retryWrites=false'.format(**connection_params)
)


db = mongoconnection.databasename
