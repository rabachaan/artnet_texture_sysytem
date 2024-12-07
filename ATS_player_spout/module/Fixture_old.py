class Fixture:

    FIXTURE_TYPES = {"RGB", "DRGB", "RGBD"}

    def __init__(self, fixture_id:int, fixture_type:str = 'RGB') -> None:
        self._fixture_id   = fixture_id
        self._fixture_typefixture_type = fixture_type
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