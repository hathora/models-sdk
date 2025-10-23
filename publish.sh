#!/bin/bash
# Quick publish script for Yapp SDK

set -e

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info yapp.egg-info

echo ""
echo "🔨 Building package..."
python -m build

echo ""
echo "✅ Build complete!"
echo ""
echo "📦 Built packages:"
ls -lh dist/

echo ""
echo "🧪 Testing local installation..."
python -m venv .test_env
source .test_env/bin/activate
pip install -q dist/*.whl
python -c "import yapp; print(f'✓ Successfully imported yapp v{yapp.__version__}')"
deactivate
rm -rf .test_env

echo ""
echo "✅ Package is ready for publishing!"
echo ""
echo "📤 Next steps:"
echo "  1. Test on Test PyPI:  twine upload --repository testpypi dist/*"
echo "  2. Test install:       pip install --index-url https://test.pypi.org/simple/ yapp"
echo "  3. Publish to PyPI:    twine upload dist/*"
echo ""
echo "Or run these commands:"
echo "  ./publish.sh test    # Upload to Test PyPI"
echo "  ./publish.sh prod    # Upload to Production PyPI"

# Handle command line arguments
if [ "$1" = "test" ]; then
    echo ""
    echo "📤 Uploading to Test PyPI..."
    twine upload --repository testpypi dist/*
    echo "✅ Uploaded to Test PyPI!"
    echo "Test with: pip install --index-url https://test.pypi.org/simple/ yapp"
elif [ "$1" = "prod" ]; then
    echo ""
    read -p "⚠️  Upload to Production PyPI? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Uploading to Production PyPI..."
        twine upload dist/*
        echo "✅ Published to PyPI!"
        echo "Install with: pip install yapp"
    else
        echo "Cancelled."
    fi
fi
