#!/bin/bash

# Coverage Report Generation Only Script
# This script generates coverage reports from existing coverage data
# Usage: ./generate_coverage_reports_only.sh [format]
# format: all|html|xml|json (default: all)

set -e  # Exit on any error

# Configuration
COVERAGE_FORMAT="${1:-all}"
REPORTS_DIR="tests/reports"

echo "📈 Generating coverage reports from collected data..."
echo "📊 Coverage format: $COVERAGE_FORMAT"

# Ensure reports directory exists
mkdir -p "$REPORTS_DIR"

# Check if coverage data exists
if ! coverage report > /dev/null 2>&1; then
    echo "❌ No coverage data found. Please run tests with coverage first."
    echo "💡 Run: ./run_tests_coverage.sh"
    exit 1
fi

# Generate coverage reports in multiple formats
echo "📈 Generating coverage reports..."

if [ "$COVERAGE_FORMAT" = "all" ] || [ "$COVERAGE_FORMAT" = "html" ]; then
    echo "📊 Generating detailed HTML coverage report..."
    coverage html -d "$REPORTS_DIR/coverage-html" --title "Code Coverage Report" --show-contexts
    echo "✅ HTML coverage report generated in $REPORTS_DIR/coverage-html/"
fi

if [ "$COVERAGE_FORMAT" = "all" ] || [ "$COVERAGE_FORMAT" = "xml" ]; then
    coverage xml -o "$REPORTS_DIR/coverage.xml"
    echo "✅ XML coverage report generated"
fi

if [ "$COVERAGE_FORMAT" = "all" ] || [ "$COVERAGE_FORMAT" = "json" ]; then
    coverage json -o "$REPORTS_DIR/coverage.json"
    echo "✅ JSON coverage report generated"
fi

# Generate text summary
coverage report > "$REPORTS_DIR/coverage-summary.txt"

# Generate detailed coverage data
coverage report --show-missing > "$REPORTS_DIR/coverage-detailed.txt"

# Generate annotated coverage report with line-by-line analysis
if [ "$COVERAGE_FORMAT" = "all" ] || [ "$COVERAGE_FORMAT" = "html" ]; then
    echo "📊 Generating annotated coverage report..."
    coverage annotate -d "$REPORTS_DIR/coverage-annotated"
    echo "✅ Annotated coverage report generated in $REPORTS_DIR/coverage-annotated/"
fi

# Create a comprehensive coverage index page
echo "📋 Creating coverage reports index..."
cat > "$REPORTS_DIR/coverage-index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Reports Dashboard</title>
    <style>
        body {
            font-family: monospace;
            line-height: 1.4;
            margin: 0;
            padding: 15px;
            background-color: white;
            color: #333;
            font-size: 14px;
        }
        h1, h2, h3 {
            color: #333;
            font-weight: normal;
            margin: 20px 0 10px 0;
            padding: 0;
            border: none;
            background: none;
            font-family: monospace;
        }
        h1 {
            font-size: 18px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }
        h3 {
            font-size: 14px;
            margin: 15px 0 5px 0;
        }
        p {
            margin: 5px 0 10px 0;
            color: #666;
            font-size: 13px;
        }
        a {
            color: #0066cc;
            text-decoration: none;
            display: block;
            margin: 5px 0;
            padding: 3px 0;
        }
        a:hover {
            text-decoration: underline;
        }
        .timestamp {
            color: #888;
            font-size: 12px;
            margin-bottom: 20px;
        }
        .report-section {
            margin: 20px 0;
            padding: 10px 0;
            border-bottom: 1px dotted #ccc;
        }
        @media (max-width: 768px) {
            body {
                padding: 8px;
                font-size: 13px;
            }
            h1 {
                font-size: 16px;
            }
            h3 {
                font-size: 13px;
            }
            p {
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <h1>Coverage Reports Dashboard</h1>
    <p class="timestamp">Generated: $(date)</p>
    
    <div class="report-section">
        <h3>Interactive HTML Report</h3>
        <p>Complete coverage report with syntax highlighting and interactive features.</p>
        <a href="coverage-html/index.html">View HTML Report</a>
    </div>
    
    <div class="report-section">
        <h3>Annotated Source Files</h3>
        <p>Source code with coverage annotations showing covered/uncovered lines.</p>
        <a href="coverage-annotated/">View Annotated Files</a>
    </div>
    
    <div class="report-section">
        <h3>Text Reports</h3>
        <p>Coverage summary and detailed missing line information in text format.</p>
        <a href="coverage-summary.txt">Coverage Summary</a>
        <a href="coverage-detailed.txt">Detailed Report</a>
    </div>
    
    <div class="report-section">
        <h3>Test Execution Results</h3>
        <p>Complete test execution logs and results.</p>
        <a href="test-results.txt">View Test Results</a>
    </div>
</body>
</html>
EOF
echo "✅ Coverage reports index created at $REPORTS_DIR/coverage-index.html"

# Generate test execution summary if the script exists
if [ -f "$REPORTS_DIR/generate_test_summary.py" ]; then
    echo "📊 Generating test execution summary..."
    python3 "$REPORTS_DIR/generate_test_summary.py"
    echo "📝 Test summary generated"
fi

echo "📊 Coverage report generation complete!"

# Display summary
echo ""
echo "🏆 Coverage Report Generation Complete!"
echo "================================"

if [ -f "$REPORTS_DIR/coverage-summary.txt" ]; then
    echo "📊 Coverage Summary:"
    echo "-------------------"
    cat "$REPORTS_DIR/coverage-summary.txt"
    echo ""
fi

echo "📁 Generated Reports:"
echo "--------------------"
find "$REPORTS_DIR" -type f -name "*" | sort
echo ""

echo "📏 Report Sizes:"
echo "---------------"
du -h "$REPORTS_DIR"/* 2>/dev/null || true

echo ""
echo "🌐 Open the coverage dashboard in your browser:"
echo "file://$(pwd)/$REPORTS_DIR/coverage-index.html"