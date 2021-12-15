import requests
import sys
import lib.RModule as rmodule
import lib.RProject as rproject
import lib.RSender as rsender


if __name__ == "__main__":
    try:
        project_id = sys.argv[1]
    except IndexError:
        print("error -> project_id not specified")


    retrieve_project_data_query = "http://rhapsody.hestiaworkshop.net/rest/projects/get_project" + project_id
    project = rproject.Project(project_id, "192.168.1.66")
    project.begin()