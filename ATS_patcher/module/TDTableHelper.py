
class TDTableHelper:
    def __init__(self, dat, dataType:str, firstRowIsData:bool = False, firstColIsData:bool = True) -> None:
        self.dat = dat
        self.dataType = dataType
        self.firstRowIsData = firstRowIsData
        self.firstColIsData = firstColIsData

        if self.firstRowIsData:
            self.startRow = 0
            self.endRow = self.dat.numRows
        else:
            self.startRow = 1
            self.endRow = self.dat.numRows

        if self.firstColIsData:
            self.startCol = 0
            self.endCol = self.dat.numCols
        else:
            self.startCol = 1
            self.endCol = self.dat.numCols

        pass
     
    def getAllData(self) -> list:
        ret_list = []

        

        for iRow in range(self.startRow, self.endRow):
            iRow_list = []
            for iCol in range(self.startCol, self.endCol):
                element = self.cellDataCast(iRow, iCol)
                iRow_list.append(element)
            
            ret_list.append(iRow_list)

        return ret_list
    
    def getDictionary(self, keyType:str, keyNum) -> dict:
        
        ret_dict = {}

        if keyType == 'Row':
            keyList = self.getSpecificRow(keyNum)
            
            allData = self.getAllData()
            
            del allData[keyNum]

            vals = allData
        elif keyType == 'Col':
            keyList = self.getSpecificCol(keyNum)

            allData = self.getAllData()

            for r in allData:
                del r[keyNum]
            
            vals = allData
        else:
            #TODO エラー処理
            raise Exception ('keyType must be \'Col\' or \'Row\'')
        

        for i in range (len(keyList)):
            ret_dict[keyList[i]] = vals[i]

        return ret_dict
            
    
    def getSpecificRow(self, specificRow: int) -> list:
        ret_list = []


        for iCol in range(self.startCol, self.endCol):
            element = self.cellDataCast(specificRow, iCol)
            ret_list.append(element)

        return ret_list

    def getSpecificCol(self, specificCol: int) -> list:
        ret_list = []


        for iRow in range(self.startRow, self.endRow):
            element = self.cellDataCast(iRow, specificCol)
            ret_list.append(element)

        return ret_list

    def cellDataCast(self, row:int, col:int):

        if self.dataType == 'cell':
            return self.dat[row, col]
        elif self.dataType =='str':
            return str(self.dat[row, col])
        elif self.dataType == 'int':
            return int(self.dat[row, col])
        elif self.dataType == 'float':
            return float(self.dat[row, col])
        
        return
        
    def setDataSpecificRow(self, row:int, data:list):
        
        if not len(data) == self.dat.numCols:
            raise Exception('data length is not match by cols')

        for iCol in range(self.dat.numCols):
            self.dat[row, 1] = data[iCol]
    
        return
    
    def setDataSpecificCol(self, col:int, data:list):
        if not len(data) == self.dat.numRows:
            raise Exception('data length is not match by rows')

        for iRow in range(self.dat.numRows):
            self.dat[iRow, col] = data[iRow]

        return
    
    def setDataFromList(self, arr:list):
        
        if not self._is_2d_list(arr):
            raise Exception('data must be 2d list.')
        
        arrSize = self._get_2d_array_shape(arr)
        
        for iRow in range(arrSize[0]):
            for iCol in range(arrSize[1]):
                self.dat[iRow, iCol] = arr[iRow][iCol]
 
        return


    #privateな関数なのでアンスコ始まりfrom ChatGPT
    def _is_2d_list(lst):
        if not isinstance(lst, list):
            return False  # リストでない場合、2次元リストではない
        if not lst:
            return False  # 空のリストの場合、2次元リストではない

        # 最初の要素を調べ、それがリストであるかどうかを確認
        first_element = lst[0]
        if not isinstance(first_element, list):
            return False  # 最初の要素がリストでない場合、2次元リストではない

        return True  # 上記の条件をすべて満たす場合、2次元リストとみなす
    
    def _get_2d_array_shape(arr):
        # 空のリストの場合、行数と列数は0
        if not arr:
            return [0, 0]

        # 最初の行の長さを取得
        num_cols = len(arr[0])

        # すべての行の長さが同じか確認
        for row in arr:
            if len(row) != num_cols:
                raise Exception ('each length of row is not same.')

        # 行数を取得
        num_rows = len(arr)

        return [num_rows, num_cols]