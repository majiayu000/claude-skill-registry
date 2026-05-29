### Git skills

---

#### How to delete all commit history in github

Deleting the .git folder may cause problems in your git repository. If you want to delete all your commit history but keep the code in its current state, it is very safe to do it as in the following:

1. Checkout/create orphan branch (this branch won't show in git branch command):

```
git checkout --orphan latest_branch
```

2. Add all the files to the newly created branch:

```
git add -A
```

3. Commit the changes:

```
git commit -am "commit message"
```

4. Delete main (default) branch (this step is permanent):

```
git branch -D main
```

5. Rename the current branch to main:

```
git branch -m main
```

6. Finally, all changes are completed on your local repository, and force update your remote repository:

```
git push -f origin main
```

PS: This will not keep your old commit history around. Now you should only see your new commit in the history of your git repository.

#### How to find/identify large commits in git history?

1. shell-1
```bash
git rev-list --objects --all \
  | grep "$(git verify-pack -v .git/objects/pack/*.idx \
           | sort -k 3 -n \
           | tail -10 \
           | awk '{print$1}')"
```
2. shell-2
```bash
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  sed -n 's/^blob //p' |
  sort --numeric-sort --key=2 |
  tail -10 |
  cut -c 1-12,41- |
  $(command -v gnumfmt || echo numfmt) --field=2 --to=iec-i --suffix=B --padding=7 --round=nearest
```

3. shell-3
```bash
#!/bin/bash
#set -x 
 
# Shows you the largest objects in your repo's pack file.
# Written for osx.
#
# @see https://stubbisms.wordpress.com/2009/07/10/git-script-to-show-largest-pack-objects-and-trim-your-waist-line/
# @author Antony Stubbs
 
# set the internal field separator to line break, so that we can iterate easily over the verify-pack output
IFS=$'\n';
 
# list all objects including their size, sort by size, take top 10
objects=`git verify-pack -v .git/objects/pack/pack-*.idx | grep -v chain | sort -k3nr | head`
 
echo "All sizes are in kB's. The pack column is the size of the object, compressed, inside the pack file."
 
output="size,pack,SHA,location"
allObjects=`git rev-list --all --objects`
for y in $objects
do
    # extract the size in bytes
    size=$((`echo $y | cut -f 5 -d ' '`/1024))
    # extract the compressed size in bytes
    compressedSize=$((`echo $y | cut -f 6 -d ' '`/1024))
    # extract the SHA
    sha=`echo $y | cut -f 1 -d ' '`
    # find the objects location in the repository tree
    other=`echo "${allObjects}" | grep $sha`
    #lineBreak=`echo -e "\n"`
    output="${output}\n${size},${compressedSize},${other}"
done
 
echo -e $output | column -t -s ', '
```
