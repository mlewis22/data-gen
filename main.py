'''
    A simple script that utilises components with the arcpy module to generate
    feature classes. Complete the config.json to indicate properties required.

    Required: ArcGIS Pro

    Licence: Apache License, Version 2.0 - http://www.apache.org/licenses/LICENSE-2.0

'''

import arcpy
import os
import json
import sys
import logging
from logging.handlers import RotatingFileHandler

def get_config(config_path=None):
    ''' gets a json config file and returns it as dict'''
    
    if config_path == None:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(current_directory, 'config.json')
    
    data = {}
    try:
        with open(config_path) as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("No Config file found")
        print(e)
        sys.exit(1)

def build_logger(level_str="INFO"):
    ''' build simple logger for application '''


    current_directory = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(current_directory, 'logs')
    
    ## build folder if doesnt exist
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    
    ## Set formating requirements
    level = logging.getLevelName(level_str)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

    logger = logging.getLogger("esri")
    logger.setLevel(level)

    ## build handler
    handler = RotatingFileHandler(
        log_path + '/output.log', maxBytes=2000, backupCount=10)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info(" ------------------ START ------------------ ")
    return logger



class Database(object):
    ''' builds an esri database connection file'''

    def __init__(self, dbtype="shapefile", properties={}):

        self.logger = logging.getLogger("esri") 
        self.type = dbtype
        self.properties = properties

        ## update folder path
        self._create_db_path()
    
    def _create_db_path(self):
        ''' private: checks to see if path to folder or DB is valid. 
            using variable "local" will create a connection file or shapefile in the
            same directory as the application. The code will look for a filegdb in that folder.
            Using an explicit path will result in the connection file being placed
            in that directory.
        '''
        
        if self.properties["folder_path"] == "local":
            self.properties["folder_path"] = os.path.dirname(os.path.realpath(__file__))
            self.logger.debug("using local directory to store db connection - " + str(self.properties["folder_path"]))

        return self.properties["folder_path"]



    def _check_existing(self):
        ''' check to see if an existing .sde database connection file exists with the same properties
            as the input.
        '''

        db_path = os.path.join(self.properties["folder_path"],self.properties["name"])
        if os.path.exists(db_path):
            self.logger.debug("remove old db connection")
            try:
                os.remove(db_path)
            except Exception as e:
                self.logger.error("failed to remove db connection file")
                self.logger.debug(e)
                raise Exception ("failed to remove db connection file")

        return db_path

    def _get_shapefile(self):
        ''' return a folder path '''

        if os.path.exists(self.properties["folder_path"]):
            return self.properties["folder_path"]
        else:
            self.logger.error("workspace path doesnt exist")
            raise Exception ("workspace path doesnt exist")

    def _get_filegdb(self):
        ''' return the filegdb path '''
        
        if os.path.exists(self.properties["folder_path"]):
            return os.path.join(self.properties["folder_path"], self.properties["name"])
        else:
            self.logger.error("workspace path doesnt exist")
            raise Exception ("workspace path doesnt exist")
        

    def get_workspace(self):
        ''' get database details  '''

        path = None 
        ## switch
        if self.type == "shapefile":
            path = self._get_shapefile()
        elif self.type == "filegdb":
            path = self._get_filegdb()
        elif self.type == "enterprise":
            path = self._get_ent_db()
        else:
            path = self._get_shapefile()

        return path

    def _get_ent_db(self):
        ''' creates an arcpy db connection file. Inputs are from esri documentation'''
            
        if self.properties["remove_existing"]:
            ## remove any old connection files
            self._check_existing()

            try:
                connection = arcpy.CreateDatabaseConnection_management(self.properties["folder_path"],
                                                        self.properties["name"],
                                                        self.properties["database_platform"],
                                                        self.properties["instance"],
                                                        self.properties["account_authentication"],
                                                        self.properties["username"],
                                                        self.properties["password"],
                                                        self.properties["save_user_pass"],
                                                        self.properties["database"],
                                                        self.properties["schema"],
                                                        self.properties["version_type"],
                                                        self.properties["version"],
                                                        self.properties["date"])
            except Exception as e:
                self.logger.error("failed to create connection file")
                self.logger.debug(e)
                raise Exception("failed to create connection file")
        else:
            self.logger.debug("keeping existing database connection")
        
        return os.path.join(self.properties["folder_path"], self.properties["name"])

        
