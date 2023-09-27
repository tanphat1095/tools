# Merge file
This tool has the purpose of combining multiple files into a single file.

For example:

In the development process, we create a lot of database scripts in several SQL files.

And when we want to release production to the customer, we have to merge those files into a smaller number of files, so we can spend less time running them.
With this tool, we can configure the path of those files and the file name of the combined result and mark the source file that was combined with SIGN config.

We can add this tool to PATH or bin directories, so we can run anywhere with a parameter specifying a direct link to the workspace or run from the workspace.

The workspace has a file. merge-env, mapping's files.

This tool can support multi-workspaces with separate configurations for each workspace.