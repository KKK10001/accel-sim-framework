#!/usr/bin/env python3

from optparse import OptionParser
import os
import subprocess
import os

this_directory = os.path.dirname(os.path.realpath(__file__)) + "/"
import sys

sys.path.insert(0, os.path.join(this_directory, "..", "job_launching"))
import common
import re
import shutil
import glob
import datetime
import yaml
import common
import re
import datetime

# We will look for the benchmarks
parser = OptionParser()
parser.add_option(
    "-B",
    "--benchmark_list",
    dest="benchmark_list",
    help="a comma seperated list of benchmark suites to run. See apps/define-*.yml for "
    + "the benchmark suite names.",
    default="rodinia_2.0-ft",
)
parser.add_option(
    "-D", "--device_num", dest="device_num", help="CUDA device number", default="0"
)
parser.add_option(
    "-n",
    "--norun",
    dest="norun",
    action="store_true",
    help="Do not actually run the apps, just create the dir structure and launch files",
)
parser.add_option(
    "-l",
    "--limit_kernel_number",
    dest="kernel_number",
    default=-99,
    help="Sets a hard limit to the number of traced kernels",
)
parser.add_option(
    "-t",
    "--terminate_upon_limit",
    dest="terminate_upon_limit",
    action="store_true",
    help="Once the kernel limit is reached, terminate the tracing process",
)
parser.add_option(
    "--spinlock_handling",
    dest="spinlock_handling",
    choices=["none", "fast_forward"],
    default="none",
    help="How to handle spinlock instructions",
)
parser.add_option(
    "--spinlock_fast_forward_iterations",
    dest="spinlock_fast_forward_iterations",
    type=int,
    default=1,
    help="Number of iterations to keep for spinlock fast forwarding. Only used if spinlock_handling is fast_forward",
)

(options, args) = parser.parse_args()

common.load_defined_yamls()

benchmarks = []
benchmarks = common.gen_apps_from_suite_list(options.benchmark_list.split(","))

cuda_version = common.get_cuda_version(this_directory)
now_time = datetime.datetime.now()
day_string = now_time.strftime("%y.%m.%d-%A")
time_string = now_time.strftime("%H:%M:%S")
logfile = day_string + "--" + time_string + ".csv"
log_path = os.path.join(this_directory, logfile)
log_file = open(log_path, "w")
log_file.write("status,benchmark,run_name,run_dir,detail\n")
overall_success = True

nvbit_tracer_path = os.path.join(this_directory, "tracer_tool")
nvbit_spinlock_path = os.path.join(this_directory, "others", "spinlock_tool")

