import java.util.*; 
import java.io.*;
import java.util.Scanner;

class RpiCom{
	
	// form variables
	private static String paramSeparator = " ";
	private static Hashtable formData = null;
	private static String queryString = null;
	
	
	// Rpi Variables
	private static String interpreterPath = "/usr/lib/cgi-bin/";
	private static String interpreterName = "RpiInterpreter.py";
	
	// param to pass to interpreter
	private static String interpreterParam = "";
	
	// interpreter environment
	private static String envName = "python";
	
	public static void main(String args[]){	
		// get data parse and generate cmd
		formData = CgiLib.ReadParse(System.in);
		queryString = getQueryString();
		interpreterParam = getParamFormQueryString(queryString);

		//  Print the required CGI header.
		System.out.println(CgiLib.Header());
		System.out.println("<p>" + interpreterParam + "</p>");
		  

		//  Print the name/value pairs sent from the browser.
		System.out.println("Here are the name/value pairs from the form:");
		System.out.println(CgiLib.Variables(formData));

		//  Print the Environment variables sent in from the Unix script.
		System.out.println("Here are the CGI environment variables/value pairs" + "passed in from the UNIX script:");
		System.out.println(CgiLib.Environment());

		// Calling Rpi Interpreter
		String cmd = buildCmd();
		try {
			callInterpreter(cmd);
		} catch (Exception e) {
			System.err.println("could not run Interpreter");
		}
		
		// Create the Bottom of the returned HTML page to close it cleanly.
		System.out.println(CgiLib.HtmlBot());
		  
	}
	
	private static void callInterpreter (String cmd) throws Exception {
		System.out.println("callInterpreter("+ cmd + ")");
		// create runtime to execute external command
		Runtime rt = Runtime.getRuntime();
		Process pr = rt.exec(cmd);
		pr.waitFor();
		 
		Scanner errScn = new Scanner(pr.getErrorStream());
		Scanner dbgScn = new Scanner(pr.getInputStream());
		
		errScn.useDelimiter("\r\n");
		dbgScn.useDelimiter("\r\n");
		
		while (errScn.hasNext()) {
			System.out.println(errScn.next());
			newLine();
		}
		
		while (dbgScn.hasNext()) {
			System.out.println(dbgScn.next());
			newLine();
		}
 
		errScn.close();
		dbgScn.close();
	}
	
	private static void newLine() {
		System.out.println("<br />");
	}
	
	private static String buildCmd() {
		return envName + paramSeparator + interpreterPath + interpreterName + paramSeparator + interpreterParam;
	}
	
	private static String getQueryString() {
		return System.getProperty("cgi.query_string");
	}
	
	private static String getParamFormQueryString(String queryString) {
		return queryString.replace("&", paramSeparator);
	}
	
	public static void addInterpreterParam(String param) {
		interpreterParam += paramSeparator + param;
	}
	
	public static void addInterpreterParam(String key, Object value) {
		interpreterParam += paramSeparator + key + "=" + value.toString();
	}
	
	public static void removeInterpreterParam(String key) {
		String[] params = interpreterParam.split(paramSeparator);
		String resultParam = "";
		for(int i = 0; i < params.length; i++) {
			if( params[i].contains(key) ) {
				params[i] = "";
			}
		}
		for(String str : params) {
			resultParam += str + paramSeparator;
		}
		interpreterParam = resultParam;
	}
}
