import TDTableHelper
import json

class TDArtnetPatchData:

    def __init__(self, patchName:str) -> None:
        self.patchName     = patchName
        self.artNetStart   = None
        self.numUniverse   = None
        self.startUniverse = None
        self.resolution    = None
        self.partition     = None
        self.origin        = None
        #patchDataのkeyはpatch001、patch002,,,,,
        self.patchData     = {}
        pass

    def printALLdata(self):

        print('patchName ' , self.patchName)
        print('artNetStart', self.artNetStart)
        print('numUniverse ', self.numUniverse)
        print('startUniverse ', self.startUniverse)
        print('resolution ', self.resolution)
        print('partition ', self.partition)
        print('origin ', self.origin)
        print('patchData ', self.patchData)
        pass

    def loadPatchDataFromDAT(self, datList:list):
        #datの配列の長さが
        self.numUniverse = len(datList)

        #forでpatchデータを辞書に格納。keyはオペレーター名、valueは二次元配列
        self.patchData = {}
        

        #TODO エラーの場合の例外処理書くこと()
        for iPatch in datList:
            patch_dat_helper = TDTableHelper.TDTableHelper(op(iPatch), dataType= 'str', firstRowIsData=True)
            patch_data = patch_dat_helper.getAllData()
            self.patchData[iPatch] = patch_data
        
        return True

    def loadPatchDataFromFile(self, filePath):
        
        with open(filePath, 'r') as file:
            data = json.load(file)

        print(data)
            
        self.patchName     = data['patchName']
        self.artNetStart   = data['artNetStart']
        self.numUniverse   = data['numUniverse']
        self.startUniverse = data['startUniverse']
        self.resolution    = data['resolution']
        self.partition     = data['partition']
        self.origin        = data['origin']
        self.patchData     = data['patchData']
        
        
        return 
        
    def setProjectParmeter(self, resolution:list, partition:int, origin:str = "Top-Left"):
        self.resolution = resolution
        self.partition  = partition
        self.origin     = origin

        pass

    def setArtnetParameter(self, numUniverse, startUniverse, artNetstart):
        self.numUniverse   = numUniverse
        self.startUniverse = startUniverse
        self.artNetStart   = artNetstart
        pass

    def saveProjectData(self, path:str):

        data_dict = {'patchName' : self.patchName,'artNetStart' : self.artNetStart, 'numUniverse' : self.numUniverse, 'startUniverse' : self.startUniverse, 'resolution' : self.resolution, 'partition' : self.partition, 'origin' : self.origin, 'patchData' : self.patchData}    
        print(data_dict)
        with open(path, 'w') as file:
            json.dump(data_dict, file)
            

        return
            