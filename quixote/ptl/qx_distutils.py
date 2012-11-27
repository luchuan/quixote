"""Provides a version of the Distutils "build_py" command that knows about
PTL files.
"""

import os, string
from glob import glob
from types import StringType, ListType, TupleType
from distutils.command.build_py import build_py

class qx_build_py(build_py):

    def find_package_modules(self, package, package_dir):
        self.check_package(package, package_dir)
        module_files = (glob(os.path.join(package_dir, "*.py")) +
                        glob(os.path.join(package_dir, "*.ptl")))
        modules = []
        setup_script = os.path.abspath(self.distribution.script_name)

        for f in module_files:
            abs_f = os.path.abspath(f)
            if abs_f != setup_script:
                module = os.path.splitext(os.path.basename(f))[0]
                modules.append((package, module, f))
            else:
                self.debug_print("excluding %s" % setup_script)
        return modules

    def build_module(self, module, module_file, package):
        if type(package) is StringType:
            package = string.split(package, '.')
        elif type(package) not in (ListType, TupleType):
            raise TypeError, \
                  "'package' must be a string (dot-separated), list, or tuple"

        # Now put the module source file into the "build" area -- this is
        # easy, we just copy it somewhere under self.build_lib (the build
        # directory for Python source).
        outfile = self.get_module_outfile(self.build_lib, package, module)
        if module_file.endswith(".ptl"): # XXX hack for PTL
            outfile = outfile[0:outfile.rfind('.')] + ".ptl"
        dir = os.path.dirname(outfile)
        self.mkpath(dir)
        return self.copy_file(module_file, outfile, preserve_mode=0)
