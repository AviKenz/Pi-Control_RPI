import java.io.*;
import java.util.Scanner;
 
public class RpiInterpreterCaller {
 
	/**
	* @param args
	* @throws IOException
	*/
	public static void call() throws IOException {
		System.out.println("RpiInterpreterCaller.call()");
		
		// set up the command and parameter
		String scriptPath = "/usr/lib/cgi-bin/";
		String scriptName = "RpiInterpreter.py";
		String scriptParams = "pin_number=5 direction=0 state=0 mode=11 interval=0 number_of_cycles=5 signal_type=0";
		String[] cmd = new String[4];
		
		cmd[0] = "python"; // check version of installed python: python -V
		cmd[1] = scriptPath;
		cmd[2] = scriptName;
		cmd[3] = scriptParams;
		
		String cmd2 = "python " + scriptPath + scriptName + " " + scriptParams;
		System.out.println(cmd2);
		 
		// create runtime to execute external command
		Runtime rt = Runtime.getRuntime();
		Process pr = rt.exec(cmd2);
		try {
			pr.waitFor();
		} catch(Exception e) {
			e.printStackTrace();
		}
		 
		Scanner errScn = new Scanner(pr.getErrorStream());
		Scanner dbgScn = new Scanner(pr.getInputStream());
		
		errScn.useDelimiter("\r\n");
		dbgScn.useDelimiter("\r\n");
		
		while (errScn.hasNext()) {
			System.out.println(errScn.next());
		}
		
		while (dbgScn.hasNext()) {
			System.out.println(dbgScn.next());
		}
 
		errScn.close();
		dbgScn.close();
		 
		
	}
}
