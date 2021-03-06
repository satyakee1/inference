# Creates version definitions used by the loadgen at compile time.

import datetime
import errno
import os
import sys


from absl import app


def func_def(name, string):
    return "const std::string& Loadgen" + name + "() {\n" + \
        "  static const std::string str = " + string + ";\n" + \
        "  return str;\n" + \
        "}\n\n"


def generate_loadgen_version_definitions(cc_filename):
    gitRev = os.popen("git rev-parse --short=10 HEAD").read()
    gitCommitDate = os.popen("git log --format=\"%cI\" -n 1").read()
    gitStatus = os.popen("git status -s -uno").read()
    gitLog = os.popen("git log --pretty=oneline -n 16 --no-decorate").read()

    dateTimeNowLocal = datetime.datetime.now().isoformat()
    dateTimeNowUtc = datetime.datetime.utcnow().isoformat()

    try:
        os.makedirs(os.path.dirname(cc_filename))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    file = open(cc_filename, "w")
    file.write("// DO NOT EDIT: Autogenerated by version_generator.py.\n\n")
    file.write("#include <string>\n\n")
    file.write("namespace mlperf {\n\n")
    file.write(func_def("Version", "\".5a1\""))
    file.write(func_def("GitRevision", "\"" + gitRev[0:-1] + "\""))
    file.write(func_def("BuildDateLocal", "\"" + dateTimeNowLocal + "\""))
    file.write(func_def("BuildDateUtc", "\"" + dateTimeNowUtc + "\""))
    file.write(func_def("GitCommitDate", "\"" + gitCommitDate[0:-1] + "\""))
    file.write(func_def("GitStatus", "R\"(" + gitStatus[0:-1] + ")\""))
    file.write(func_def("GitLog", "R\"(" + gitLog[0:-1] + ")\""))
    file.write("}  // namespace mlperf\n");
    file.close()


def main(argv):
    if len(argv) > 2:
        raise app.UsageError('Too many command-line arguments.')
    generate_loadgen_version_definitions(argv[1])


if __name__ == '__main__':
  app.run(main)
