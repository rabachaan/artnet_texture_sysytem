import TDTableHelper

from typing import List, Optional, Any

class Fixture:

    FIXTURE_TYPES = {"RGB", "DRGB", "RGBD"}

    def __init__(self, fixture_id:int, fixture_type:str = 'RGB') -> None:
        self._fixture_id   = fixture_id
        self._fixture_type = fixture_type
        self._universe     = None
        self.addressR     = None
        self.addressG     = None
        self.addressB     = None
        self.addressA     = None
    
    
    #一度設定したら変更不可
    @property
    def id(self):
        return self._fixture_id
    
    @property
    def fixture_type(self):
        return self._fixture_type

    @fixture_type.setter
    def fixture_type(self, fixture_type):
        if fixture_type not in Fixture.FIXTURE_TYPES:
            raise ValueError(f"INVALID type: {type}. Valid types are : {Fixture.FIXTURE_TYPES}")
        self._fixture_type = fixture_type


    @property
    def universe(self):
        return self._universe
    
    @universe.setter
    def universe(self, universe):
        self._universe = universe

    def set_address_from_R(self, address:int):

        if self.fixture_type == 'RGB':
            if address + 2 > 512:
                raise ValueError('The address must be less than 512.')
            self.addressR = address
            self.addressG = address + 1
            self.addressB = address + 2
            self.addressA = None
        elif self.fixture_type == 'DRGB':
            if address + 3 > 512:
                raise ValueError('The address must be less than 512.')
            self.addressA = address
            self.addressR = address + 1
            self.addressG = address + 2 
            self.addressB = address + 3
        elif self.fixture_type == 'RGBD':
            if address + 3 > 512:
                raise ValueError('The address must be less than 512.')
            self.addressR = address
            self.addressG = address + 1
            self.addressB = address + 2 
            self.addressA = address + 3
        else:
            raise AttributeError('define fixture type properly')
    
        return
    
    def set_fixture_type_from_address(self):
        if not self.addressR and self.addressG and self.addressB and self.addressA:
            raise Exception('set address properly')
        
        if self.addressA == -1:
            self.fixture_type = 'RGB'
        elif self.addressR + 3 == self.addressA:
            self.fixture_type = 'RGBD'
        elif self.addressR - 1 == self.addressA:
            self.fixture_type = 'DRGB'
        else:
            raise Exception('set address properly')
        
        return
    
    def __repr__(self):
        return f"Fixture(id={self._fixture_id}, type={self._fixture_type}, universe={self._universe})"

