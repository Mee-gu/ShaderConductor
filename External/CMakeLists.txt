# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

set(cxxopts_REV "3f2d70530219e09fe7e563f86126b0d3b228a60d")
set(googletest_REV "440527a61e1c91188195f7de212c63c77e8f0a45")
set(DirectXShaderCompiler_REV "362defac9072f9bfd81fdfeb4dc8db9226f38d5f")
set(SPIRV_Cross_REV "f734d78c1536b9c786bd54ab6a30caa4f8cb0bff")

function(UpdateExternalLib name url rev submodules)
	set(need_checkout FALSE)
	set(need_submodule_init FALSE)
	set(external_folder "${SC_ROOT_DIR}/External")
	set(external_lib_folder "${external_folder}/${name}")
	if(EXISTS ${external_lib_folder})
		message(STATUS "Updating ${name} to revision ${rev}...")
		execute_process(COMMAND "git" "fetch" "origin" WORKING_DIRECTORY "${external_lib_folder}")
		execute_process(COMMAND "git" "rev-parse" "HEAD" WORKING_DIRECTORY "${external_lib_folder}" OUTPUT_VARIABLE head_rev)
		string(STRIP ${head_rev} head_rev)
		if (${head_rev} STREQUAL ${rev})
			set(need_checkout FALSE)
		else()
			set(need_checkout TRUE)
		endif()
	else()
		message(STATUS "Cloning ${name} revision...")
		execute_process(COMMAND "git" "clone" ${url} "-n" WORKING_DIRECTORY "${external_folder}")
		set(need_checkout TRUE)
		if(submodules)
			set(need_submodule_init TRUE)
		endif()
	endif()
	if(need_checkout)
		message(STATUS "Checking out to revision ${rev}...")
		execute_process(COMMAND "git" "checkout" "-q" ${rev} WORKING_DIRECTORY "${external_lib_folder}")
		if(submodules)
			if(need_submodule_init)
				message(STATUS "Initializing submodules...")
				set(init_param "--init")
			else()
				message(STATUS "Updating submodules...")
				set(init_param "")
			endif()
			execute_process(COMMAND "git" "submodule" "update" ${init_param} WORKING_DIRECTORY "${external_lib_folder}")
		endif()
	endif()
endfunction()

UpdateExternalLib("cxxopts" "git://github.com/jarro2783/cxxopts.git" ${cxxopts_REV} FALSE)
UpdateExternalLib("googletest" "git://github.com/google/googletest" ${googletest_REV} FALSE)
UpdateExternalLib("DirectXShaderCompiler" "git://github.com/Microsoft/DirectXShaderCompiler.git" ${DirectXShaderCompiler_REV} TRUE)
UpdateExternalLib("SPIRV-Cross" "git://github.com/KhronosGroup/SPIRV-Cross.git" ${SPIRV_Cross_REV} FALSE)

