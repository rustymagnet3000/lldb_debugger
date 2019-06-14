## import script:  (lldb) command script import ~/Coding/lldb_ios_ripper/scratch.py
import lldb

def __lldb_init_module(debugger, internal_dict):
    
    debugger.HandleCommand('command script add -f scratch.YDWhere yd_whereamI')
    debugger.HandleCommand('command script add -f scratch.YDStoppedThreads yd_looper')
    
    print "[+] NEW Rusty commands successfully added"


def getRegisterString(target):
    triple_name = target.GetTriple()
    if 'x86_64' in triple_name:
        return 'simulator 64 bit'
    elif 'arm64' in triple_name:
        return 'arm 64 bit'
    elif 'arm' in triple_name:
        return 'arm 32'
    raise Exception('unknown device')

def Chip(debugger, command, result, internal_dict):
    '''Gets the chip type underneath an iOS app'''
    target = debugger.GetSelectedTarget()
    triple_name = target.GetTriple()
    print("[+] triple_name:: {}".format(type(triple_name)))
    a = getRegisterString(target)
    result.AppendMessage(a)

def YDWhere(debugger, command, result, internal_dict):
    '''
        Print the function where you have stopped
    '''
    name = lldb.frame.GetFunctionName()
    print("[+] Inside function: " + str(name))


def HelloWorld(debugger, command, result, internal_dict):
    '''HelloWorld, works regardless of where lldb stopped'''
    ci = debugger.GetCommandInterpreter()
    res = lldb.SBCommandReturnObject()
    ci.HandleCommand('script print "Hello World smoke test"', res)

def GetBundleIdentifier(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    mainThread = process.GetThreadAtIndex(0)
    currentFrame = mainThread.GetSelectedFrame()
    bundleIdentifier = currentFrame.EvaluateExpression("(NSString *)[[NSBundle mainBundle] bundleIdentifier]").GetObjectDescription()
    print("[+] bundleIdentifier:: {}".format(type(bundleIdentifier)))
    if not bundleIdentifier:
        result.AppendMessage("No bundle ID available, at this point of lldb. Did you stop before the AppDelegate?")
    result.AppendMessage(bundleIdentifier)

def PrintFrame(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()

    for frame in thread:
            print >>result, str(frame)

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f ios_enumerator.HelloWorld yd_hello')
	debugger.HandleCommand('command script add -f scratch.YDWhere yd_whereamI')
    debugger.HandleCommand('command script add -f ios_enumerator.Chip yd_chip')
    debugger.HandleCommand('command script add -f ios_enumerator.PrintFrame yd_frame_print')
    debugger.HandleCommand('command script add -f ios_enumerator.GetBundleIdentifier yd_bundle_id')
    debugger.HandleCommand('command script add -f ios_enumerator.GetBundleIdentifier yd_bundle_id')
    print "[+] Rusty's Dec-6-2018 commands successfully added"
