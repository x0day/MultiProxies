__author__ = 'DM_'

import sqlite3
import os

basepath = r'modules/'
# dbpath = r'db/MultiProxiesDb.db'

def searchFromDB(keyWord, DBFilePath=r'db/MultiProxiesDb.db'):
    db = sqlite3.connect(DBFilePath)
    cu = db.cursor()
    cu.execute("select * from ModulesTable where ModuleName like '%" + keyWord + "%'")
    return cu.fetchall()

def showModulesDict(ModuleType, db=r'db/MultiProxiesDb.db'):
    db = sqlite3.connect(db)
    cu = db.cursor()
    OutDict = ''
    ReturnLst = []
    if ModuleType.lower() in ['auxiliary', 'exploit', '']:
        cu.execute("select * from ModulesTable where ModuleType like '%" + ModuleType + "%'")
        for lst in cu.fetchall():
            ReturnLst.append(lst)
    return ReturnLst


def returnModuleName(modulename, db=r'db/MultiProxiesDb.db'):
    db = sqlite3.connect(db)
    cu = db.cursor()
    try:
        cu.execute("select Module, ModuleName, ModulePath from ModulesTable where id=:id",{"id":int(modulename)})

    except ValueError:
        cu.execute("select Module, ModuleName, ModulePath from ModulesTable where Module like:modulename",{"modulename":modulename})

    out = cu.fetchone()
    if out:
        return out

def listmodules(basepath, modules):
    import re
    files = os.listdir(basepath)
    if ("__init__.py" in files) and not ("private" in files):
        for path in files:
            currentpath = os.path.join(basepath, path)
            filename = os.path.basename(currentpath)
            if os.path.isfile(currentpath):
                if not re.match("(__init__\.py[c]?)|([\s\S]+?\.pyc)", filename):
                    modulepath, ext = os.path.splitext(os.path.relpath(currentpath))
                    filedir, filename = os.path.split(modulepath)
                    filepath = modulepath + ext
                    modulename = modulepath.replace("\\", ".")
                    modules[filename] = dict()
                    modules[filename]["filepath"] = filepath
                    modules[filename]["modulename"] = modulename
            else:
                listmodules(currentpath, modules)

def returnAllModules():
    modules = dict()
    AllModules = dict()
    for type in os.listdir(basepath):
        currentpath = os.path.join(basepath, type)
        if os.path.isdir(currentpath):
            AllModules[type] = dict()
            listmodules(currentpath, modules)
            AllModules[type] = modules.copy()
            modules.clear()
    return AllModules

def updateDB(DBFilePath=r'db/MultiProxiesDb.db'):

    db = sqlite3.connect(DBFilePath)

    DeleteDBTable = "DROP TABLE IF EXISTS ModulesTable"
    CreateDB = "create table " \
               "if not exists ModulesTable " \
               "(id integer primary key,Module varchar(50) UNIQUE, ModuleName varchar(100) UNIQUE,ModuleType text NULL, ModulePath text Null)"
    db.execute(DeleteDBTable)
    db.execute(CreateDB)

    types = AllModules.keys()
    types.sort()
    for type in types:
        for module in AllModules[type]:
#        print Module, ModulesType[Module]
            InsertSql = 'insert into ModulesTable(Module,ModuleName,ModuleType,ModulePath) ' \
                        'values("%s","%s","%s","%s")' % (module,
                                                    AllModules[type][module]["modulename"],
                                                    type,
                                                    AllModules[type][module]["filepath"]
            )
            db.execute(InsertSql)
    db.commit()

def returnAllModuleLst(AllModules):
    AllModulesLst = []
    for type in AllModules:
        for module in AllModules[type]:
            AllModulesLst.append(module)
    return AllModulesLst

def returnDatabaseModuleLst(db=r'db/MultiProxiesDb.db'):
    db = sqlite3.connect(db)

    cu = db.cursor()
    cu.execute("select Module from ModulesTable")
    DataBaseModulesLst = []
    for module in cu.fetchall():
        DataBaseModulesLst.append(module[0])
    return DataBaseModulesLst

AllModules = returnAllModules()
AllModulesLst = returnAllModuleLst(AllModules)
DataBaseModulesLst = returnDatabaseModuleLst()