# Security review

This advisory documents the findings of security vulnerabilities contained in the `Api::V1::MobileController` Rails controller. At the time of writing, the version of the vulnerable software could not be verified.

## Potential problem 1 - Authentication bypass

All actions implemented by this controller are accessible without authentication. It is assumed that the code in [line 2](./MobileController.rb#L2) `skip_before_action :authenticated` bypasses authentication, making all actions here publicly available. More information in A7 from OWASP Top Ten - [Missing Function Level Access Control](https://www.owasp.org/index.php/Top_10_2013-A7-Missing_Function_Level_Access_Control)

A recommendation would be to ensure all actions defined here are indeed public.

## Problem 2 - Insecure redirect

The action `redirect` is executed before any actions as defined by [line 4](./MobileController.rb#L4). The parameter `redirect_to` is not properly sanitized and allows redirection to any URL.	More information in A10 from OWASP Top Ten - [Unvalidated Redirects and Forwards](https://www.owasp.org/index.php/Top_10_2013-A10-Unvalidated_Redirects_and_Forwards)

The recommendation here would be to validate the `redirect_to` input parameter to only valid targets, or create a map between indexes and targets where a specific validated index would redirect to a specific target.

## Problem 3 - Remote Code Execution

[The safest way to constantize is never](http://gavinmiller.io/2016/the-safesty-way-to-constantize/). The unsanitized parameter `class` is mapped into an internal Rails object via the calls `classify.constantize`. This allows the attacker to instantiate whatever object he wants by passing the desired code through the parameter `class`, thus getting remote code execution. This can be seen in lines [10](./MobileController.rb#L10), [17](./MobileController.rb#L17) and [26](./MobileController.rb#L26). More information in A1 from OWASP Top Ten - [Injection](https://www.owasp.org/index.php/Top_10_2013-A1-Injection)

The recommendation is similar to the one in problem 2, where a whitelist of possible variations of the variable `class` can be considered for input, or indexes to instantiate a specific model.

## Problem 4 - SQL Injection

In action `show_details`, [line 27](./MobileController.rb#L27), the parameter `q` is not properly sanitized allowing an attacker to inject code into the `model.where()` method, which seems to be a SQL query. This allows for many nasty things and should never be allowed.

The recomendation is to parameterize and sanitize any string before injecting it into other strings.


#Note

Usually an advisory will come with much more information such as:

* Criticality and link to the classification methodology
* Publish Date
* Affected Systems and Software and their versions
* Executive Summary
* Temporary Workarounds

The above review can be greatly enhanced with information but it makes the point of identifying the vulnerabilities, giving more information through links and a quick recommendation which I believe is sufficient for this challenge.

For the code analysis, one can do it by looking at the code or by running static code analysis tools such as brakeman. The following warnings were highlighted by brakeman for this particular controller:

```  
== Warnings ==

Confidence: High
Category: Redirect
Check: Redirect
Message: Possible unprotected redirect
Code: redirect_to(params[:redirect_to])
File: app/controllers/MobileController.rb
Line: 41

Confidence: High
Category: Remote Code Execution
Check: UnsafeReflection
Message: Unsafe reflection method constantize called with parameter value
Code: params[:class].classify.constantize
File: app/controllers/MobileController.rb
Line: 10

Confidence: High
Category: Remote Code Execution
Check: UnsafeReflection
Message: Unsafe reflection method constantize called with parameter value
Code: params[:class].classify.constantize
File: app/controllers/MobileController.rb
Line: 17

Confidence: High
Category: Remote Code Execution
Check: UnsafeReflection
Message: Unsafe reflection method constantize called with parameter value
Code: "#{params[:class]}Details".classify.constantize
File: app/controllers/MobileController.rb
Line: 26

Confidence: Medium
Category: SQL Injection
Check: SQL 
Message: Possible SQL injection
Code: "#{params[:class]}Details".classify.constantize.where("name = '#{params[:q]}' or id = '#{params[:q]}'")
File: app/controllers/MobileController.rb
Line: 27

```