for bench in benchmarks:
    edir, ddir, exe, argslist = bench
    for argpair in argslist:
        args = argpair["args"]
        run_name = os.path.join(exe, common.get_argfoldername(args))
        this_run_dir = os.path.abspath(
            os.path.expandvars(
                os.path.join(
                    this_directory,
                    "..",
                    "..",
                    "hw_run",
                    "traces",
                    "device-" + options.device_num,
                    cuda_version,
                    run_name,
                )
            )
        )
        this_trace_folder = os.path.join(this_run_dir, "traces")
        if not os.path.exists(this_run_dir):
            os.makedirs(this_run_dir)
        if not os.path.exists(this_trace_folder):
            os.makedirs(this_trace_folder)

        # link the data directory
        try:
            benchmark_data_dir = common.dir_option_test(
                os.path.join(ddir, exe, "data"), "", this_directory
            )
            if os.path.lexists(os.path.join(this_run_dir, "data")):
                os.remove(os.path.join(this_run_dir, "data"))
            os.symlink(benchmark_data_dir, os.path.join(this_run_dir, "data"))
        except common.PathMissing:
            pass

        all_data_link = os.path.join(this_run_dir, "data_dirs")
        if os.path.lexists(all_data_link):
            os.remove(all_data_link)
        top_data_dir_path = common.dir_option_test(ddir, "", this_directory)
        os.symlink(top_data_dir_path, all_data_link)

        if args == None:
            args = ""
        exec_path = common.file_option_test(os.path.join(edir, exe), "", this_directory)
        sh_contents = "set -e\n"

        if options.terminate_upon_limit:
            sh_contents += "export TERMINATE_UPON_LIMIT=1; "

        if "mlperf" in exec_path:
            # For mlperf by default we turn this flag on
            sh_contents += "export TERMINATE_UPON_LIMIT=0; "
            exec_path = ". " + exec_path

            if options.kernel_number > 0:
                sh_contents +=  ('\nexport DYNAMIC_KERNEL_RANGE="0-'+str(options.kernel_number)+'"\n')
            else:
                sh_contents +=  ('\nexport DYNAMIC_KERNEL_RANGE="0-'+str(50)+'"\n')
        else:
            if options.kernel_number > 0:
                sh_contents +=  ('\nexport DYNAMIC_KERNEL_RANGE="0-'+str(options.kernel_number)+'"\n')
            else:
                sh_contents +=  ('\nexport DYNAMIC_KERNEL_RANGE=""\n')

        # first we generate the traces (.trace and kernelslist files)
        # then, we do post-processing for the traces and generate (.traceg and kernelslist.g files)
        # then, we delete the intermediate files ((.trace and kernelslist files files)
        sh_contents += (
            '\nexport CUDA_VERSION="'
            + cuda_version
            + '"; export CUDA_VISIBLE_DEVICES="'
            + options.device_num
            + '" ; '
        )
        
        tracer_contents = (
            sh_contents
            + "\nrm -f traces/*"
            + "\nexport TRACES_FOLDER="
            + this_run_dir
            + f"; ENABLE_SPINLOCK_FAST_FORWARD={1 if options.spinlock_handling == 'fast_forward' else 0} SPINLOCK_ITER_TO_KEEP={options.spinlock_fast_forward_iterations} CUDA_INJECTION64_PATH="
            + os.path.join(nvbit_tracer_path, "tracer_tool.so")
            + " "
            + exec_path
            + " "
            + str(args)
            + " ; "
            + os.path.join(
                nvbit_tracer_path, "traces-processing", "post-traces-processing"
            )
            + " "
            + this_trace_folder
            + " ; rm -f "
            + this_trace_folder
            + "/*.trace ; rm -f "
            + this_trace_folder
            + "/kernelslist "
        )
        
        # Spinlock tool run script
        # will run twice, once for phase 0 and once for phase 1
        spinlock_contents = (
            sh_contents
            + "\nrm -f spinlock_detection/*"
            + "\nexport TRACES_FOLDER="
            + this_run_dir
            + "; SPINLOCK_PHASE=0 CUDA_INJECTION64_PATH="
            + os.path.join(nvbit_spinlock_path, "spinlock_tool.so")
            + " "
            + exec_path
            + " "
            + str(args)
            + " ; "
            + " SPINLOCK_PHASE=1 CUDA_INJECTION64_PATH="
            + os.path.join(nvbit_spinlock_path, "spinlock_tool.so")
            + " "
            + exec_path
            + " "
            + str(args)
            + " ; "
        )

        for path, content in [("run.sh", tracer_contents), ("run_spinlock_detection.sh", spinlock_contents)]:
            open(os.path.join(this_run_dir, path), "w").write(content)
            if subprocess.call(["chmod", "u+x", os.path.join(this_run_dir, path)]) != 0:
                exit(f"Error chmod {path} runfile")


        if not options.norun:
            saved_dir = os.getcwd()
            os.chdir(this_run_dir)
            print("Running {0}".format(exe))

            # Call the spinlock detection script
            if options.spinlock_handling == 'fast_forward':
                spinlock_rc = subprocess.call(["bash", "run_spinlock_detection.sh"])
                if spinlock_rc != 0:
                    overall_success = False
                    log_file.write(
                        f"FAIL_SPINLOCK,{exe},{run_name},{this_run_dir},Command: bash run_spinlock_detection.sh\n"
                    )
                    log_file.flush()
                    os.chdir(saved_dir)
                    continue

            run_rc = subprocess.call(["bash", "run.sh"])
            if run_rc != 0:
                overall_success = False
                log_file.write(
                    f"FAIL,{exe},{run_name},{this_run_dir},Command: bash run.sh\n"
                )
                try:
                    with open(os.path.join(this_run_dir, "run.sh"), "r") as run_sh:
                        log_file.write("run.sh contents:\n")
                        run_sh_contents = run_sh.read()
                        log_file.write(run_sh_contents)
                        if not run_sh_contents.endswith("\n"):
                            log_file.write("\n")
                except OSError:
                    log_file.write("<unable to read run.sh>\n")
                log_file.write("---\n")
                log_file.flush()
            else:
                log_file.write(
                    f"PASS,{exe},{run_name},{this_run_dir},Command: bash run.sh\n"
                )
                log_file.flush()
            os.chdir(saved_dir)

log_file.close()
if not overall_success:
    print(f"Some workloads failed. See log: {log_path}")
    sys.exit(1)
print(f"All workloads passed. Log saved to {log_path}")
