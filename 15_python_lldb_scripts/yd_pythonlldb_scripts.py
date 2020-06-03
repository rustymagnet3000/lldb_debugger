#!/usr/bin/python
# ----------------------------------------------------------------------
#  load the script:  (lldb) command script import yd_pythonlldb_scripts.py
# ----------------------------------------------------------------------
import sys
sys.path.append('/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Resources/Python')
import lldb

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDBypassURLSessionTrust yd_bypass_urlsession')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDHelloSmoke yd_hello_smoke')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDWhere yd_where_am_I')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDChip yd_chip')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDPrintFrame yd_frame_print')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDGetBundleIdentifier yd_bundle_id')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDThreadBeauty yd_thread_list')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDPrintRegisters yd_print_registers')


def YDBypassURLSessionTrust(debugger, command, result, internal_dict):
    """
        Sets the NSURLSessionAuthChallengeDisposition to Default. Requires user to stop when the $RSI register contained the NSURLSessionAuthChallengeDisposition
    """
    print("[*]URLSession trust bypass started")
    valuersi = lldb.frame.FindRegister("rsi")
    valueesi = lldb.frame.FindValue("esi", lldb.eValueTypeConstResult)
    print("[*]Original of NSURLSessionAuthChallengeDisposition: " + str(valuersi.unsigned))

    if valuersi.unsigned == 2:
        print "[!]Found rsi cancel"
    if valueesi.unsigned == 2:
        print "[!]Found esi cancel"

    thread = lldb.frame.GetThread()
    process = thread.GetProcess()
    process.Continue()


def YDPrintRegisters(debugger, command, result, internal_dict):
    """
        Prints registers. Copied from https://lldb.llvm.org/python_reference/lldb.SBValue-class.html
        Good way to show how to deal with SBValue Type
    """
    print("[*]YDPrintRegisters started")
    registerSet = lldb.frame.registers # Returns an SBValueList.
    for regs in registerSet:
        if 'general purpose registers' in regs.name.lower():
            GPRs = regs
            break

    print('%s (number of children = %d):' % (GPRs.name, GPRs.num_children))
    for reg in GPRs:
        print('Name: ', reg.name, ' Value: ', reg.value)

def getRegisterString(target):
    triple_name = target.GetTriple()
    if 'x86_64' in triple_name:
        return 'simulator 64 bit'
    elif 'arm64' in triple_name:
        return 'arm 64 bit'
    elif 'arm' in triple_name:
        return 'arm 32'
    raise Exception('unknown device')


def YDChip(debugger, command, result, internal_dict):
    """
        Gets the chip type underneath an iOS app
    """
    target = debugger.GetSelectedTarget()
    triple_name = target.GetTriple()
    print("[*] triple_name:: {}".format(type(triple_name)))
    a = getRegisterString(target)
    result.AppendMessage(a)


def YDWhere(debugger, command, result, internal_dict):
    """
        Print the function where you have stopped
    """
    name = lldb.frame.GetFunctionName()
    if not lldb.frame.IsValid():
        return ("no frame here")
    else:
        print("[*] Inside function: " + str(name))
        print("[*] line: " + str(lldb.frame.GetLineEntry().GetLine()))


def YDHelloSmoke(debugger, command, result, internal_dict):
    """
        HelloWorld, works regardless of where lldb stopped
    """
    ci = debugger.GetCommandInterpreter()
    res = lldb.SBCommandReturnObject()
    ci.HandleCommand('script print "[*] Hello World smoke test"', res)


def YDGetBundleIdentifier(debugger, command, result, internal_dict):
    """
        Prints the app's Bundle Identifier, if you stopped at a sensible point
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    bundleIdentifier = currentFrame.EvaluateExpression(
        "(NSString *)[[NSBundle mainBundle] bundleIdentifier]").GetObjectDescription()
    print("[*] bundleIdentifier:: {}".format(type(bundleIdentifier)))
    if not bundleIdentifier:
        result.AppendMessage("[*] No bundle ID available. Did you stop before the AppDelegate?")
    result.AppendMessage(bundleIdentifier)


def YDPrintFrame(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()

    for frame in thread:
        if not frame.IsValid():
            print("[*] no frame here. did you stop too early?")
        else:
            print >> result, str(frame)


def YDThreadBeauty(debugger, command, result, internal_dict):
    """
        Prints a prettier thread list
    """
    debugger.HandleCommand(
        'settings set  thread-format \"thread: #${thread.index}\t${thread.id%tid}\n{ ${module.file.basename}{`${function.name-with-args}\n\"')
    debugger.HandleCommand('thread list')
