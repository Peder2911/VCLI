
import views
import os
import logging
import json

from views.storage.orm import Variable,Varset,Theme,Specification,RunPeriodization,Model
from sqlalchemy.orm import sessionmaker

import functools
import operator as op

class OrmExplorer:
    _model = None

    def list(self):
        return self._getSession().query(self._model).all()

    def _inspect(self,instance):
        return str(instance)

    def inspect(self,name):
        i = self._getSession().query(self._model).filter(self._model.name == name).first()
        return self._inspect(i)

    def _getSession(self):
        return sessionmaker(bind=views.storage.orm.create_engine())()

def compose(*args):
    return "\n".join(args)

class Explorer:
    class variables(OrmExplorer):
        _model = Variable
        def _inspect(self,instance):
            lines = []
            lines += [f"Variable {instance.name}"]
            lines += [f"\tDependent variable in {len(instance.models)} models:"]
            lines += ["\t\t"+m.name for m in instance.models]
            lines += [f"\tPart of {len(instance.varsets)} variable sets:"]
            lines += ["\t\t"+vs.name for vs in instance.varsets]

            try:
                themes = functools.reduce(op.add,[vs.themes for vs in instance.varsets])
            except TypeError:
                themes = []
            lines += [f"\tIncluded in {len(themes)} themes:"]
            lines += ["\t\t"+th.name for th in themes] 

            return "\n".join(lines) 

    class variablesets(OrmExplorer):
        _model = Varset 
        def _inspect(self,instance):
            lines = []
            lines += [f"Variable set {instance.name}"]
            lines += [f"\tContains {len(instance.variables)} variables:"]
            lines += ["\t\t"+v.name for v in instance.variables]
            lines += [f"\tPart of {len(instance.themes)} themes:"]
            lines += ["\t\t"+th.name for th in instance.themes]
            return "\n".join(lines) 

    class themes(OrmExplorer):
        _model = Theme 
        def _inspect(self,instance):
            lines = []
            lines += [f"Theme {instance.name}"]
            lines += [f"\tContains {len(instance.varsets)} variable sets:"]
            lines += ["\t\t"+vs.name for vs in instance.varsets]
            lines += [f"\tApplied in {len(instance.models)} models:"]
            lines += ["\t\t"+m.name for m in instance.models]
            return "\n".join(lines) 

    class periodizations(OrmExplorer):
        _model = RunPeriodization
        def _inspect(self,instance):
            return compose(
                f"Periodization {instance.name}",
                "\n".join(["\t"+str(tp) for tp in instance.periodsets])
            )

    class specifications(OrmExplorer):
        _model = Specification 
        def _inspect(self,instance):
            return compose(
                    f"Specification {instance.name}",
                    f"\t Composed of {len(instance.themes)} themes:",
                    "\n".join(["\t\t"+th.name for th in instance.themes])
                )

    class models(OrmExplorer):
        _model = Model

        def inspect(self,id):
            i = self._getSession().query(self._model).filter(self._model.id == id).first()
            return self._inspect(i)

        def _inspect(self,instance):
            return compose(
                    f"Model of {instance.specification.name} with {instance.estimator.name}",
                    f"\t{len(instance.runs)} runs"
                )
