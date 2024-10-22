import helpers.helper_zz as helper_zz
import Patch_locator
import Patch_evolution
import Patch_matcher_src
import Fiber_inputs
import os,sys
refsourcepath=Fiber_inputs.refsourcepath
refkernelpath=Fiber_inputs.refkernelpath

def Locate_patch_repository(repo,branch,patchesinfo):
    Patch_locator.patchlocator(repo,branch,patchesinfo)

def Locate_patch_sourcecodesnapshot(repo,branch,patchesinfo,targetkernel_list):
    Patch_locator.patchlocator(repo,branch,patchesinfo)
    Patch_evolution.Patchevolution_tracker(repo,branch,patchesinfo)
    for targetkernel in targetkernel_list: 
        Patch_matcher_src.compare_sourcecode(branch,targetkernel)

def Locate_patch_binarysnapshot(repo,branch,patchesinfo,config,targetkernel_list):
    print 'repo:',repo,'branch:',branch,'patchesinfo:',patchesinfo,'config:',config
    Patch_locator.patchlocator(repo,branch,patchesinfo)
    Patch_evolution.Patchevolution_tracker(repo,branch,patchesinfo)
    Fiber_inputs.get_refsources(repo,branch)
    Fiber_inputs.get_refkernels(repo,branch,config)

    Fiber_inputs.Get_debuginfo()
    Fiber_inputs.get_patches(repo,branch)

    Fiber_inputs.generate_pickcommands(branch,config)
    Fiber_inputs.generate_extcommands(branch,config)
    Fiber_inputs.generate_matchcommands_ref(branch,config)
    for targetkernel in targetkernel_list:
        Fiber_inputs.generate_matchcommands_target(branch,targetkernel,config)

def Locate_patch():
    mode = sys.argv[1]
    repo=sys.argv[2]
    branch=sys.argv[3]
    patchesinfo=sys.argv[4]
    if mode == 'repo':
        Locate_patch_repository(repo,branch,patchesinfo)
    elif mode == 'source':
        targetkernel_list=sys.argv[5:]
        Locate_patch_sourcecodesnapshot(repo,branch,patchesinfo,targetkernel_list)
    elif mode == 'binary':
        config=sys.argv[5]
        targetkernel_list=sys.argv[6:]
        Locate_patch_binarysnapshot(repo,branch,patchesinfo,config,targetkernel_list)
    else:
        print 'invalid mode',mode,'not in ["repo","source","binary"]'

if __name__ == '__main__':
    Locate_patch()
