#!/usr/bin/python
# ----------------------------------------------------------------------
#  load / reload script:  (lldb) command script import yd_pythonlldb_scripts.py
# ----------------------------------------------------------------------
import sys
sys.path.append('/Applications/Xcode.app/Contents/SharedFrameworks/LLDB.framework/Resources/Python')
import lldb

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDBypassURLSessionTrust yd_bypass_urlsession')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDBypassExceptionPortCheck yd_bypass_exception_port_check')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDBypassPtraceSymbol yd_bypass_ptrace_symbol')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDBypassPtraceSyscall yd_bypass_ptrace_syscall')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDHelloWorld yd_hello_world')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDWhere yd_where')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDMachinePlatform yd_chip')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDPrintFrame yd_frame_print')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDGetBundleIdentifier yd_bundle_id')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDThreadBeauty yd_thread_list')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDPrintFourRegisters yd_registers_top4')
    debugger.HandleCommand('command script add -f yd_pythonlldb_scripts.YDPrintRegisters yd_registers_all')

def YDBypassPtraceSymbol(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug ptrace code.
        The code sets a breakpoint on ptrace inside of libsystem_kernel.dylib.
        Then it calls out to another Python function.
        This function returns from the Thread without executing the ptrace call.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F ptrace -s libsystem_kernel.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F yd_pythonlldb_scripts.YDDebuggerPatching fooName')
    thread = frame.GetThread()
    thread_id = thread.GetThreadID()
    message = ("[*]Breakpoint set. Continue..thread_id:{}".format(str(thread_id)))
    result.AppendMessage(message)



def YDBypassPtraceSyscall(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug ptrace code, when the call is written in assembler.
        The code sets a breakpoint on ptrace inside of libsystem_kernel.dylib.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F syscall -s libsystem_kernel.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F yd_pythonlldb_scripts.YDDebuggerPatching fooName')
    thread = frame.GetThread()
    thread_id = thread.GetThreadID()
    message = ("[*]Breakpoint set. Continue..thread_id:{}".format(str(thread_id)))
    result.AppendMessage(message)


def YDPatcher(frame, register, patch):
    error = lldb.SBError()
    result = frame.registers[0].GetChildMemberWithName(register).SetValueFromCString(patch, error)
    messages = {None: 'error', True: 'PATCHED', False: 'fail'}
    print ("[*] Result: " + messages[result])


def setTargetRegister(fnc_name):
    # type: (str) -> str
    if 'task_get_exception_ports' in fnc_name:
        return 'arg2'
    elif 'ptrace' in fnc_name:
        return 'arg1'
    elif 'syscall' in fnc_name:
        return 'arg2'
    else:
        return 'arg1'

def YDDebuggerPatching(sbframe, sbbreakpointlocation, dict):
    """
        Function to patch register values.
        First looks up the calling Function Name.
        Then calls out to setTargetRegister() to find out what register to patch.
    """

    hits = sbbreakpointlocation.GetHitCount()
    function_name = sbframe.GetFunctionName()
    thread = sbframe.GetThread()
    thread_id = thread.GetThreadID()
    target_register = setTargetRegister(function_name)
    instruction = sbframe.FindRegister(target_register)
    print("[*] target_register={0}\toriginal instruction:{1}".format(target_register, instruction))
    print("[*] Hits={0}:{1} (\t\tthread_id:{2}\tinstruction:{3}\tnum_frames:{4})".format(str(hits), function_name, str(thread_id), str(instruction.unsigned), thread.num_frames))
    if instruction.unsigned > 0:
        YDPatcher(sbframe, target_register, '0x0')


def YDBypassExceptionPortCheck(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug code that works by detecting exception ports.
        The code sets a breakpoint on task_get_exception_ports.
        Then it calls out to another Python function.
        This other function overwrites a function parameter passed into task_get_exception_ports.
        Print to logs, if it fires.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -n task_get_exception_ports -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F yd_pythonlldb_scripts.YDDebuggerPatching fooName')
    message = ("[*]Breakpoint set. Continue...")
    result.AppendMessage(message)

def YDBypassURLSessionTrust(debugger, command, exe_ctx, result, internal_dict):
    """
        Sets the NSURLSessionAuthChallengeDisposition to Default.
        Requires user to stop when the $RSI register contained the NSURLSessionAuthChallengeDisposition.
        Uses $arg alias to make it work on x86_64 and arm64 ( iOS simulator / macOS / iOS device )
    """

    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return

    print("[*]URLSession trust bypass started")
    disposition = frame.FindRegister("rsi")
    print("[*]Original of NSURLSessionAuthChallengeDisposition: " + str(disposition))

    if disposition.unsigned == 2:
        print "[!]NSURLSessionAuthChallengeDisposition set to Cancel."
        error = lldb.SBError()
        result = frame.registers[0].GetChildMemberWithName('arg2').SetValueFromCString('0x1', error)
        messages = {None: 'error', True: 'pass', False: 'fail'}
        print ("[*]PATCHING result: " + messages[result])

    thread = frame.GetThread()
    process = thread.GetProcess()
    process.Continue()


def YDPrintFourRegisters(debugger, command, exe_ctx, result, internal_dict):
    """
        Prints the four registers often used to pass function parameters.
        Tries to print as decimal and then as char *.
        Uses $arg alias to make it work on x86_64 and arm64 ( iOS simulator / macOS / iOS device )
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return

    focalregisters = ['arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'args8']
    for i in focalregisters:
        reg = frame.FindRegister(i)
        if reg.description is None:
            print("[*]{0}\t:{1}\t\t:{2}".format(i, reg.value, reg.GetValueAsUnsigned()))
        else:
            print(i, reg.description)

def YDPrintRegisters(debugger, command, exe_ctx, result, internal_dict):
    """
        Prints registers. Variant of https://lldb.llvm.org/python_reference/lldb.SBValue-class.html
        Good way to show how using exe_ctx to get the Register values
    """

    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return

    print("[*]Frame " + str(frame))
    registerset = frame.registers # Returns an SBValueList.
    for regs in registerset:
        if 'general purpose registers' in regs.name.lower():
            GPRs = regs
            break

    print('%s (number of children = %d):' % (GPRs.name, GPRs.num_children))
    for reg in GPRs:
        print(reg.name, ' Value: ', reg.value)

def printChipType(target):
    # type: (SBObject) -> void
    if 'x86_64' in target:
        print('[*]simulator 64 bit')
    elif 'arm64' in target:
        print('[*]arm 64 bit')
    elif 'arm' in target:
        print('[*]arm 32 bit')


def YDMachinePlatform(debugger, command, result, internal_dict):
    """
        Get the chip underneath the O/S. Required to check Assembler instructions.
    """
    target = debugger.GetSelectedTarget()
    triple_name = target.GetTriple()
    printChipType(triple_name)
    result.AppendMessage(triple_name)


def YDWhere(debugger, command, exe_ctx, result, internal_dict):
    """
        Print the function where you have stopped
    """
    frame = exe_ctx.frame
    name = frame.GetFunctionName()
    if not frame.IsValid():
        return ("no frame here")
    else:
        print("[*] Inside function: " + str(name))
        print("[*] line: " + str(frame.GetLineEntry().GetLine()))


def YDAutoContinue(debugger, result):
    """
        Auto-Continues after script has ran.
        debugger.SetAsync(True) allows a clean auto-continue. lldb can run in two modes "synchronous" or "asynchronous".
        Tell lldb the function restarted the target with lldb.eReturnStatusSuccessContinuingNoResult.
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    result.SetStatus(lldb.eReturnStatusSuccessContinuingNoResult)
    debugger.SetAsync(True)
    process.Continue()


def YDHelloWorld(debugger, command, result, internal_dict):
    """
        HelloWorld function. It will print "Hello World", regardless of where lldb stopped.
    """
    print("[*] Hello World")
    YDAutoContinue(debugger, result)



def YDGetBundleIdentifier(debugger, command, result, internal_dict):
    """
        Prints the app's Bundle Identifier, if you stopped at a sensible point
    """
    target = debugger.GetSelectedTarget().GetProcess()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    bundleIdentifier = currentFrame.EvaluateExpression("(NSString *)[[NSBundle mainBundle] bundleIdentifier]").GetObjectDescription()
    print("[*]Bundle Identifier:")
    if not bundleIdentifier:
        result.AppendMessage("[*]No bundle ID available. Did you stop before the AppDelegate?")
    result.AppendMessage(bundleIdentifier)
    process.Continue()

def thread_printer_func (thread,unused):
  return "Thread %s has %d frames\n" % (thread.name, thread.num_frames)

def YDPrintFrame(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    print("[*] Thread:{0}\tnum_frames={1}".format(thread.name, thread.num_frames))
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
