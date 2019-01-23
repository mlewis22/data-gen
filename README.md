# data-gen
A simple automated tool for building feature classes within chosen workspaces. Utilises the arcpy module delivered with ArcGIS Pro


# Requirements
- ArcGIS Pro
- arcpy
- Python 3.6


# Running
the run.bat contains a command to run the ArcGIS Pro python.exe. 

In powershell or command, change your working directory to this repository


```shell
    cd c:/data-get
```

run the bat command 

```shell
    .\run.bat
```

for more details on using stand alone scripts with ArGIS Pro, please visit - http://pro.arcgis.com/en/pro-app/arcpy/get-started/using-conda-with-arcgis-pro.htm

# Config

The following section covers the properties found within the config.json. Many properties utilise the same inputs as found within  the Arcpy documentation - 

- [Create Database Connection](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm)

- [Create Feature Class](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm)

- [Add Fields (multiple)](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-fields.htm)

The following sections detail the properties.

| Property | Description |
| --- | --- |
| `log_level` | string representing python log level, **DEBUG, INFO, WARNING** files |
| `database` | An array of **workspaces** which feature classes will be created in. Supports, Enterprise Geodatabases, Shapefiles and FileGeodatabase |
| `featureclass` | An array of **Feature Classes** which will be created.|
| `fields` | An array of **Fields** which will be created. Inputs based on the following geoprocessing tool - [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-fields.htm). |



## 'database' Property
| Property | Description |
| --- | --- |
| `type` | **enterprise** (any esri supported enterprise db), **filegdb** (File Geodatabase), **shapefile** (Esri Shapefile) |
| `properties.remove_existing` | Specifices if an existing connection file should be removed as the script is run. Improves speed if your connection requirements havent changed. Required to be set as *true* on intiall run. |
| `properties.folder_path` | can either be a specific path such as 'c:/temp' or use the holding string *local* to place output files in same directory at main.py |
| `properties.name` | **enterprise**: the name of the connection .sde file, **filegdb**: the name of the .gdb targeted |
| `properties.database_platform` | **enterprise only**: platform type as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.instance` | **enterprise only**: instance property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.account_authentication` | **enterprise only**: account_authentication property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.username` | **enterprise only**: username required as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.password` | **enterprise only**: password required as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.save_user_pass` | **enterprise only**: save_user_pass property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.database` | **enterprise only**: database property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.schema` | **enterprise only**: schema property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.version_type` | **enterprise only**: version_type property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.version` | **enterprise only**: version property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |
| `properties.date` | **enterprise only**: date property as specified by [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-database-connection.htm). |


## 'featureclass' Property
| Property | Description |
| --- | --- |
| `featureclass.shema_index` | the array index of the schema found in the fields property |
| `featureclass.out_name` | the name of the output feature class |
| `featureclass.geometry_type` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.template` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.has_m` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.has_z` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.spatial_reference` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.config_keyword` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.spatial_grid_1` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.spatial_grid_2` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.spatial_grid_3` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |
| `featureclass.out_alias` | property as specified at [Esri Documentation](http://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm). |



