# pySyncit

This is a simple tool designed to keep folders and files in sync with two modes: update and mirror.
- A mirror sync will adjust the destination folders/files to match the source folders/files by deleting any files and folders that exist in the destination location but do not appear in the source folders/files.
- An update sync will only copy new and updated files to the destination folders/files.

Synchronizing files between directories is a common task for managing backups, ensuring consistency across multiple storage locations, and keeping data organized.

While many tools are available for this purpose, creating a Python script for directory synchronization provides greater flexibility and control.

## Contribution
* Fork this repository.
* Make pull requests with proper commit message.