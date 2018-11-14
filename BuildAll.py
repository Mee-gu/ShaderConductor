#!/usr/bin/env python
#-*- coding: ascii -*-

# ShaderConductor
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import multiprocessing, os, platform, subprocess, sys

def FindProgramFilesFolder():
	env = os.environ
	if "64bit" == platform.architecture()[0]:
		if "ProgramFiles(x86)" in env:
			programFilesFolder = env["ProgramFiles(x86)"]
		else:
			programFilesFolder = "C:\Program Files (x86)"
	else:
		if "ProgramFiles" in env:
			programFilesFolder = env["ProgramFiles"]
		else:
			programFilesFolder = "C:\Program Files"
	return programFilesFolder

def FindVS2017Folder(programFilesFolder):
	tryVswhereLocation = programFilesFolder + "\\Microsoft Visual Studio\\Installer\\vswhere.exe"
	if os.path.exists(tryVswhereLocation):
		vsLocation = subprocess.check_output([tryVswhereLocation,
			"-latest",
			"-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
			"-property", "installationPath",
			"-version", "[15.0,16.0)",
			"-prerelease"]).decode().split("\r\n")[0]
		tryFolder = vsLocation + "\\VC\\Auxiliary\\Build\\"
		tryVcvarsall = "VCVARSALL.BAT"
		if os.path.exists(tryFolder + tryVcvarsall):
			return tryFolder
	else:
		names = ("Preview", "2017")
		skus = ("Community", "Professional", "Enterprise")
		for name in names:
			for sku in skus:
				tryFolder = programFilesFolder + "\\Microsoft Visual Studio\\%s\\%s\\VC\\Auxiliary\\Build\\" % (name, sku)
				tryVcvarsall = "VCVARSALL.BAT"
				if os.path.exists(tryFolder + tryVcvarsall):
					return tryFolder
	return ""

if __name__ == "__main__":
	originalDir = os.path.abspath(os.curdir)

	if not os.path.exists("Build"):
		os.mkdir("Build")

	host_platform = sys.platform
	if 0 == host_platform.find("win"):
		host_platform = "win"
	elif 0 == host_platform.find("linux"):
		host_platform = "linux"
	elif 0 == host_platform.find("darwin"):
		host_platform = "darwin"

	argc = len(sys.argv);
	if (argc > 1):
		buildSys = sys.argv[1]
	else:
		if host_platform == "win":
			buildSys = "vs2017"
		else:
			buildSys = "ninja"
	if (argc > 2):
		arch = sys.argv[2]
	else:
		arch = "x64"
	if (argc > 3):
		configuration = sys.argv[3]
	else:
		configuration = "Release"

	multiConfig = (buildSys.find("vs") == 0)

	buildDir = "Build/%s-%s" % (buildSys, arch)
	if not multiConfig:
		buildDir += "-%s" % configuration;
	if not os.path.exists(buildDir):
		os.mkdir(buildDir)
	os.chdir(buildDir)
	buildDir = os.path.abspath(os.curdir)

	parallel = multiprocessing.cpu_count()

	cmdList = []
	if host_platform == "win":
		vs2017Folder = FindVS2017Folder(FindProgramFilesFolder())
		if "x64" == arch:
			vcOption = "amd64"
		elif "x86" == arch:
			vcOption = "x86"
		else:
			LogError("Unsupported architecture.\n")
		cmdList.append("%sVCVARSALL.BAT %s && cd /d \"%s\"" % (vs2017Folder, vcOption, buildDir))
	if (buildSys == "ninja"):
		if host_platform == "win":
			cmdList.append("set CC=cl.exe")
			cmdList.append("set CXX=cl.exe")
		cmdList.append("cmake -G Ninja -DCMAKE_BUILD_TYPE=\"%s\" -DSC_ARCH_NAME=\"%s\" ../../" % (configuration, arch))
		cmdList.append("ninja -j%d" % parallel)
	else:
		cmdList.append("cmake -G \"Visual Studio 15\" -T host=x64 -A %s ../../" % arch)
		cmdList.append("MSBuild ALL_BUILD.vcxproj /nologo /m:%d /v:m /p:Configuration=%s,Platform=%s" % (parallel, configuration, arch))
	cmd = ""
	for i in range(0, len(cmdList)):
		cmd += cmdList[i]
		if i != len(cmdList) - 1:
			cmd += " && "
	print(buildDir)
	print(cmd)
	subprocess.call(cmd)

	os.chdir(originalDir)
