# Chapter 2: Linux Command Primer

**Essential Commands for Server Management**

---

## Learning Objectives

By the end of this chapter, you'll be able to:
- ✅ Navigate the Linux filesystem
- ✅ Create, edit, and delete files
- ✅ Understand command structure and options
- ✅ Use sudo for administrative tasks
- ✅ Read and search file contents
- ✅ Manage processes and permissions

**Time Required:** 30-45 minutes

---

## Why Learn Command Line?

### The Power of Text

**Servers don't have graphical interfaces** - everything is done via text commands.

**Think of it like:**
- **GUI (Graphical):** Clicking folders, dragging files
- **CLI (Command Line):** Typing exact instructions

**Command line is:**
- Faster (once you know it)
- More powerful (can automate)
- Universal (works on any server)
- Professional (how real work gets done)

---

## Command Structure

### Anatomy of a Command

```bash
command -options argument
```

**Example:**
```bash
ls -la /home
```

**Breaking it down:**
- `ls` = command (list files)
- `-la` = options (long format, show all)
- `/home` = argument (which directory)

### Common Patterns

**No arguments:**
```bash
pwd        # Show current directory
date       # Show current date/time
whoami     # Show current user
```

**With arguments:**
```bash
cd /var/log      # Change to /var/log directory
cat myfile.txt   # Show contents of myfile.txt
```

**With options:**
```bash
ls -l            # List in long format
ls -a            # List all (including hidden)
ls -la           # Both options together
```

---

## Essential Commands

### 1. Navigation Commands

#### `pwd` - Print Working Directory

**What it does:** Shows where you are in the filesystem.

```bash
pwd
```

**Output example:**
```
/home/yourusername
```

**Think of it as:** "Where am I right now?"

---

#### `ls` - List Directory Contents

**What it does:** Shows files and folders in current directory.

**Basic usage:**
```bash
ls                    # List files
ls -l                 # Long format (permissions, size, date)
ls -a                 # Show hidden files (start with .)
ls -la                # Long format + hidden files
ls -lh                # Human-readable sizes (KB, MB, GB)
ls /var/log           # List specific directory
```

**Output example:**
```bash
$ ls -la
total 32
drwxr-xr-x  5 user user 4096 Nov 12 10:30 .
drwxr-xr-x  3 root root 4096 Nov 10 15:00 ..
-rw-r--r--  1 user user  220 Nov 10 15:00 .bash_logout
drwxrwxr-x  2 user user 4096 Nov 12 10:30 my_project
-rw-rw-r--  1 user user  100 Nov 12 10:25 notes.txt
```

**Reading the output:**
- `d` = directory, `-` = file
- `rwx` = read, write, execute permissions
- Numbers = file size in bytes
- Date/time = last modified
- Name = file/folder name

---

#### `cd` - Change Directory

**What it does:** Move to a different directory.

**Common uses:**
```bash
cd /home              # Go to /home directory
cd ..                 # Go up one level
cd ~                  # Go to your home directory
cd                    # Also goes home (shortcut)
cd -                  # Go to previous directory
```

**Examples:**
```bash
$ pwd
/home/user

$ cd /var/log
$ pwd
/var/log

$ cd ..
$ pwd
/var

$ cd ~
$ pwd
/home/user
```

---

### 2. File Operations

#### `mkdir` - Make Directory

**What it does:** Creates new directories.

```bash
mkdir myproject              # Create one directory
mkdir -p path/to/deep/dir    # Create nested directories
mkdir dir1 dir2 dir3         # Create multiple at once
```

**The `-p` flag is important:**
```bash
mkdir project/src/components    # ERROR if project doesn't exist
mkdir -p project/src/components # Creates all directories needed
```

---

#### `touch` - Create Empty File

**What it does:** Creates a new empty file (or updates timestamp if exists).

```bash
touch myfile.txt
touch file1.txt file2.txt file3.txt
```

**Use it to:**
- Create placeholder files
- Test if you have write permission
- Update file modification time

---

#### `cp` - Copy Files

**What it does:** Copies files or directories.

```bash
cp source.txt destination.txt        # Copy file
cp file.txt /backup/file.txt         # Copy to different location
cp -r directory/ /backup/directory/  # Copy directory (recursive)
```

**Important:** Use `-r` for directories!

---

#### `mv` - Move or Rename

**What it does:** Moves files to new location OR renames them.

**Moving:**
```bash
mv file.txt /tmp/file.txt       # Move to /tmp
mv *.txt documents/             # Move all .txt files
```

**Renaming:**
```bash
mv oldname.txt newname.txt      # Rename file
mv old_folder new_folder        # Rename directory
```

---

