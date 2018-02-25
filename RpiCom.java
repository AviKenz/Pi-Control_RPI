import java.util.*; 
import java.io.*;
import java.util.Scanner;

class RpiCom{
	
	// form variables
	private static String scriptParamSeparator = " ";
	private static Hashtable formData = null;
	private static String queryString = null;
	
	// User App
	private static String userAppPath = "/usr/lib/cgi-bin/";
	private static String userAppName = "UserApp.py";
	private static String userAppParams = "";
	
	// user app environment
	private static String envName = "python";
	
	public static void main(String args[]){	
		
		// recieve and parse form params passed by the CGI-Script 
		formData = CgiLib.ReadParse(System.in);
		queryString = getQueryString();
		userAppParams = getParamFormQueryString(queryString);

		//  Print the HTML CGI header.
		System.out.println(CgiLib.Header());
		
		// delete default margin between paragraph elements
		System.out.println("<style type='text/css'>p {margin-top: 0px; margin-bottom: 0px}</style>");

		//  Print the Environment variables sent in from the CGI script.
		System.out.println("<h4 style='color: blue'><u>Here are the CGI environment variables/value pairs passed in from the CGI script: </u></h4>");
		System.out.println(CgiLib.Environment());

		// Run user App and get Output
		String cmd = generateCmd();
		try {
			runUserSoftware(cmd);
		} catch (Exception e) {
			System.err.println("could not run user app");
		}
		
		// Create the Bottom of the returned HTML page to close it cleanly.
		System.out.println(CgiLib.HtmlBot());
		  
	}
	
	private static void runUserSoftware (String cmd) throws Exception {
		System.out.println("<div id='comMessage'>");
		System.out.println("<h4 style='color: blue'><u>Here is the user command used to run user software: </u></h4>");
		System.out.println("<p class='com debug'>" + cmd + "</p>");
		
		// create runtime to execute external command
		Runtime rt = Runtime.getRuntime();
		Process pr = rt.exec(cmd);
		pr.waitFor();
		 
		// print user app ouput on HTML
		getProcessOuput(pr);
	}
	
	private static void newLine() {
		System.out.println("<br />");
	}
	
	private static String generateCmd() {
		return envName + scriptParamSeparator + userAppPath + userAppName + scriptParamSeparator + userAppParams;
	}
	
	private static String getQueryString() {
		return System.getProperty("cgi.query_string");
	}
	
	private static String getParamFormQueryString(String queryString) {
		return queryString.replace("&", scriptParamSeparator);
	}
	
	private static void getProcessOuput(Process pr) {
		Scanner errScn = new Scanner(pr.getErrorStream());
		errScn.useDelimiter("\r\n");
		Scanner dbgScn = new Scanner(pr.getInputStream());
		dbgScn.useDelimiter("\r\n");
		
		System.out.println("<h4 style='color: blue'><u>Here is the user software output: </u></h4>");
		while (errScn.hasNext()) {
			System.out.println(errScn.next());
			newLine();
		}
		
		while (dbgScn.hasNext()) {
			System.out.println(dbgScn.next());
			newLine();
		}
		System.out.println("</div>");
 
		errScn.close();
		dbgScn.close();
	}
}
