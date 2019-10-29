from o3seespy.base_model import OpenseesObject
import tempfile
import os
import numpy as np


class RecorderBase(OpenseesObject):
    op_base_type = "recorder"


class NodeToFile(RecorderBase):
    op_type = "Node"

    def __init__(self, osi, fname, node, dofs, mtype, nsd=8):
        self._parameters = [self.op_type, '-file', fname, '-precision', nsd, '-node', node.tag, '-dof', *dofs, mtype]
        self.to_process(osi)


class NodesToFile(RecorderBase):
    op_type = "Node"

    def __init__(self, osi, fname, nodes, dofs, mtype, nsd=8):
        node_tags = [x.tag for x in nodes]
        self._parameters = [self.op_type, '-file', fname, '-precision', nsd, '-node', *node_tags, '-dof', *dofs, mtype]
        self.to_process(osi)


class NodeToArrayCache(RecorderBase):  # TODO: implement NodeToArray where data saved to memory and loaded as array without collect
    op_type = "Node"

    def __init__(self, osi, node, dofs, mtype, nsd=8):
        self.tmpfname = tempfile.NamedTemporaryFile(delete=False).name
        self._parameters = [self.op_type, '-file', self.tmpfname, '-precision', nsd, '-node', node.tag, '-dof', *dofs, mtype]
        self.to_process(osi)

    def collect(self):
        try:
            a = np.loadtxt(self.tmpfname, dtype=float)
        except ValueError as e:
            print('Warning: Need to run opy.wipe() before collecting arrays')
            raise ValueError(e)
        try:
            os.unlink(self.tmpfname)
        except PermissionError:
            print('Warning: Need to run opy.wipe() before collecting arrays')
        return a


class ElementToFile(RecorderBase):
    op_type = "Element"

    def __init__(self, osi, fname, element, material=None, args=None, nsd=8):
        if args is None:
            args = []
        extra_pms = []
        if material is not None:
            extra_pms += ['material', material]
        self._parameters = [self.op_type, '-file', fname, '-precision', nsd, '-ele', element.tag, *extra_pms, *args]
        self.to_process(osi)


class ElementToArrayCache(RecorderBase):  # TODO: implement ElementToArray where data saved to memory and loaded as array without collect
    op_type = "Element"

    def __init__(self, osi, element, material=None, args=None, nsd=8):
        if args is None:
            args = []
        extra_pms = []
        if material is not None:
            extra_pms += ['material', material]
        self.tmpfname = tempfile.NamedTemporaryFile(delete=False).name

        self._parameters = [self.op_type, '-file', self.tmpfname, '-precision', nsd, '-ele', element.tag, *extra_pms, *args]
        self.to_process(osi)

    def collect(self):
        try:
            a = np.loadtxt(self.tmpfname, dtype=float)
        except ValueError as e:
            print('Warning: Need to run opy.wipe() before collecting arrays')
            raise ValueError(e)
        try:
            os.unlink(self.tmpfname)
        except PermissionError:
            print('Warning: Need to run opy.wipe() before collecting arrays')
        return a