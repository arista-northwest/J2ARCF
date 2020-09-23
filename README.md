Prepared by: <msft-team@arista.com>  
Date: September 22nd, 2020  
Version: 1.0

# J2ARCF Tool

A simple python script that looks at Juniper's router policy language and converts the framework to Arista's RCF policy language. The script evaluates JUNOS "display set" policy-statements and functionaly breaks them into two parts.

## FILE
Set your READ file path in the script: `READ_FILE=/path/to/file`


The script will run a loop over the policy language and only convert lines with a `policy-statement` value. This version of the script will print the converted language to screen.


## PARSE

The parse function evaluates the "from" statement in JUNOS.

In here we define a parse value list.

```
def parse(): 
	pv = ['protocol bgp']
```

If you wish to create a new term to evaluate simply add to the pv list.  Once you have added to the list with the term you wish to evaluate, the script will begin your string search to find the criteria you would like to equate to a RCF statement.

In this example we are looking for `protocol bgp` and writing out what the converted RCF statement. 

```
if row[0].find(pv[0]) > 1:
	v1 = row[0].find(pv[0])
	v2 = len(pv[0])
	v = ('####{NewFeature}#### source_protocol is BGP')
```

All terms with a policy-statement get evaluated.  If for whatever reason the script found a term that needs converted but has not been specified in our parse value list, the following error will be written in the converted RCF funtion.

```
#UNDEFINED-FROM-POLICY"
```

## SET VALUE

The setvalue function evaluates the "then" statement in JUNOS.

In here we define a set value list.

```
def setvalue():
    sv = ['local-preference']
```

If you wish to create a new term to evaluate simply add to the sv list.  Once you have added to the list with the term you wish to evaluate, the script will begin your string search to find the criteria you would like to equate to a RCF statement.

In this example we are looking for `local-preference` and writing out what the converted RCF statement. 

```
if row[0].find(sv[0]) > 1:
    v1 = row[0].find(sv[0])
    v2 = len(sv[0])
    v = ('local_preference =' + row[0][v1+v2:])
```

All terms with a policy-statement get evaluated.  If for whatever reason the script found a term that needs converted but has not been specified in our parse value list, the following error will be written in the converted RCF funtion.

```
#UNDEFINED-THEN-POLICY"
```

## EXAMPLE JUNOS POLICY

Here is an example of a JUNOS policy.

```
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068_overload from protocol bgp
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068_overload from as-path AS8068
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068_overload from color 10293
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068_overload then local-preference 10
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068_overload then accept
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068 from protocol bgp
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068 from as-path AS8068
set policy-options policy-statement ADVERTISE-AS8068 term allow_8068 then accept
```

Here is what the J2ARCF tool converted the policy to.

```
#########################FUNCTION########################
function  ADVERTISE-AS8068  () {
#########################TERM############################
#  ALLOW_8068_OVERLOAD  
#########################################################
if source_protocol is BGP and
as_path match as_path_list AS8068 and
ext_community match ext_community_list_COLOR_10293 {
local_preference = 10 ;
return true ;
#########################TERM############################
#  ALLOW_8068  
#########################################################
} else if source_protocol is BGP and
as_path match as_path_list AS8068 {		
return true ;
}
```

## NOTES
The tool takes all route-filters, prefix-lists, and prefix-list-range commands and populates a prefix-list to call within the function and it is named after the term.

Version 1.0 

- Fixing bugs with string search logic
- Fixing bugs with operator logic `if, and, or, not, {}`
- Adding new RCF language the RCF statement commented out

