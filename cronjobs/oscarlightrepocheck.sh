#!  /bin/bash

printUsage() {
	echo "Usage: <oscarlightrepocheck.sh> <oscarLightRepo Dir>"
}

if [[ -z "$1" ]] ; then
	printUsage
	exit 1
fi

pr() {
	datetime=$(date +%Y%m%d_%H%M%S)
	echo "[$datetime] $*"
	
}

todir="$1"

cd $todir
rc=$?
if [[ $rc -ne 0 ]] ; then
	pr "There was a failure cd'ing to '$todir' ; rc=$rc"
	exit $rc
fi

pr "Running cmd >> git fetch"
git fetch
rc=$?
if [[ $rc -ne 0 ]] ; then
	pr "There was a failure calling >> git fetch ; rc=$rc"
	exit $rc
fi

pr "Running cmd >> git log HEAD..origin/master --oneline"
output=$(git log HEAD..origin/master --oneline)
rc=$?
if [[ $rc -ne 0 ]] ; then
	pr "There was a failure calling >> git log HEAD..origin/master --oneline ; rc=$rc"
	exit $rc
fi

datetime=$(date +%Y%m%d_%H%M%S)
if [[ -z "$output" ]] ; then
# this means there is nothing to update.
	pr "Nothing to update"
	exit 0
else
	pr "Found changes..."
	pr "Running cmd >> git pull"
	rc=$?
	if [[ $rc -ne 0 ]] ; then
		pr "There was a failure calling >> git pull ; rc=$rc"
		exit $rc
	else
		pr "Succeeded in updating the repository"
		exit 0
	fi
fi


