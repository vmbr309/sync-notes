# notes-sync

A CLI tool to sync a notes repository automatically.


## Features:

- git pull
- auto stage changes
- timestamped commits
- git push
- optional [Skate](https://github.com/charmbracelet/skate) config

Built with ChatGPT (for now)

## Behavior

When executed, the program performs the following steps:
	1.	git pull
	2.	Detects uncommitted changes
	3.	If changes exist:
	•	git add .
	•	git commit
	•	git push
	4.	If no changes exist:
	•	prints a message and exits

## Instalation

### Using PIPX:

1. Install PIPX (via Brew onMacOS):

``` shell
brew install pipx
```
2. Clone this repo:

``` shell
git clone https://github.com/vmbr309/sync-notes.git 
```

3. CD into the cloned repo and run PIPX Install

``` shell
cd notes-sync
pipx install .
```

## Usage

1. Install Skate

``` shell
brew tap charmbracelet/tap && brew install charmbracelet/tap/skate
```

2. Set your values:

``` shell
skate set NOTES_REPO <path-to-your-notes>
skate set NOTES_COMMIT_MSG <commit-message> # your custom commit message, in "quotes"
```

3. Ensure your keys for pushing to the remote repo are properly set, then:

``` shell
notes-sync
```

Will automatically push to the set NOTES_REPO

### Available Arguments

``` shell
notes-sync [repo] # sync to your desired repo
notes-sync -m, --message # add your commit message. A timestamp is automatically appended.
notes-sync -h, --help # show help docs

```




