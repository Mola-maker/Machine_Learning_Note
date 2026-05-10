1. stand for :Secure Hash Algorithm, 1st version
2. functions:
	1. takes any input (a single character, a 10GB file, anything) and produces a fixed 160-bit output, written as 40 hex characters(16)
		1. "hello" → aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d 
		2. "hello!" → 92a02fce14da11de1bd6cdce93443c89b8c1ff60 
		3. "" (empty) → da39a3ee5e26b9b4d883e98df0a4f1c4b7c5e7a6
	2. - **Deterministic** — same input always produces the same output. Forever. On any computer.
	  - **Fixed size** — output is always exactly 40 hex characters, regardless of input size.
	 - **Avalanche effect** — change one bit of input, ~half the output bits change. There's no relationship between similar inputs and similar outputs.
 command  
	 Get-FileHash (filename.xxx)-Algorithm SHA1
	 echo "hello" | git hash-object --stdin (in GIT)
 3.SHA-1 in GIT :
	 When you `git commit`:
		1. Git builds a **tree** object listing every file's name + blob hash.
		2. Git hashes the tree → e.g., `e5f6g7h8...`.
		3. Git builds a **commit** object containing: tree hash + parent commit hash + author + message.
		4. Git hashes the commit → e.g., `9f8e7d6c...`.
		5. hash is taking effect on every classes 
		6. **Every commit hash you see in `git log` is a SHA-1.** Try it:

powershell

```powershell
cd D:\OBfile\Machine_Learning_Note
git log --oneline
```

Each 7-character prefix you see is the first 7 hex of a 40-character SHA-1.

powershell

```powershell
git log -1 --format=%H
```

That's the full 40-character hash of the latest commit.

4.content-addressed storage 
	Files aren't stored by name — they're stored by the hash of their content. 
	The same file content, anywhere in your repo, hashes to the same value, so Git stores it once.
	Two files with identical content (say, two empty `.gitkeep` files) → same blob, stored exactly once. 
	Different files with same name across commits → different blobs, both stored. The name is just a label in a tree object pointing at the content.
5.**Renaming a file is "free."** The blob doesn't change — only the tree's filename → hash mapping changes. Git can detect renames by noticing two trees that point at the same blob from different filenames.

**Identical history is automatically deduplicated.** If you and a friend independently make a commit with identical content, parent, author, and timestamp, you'd get the same SHA-1. (In practice, timestamps differ by milliseconds, so this is theoretical.)

**History is tamper-evident.** Each commit hash includes its parent's hash. If someone alters an ancient commit, that commit's hash changes, which means the next commit (which records the parent's hash) is now wrong, which means _its_ hash should change too, and so on. Altering one old commit invalidates every commit after it. This is the same idea as a blockchain — Git is, technically, a blockchain.
6.now git use SHA-256 256bits  much more safer