class FeatureClass(object):
    ''' create an esri feature class'''

    def __init__(self, properties, fctype):
        self.logger = logging.getLogger("esri")
        self.type = fctype
        self.schema = properties["schema"]
        self.out_path = properties["out_path"]
        self.out_name = properties["out_name"]
        self.geometry_type = properties["geometry_type"]
        self.template = properties["template"]
        self.has_m = properties["has_m"]
        self.has_z = properties["has_z"]
        self.spatial_reference = self.get_sr(properties["spatial_reference"])
        self.config_keyword = properties["config_keyword"]
        self.spatial_grid_1 = properties["spatial_grid_1"]
        self.spatial_grid_2 = properties["spatial_grid_2"]
        self.spatial_grid_3 = properties["spatial_grid_3"]
        self.out_alias = properties["out_alias"]

    def get_sr(self, wkid=4326):
        ''' build arcpy spatial ref using wkid'''
        self.logger.debug("building spatial reference using wkid -" + str(wkid))
        try:
            sr = arcpy.SpatialReference(wkid)
        except Exception as e:
            self.logger.error("failed to create spatial reference")
            self.logger.debug(e)
            raise Exception ("failed to create spatial reference")
        return sr

    def _condence_fields(self):
        ''' cut field sizes to meet shapefile requiremenst '''

        previous = []
        count = 0
        for field in self.schema:
            ## Check if condensing field causes duplicate
            if field[0][:10] not in previous:
                field[0] = field[0][:10]
                previous.append(field[0])
            else:
                field[0] = field[0][:9] + str(count)
                previous.append(field[0])
                count += 1
      
    def _remove_existing(self):
        ''' remove any existing feature classes'''

        arcpy.env.workspace = self.out_path
        try:

            if arcpy.Exists(self.out_name):
                self.logger.debug("Removing existing feature class - " + str(self.out_name))

                try:
                    arcpy.Delete_management(self.out_name)
                except Exception as e:
                    self.logger.error("unable to delete feature class")
                    self.logger.debug(e)
                    raise Exception("unable to delete feature class")

        except Exception as e:
            self.logger.error("remove_existing Failed: Unable to check or remove existing data.")
            self.logger.debug(e)
            raise Exception("remove_existing Failed: Unable to check or remove existing data.")

    def _create_fields(self):
        ''' create fields for feature class '''

        print (".... Creating Fields")
        self.logger.debug("creating fields")
        arcpy.env.workspace = self.out_path

        try:
            arcpy.management.AddFields(self.out_name, self.schema)
        except Exception as e:
            self.logger.error("failed to create fields for feature class - " + self.out_name)
            self.logger.debug(e)
            raise Exception("failed to create fields for feature class - " + self.out_name)

    def create(self):
        ''' call to begin creating a feature class'''
        
        # append shapefile extention
        if self.type == "shapefile":
            self.out_name = self.out_name + ".shp"
            self._condence_fields()

        try:
            self._remove_existing()
            arcpy.CreateFeatureclass_management (self.out_path, self.out_name, self.geometry_type,
                                                self.template, self.has_m, self.has_z, self.spatial_reference,
                                                self.config_keyword, self.spatial_grid_1, self.spatial_grid_2, 
                                                self.spatial_grid_3, self.out_alias)
            self._create_fields()
        except Exception as e:
            self.logger.error("Failed to create feature class")
            self.logger.debug(e)
            raise Exception("Failed to create feature class")

        

        return self.out_path


def main(config_path=None):
    ''' main run file '''

    print ("starting....")
    config = get_config(config_path)
    logger = build_logger(config["log_level"])

    logger.info("creating database connection")
    
    
    count = 0
    for database_config in config["database"]:
        print("... Creating Workspace - " + str(count))
        count +=1
        
        database = Database(database_config["type"],
                            database_config['properties'])
        db_path = database.get_workspace()
        print("... Creating Feature Classes")
        ## loop over each feature class in the config.
        for fcprops in config["featureclass"]:
            
            logger.info("creating feature class - " + fcprops["out_name"])

            ## add extra properties
            fcprops["schema"] = config["fields"][fcprops["shema_index"]]
            fcprops["out_path"] = db_path

            ## build feature class
            featureclass = FeatureClass(fcprops, database.type)
            featureclass.create()

            print("... Complete!")
            print ("           ")

    logger.info(" ------------------ END ------------------ ")
    print (" ------------------ END ------------------ ")


if __name__ == '__main__':
    main()
    
    