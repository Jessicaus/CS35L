# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions
# outside of this one, each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the
# imported functions.

"""
I used command `strace -f -e execve python3 topo_order_commits.py`
(use strace -f, but executed using python3) to give the following result:

execve("/usr/local/cs/bin/python3", 
["python3", "topo_order_commits.py"], 0x7ffd2ce98be0 /* 50 vars */) = 0

899f4d0a0126ddf2cd4678706003f8fa83345705 main
+++ exited with 0 +++

There is only one execve call shown, thus my code only starts one process,
and it is a python3 process. Thus, i did not invoke any other shell commands
or git commands.
"""

import os
import sys
import zlib

sys.setrecursionlimit(10000)

# get .git root directory
def get_git_directory():
    cur_dir = os.getcwd()
    while True:
        if os.path.exists(os.path.join(cur_dir, '.git')):
            return cur_dir
        par_dir = os.path.dirname(cur_dir)
        if par_dir == cur_dir:
            sys.stderr.write("Not inside a Git repository\n")
            sys.exit(1)
        cur_dir = par_dir

# get local branch names (commits and their names)
def get_local_branches(git_dir):
    heads_dir = os.path.join(git_dir, '.git', 'refs', 'heads')
    branches = {}
    for root, dirs, files in os.walk(heads_dir):
        # print("root=", root)
        # print("dirs=", dirs)
        for file in files:
            branch_dir = os.path.join(root, file)
            branch_name = os.path.relpath(branch_dir, heads_dir)
            """print(rel_path)
            print(os.path.join(root, file))
            branches.append(rel_path)"""
            """rel_path2 = os.path.join
            (git_dir, '.git', 'refs', 'heads', rel_path)
            with open(rel_path2, 'r') as f:
                commit_hash = f.read().strip()
                # print(commit_hash)
                f.close()"""
            with open(branch_dir, 'r') as f:
                commit_hash = f.read().strip()

            # if the commit hash is not inside the dictionary yet
            if commit_hash not in branches:
                branches[commit_hash] = []
            branches[commit_hash].append(branch_name)
            # print(branches[commit_hash])
        for commit_hash in branches:
            branches[commit_hash].sort()
    # returns the dictionary of each head commits with their branch names
    return branches


class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# find object files with commit name, return parent commit names
def read_commit_object(git_dir, commit_hash):
    obj_dir = os.path.join(git_dir, '.git', 'objects', commit_hash[:2])
    obj_file = os.path.join(obj_dir, commit_hash[2:])
    try:
        with open(obj_file, 'rb') as f:  # read as binary code
            compressed = f.read()
        decompressed = zlib.decompress(compressed).decode()
        # print(decompressed)

        # Parse parents
        parents = []
        for line in decompressed.split('\n'):
            if line.startswith('parent '):
                parents.append(line.split()[1])
            elif line == '':
                break
        return parents  # returns list of parents with their commit hashes
    except FileNotFoundError:
        # print(f"Warning: Commit object {commit_hash}
        # is not a loose object (likely packed). Skipping.")
        return None

# build commit graph
def build_commit_graph(git_dir, branches):
    visited = {}  # create visited dictionary

    def dfs(commit_hash):
        if commit_hash in visited:
            return visited[commit_hash]

        cur = CommitNode(commit_hash)
        visited[commit_hash] = cur

        parents = read_commit_object(git_dir, commit_hash)
        if parents is not None:
            for parent_hash in parents:
                parent = dfs(parent_hash)
                cur.parents.add(parent)
                parent.children.add(cur)

    for branch in branches:
        """heads_dir = os.path.join(git_dir, '.git', 'refs', 'heads', branch)
        with open(heads_dir, 'r') as f:
            commit_hash = f.read().strip()
            print(commit_hash)
            read_commit_object(git_dir, commit_hash)
            f.close()"""
        dfs(branch)

# sort the commits
def topo_sort(git_dir, branches):
    order = []  # contains the final list of commit hashes to be printed
    visited = {}  # contains which nodes are visited

    def dfs(commit_hash):
        if commit_hash in visited:
            return visited[commit_hash]

        cur = CommitNode(commit_hash)
        visited[commit_hash] = cur

        parents = read_commit_object(git_dir, commit_hash)
        if parents:
            for parent_hash in parents:
                parent = dfs(parent_hash)  # go visit parent first
                cur.parents.add(parent_hash)
                parent.children.add(commit_hash)

        order.append(commit_hash)
        return cur

    for branch in branches:
        dfs(branch)  # goes through all the branches
    order.reverse()
    # because the previous recursion goes to
    # oldest commits first (root_commits),
    # we need to reverse for newest commmits to come first

    def print_graph(order, visited):
        sticky_start = False
        for i, commit_hash in enumerate(order):
            cur = visited[commit_hash]
            if sticky_start:
                print("=" + " ".join(cur.children))
                sticky_start = False

            if commit_hash in branches:
                print(commit_hash + " " + " ".join(branches[commit_hash]))
            else:
                print(commit_hash)

            # check if is last commit
            if i + 1 < len(order):
                next_commit = order[i + 1]
                if next_commit not in cur.parents:
                    print(" ".join(cur.parents) + "=\n")
                    sticky_start = True
    print_graph(order, visited)


def topo_order_commits():
    # print(get_git_directory())
    # branches = get_local_branches(get_git_directory())
    # build_commit_graph(get_git_directory(), branches)
    git_dir = get_git_directory()
    topo_sort(git_dir, get_local_branches(git_dir))


if __name__ == '__main__':
    topo_order_commits()
