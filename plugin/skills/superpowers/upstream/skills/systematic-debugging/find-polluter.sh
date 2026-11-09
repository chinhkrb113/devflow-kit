#!/usr/bin/env bash
# Bisection script to find which test creates unwanted files/state
# Usage: ./find-polluter.sh <file_or_dir_to_check> <test_pattern>
# Example: ./find-polluter.sh '.git' 'src/**/*.test.ts'

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 <file_to_check> <test_pattern>"
  echo "Example: $0 '.git' 'src/**/*.test.ts'"
  exit 1
fi

POLLUTION_CHECK="$1"
TEST_PATTERN="$2"

echo "🔍 Searching for test that creates: $POLLUTION_CHECK"
echo "Test pattern: $TEST_PATTERN"
echo ""

# Get list of test files (find . emits ./-prefixed paths, so accept the
# pattern written with or without a leading ./)
TEST_PATTERN="${TEST_PATTERN#./}"
# find -path can't match '**/' against zero directory levels, so a pattern
# like src/**/*.test.ts would skip src/top.test.ts; also try the pattern
# with '**/' collapsed to cover files directly under the base directory.
TEST_FILES=$(find . \( -path "./$TEST_PATTERN" -o -path "./${TEST_PATTERN//\*\*\//}" \) | sort -u)
if [ -z "$TEST_FILES" ]; then
  TOTAL=0
else
  TOTAL=$(printf '%s\n' "$TEST_FILES" | wc -l | tr -d ' ')
fi

echo "Found $TOTAL test files"
echo ""

# A clean verdict needs tests that actually ran against a clean starting state.
if [ "$TOTAL" -eq 0 ]; then
  echo "❌ No test files match '$TEST_PATTERN' - nothing was checked" >&2
  exit 2
fi
if [ -e "$POLLUTION_CHECK" ]; then
  echo "❌ '$POLLUTION_CHECK' already exists - remove it first, or no test can be blamed" >&2
  exit 2
fi
if ! command -v npm > /dev/null 2>&1; then
  echo "❌ npm not found - cannot run the tests" >&2
  exit 2
fi

COUNT=0
FAILED_RUNS=0
for TEST_FILE in $TEST_FILES; do
  COUNT=$((COUNT + 1))

  # Skip if pollution already exists
  if [ -e "$POLLUTION_CHECK" ]; then
    echo "⚠️  Pollution already exists before test $COUNT/$TOTAL"
    echo "   Skipping: $TEST_FILE"
    continue
  fi

  echo "[$COUNT/$TOTAL] Testing: $TEST_FILE"

  # Run the test
  # A failing test can still pollute, so keep going; count failures for the verdict.
  npm test "$TEST_FILE" > /dev/null 2>&1 || FAILED_RUNS=$((FAILED_RUNS + 1))

  # Check if pollution appeared
  if [ -e "$POLLUTION_CHECK" ]; then
    echo ""
    echo "🎯 FOUND POLLUTER!"
    echo "   Test: $TEST_FILE"
    echo "   Created: $POLLUTION_CHECK"
    echo ""
    echo "Pollution details:"
    ls -la "$POLLUTION_CHECK"
    echo ""
    echo "To investigate:"
    echo "  npm test $TEST_FILE    # Run just this test"
    echo "  cat $TEST_FILE         # Review test code"
    exit 1
  fi
done

echo ""
if [ "$FAILED_RUNS" -eq "$TOTAL" ]; then
  echo "❌ All $TOTAL test runs failed - inconclusive (check that 'npm test <file>' works here)" >&2
  exit 2
fi
echo "✅ No polluter found - all tests clean!"
exit 0