#### `rm` - Remove Files

**What it does:** Deletes files and directories.

**⚠️ WARNING:** No undo! Files are gone forever.

```bash
rm file.txt                  # Delete file
rm file1.txt file2.txt       # Delete multiple files
rm *.txt                     # Delete all .txt files
rm -r directory/             # Delete directory and contents
rm -rf directory/            # Force delete (no prompts)
```

**Safety tips:**
- Always double-check before `rm -rf`
- Use `ls` first to verify what you're deleting
- Start with `rm -i` (interactive) when learning

---

### 3. File Viewing Commands

#### `cat` - Concatenate and Display

**What it does:** Shows entire file contents.

```bash
cat file.txt                 # Display file
cat file1.txt file2.txt      # Display multiple files
cat > newfile.txt            # Create file (Ctrl+D to save)
```

**Good for:** Small files you want to see completely.

**Not good for:** Large files (they scroll forever).

---

#### `less` - Page Through Files

**What it does:** View large files one page at a time.

```bash
less bigfile.log
```

**Controls:**
- `Space` = next page
- `b` = previous page
- `/searchterm` = search forward
- `?searchterm` = search backward
- `q` = quit

**Better than `cat` for:** Log files, large text files.

---

#### `head` and `tail`

**What they do:** Show beginning or end of file.

```bash
head file.txt            # First 10 lines
head -n 20 file.txt      # First 20 lines
tail file.txt            # Last 10 lines
tail -n 50 file.txt      # Last 50 lines
tail -f /var/log/app.log # Follow file (live updates)
```

**`tail -f` is incredibly useful** for watching log files in real-time!

---

#### `grep` - Search in Files

**What it does:** Finds lines containing search term.

```bash
grep "error" logfile.txt              # Find lines with "error"
grep -i "error" logfile.txt           # Case-insensitive
grep -r "TODO" ./                     # Search all files recursively
grep -n "function" script.js          # Show line numbers
grep -v "debug" logfile.txt           # Show lines WITHOUT "debug"
```

**Essential for:** Searching logs, finding configuration, debugging.

---

### 4. Text Editing

#### `nano` - Simple Text Editor

**What it does:** Edit files in the terminal.

```bash
nano filename.txt
```

**Controls (shown at bottom):**
- `Ctrl+O` = Save (Write Out)
- `Ctrl+X` = Exit
- `Ctrl+K` = Cut line
- `Ctrl+U` = Paste line
- `Ctrl+W` = Search

**Best for beginners** - easy to use, shows commands on screen.

---

#### `vim` - Advanced Editor (Optional)

**What it does:** Powerful but complex editor.

**Basic survival:**
```bash
vim filename.txt
# Press 'i' to enter Insert mode
# Type your changes
# Press Esc to exit Insert mode
# Type ':wq' and Enter to save and quit
# Type ':q!' and Enter to quit without saving
```

**You'll encounter vim** when editing git commits or system files. Know the basics to escape!

---

### 5. System Information

#### `whoami` - Current User

```bash
whoami
# Output: yourusername
```

---

#### `hostname` - Server Name

```bash
hostname
# Output: server-name
```

---

#### `df` - Disk Space

```bash
df -h                # Disk space (human-readable)
```

