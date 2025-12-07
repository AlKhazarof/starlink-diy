# Conflict Resolutions

This directory contains resolved versions of files that have merge conflicts in open pull requests.

## Purpose

When PRs have merge conflicts with the main branch, this directory provides:
- Pre-resolved versions of conflicting files
- Documentation explaining the conflicts and resolutions
- Helper scripts to apply the resolutions

## Structure

```
conflict-resolutions/
└── pr-2/                      # Resolution for Pull Request #2
    ├── README.md              # Resolved README.md
    ├── .gitignore             # Resolved .gitignore
    ├── RESOLUTION.md          # Detailed conflict analysis and instructions
    └── apply-resolution.sh    # Helper script to apply resolutions
```

## How to Use

Each PR subdirectory contains:

1. **Resolved files** - The final versions with conflicts resolved
2. **RESOLUTION.md** - Detailed explanation of conflicts and resolution strategy
3. **apply-resolution.sh** - Automated script to apply resolutions

### Quick Start

To resolve conflicts for a specific PR:

```bash
# Navigate to the PR's resolution directory
cd conflict-resolutions/pr-2

# Read the resolution documentation
cat RESOLUTION.md

# Apply the resolutions automatically
./apply-resolution.sh
```

### Manual Application

If you prefer manual control:

```bash
# 1. Checkout the PR branch
git checkout <pr-branch-name>

# 2. Attempt to merge main
git merge main

# 3. When conflicts occur, copy resolved files
cp conflict-resolutions/pr-2/README.md README.md
cp conflict-resolutions/pr-2/.gitignore .gitignore

# 4. Complete the merge
git add .
git commit
git push
```

## Current Resolutions

### PR #2: Cloud Agent Delegation

- **Branch**: `copilot/delegate-to-cloud-agent`
- **Status**: Has merge conflicts with main
- **Conflicting files**: README.md, .gitignore
- **Resolution available**: ✅ Yes
- **See**: [pr-2/RESOLUTION.md](pr-2/RESOLUTION.md)

## Notes

- Always review resolved files before applying them
- Test the merged code after applying resolutions
- Run the test suite to ensure nothing broke
- If new conflicts arise, update the resolved versions in this directory

## Contributing

If you encounter merge conflicts not covered here:

1. Create a new subdirectory for the PR (e.g., `pr-5/`)
2. Add resolved versions of conflicting files
3. Create a RESOLUTION.md explaining the conflicts
4. Optionally add a helper script
5. Update this README with the new resolution

## Automated Updates

This directory is maintained by automated tools and may be regenerated when:
- New conflicts are detected
- Main branch changes significantly
- PR branches are updated

Always check timestamps and commit messages to ensure you're using the latest resolutions.
