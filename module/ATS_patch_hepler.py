import csv
import TDTableHelper
from PatchData import Fixture


class ATS_patch_helper:

    def __init__(self, csv_path, artnet_start, partiton) -> None:

        self.meshGroup_dat = None
        self.primitve_dat  = None
        self.vertex_dat    = None
        self.artnet_start  = artnet_start
        self.partiton      = partiton

        mesh_fixture_dict = self._csv_to_dict(csv_path, 'Object', ['Address','FixtureType'])
        self.csv_dict = mesh_fixture_dict
        pass


    def load_patch_sheet_from_csv(self, csv_path):
        mesh_fixture_dict = self._csv_to_dict(csv_path, 'Object', ['FixtureID', 'Address','FixtureType'])
        self.csv_dict = mesh_fixture_dict

    #chatGPT
    def _csv_to_dict(self, csv_file, key_column, value_columns:list):
        result_dict = {}

        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                key = row[key_column]
                #TDが'.'を'_'変えちゃうのでこうするしかない
                key = key.replace('.', '_')
                value_list = []
                for i in value_columns:
                    value_list.append(row[i])
                result_dict[key] = value_list

        return result_dict

    def _makeMeshUVDict(self, meshGroupDict:dict, primitveMaxIndexDict:dict, primitveUVDict:dict):

        #TODO　なんか条件でエラー吐かなきゃいけない気がするけどこれじゃない
        """if not len(meshGroupDict) == len(primitveMaxIndexDict) == len(primitveUVDict):
            print('len(meshGroupDict)' , len(meshGroupDict))
            print('len(primitveMaxIndexDict)' , len(primitveMaxIndexDict))
            print('len(primitveUVDict)' , len(primitveUVDict))
            raise Exception('dict size not same!!!!!!!!!')"""

        meshUVDict = {}
        for mesh in meshGroupDict.keys():
            grp = meshGroupDict[mesh][0]

            if not grp in primitveMaxIndexDict:
                continue

            primitve = primitveMaxIndexDict[grp][0]
            uv = [float(primitveUVDict[primitve][1]), float(primitveUVDict[primitve][2])]

            meshUVDict[mesh] = uv

            #print(mesh, meshUVDict[mesh])
        #print(meshUVDict)

        return meshUVDict

    def make_universe_list(self) ->list:
        if not self.csv_dict:
            raise Exception('csv data is not defined')
        
        u_list = []

        for v in self.csv_dict.items():
            univ = int(float(v[1]))
            if not univ in u_list:
                u_list.append(univ)

        sorted_universe_list = sorted(u_list)

        return sorted_universe_list
    
    def make_fixture_dict(self) -> dict:
        if not self.csv_dict:
            raise Exception('csv data is not defined')

        f_dict = {}
        #keyはメッシュ名、valueは['FixtureID', 'Address','FixtureType']
        for k, v in self.csv_dict.items():
            fixture = Fixture(fixture_id= int(v[0]))
            fixture.universe = int(float(v[1])) - (1 - self.artnet_start)
            #実際のuniverseと表示されているuniverseがズレるのでshown_universeを使う。
            shown_universe = int(float(v[1]))
            fixture.fixture_type = v[2]
            address = round((float(v[1]) - shown_universe) * 1000)
            fixture.set_address_from_R(address)

            f_dict[k] = fixture

        return f_dict
    
    def make_patch_grid(self) -> list:
        if not self.meshGroup_dat and self.primitve_dat and self.vertex_dat:
            raise Exception ('SOP data OPs are not defined')
        if not self.csv_dict:
            raise Exception('csv data is not defined')
        
        #各Meshの最後の頂点のUVとメッシュ名を対応させた辞書を作る
        meshGroupHelper = TDTableHelper.TDTableHelper(self.meshGroup_dat,'str', firstRowIsData=False)
        meshGroupDict = meshGroupHelper.getDictionary('Col', 0)



        sop_primitive_helper = TDTableHelper.TDTableHelper(self.primitve_dat, 'str', firstRowIsData= False)
        primitveMaxIndexDict = sop_primitive_helper.getDictionary('Col', 1)

        sop_vertex_helper = TDTableHelper.TDTableHelper(self.vertex_dat, 'str', firstRowIsData= False)
        primitveUVDict = sop_vertex_helper.getDictionary('Col', 0)

        meshUVDict =  self._makeMeshUVDict(meshGroupDict,primitveMaxIndexDict, primitveUVDict)
        #各Meshの最後の頂点のUVとメッシュ名を対応させた辞書を作る

        #f_dict = self.make_fixture_dict()

        p_grid = [['' for _ in range(self.partiton)] for _ in range(self.partiton)]

        #
        for mesh_name, v in self.csv_dict.items():
            uv = meshUVDict[mesh_name]
            #int(UV(x or y) / (1 / partition))と同じ
            gridx = int(uv[0] * self.partition)
            gridy = int((1 - uv[1]) * self.partition) 

            #v[0] == FixtureID
            p_grid[gridx][gridy] = v[0]

        return p_grid