**Output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        25G  5.2G   18G  23% /
```

---

#### `du` - Directory Size

```bash
du -sh *             # Size of each item in current directory
du -sh /var/log      # Size of specific directory
```

---

#### `free` - Memory Usage

```bash
free -h              # Memory (human-readable)
```

---

#### `top` - Process Monitor

```bash
top                  # Live view of running processes
```

**Controls:**
- `q` = quit
- `k` = kill process
- `M` = sort by memory
- `P` = sort by CPU

**Better alternative:** `htop` (install with `sudo apt install htop`)

---

### 6. Permissions and Ownership

#### Understanding Permissions

**Every file has:**
- **Owner** - User who owns it
- **Group** - Group that owns it
- **Permissions** - Who can read/write/execute

**Permission format:**
```
-rw-r--r--
```

**Breaking it down:**
```
- rw- r-- r--
│ │   │   │
│ │   │   └── Others: read only
│ │   └────── Group: read only
│ └────────── Owner: read + write
└──────────── File type (- = file, d = directory)
```

**Permission values:**
- `r` = read (4)
- `w` = write (2)
- `x` = execute (1)
- `-` = no permission (0)

---

#### `chmod` - Change Permissions

**What it does:** Modifies file permissions.

**Symbolic method:**
```bash
chmod +x script.sh          # Add execute permission
chmod -w file.txt           # Remove write permission
chmod u+x,g+r file.txt      # User execute, group read
```

**Numeric method:**
```bash
chmod 644 file.txt          # rw-r--r-- (common for files)
chmod 755 script.sh         # rwxr-xr-x (common for scripts)
chmod 700 private.txt       # rwx------ (owner only)
```

**Common patterns:**
- `644` = Files (owner can edit, others can read)
- `755` = Executables (owner can edit/run, others can run)
- `600` = Private files (owner only)
- `700` = Private scripts (owner only)

---

#### `chown` - Change Owner

**What it does:** Changes file owner/group.

```bash
sudo chown user file.txt              # Change owner
sudo chown user:group file.txt        # Change owner and group
sudo chown -R user:group directory/   # Recursive
```

**Usually requires sudo** because you're changing ownership.

---

### 7. Sudo - Superuser Do

#### What is sudo?

**sudo** = "Superuser Do" = Run command as administrator

**Without sudo:**
```bash
apt update
# Error: Permission denied
```

**With sudo:**
```bash
sudo apt update
# Works! (may ask for password)
```

**When to use sudo:**
- ✅ Installing software
- ✅ Editing system files
- ✅ Changing system settings
- ✅ Managing services

**When NOT to use sudo:**
- ❌ Regular file operations in your home directory
- ❌ Running your own scripts
- ❌ Creating your own files

**Rule of thumb:** Only use sudo when command fails without it.

---

### 8. Process Management

#### `ps` - Process Status

```bash
ps                    # Your processes
ps aux                # All processes
ps aux | grep nginx   # Find nginx processes
```

---

#### `kill` - Terminate Process

```bash
kill 1234             # Kill process ID 1234
kill -9 1234          # Force kill (SIGKILL)
killall nginx         # Kill all nginx processes
```

**Finding process ID:**
```bash
ps aux | grep myapp
# Output shows PID in second column
```

---

### 9. Network Commands

#### `ping` - Test Connectivity

```bash
ping google.com          # Test if server is reachable
ping -c 4 google.com     # Ping 4 times and stop
```

**Ctrl+C to stop**

---

#### `curl` - Transfer Data

```bash
curl https://example.com              # Download webpage
curl -I https://example.com           # Show headers only
curl -o file.html https://example.com # Save to file
```

---

#### `wget` - Download Files

```bash
wget https://example.com/file.zip     # Download file
wget -O newname.zip https://...       # Download with new name
```

---

### 10. Pipes and Redirection

#### Pipes (`|`) - Chain Commands

**What it does:** Sends output of one command to another.

```bash
ls -la | grep ".txt"              # List only .txt files
cat logfile.txt | grep "error"    # Show only error lines
ps aux | grep nginx | wc -l       # Count nginx processes
```

**Reads as:** "Do command 1, THEN pass results to command 2"

---

#### Redirection (`>` and `>>`)

**What it does:** Saves output to file.

```bash
ls -la > file_list.txt         # Write to file (overwrites)
echo "new line" >> file.txt    # Append to file
```

**Examples:**
```bash
# Save error log
grep "error" app.log > errors.txt

# Append to log
echo "$(date): Task completed" >> daily.log

# Redirect errors
command 2> errors.log          # Save error messages
command > output.log 2>&1      # Save both output and errors
```

---

## Combining Commands

### Real-World Examples

**Find large files:**
```bash
du -sh * | sort -h
```

**Count lines in all .txt files:**
```bash
cat *.txt | wc -l
```

**Find and delete old log files:**
```bash
find /var/log -name "*.log" -mtime +30 -delete
```

**Show last 100 errors from log:**
```bash
grep "ERROR" /var/log/app.log | tail -100
```

**Monitor live logs:**
```bash
tail -f /var/log/syslog | grep --color "error"
```

---

## Practice Exercises

### Exercise 1: Navigation

```bash
# 1. Where are you?
pwd

# 2. List files (including hidden)
ls -la

# 3. Go to /tmp directory
cd /tmp

# 4. Go back to your home
cd ~
```

---

### Exercise 2: File Operations

```bash
# 1. Create a directory called 'practice'
mkdir practice

# 2. Go into it
cd practice

# 3. Create three empty files
touch file1.txt file2.txt file3.txt

# 4. List them
ls -l

# 5. Put some text in file1.txt
echo "Hello World" > file1.txt

# 6. View it
cat file1.txt

# 7. Copy it to file4.txt
cp file1.txt file4.txt

# 8. Rename file2.txt to backup.txt
mv file2.txt backup.txt

# 9. Delete file3.txt
rm file3.txt

# 10. List what's left
ls -l
```

---

### Exercise 3: Searching

```bash
# 1. Create a file with some content
cat > sample.txt << EOF
This is line 1
Error on line 2
This is line 3
Another error on line 4
Final line 5
EOF

