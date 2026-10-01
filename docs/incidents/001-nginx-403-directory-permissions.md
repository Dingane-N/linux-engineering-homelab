# Incident 001 - Nginx 403 Caused by Directory Permissions

## Environment

Affected system: DingasHost3 
Operating system: RHEL 10 
Role: Application Node B 
Service: Nginx 
Management IP: 10.10.10.21

## Symptom

Requests to the application returned:

HTTP/1.1 403 Forbidden

The problem occurred both locally and remotely from DingasHost1.

## Initial Validation

The following components were healthy:

- Nginx service active
- Nginx configuration syntax valid
- Port 80 listening
- firewalld permitted HTTP
- SELinux remained Enforcing
- Application file existed
- SELinux context was httpd_sys_content_t

## Evidence

Nginx error log reported:

Permission denied

while attempting to access:

/usr/share/nginx/html/dingas-app/index.html

## Root Cause

A permissions command intended for regular files mistakenly targeted
directories:

find /usr/share/nginx/html/dingas-app -type d -exec chmod 644 {} \;

This removed the execute/traverse permission from the application directory.

Incorrect directory permissions:

drw-r--r--

## Remediation

Directories were restored to mode 755:

find /usr/share/nginx/html/dingas-app -type d -exec chmod 755 {} \;

Regular files were set to mode 644:

find /usr/share/nginx/html/dingas-app -type f -exec chmod 644 {} \;

SELinux contexts were restored:

restorecon -RFv /usr/share/nginx/html/dingas-app

## Validation

Local request:

curl -H 'Host: dingashost3.lab.test' http://10.10.10.21/

Remote request from DingasHost1:

curl -H 'Host: dingashost3.lab.test' http://10.10.10.21/

Result:

HTTP/1.1 200 OK

## Lessons Learned

- Successful command execution does not mean the command was correct.
- Directories require execute permission for traversal.
- Validate permissions with namei, ls, and service logs.
- Do not disable SELinux before proving SELinux is responsible.
- Troubleshoot layer by layer instead of changing multiple controls at once.
