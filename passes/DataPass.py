from passes.PassClasses import Pass

class cfg():
    name = "Control Flow Graph"
    def __init__(self) -> None:
        pass

    def run():
        pass

class DataPass(Pass):

    name = "data"
    export = cfg.name

    requires = {

    }

    def run(state):
        controlflow = cfg()
        state.addData(controlflow)