# 2. View the file
cat sample.txt

# 3. Search for "error" (case-insensitive)
grep -i "error" sample.txt

# 4. Count how many lines have "error"
grep -i "error" sample.txt | wc -l

# 5. Show line numbers
grep -n "error" sample.txt
```

---

## Command Cheat Sheet

### Navigation
```bash
pwd                  # Where am I?
ls -la               # What's here?
cd /path/to/dir      # Go there
cd ..                # Go up one level
cd ~                 # Go home
```

### Files
```bash
mkdir dirname        # Create directory
touch filename       # Create empty file
cp source dest       # Copy
mv old new           # Move/rename
rm filename          # Delete file
rm -r dirname        # Delete directory
```

### Viewing
```bash
cat file.txt         # Show entire file
less file.txt        # Page through file (q to quit)
head file.txt        # First 10 lines
tail file.txt        # Last 10 lines
tail -f file.txt     # Follow file (live updates)
```

### Searching
```bash
grep "term" file     # Search in file
grep -r "term" dir/  # Search in directory
find . -name "*.txt" # Find files by name
```

### System
```bash
whoami               # Current user
hostname             # Server name
df -h                # Disk space
free -h              # Memory usage
top                  # Process monitor
ps aux               # All processes
```

### Permissions
```bash
chmod 644 file       # Set permissions
chmod +x script.sh   # Make executable
chown user file      # Change owner
```

---

## Common Patterns You'll Use

### Check if service is running
```bash
ps aux | grep servicename
```

### View last 100 lines of log
```bash
tail -100 /var/log/syslog
```

### Find large directories
```bash
du -sh */ | sort -h
```

### Count files in directory
```bash
ls -1 | wc -l
```

### Create and enter directory
```bash
mkdir mydir && cd mydir
```

### Backup a file before editing
```bash
cp config.txt config.txt.backup
```

---

## Tips for Success

### 1. Tab Completion

**Press Tab to auto-complete:**
```bash
cd /var/l[Tab]
# Becomes: cd /var/log
```

**Press Tab twice to see options:**
```bash
cd /var/[Tab][Tab]
# Shows: backups/ cache/ lib/ local/ log/ ...
```

**Saves tons of typing!**

---

### 2. Command History

**Up/Down arrows** - Navigate previous commands

**Ctrl+R** - Search command history
```bash
# Press Ctrl+R
# Type: grep
# Shows last command containing "grep"
# Press Enter to run it
```

**`history` command** - See all past commands
```bash
history              # Show all commands
history | grep docker # Find docker commands
!123                 # Run command #123 from history
!!                   # Run previous command
sudo !!              # Run previous command with sudo
```

---

### 3. Clearing the Screen

```bash
clear                # Clear screen (or Ctrl+L)
```

---

### 4. Canceling Commands

**Ctrl+C** - Stop current command

**Ctrl+Z** - Suspend command (background it)

---

### 5. Getting Help

```bash
man ls               # Manual for ls command
ls --help            # Quick help
command --help       # Works for most commands
```

---

## Troubleshooting

### "Command not found"

**Problem:** Typo or command not installed

**Solution:**
```bash
# Check spelling
which commandname

# Install if needed (Ubuntu/Debian)
sudo apt install packagename
```

---

### "Permission denied"

**Problem:** Don't have rights to do that

**Solution:**
```bash
# Try with sudo
sudo command

# Or check file permissions
ls -l filename
```

---

### Can't exit vim

**Problem:** Stuck in vim

**Solution:**
```
Press Esc
Type :q!
Press Enter
```

---

### Deleted wrong file

**Problem:** Used `rm` by mistake

**Solution:** Unfortunately, no easy undo. This is why:
- Always use `ls` first to verify
- Use `rm -i` when learning (prompts for confirmation)
- Make backups of important files

---

## Next Steps

**You now know:**
- ✅ Essential Linux commands
- ✅ How to navigate filesystem
- ✅ How to create, edit, delete files
- ✅ How to search and filter
- ✅ Basic permissions and ownership

**In Chapter 3, you'll learn:**
- Linux file structure (/etc, /var, /home)
- File permissions in depth
- User and group management
- Security implications

---

## Practice Before Moving On

**Spend 15-20 minutes:**
1. Navigate around your computer using `cd`, `ls`, `pwd`
2. Create a practice directory with files
3. Try different commands from this chapter
4. Get comfortable with the terminal

**The more you practice now, the easier the rest of the course will be!**

---

[← Previous: Chapter 1 - Introduction](01-introduction.md) | [Next: Chapter 3 - Linux Permissions →](03-linux-permissions.md)