class PatchData:

    def __init__(self, patch_name:str) -> None:
        self._patch_name: str = patch_name
        self._artnet_start: int = 0
        self._universe_list: Optional[List[int]] = None
        self.resolution: Optional[int] = None
        self.partition: Optional[int] = None
        self._patch_grid: Optional[List[List[int]]] = None
        self._fixture_dict: Optional[dict] = None
        pass

    def __repr__(self) -> str:
        universe_list_str = (
            "[\n  " + ",\n  ".join(map(str, self._universe_list)) + "\n]" 
            if self._universe_list else "None"
        )
        patch_grid_str = (
            "[\n  " + ",\n  ".join([str(row) for row in self._patch_grid]) + "\n]" 
            if self._patch_grid else "None"
        )
        fixture_dict_str = (
            "{\n  " + ",\n  ".join([f"{key}: {val}" for key, val in self._fixture_dict.items()]) + "\n}" 
            if self._fixture_dict else "None"
        )

        return (
            f"PatchData(\n"
            f"  patch_name={self._patch_name!r},\n"
            f"  artnet_start={self._artnet_start},\n"
            f"  universe_list={universe_list_str},\n"
            f"  resolution={self.resolution},\n"
            f"  partition={self.partition},\n"
            f"  patch_grid={patch_grid_str},\n"
            f"  fixture_dict={fixture_dict_str}\n"
            f")"
        )

    @property
    def patch_name(self) -> str:
        return self._patch_name
    
    @patch_name.setter
    def patch_name(self, patch_name) -> None:
        self._patch_name = patch_name
        return
    
    @property
    def artnet_start(self) -> int:
        return self._artnet_start

    @artnet_start.setter
    def artnet_start(self, artnet_start: int) -> None:
        self._artnet_start = artnet_start

    @property
    def universe_list(self) -> Optional[List[int]]:
        return self._universe_list

    @universe_list.setter
    def universe_list(self, universe_list: Optional[List[int]]) -> None:
        if universe_list is not None:
            # 重複チェック
            if len(universe_list) != len(set(universe_list)):
                raise ValueError("The list contains duplicate elements.")

            # 昇順チェック
            if universe_list != sorted(universe_list):
                raise ValueError("The list is not sorted in ascending order.")

        self._universe_list = universe_list


    #patch_gridは二次元配列。親リストの要素がX軸、サブリスがY軸
    @property
    def patch_grid(self) -> Optional[List[List[int]]]:
        return self._patch_grid

    #patchGridは二次元配列で親配列と子配列の長さが同じでなければならない。
    @patch_grid.setter
    def patch_grid(self, patch_grid:list) -> None:
        lenX = len(patch_grid)
        for y in patch_grid:
            if not isinstance(y, list):
                raise ValueError('INVALID type: patch_grid must be list of list.')
            if len(y) != lenX:
                raise ValueError('List and Sublist must be same length')
            
        self._patch_grid = patch_grid

    @property
    def fixture_dict(self) -> Optional[dict]:
        return self._fixture_dict
    
    @fixture_dict.setter
    def fixture_dict(self, fixture_dict:dict)-> None:
        empty_fixture = Fixture(0,'RGB')
        for f in fixture_dict.values():
            if not isinstance(f, type(empty_fixture)):
                raise Exception('fixture_dict must be configured Fixture Class')
            self._fixture_dict = fixture_dict

    def make_patch_grid_from_DAT(self, dat) -> bool:
        if not dat.numRows == dat.numCols:
            raise Exception('Row and Col must be same size.')
        dat_helper = TDTableHelper.TDTableHelper(dat,'cell',True, True)
        gird = dat_helper.getAllData()
        
        for r in gird:
            for c in range(len(r)):
                    if len(str(r[c])) > 0:
                        r[c] = int(r[c])
                    else:
                        r[c] = ''
        self.patch_grid = gird

        return True
    
    def make_fixture_dict_from_DAT(self, dat) -> bool:
        if not dat.row(0) == ['fixtureID', 'R', 'G', 'B', 'A']:
            raise Exception ('1st row must be \'fixtureID\', \'R\', \'G\', \'B\', \'A\'')
        
        dat_helper = TDTableHelper.TDTableHelper(dat,'str')
        dat_dict = dat_helper.getDictionary()

        f_dict = {}

        for key, val in dat_dict.items():
            fixture = Fixture(fixture_id=int(key))
            fixture.universe = int(float(val[0])) - (1 - self.artnet_start)
            #実際のuniverseと表示されているuniverseがズレるのでshown_universeを使う。
            shown_universe = int(float(val[0]))
            fixture.addressR = round((float(val[0]) - shown_universe) * 1000)
            fixture.addressG = round((float(val[1]) - shown_universe) * 1000)
            fixture.addressB = round((float(val[2]) - shown_universe) * 1000)
            if float(val[3]) > 0:
                fixture.addressA = round((float(val[3]) - shown_universe) * 1000)
            else:
                fixture.addressA = -1

        
            fixture.set_fixture_type_from_address()

            f_dict[key] = fixture

        self.fixture_dict = f_dict
        return
    
    def make_universe_list_from_fixture_dict(self):
        if not self.fixture_dict:
            raise Exception('fixture_dict is not defined')
        
        u_list = []
        
        for fixture in self.fixture_dict.values():
            univ = fixture.universe
            if not univ in u_list:
                u_list.append(univ)

        self.universe_list = sorted(u_list)

        return

