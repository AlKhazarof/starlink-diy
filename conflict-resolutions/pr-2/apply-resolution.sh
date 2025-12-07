#!/bin/bash

# PR #2 Conflict Resolution Helper Script
# This script helps apply the resolved files to PR #2 branch

set -e

echo "================================================"
echo "PR #2 Conflict Resolution Helper"
echo "================================================"
echo ""

# Get the current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo ""

# Check if we're on the PR #2 branch
if [ "$CURRENT_BRANCH" != "copilot/delegate-to-cloud-agent" ]; then
    echo "⚠️  You are not on the copilot/delegate-to-cloud-agent branch"
    echo ""
    read -p "Do you want to checkout the branch now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Checking out copilot/delegate-to-cloud-agent..."
        git checkout copilot/delegate-to-cloud-agent
    else
        echo "Exiting. Please checkout the branch manually first."
        exit 1
    fi
fi

echo "Step 1: Fetching latest changes from remote..."
git fetch origin

echo ""
echo "Step 2: Attempting to merge main branch..."
if git merge origin/main; then
    echo "✅ Merge completed successfully - no conflicts!"
    exit 0
else
    echo "⚠️  Merge conflicts detected. Applying resolutions..."
fi

echo ""
echo "Step 3: Applying resolved files..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy resolved files
echo "  - Copying README.md..."
cp "$SCRIPT_DIR/README.md" README.md

echo "  - Copying .gitignore..."
cp "$SCRIPT_DIR/.gitignore" .gitignore

echo ""
echo "Step 4: Staging resolved files..."
git add README.md .gitignore

echo ""
echo "Step 5: Checking for other conflicts..."
if git diff --name-only --diff-filter=U | grep -q .; then
    echo "⚠️  There are still other conflicting files:"
    git diff --name-only --diff-filter=U
    echo ""
    echo "Please resolve these manually before continuing."
    exit 1
else
    echo "✅ All conflicts resolved!"
fi

echo ""
echo "Step 6: Completing the merge..."
read -p "Do you want to commit the merge now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Resolve merge conflicts with main branch

- Merged README.md: Combined project vision from main with cloud agent features
- Updated .gitignore: Using comprehensive version from main branch
- All features from both branches preserved"
    
    echo ""
    echo "✅ Merge committed successfully!"
    echo ""
    echo "Step 7: Push the changes..."
    read -p "Do you want to push to origin now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin copilot/delegate-to-cloud-agent
        echo ""
        echo "🎉 All done! PR #2 should now be mergeable."
    else
        echo "Remember to push your changes: git push origin copilot/delegate-to-cloud-agent"
    fi
else
    echo "Merge not committed. You can commit manually when ready:"
    echo "  git commit"
    echo "  git push origin copilot/delegate-to-cloud-agent"
fi

echo ""
echo "================================================"
echo "Resolution complete!"
echo "================================================"
