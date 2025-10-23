# Publishing Yapp to PyPI

This guide explains how to publish the Yapp SDK to PyPI so users can install it with `pip install yapp`.

## Prerequisites

1. **Create PyPI Account**
   - Register at https://pypi.org/account/register/
   - Register at https://test.pypi.org/account/register/ (for testing)

2. **Install Build Tools**
   ```bash
   pip install --upgrade pip build twine
   ```

3. **Configure PyPI Authentication**

   Create `~/.pypirc`:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YourAPITokenHere

   [testpypi]
   username = __token__
   password = pypi-YourTestAPITokenHere
   ```

   Or use environment variables:
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-YourAPITokenHere
   ```

## Publishing Steps

### 1. Update Version

Update version in both files:
- `pyproject.toml` - line 7: `version = "0.1.0"`
- `setup.py` - line 18: `version="0.1.0"`
- `yapp/__init__.py` - line 5: `__version__ = "0.1.0"`

### 2. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info
```

### 3. Build the Package

```bash
python -m build
```

This creates:
- `dist/yapp-0.1.0.tar.gz` (source distribution)
- `dist/yapp-0.1.0-py3-none-any.whl` (wheel distribution)

### 4. Test the Build Locally

```bash
# Create a virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from the wheel
pip install dist/yapp-0.1.0-py3-none-any.whl

# Test the installation
python -c "import yapp; print(yapp.__version__)"

# Test basic functionality
python -c "
import yapp
client = yapp.Yapp(api_key='test')
print('Import successful!')
"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

### 5. Upload to Test PyPI (Recommended First)

```bash
twine upload --repository testpypi dist/*
```

Test installation from Test PyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps yapp
```

### 6. Upload to Production PyPI

```bash
twine upload dist/*
```

Or with explicit credentials:
```bash
twine upload --repository pypi dist/*
```

### 7. Verify Installation

```bash
pip install yapp
```

## Quick Publish Script

Save this as `publish.sh`:

```bash
#!/bin/bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

echo "🔨 Building package..."
python -m build

echo "✅ Build complete!"
echo ""
echo "📦 Built packages:"
ls -lh dist/

echo ""
echo "Next steps:"
echo "  Test PyPI: twine upload --repository testpypi dist/*"
echo "  Production: twine upload dist/*"
```

Make it executable:
```bash
chmod +x publish.sh
```

## Publishing Checklist

Before each release:

- [ ] Update version numbers in all files
- [ ] Update CHANGELOG.md (create one if needed)
- [ ] Run tests: `pytest tests/` (when tests exist)
- [ ] Update README.md if needed
- [ ] Clean old builds: `rm -rf build/ dist/ *.egg-info`
- [ ] Build package: `python -m build`
- [ ] Test locally: Install from wheel and test imports
- [ ] Upload to Test PyPI: `twine upload --repository testpypi dist/*`
- [ ] Test from Test PyPI: `pip install --index-url https://test.pypi.org/simple/ yapp`
- [ ] Upload to Production PyPI: `twine upload dist/*`
- [ ] Create git tag: `git tag v0.1.0 && git push --tags`
- [ ] Create GitHub release with release notes

## Troubleshooting

### "The user isn't allowed to upload to project"
- The package name might be taken
- Try a different name in `setup.py` and `pyproject.toml`

### "File already exists"
- You're trying to upload the same version twice
- Increment the version number

### "Invalid credentials"
- Check your API token in `~/.pypirc`
- Ensure you're using `__token__` as username
- Get a new token from PyPI settings

### Import errors after installation
- Make sure `__init__.py` exists in the `yapp/` directory
- Check MANIFEST.in includes all necessary files

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI API token to GitHub Secrets as `PYPI_API_TOKEN`.

## Version Management

Use semantic versioning (semver):
- `0.1.0` - Initial development
- `0.1.1` - Bug fixes
- `0.2.0` - New features (backwards compatible)
- `1.0.0` - Stable release
- `2.0.0` - Breaking changes

## Post-Publication

After publishing:

1. Test installation: `pip install yapp`
2. Update documentation with installation instructions
3. Announce on social media, forums, etc.
4. Monitor PyPI stats: https://pypi.org/project/yapp/
5. Watch for issues and user feedback

## Resources

- PyPI: https://pypi.org/
- Test PyPI: https://test.pypi.org/
- Python Packaging Guide: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
