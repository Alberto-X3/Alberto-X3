from os import listdir
import importlib
import Utils


required = ["__main__", "EVENTS", "HELP"]

MODULES = [module.replace(".py", "") for module in listdir("./Modules") if module.endswith(".py") and not module == "__init__.py"]
libs = {}


for lib in MODULES.copy():

    libs[lib] = importlib.import_module(f"Modules.{lib}", "Modules")

    if not hasattr(libs[lib], "__main__"):
        del libs[lib]
        MODULES.remove(lib)

    if not hasattr(libs[lib], "EVENTS"):
        libs[lib] = []

    if not hasattr(libs[lib], "HELP"):
        if Utils.EVENT.on_message in libs[lib].EVENTS:
            libs[lib] = Utils.Help(vanish=True)
