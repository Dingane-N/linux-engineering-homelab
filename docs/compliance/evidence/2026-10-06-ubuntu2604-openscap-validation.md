# Ubuntu 26.04 OpenSCAP Content Validation

**Date:** 2026-10-06
**System:** dingashost4.lab.test
**Operating System:** Ubuntu 26.04.1 LTS
**Compliance Tool:** OpenSCAP 1.4.3
**ComplianceAsCode Release:** 0.1.82

---

## Objective

The objective of this session was to obtain native Ubuntu 26.04 ComplianceAsCode content and determine whether DingasHost4 could undergo a formal OpenSCAP baseline compliance assessment.

The intention was to establish the following workflow:

Ubuntu 26.04 Datastream
ComplianceAsCode 0.1.82 was downloaded and extracted on DingasHost4.
The Ubuntu 26.04 source datastream was located at:
	~/scap/0.1.82/scap-security-guide-0.1.82/ssg-ubuntu2604-ds.xml

The datastream was assigned to:
	DS="$(find "$HOME/scap/0.1.82" \
	-type f \
	-name 'ssg-ubuntu2604-ds.xml' \
	-print -quit)"

Verification:
	echo "$DS"
	test -f "$DS" && echo "Datastream OK"

Result:
	Datastream OK

OpenSCAP CPE Packaging Issue
During initial inspection, OpenSCAP failed because the expected default CPE files were absent from:
	/usr/share/openscap/cpe/

The required OpenSCAP 1.4.3 CPE files were obtained and installed as:
	/usr/share/openscap/cpe/openscap-cpe-dict.xml
	/usr/share/openscap/cpe/openscap-cpe-oval.xml

Final permissions and ownership were validated as:
	regular file | -rw-r--r-- | root:root

After correcting the CPE files, OpenSCAP successfully parsed the Ubuntu 26.04 source datastream.

Datastream Validation
The source datastream was validated with:
	oscap ds sds-validate "$DS"
	echo $?

Result response:
	0

An exit status of 0 confirmed that the datastream passed source datastream validation.
Profile Investigation
After Datastream validation was successful, the following command was used to inspect available profiles:
	oscap info --profiles "$DS"

*No evaluable profiles were returned.*

Further inspection confirmed that the datastream contains only two Ubuntu 26.04 rule identifiers:
	grep -o 'xccdf_org.ssgproject.content_rule_[^"]*' "$DS" \
	| sort -u

Result:
	xccdf_org.ssgproject.content_rule_installed_OS_is_vendor_supported
	xccdf_org.ssgproject.content_rule_ufw_rules_for_open_ports

Rule count:
	grep -o 'xccdf_org.ssgproject.content_rule_[^"]*' "$DS" \
	| sort -u \
	| wc -l

Result response:
	2

Engineering Decision
A formal Ubuntu 26.04 compliance baseline was not generated from this content.
The available datastream was validated successfully, but it does not currently expose a sufficiently comprehensive security profile for the intended PCI-DSS-aligned Ubuntu assessment.
Ubuntu 24.04 security profiles were deliberately not applied to the Ubuntu 26.04 server.
This avoids presenting results generated from a different operating system baseline as valid Ubuntu 26.04 compliance evidence.

The following stages are therefore deferred:
Formal baseline compliance scan
        |
        v
Failed-control analysis
        |
        v
Automated/selective remediation
        |
        v
Post-remediation comparison

These stages will resume when appropriate Ubuntu 26.04 compliance content is available.
Current Compliance Status
	OpenSCAP installed                     COMPLETE
	OpenSCAP execution verified            COMPLETE
	Ubuntu 26.04 datastream obtained       COMPLETE
	CPE dependency issue resolved          COMPLETE
	Datastream validation                  COMPLETE
	Profile discovery                      COMPLETE
	Formal baseline assessment             DEFERRED
	Compliance remediation                 DEFERRED

Next Implementation Stage

Development continues with controls that can be implemented and tested independently of the unavailable Ubuntu 26.04 compliance profile:


PostgreSQL backup automation
        |
        v
Backup restoration validation
        |
        v
Centralized log retention
        |
        v
Security event detection
        |
        v
SIEM-style correlation
        |
        v
Ansible least-privilege hardening


Ubuntu 26.04 SCAP content
        |
        v
Baseline compliance scan
        |
        v
Analyze failed controls
        |
        v
Selective remediation
        |
        v
Re-scan and compare