set(ENABLE_SPIRV_CODEGEN ON CACHE BOOL "" FORCE)
set(CLANG_ENABLE_ARCMT OFF CACHE BOOL "" FORCE)
set(CLANG_ENABLE_STATIC_ANALYZER OFF CACHE BOOL "" FORCE)
set(CLANG_INCLUDE_TESTS OFF CACHE BOOL "" FORCE)
set(LLVM_INCLUDE_TESTS OFF CACHE BOOL "" FORCE)
set(HLSL_INCLUDE_TESTS OFF CACHE BOOL "" FORCE)
set(LLVM_TARGETS_TO_BUILD "None" CACHE STRING "" FORCE)
set(LLVM_INCLUDE_DOCS OFF CACHE BOOL "" FORCE)
set(LLVM_INCLUDE_EXAMPLES OFF CACHE BOOL "" FORCE)
set(LIBCLANG_BUILD_STATIC ON CACHE BOOL "" FORCE)
set(LLVM_OPTIMIZED_TABLEGEN OFF CACHE BOOL "" FORCE)
set(LLVM_REQUIRES_EH ON CACHE BOOL "" FORCE)
set(LLVM_APPEND_VC_REV ON CACHE BOOL "" FORCE)
set(LLVM_ENABLE_RTTI ON CACHE BOOL "" FORCE)
set(LLVM_ENABLE_EH ON CACHE BOOL "" FORCE)
set(LLVM_DEFAULT_TARGET_TRIPLE "dxil-ms-dx" CACHE STRING "" FORCE)
set(CLANG_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(LLVM_REQUIRES_RTTI ON CACHE BOOL "" FORCE)
set(CLANG_CL OFF CACHE BOOL "" FORCE)
set(DXC_BUILD_ARCH "x64" CACHE STRING "" FORCE) # TODO: Support more architectures
set(SPIRV_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(SPIRV_SKIP_EXECUTABLES ON CACHE BOOL "" FORCE)
set(SPIRV_SKIP_TESTS ON CACHE BOOL "" FORCE)
add_subdirectory(DirectXShaderCompiler EXCLUDE_FROM_ALL)
set(dxc_folder "External/DirectXShaderCompiler")
set_target_properties("clang" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dndxc" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxa" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxc" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxl" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxopt" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxr" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("dxv" PROPERTIES FOLDER "${dxc_folder}/Clang executables")
set_target_properties("clangAnalysis" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangAST" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangASTMatchers" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangBasic" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangCodeGen" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangDriver" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangEdit" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangFormat" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangFrontend" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangFrontendTool" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangIndex" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangLex" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangParse" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangRewrite" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangRewriteFrontend" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangSema" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangSPIRV" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangTooling" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("clangToolingCore" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("d3dcompiler_dxc_bridge" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("dxcompiler" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("dxlib_sample" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("dxrfallbackcompiler" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("libclang" PROPERTIES FOLDER "${dxc_folder}/Clang libraries")
set_target_properties("ClangAttrClasses" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrDump" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrHasAttributeImpl" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrImpl" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrList" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrParsedAttrImpl" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrParsedAttrKinds" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrParsedAttrList" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrParserStringSwitches" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrPCHRead" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrPCHWrite" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrSpellingListIndex" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrTemplateInstantiate" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangAttrVisitor" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentCommandInfo" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentCommandList" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentHTMLNamedCharacterReferences" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentHTMLTags" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentHTMLTagsProperties" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangCommentNodes" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDeclNodes" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticAnalysis" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticAST" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticComment" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticCommon" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticDriver" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticFrontend" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticGroups" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticIndexName" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticLex" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticParse" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticSema" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangDiagnosticSerialization" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("ClangStmtNodes" PROPERTIES FOLDER "${dxc_folder}/Clang tablegenning")
set_target_properties("SPIRV-Tools" PROPERTIES FOLDER "${dxc_folder}/External dependencies")
set_target_properties("SPIRV-Tools-opt" PROPERTIES FOLDER "${dxc_folder}/External dependencies")
set_target_properties("LLVMAnalysis" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMAsmParser" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMBitReader" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMBitWriter" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMCore" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMDxcSupport" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMDxrFallback" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMHLSL" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMInstCombine" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMipa" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMipo" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMIRReader" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMLinker" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMLTO" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMMSSupport" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMOption" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMProfileData" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMScalarOpts" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMSupport" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMTableGen" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMTarget" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMTransformUtils" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("LLVMVectorize" PROPERTIES FOLDER "${dxc_folder}/Libraries")
set_target_properties("ClangDriverOptions" PROPERTIES FOLDER "${dxc_folder}/Tablegenning")
set_target_properties("DxcEtw" PROPERTIES FOLDER "${dxc_folder}/Tablegenning")
set_target_properties("intrinsics_gen" PROPERTIES FOLDER "${dxc_folder}/Tablegenning")
set_target_properties("TablegenHLSLOptions" PROPERTIES FOLDER "${dxc_folder}/Tablegenning")
set_target_properties("dxexp" PROPERTIES FOLDER "${dxc_folder}/Tools")
set_target_properties("clang-tblgen" PROPERTIES FOLDER "${dxc_folder}/Utils")
set_target_properties("GIT_COMMIT_INFO_ALWAYS_REBUILD" PROPERTIES FOLDER "${dxc_folder}/Utils")
set_target_properties("llvm-tblgen" PROPERTIES FOLDER "${dxc_folder}/Utils")

add_subdirectory(SPIRV-Cross EXCLUDE_FROM_ALL)
set(spirv_cross_folder "External/SPIRV-Cross")
set_target_properties("spirv-cross" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-core" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-cpp" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-glsl" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-hlsl" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-msl" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-reflect" PROPERTIES FOLDER ${spirv_cross_folder})
set_target_properties("spirv-cross-util" PROPERTIES FOLDER ${spirv_cross_folder})

set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
set(BUILD_GMOCK OFF CACHE BOOL "" FORCE)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
add_subdirectory(googletest EXCLUDE_FROM_ALL)
set(googletest_folder "External/googletest")
set_target_properties("gtest" PROPERTIES FOLDER ${googletest_folder})
set_target_properties("gtest_main" PROPERTIES FOLDER ${googletest_folder})
