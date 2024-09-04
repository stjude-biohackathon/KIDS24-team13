import sys
sys.path.append('/Volumes/ctrbioimageinformatics/common/BioHackathon/2024/pyidms/plugins')
from common.group import Group
from common.idms_api import IdmsAPI
from common.image_collection import ImageCollection
from common.owner import Owner
from common.project import Project
from common.roi_box_data import RoiBoxData
from common.roi_box_seg_data import RoiBoxSegData


class IDMS_Backend():
    def __init__(self, idms_api=None):
        if idms_api:
            self.idms_api = idms_api
        else:
            self.idms_api = IdmsAPI(endpoint='http://idms.stjude.org:8888/idms/api',
                                    token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbj1TaGFreWFcXCwgTmlzaGFudCxvdT1UT1Usb3U9RGVwYXJ0bWVudHMsb3U9U3lzdGVtVXNlcnMsZGM9c3RqdWRlLGRjPXNqY3JoLGRjPWxvY2FsIiwidXNlciI6Im5zaGFreWEiLCJpYXQiOjE3MjQ5NDg3MTgsImV4cCI6MTcyNTU1MzUxOH0.58_5HwsEltyxhz3Uz8ZJ1mODN9h0Q2153IYpS6ppwzo')

    def get_owners(self):
        owner = Owner(self.idms_api)
        return [owners['owner'] for owners in owner.search()]

    def get_projects(self, owner=None):
        project = Project(self.idms_api)
        return [projects['project'] for projects in project.search(owners=[owner])]

    def get_groups(self, owner=None, project=None):
        group = Group(self.idms_api)
        return [groups['group'] for groups in group.search(owners=[owner], projects=[project])]

    def get_image_collections(self, owner=None, project=None, group=None):
        image_collection = ImageCollection(self.idms_api)
        return image_collection.search(owner=[owner], project=[project], group=[group], image_data_engine=['fileSystem'])

    def get_image_collection_details(self, image_collection_id):
        image_collection = ImageCollection(self.idms_api)
        return image_collection.details(image_collection_id)

    def get_roi_boxes(self, owner=None, project=None, group=None, image_collection=None):
        roi_boxes = RoiBoxData(self.idms_api)
        return roi_boxes.search(owners=[owner], projects=[project], groups=[group],
                                image_collections=[image_collection])

    def create_roi_box(self, x, y, z, sizeX, sizeY, sizeZ, image_collection_id, name=None, description=None):
        roi_boxes = RoiBoxData(self.idms_api)
        return roi_boxes.create(x, y, z, sizeX, sizeY, sizeZ, image_collection_id, name, description)

    def get_roi_box_details(self, box_id):
        roi_boxes = RoiBoxData(self.idms_api)
        return roi_boxes.details(box_id)

    def get_roi_box_seg(self, owner=None, project=None, group=None, image_collection=None, roi_boxes=None):
        roi_box_seg = RoiBoxSegData(self.idms_api)
        return roi_box_seg.search(owners=[owner], projects=[project], groups=[group],
                                  image_collections=[image_collection], box_names=roi_boxes)

    def create_roi_box_seg(self, box_id, location, name=None, description=None):
        roi_box_seg = RoiBoxSegData(self.idms_api)
        return roi_box_seg.create(box_id, location, name, description)


if __name__ == '__main__':
    idms = IDMS_Backend()
    print(f'Owners: {idms.get_owners()}')
    print(f"Projects: {idms.get_projects('biohackathon')}")
    print(f"Groups: {idms.get_groups('biohackathon', '2024')}")
    print(f"Image Collections: {idms.get_image_collections('biohackathon', '2024', 'Microglia_Samples')}")
    print(f"Image Collection Details: {idms.get_image_collection_details('ic_3422f10e2b0bf10e2b0b6e80ccd6ffffffff1725371996398')}")
    print(f"Roi Boxes: {idms.get_roi_boxes('biohackathon', '2024', 'Microglia_Samples', 'B-T97L974C_s1' )}")
    print(f"Roi Box Segmentations: {idms.get_roi_box_seg('biohackathon', '2024', 'Microglia_Samples', 'B-T97L974C_s1','box1' )}")


