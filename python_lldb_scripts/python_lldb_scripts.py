#!/usr/bin/python
# ----------------------------------------------------------------------
#  load / reload script:  (lldb) command script import python_lldb_scripts.py
# ----------------------------------------------------------------------
import lldb
from console import Console

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f python_lldb_scripts.__hello_world yd_hello_world')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__where yd_where')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__machine_platform yd_chip')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__get_bundle_id yd_bundle_id')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__frame_beautify yd_pretty_frame')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__thread_beautify yd_pretty_thread_list')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__print_four_registers yd_registers_top4')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__print_registers yd_registers_all')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__dl_symbol_snooper yd_dlsym_snooper')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__hw_class yd_class')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__bypass_urlsession_trust yd_bypass_urlsession')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__bypass_exception_port_check yd_bypass_exception_port_check')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__bypass_ptrace_symbol yd_bypass_ptrace_symbol')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__bypass_ptrace_syscall yd_bypass_ptrace_syscall')
    debugger.HandleCommand('command script add -f python_lldb_scripts.__bypass_sysctl_symbol yd_bypass_sysctl_symbol')

def __bypass_sysctl_symbol(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug sysctl code.
        The code sets a breakpoint inside of libsystem_c.dylib.
        When the breakpoint fires, it calls to another function.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F sysctl -s libsystem_c.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.__sysctl_patch fooName')


def __sysctl_patch(sbframe, sbbreakpointlocation, dict):
    """
        A custom patch function for sysctl()
        Ideally it wouldn't be a custom function but this API passes in a four part int array pointer
        Whereas other APIs just pass a single Int value ( and not a int * )
    """
    hits = sbbreakpointlocation.GetHitCount()
    function_name = sbframe.GetFunctionName()
    print("[*]Hits={0}:{1}".format(str(hits), function_name))
    thread = sbframe.GetThread()
    process = thread.GetProcess()
    process_info = process.GetProcessInfo()
    if process_info.IsValid():
        options = lldb.SBExpressionOptions()
        target_register = __set_target_register(function_name)
        raw_ptr_mib = sbframe.FindRegister(target_register)
        # the ptr_to_mib gives address of first mib[0].  I need mib[3].  That is lldb) po (int *) mib + 12
        #  ptr_pid_from_mib = ptr_to_mib + 12
        offset = raw_ptr_mib.GetValueAsUnsigned() + 12
        offset_type = raw_ptr_mib.GetType()
        print("[*]Register:{0}\n[*]Address of mib[0]:{1}".format(target_register, raw_ptr_mib.GetValue()))
        print("[*]mib[0]:{0}\n[*]mib[3]:{1}".format(raw_ptr_mib.GetValueAsUnsigned(), offset))
        val = lldb.target.CreateValueFromAddress("temp", lldb.SBAddress(raw_ptr_mib.GetValueAsUnsigned(), lldb.target), offset_type)
        print(val.GetValueAsUnsigned(), type(val))
        if 1 == process.GetProcessID():
            print("[*]Read PID from MIB array:{0}".format(pid_from_mib))
            ppid = sbframe.EvaluateExpression('(int *)getppid();', options)
            print("[*]Parent process ID\t{0}\t{1}".format(ppid.unsigned, type(ppid.GetValueAsUnsigned())))
            result = process.WriteMemory(ptr_pid_from_mib, ppid.GetValueAsUnsigned(), error)
            messages = {None: 'error', True: 'PATCHED', False: 'fail'}
            print ("[*]Result: " + messages[result])


def __dl_symbol_snooper(debugger, command, exe_ctx, result, internal_dict):
    """
        Snoop on dlsym().  Useful to understand how an iOS app starts.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F dlsym -s libdyld.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.__cstring_printer fooName')
    message = ("[*]Breakpoint set. Continue...")
    result.AppendMessage(message)
    __auto_continue(debugger, result)


def __cstring_printer(frame, sbbreakpointlocation, dict):
    """
        dlsym() returns the address of the code or data location specified by the symbol.
        In the $arg2 register you always have a pointer to a const char * that is located in the Data section of binary.
        With the pointer can then call SBProcess.ReadCStringFromMemory
    """
    function_name = frame.GetFunctionName()
    target_register = __set_target_register(function_name)
    symbol_str_address = frame.FindRegister(target_register)
    thread = frame.GetThread()
    process = thread.GetProcess()
    error = lldb.SBError()
    c_string = process.ReadCStringFromMemory(int(symbol_str_address.GetValue(), 16), 256, error)
    if not error.Success():
        print(error)
        return None
    else:
        print("[*] dlsym for:({0})".format(c_string))


def __bypass_ptrace_symbol(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug ptrace code.
        The code sets a breakpoint on ptrace inside of libsystem_kernel.dylib.
        Then it calls out to another Python function.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F ptrace -s libsystem_kernel.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.__prepare_patch fooName')



def __bypass_ptrace_syscall(debugger, command, exe_ctx, result, internal_dict):
    """
        A script to stop anti-debug ptrace code, when the call is written in assembler.
        The code sets a breakpoint on ptrace inside of libsystem_kernel.dylib.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('b -F syscall -s libsystem_kernel.dylib -N fooName --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.__prepare_patch fooName')
    thread = frame.GetThread()
    thread_id = thread.GetThreadID()
    message = ("[*]Breakpoint set. Continue..thread_id:{}".format(str(thread_id)))
    result.AppendMessage(message)


def __final_patch(frame, register, patch):
    error = lldb.SBError()
    result = frame.registers[0].GetChildMemberWithName(register).SetValueFromCString(patch, error)
    messages = {None: 'error', True: 'PATCHED', False: 'fail'}
    print ("[*] Result: " + messages[result])


def __set_target_register(fnc_name):
    # type: (str) -> str
    if 'task_get_exception_ports' in fnc_name:
        return 'arg2'
    elif 'ptrace' in fnc_name:
        return 'arg1'
    elif 'dlsym' in fnc_name:
        return 'arg2'
    elif 'syscall' in fnc_name:
        return 'arg2'
    elif 'sysctl' in fnc_name:
        return 'arg1'
    else:
        return 'arg1'

def __prepare_patch(sbframe, sbbreakpointlocation, dict):
    """
        Function to patch register values.
        First looks up the calling Function Name.
        Then calls out to setTargetRegister() to find out what register to patch.
    """

    hits = sbbreakpointlocation.GetHitCount()
    function_name = sbframe.GetFunctionName()
    thread = sbframe.GetThread()
    thread_id = thread.GetThreadID()
    target_register = __set_target_register(function_name)
    instruction = sbframe.FindRegister(target_register)
    print("[*] target_register={0}\toriginal instruction:{1}".format(target_register, instruction))
    print("[*] Hits={0}:{1} (\t\tthread_id:{2}\tinstruction:{3}\tnum_frames:{4})".format(str(hits), function_name, str(thread_id), str(instruction.unsigned), thread.num_frames))
    if instruction.unsigned > 0:
        __final_patch(sbframe, target_register, '0x0')


def __bypass_exception_port_check(debugger, command, exe_ctx, result, internal_dict):
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
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.YDDebuggerPatching fooName')
    message = ("[*]Breakpoint set. Continue...")
    result.AppendMessage(message)


def __bypass_urlsession_trust(debugger, command, exe_ctx, result, internal_dict):
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


def __print_four_registers(debugger, command, exe_ctx, result, internal_dict):
    """
        Prints the four registers often used to pass function parameters.
        Tries to print as decimal and then as char *.
        Uses $arg alias to make it work on x86_64 and arm64 ( iOS simulator / macOS / iOS device )
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return

    focal_registers = ['arg0', 'arg1', 'arg2', 'arg3', 'arg4']
    for i in focal_registers:
        reg = frame.FindRegister(i)
        if reg.description is None:
            print("[*]{0}\t:{1}\t\t:{2}".format(i, reg.value, reg.GetValueAsUnsigned()))
        else:
            print(i, reg.description)


def __print_registers(debugger, command, exe_ctx, result, internal_dict):
    """
        Prints registers. Variant of https://lldb.llvm.org/python_reference/lldb.SBValue-class.html
        Good way to show how using exe_ctx to get the Register values
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    print("[*]Frame " + str(frame))
    register_set = frame.registers # Returns an SBValueList.
    for regs in register_set:
        if 'general purpose registers' in regs.name.lower():
            GPRs = regs
            print('%s (number of children = %d):' % (GPRs.name, GPRs.num_children))
            for reg in GPRs:
                print(reg.name, ' Value: ', reg.value)
            break


def __print_chip_type(target):
    if 'x86_64' in target:
        print('[*]simulator 64 bit')
    elif 'arm64' in target:
        print('[*]arm 64 bit')
    elif 'arm' in target:
        print('[*]arm 32 bit')


def __machine_platform(debugger, command, result, internal_dict):
    """
        Get the chip underneath the O/S. Required to check Assembler instructions.
    """
    target = debugger.GetSelectedTarget()
    triple_name = target.GetTriple()
    __print_chip_type(triple_name)
    result.AppendMessage(triple_name)


def __where(debugger, command, exe_ctx, result, internal_dict):
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


def __auto_continue(debugger, result):
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


def __get_bundle_id(debugger, command, result, internal_dict):
    """
        Prints the app's Bundle Identifier, if you stopped at the app fully loaded
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    bundle_id = currentFrame.EvaluateExpression("(NSString *)[[NSBundle mainBundle] bundleIdentifier]").GetObjectDescription()
    print("[*]Bundle Identifier:")
    if not bundle_id:
        result.AppendMessage("[*]No bundle ID available. Did you stop before the AppDelegate?")
    result.AppendMessage(bundle_id)


def __thread_printer_func(thread):
  return "Thread %s has %d frames\n" % (thread.name, thread.num_frames)

def __frame_beautify(debugger, command, result, internal_dict):
    """
        Prints a prettier frame
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    print("[*] Thread:{0}\tnum_frames={1}".format(thread.name, thread.num_frames))
    for frame in thread:
        if not frame.IsValid():
            print("[*] no frame here. did you stop too early?")
        else:
            print >> result, str(frame)


def __thread_beautify(debugger, command, result, internal_dict):
    """
        Prints a prettier thread list
    """
    debugger.HandleCommand(
        'settings set  thread-format \"thread: #${thread.index}\t${thread.id%tid}\n{ ${module.file.basename}{`${function.name-with-args}\n\"')
    debugger.HandleCommand('thread list')

def __hello_world(debugger, command, result, internal_dict):
    """
        HelloWorld function. It will print "Hello World", regardless of where lldb stopped.
    """
    print("[*] Hello World")
    __auto_continue(debugger, result)
