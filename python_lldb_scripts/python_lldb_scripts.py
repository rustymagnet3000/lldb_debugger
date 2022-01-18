#!/usr/bin/python
# ----------------------------------------------------------------------
# reload all:       (lldb) reload_lldbinit
# reload single:    (lldb) command script import python_lldb_scripts.py
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
    debugger.HandleCommand('command script add -f python_lldb_scripts.__ios_urls yd_ios_urls')


def __ios_urls(debugger, command, exe_ctx, result, internal_dict):
    """
        Used for iOS apps. Prints URLs that are set via NSURL.
        Good way to show what an app is doing.
    """
    frame = exe_ctx.frame
    if frame is None:
        result.SetError('[!]You must have the process suspended in order to execute this command')
        return
    debugger.HandleCommand('breakpoint set -b "-[NSURL(NSURL) initWithString:]"  -N nsurlbr --auto-continue true')
    debugger.HandleCommand('breakpoint command add -F python_lldb_scripts.__url_introspection nsurlbr')
    print("[*]Set NSURL introspection!  Expect to see some URLs")


def __url_introspection(sbframe, sbbreakpointlocation, dict):
    """
        When stopping inside of NSURL initWithString, we want to print the function argument to reveal what URLs were called.
        Useful to detect when somebody is using a proxy unaware clients like openSSL to communicate.
        #register $arg3 is URL value
    """
    hits = sbbreakpointlocation.GetHitCount()
    register = 'arg3'
    url_sb_value = sbframe.FindRegister(register)
    print(f"NSURL\t{url_sb_value.GetObjectDescription()} \
            : Hits={str(hits)} \
            func_name:{sbframe.GetFunctionName()}"
          )


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
    if bundle_id is None:
        result.AppendMessage("[*]No Bundle ID available. Did you stop before the AppDelegate?")
    else:
        result.AppendMessage(f"[*]Bundle ID:\t{bundle_id}")


def __thread_printer_func(thread):
  return "Thread %s has %d frames\n" % (thread.name, thread.num_frames)


def __frame_beautify(debugger, command, result, internal_dict):
    """
        Prints a prettier list of frames
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    print("[*] Thread:{0}\tnum_frames={1}".format(thread.name, thread.num_frames))
    for frame in thread:
        if not frame.IsValid():
            print("[*] no frame here. did you stop too early?")
        else:
            print(f"{str(frame)}")


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
