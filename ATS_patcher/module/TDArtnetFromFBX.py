import csv

import TDTableHelper
import TDArtnetPatchData


class TDArtnetFromFBX:

    def __init__(self) -> None:
        self.artNetStart   = None
        self.resolution    = None
        self.partition     = None
        self.origin        = None
        self.startUniverse = None
        self.numUniverse   = None
        self.meshGroup_dat = None
        self.primitve_dat  = None
        self.vertex_dat    = None
        pass

    def setSopInfoDat(self, meshGroup_dat, primitve_dat, vertex_dat):
        self.meshGroup_dat = meshGroup_dat
        self.primitve_dat  = primitve_dat 
        self.vertex_dat    = vertex_dat   

    def setProjectData(self, parOp):

        self.artNetStart = int(parOp['Artnetstart'])
        self.resolution  = [int(parOp['Resolutionx']),int(parOp['Resolutiony'])]
        self.partition   = int(parOp['Partition'])
        self.origin      = int(parOp['Origin'])

        return True

    def getUniverseInfo(self,addressList:list):

        maxAdd = max(addressList)
        minAdd = min(addressList)

        startUniverse = int(minAdd)
        numUniverse   = int(maxAdd) - int(minAdd) + 1 

        return startUniverse, numUniverse

    def setUniverseInfo(self, start, num):

        self.startUniverse = start
        self.numUniverse = num

        return

    

    #chatGPT
    def csv_to_dict(self, csv_file, key_column, value_column):
        result_dict = {}

        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                key = row[key_column]
                key = key.replace('.', '_')
                value = row[value_column]
                result_dict[key] = value

        return result_dict



    def makeMeshUVDict(self, meshGroupDict:dict, primitveMaxIndexDict:dict, primitveUVDict:dict):

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


    def makePatchDataDict(self, meshAddressDict:dict, meshUVDict:dict):
        #numUniverseとpartitonから必要な長さの空の配列を必要数つくる
        patchData = {}

        #
        #partitionの二乗の長さの空の配列を作成する
        #patchData:dictの中にnumUniverse分作成する
        for i in range(self.numUniverse):
            patchData['patch' + str(i + 1).zfill(3)] = [['' for _ in range(self.partition)] for _ in range(self.partition)]
        #
        #
        patchKeyList = list(patchData.keys())
        patchKeyList.sort()

        meshList = meshAddressDict.keys()

        
        for mesh in meshList:
            if mesh == '':
                continue
            address = meshAddressDict[mesh]
            univ = int(float(address))
            

            #FBXのメッシュ名が変わる。末尾に'.001'とかつく
            #なんとかする
            #何とかなってそう


            
            uv = meshUVDict[mesh]


            #部分一致の場合はこれ 2023/12
            """UVmatch = [meshUVDict[key] for key in meshUVDict if mesh in key]
            if len(UVmatch) == 0:
                print(mesh)
                continue
            else:
                uv = UVmatch[0]"""
            
            #print(UV)
 
            #int(UV(x or y) / (1 / partition))と同じ
            gridx = int(uv[0] * self.partition)
            gridy = int((1 - uv[1]) * self.partition) 

            patchName = 'patch' + str(univ - self.startUniverse + 1).zfill(3)
            patchData[patchName][gridy][gridx] = address

        return patchData
    
    


    def getPatchDataFromFBX(self):


        #各Meshの最後の頂点のUVとメッシュ名を対応させた辞書を作る
        meshGroupHelper = TDTableHelper.TDTableHelper(self.meshGroup_dat,'str', firstRowIsData=False)
        meshGroupDict = meshGroupHelper.getDictionary('Col', 0)



        sop_primitive_helper = TDTableHelper.TDTableHelper(self.primitve_dat, 'str', firstRowIsData= False)
        primitveMaxIndexDict = sop_primitive_helper.getDictionary('Col', 1)

        sop_vertex_helper = TDTableHelper.TDTableHelper(self.vertex_dat, 'str', firstRowIsData= False)
        primitveUVDict = sop_vertex_helper.getDictionary('Col', 0)

        meshUVDict =  self.makeMeshUVDict(meshGroupDict,primitveMaxIndexDict, primitveUVDict)
        #各Meshの最後の頂点のUVとメッシュ名を対応させた辞書を作る




        
        #csvからメッシュとアドレスを対応させた辞書を作る
        csv_path = ui.chooseFile(fileTypes = ['csv'], title = 'choose csv File')
        meshAddressDict = self.csv_to_dict(csv_path, 'Object', 'Address')
        #print(meshAddressDict)

        #print(len(meshUVDict))
        #print(len(meshAddressDict))

        #
        #一致しないキーの数が１より多い場合は何が違うのかprintしておく。パッチされてない''の分だけ常に違うはず
        #ただし、meshAddressDict(Excelデータ)が少ない分には問題ない。
        #違うメッシュだけど同じアドレスとかあるから ex:6回路
        #
        
        """different_keys = set(meshUVDict.keys()) ^ set(meshAddressDict.keys())
        if len(different_keys) > 1:
            print(different_keys)
            print(len(different_keys))"""

        #map関数よくわかんないけどchatGPTが教えてくれた
        addressList = list(map(float, meshAddressDict.values()))

        sUniverse, nUniverse = self.getUniverseInfo(addressList)
        self.setUniverseInfo(sUniverse, nUniverse)

        #self.setProjectData()

        self.patchData = self.makePatchDataDict(meshAddressDict, meshUVDict)

        return
