'''
Created on Feb 8, 2015

@author: oly
'''

class Check:
    def __init__(self):
        pass
    
    def handle(self, perioddata):
        pass
    
    def check(self):
        raise NotImplementedError
    
    def ready(self):
        raise NotImplementedError

    def recommendedPreload(self):
        return 0

class GreaterThanOrEqualToCheck(Check):
    def __init__(self, compare, compareto):
        Check.__init__(self)
        self.compare = compare
        self.compareto = compareto
    
    def handle(self, perioddata):
        pass
    
    def check(self):
        if self.ready() == False:
            return None
        return self.compare.value() >= self.compareto.value()
    
    def ready(self):
        return self.compare.ready() and self.compareto.ready()

    def recommendedPreload(self):
        return max(self.compare.recommendedPreload(),self.compareto.recommendedPreload())
