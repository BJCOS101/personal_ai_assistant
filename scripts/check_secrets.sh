#!/bin/bash

# Script to check for accidentally committed secrets
echo "🔍 Checking for exposed secrets..."

# Check if .env is in git
if git ls-files --error-unmatch .env 2>/dev/null; then
    echo "❌ ERROR: .env file is tracked by git!"
    echo "   Run: git rm --cached .env"
    exit 1
fi

# Check for common secret patterns in git
if git grep -E "(api[_-]?key|secret|token|password)\s*=\s*['\"][a-zA-Z0-9]+" HEAD -- '*.py' '*.js' '*.ts' '*.tsx' 2>/dev/null; then
    echo "❌ ERROR: Potential secrets found in code!"
    echo "   Review the files above and remove hardcoded secrets"
    exit 1
fi

# Check for API key patterns
if git grep -E "(sk-[a-zA-Z0-9]{32,}|gsk_[a-zA-Z0-9]{32,}|hf_[a-zA-Z0-9]{32,})" HEAD 2>/dev/null; then
    echo "❌ ERROR: API keys found in repository!"
    echo "   These must be removed immediately"
    exit 1
fi

echo "✅ No obvious secrets detected in git"
echo "⚠️  Remember: Always use .env for sensitive data"