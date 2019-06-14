#!/usr/bin/python
#----------------------------------------------------------------------
# (lldb) command script import ~/Coding/debugger_playground/15_python_lldb_scripts/yd_scratchpad.py
#----------------------------------------------------------------------

import lldb

def __lldb_init_module(debugger, internal_dict):
    print "[+] Rusty's WIP script started."
    debugger.HandleCommand('command script add -f yd_scratchpad.YDNewVC yd_new_vc')
    print "[+] Finished."

def verifyStoppedInValidFrame(target):
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()
    if not frame.IsValid():
        raise Exception('stopped inside invalid frame')

    return("[+] Stopped inside good frame")

def YDNewVC(debugger, command, result, internal_dict):
    """
        Create a new UIViewController and get the pointer to new VC instance
    """
    target = debugger.GetSelectedTarget()
    a = verifyStoppedInValidFrame(target)
    result.AppendMessage(a)
    result.AppendMessage("[+] Setting context to ObjC and then create new UIViewController: ")
    debugger.HandleCommand('settings set target.language objc')
    c = lldb.frame.EvaluateExpression('[UIViewController new]')
    result.AppendMessage("[+] New: " + str(c.description))





