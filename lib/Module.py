__author__ = 'DM_'


class useModule():
    def __init__(self, moduleName):
        self.moduleName = moduleName

    def load(self):
        ModuleClass = getattr(__import__(self.moduleName, fromlist=["ModuleClass"]), "ModuleClass")
        self._ModuleClass = ModuleClass
        self.moduleParams = self._ModuleClass.options
        self.moduleInfo = self._ModuleClass.info
        self.moduleDoc = self._ModuleClass.__doc__
        return True

    def reload(self):
        import sys
        if self.moduleName in sys.modules:
            del sys.modules[self.moduleName]

        ModuleClass = getattr(__import__(self.moduleName, fromlist=["ModuleClass"]), "ModuleClass")
        self._ModuleClass = ModuleClass
        self.moduleParams = self._ModuleClass.options
        self.moduleInfo = self._ModuleClass.info
        self.moduleDoc = self._ModuleClass.__doc__
        return True

    def setOptions(self, options):
        for key in options.keys():
            if key in self.moduleParams.keys():
                self.moduleParams[key] = options[key]

    def run(self):
        ModuleClass = self._ModuleClass()
        ModuleClass.options = self.moduleParams
        ModuleClass.exploit()