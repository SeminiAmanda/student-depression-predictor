#!/bin/bash
echo "Setting up Git filters for Jupyter notebooks..."

# Check if nbstripout is installed on host
if ! command -v nbstripout &> /dev/null; then
    echo "Installing nbstripout on host..."
    pip install nbstripout
else
    echo "nbstripout already installed"
fi

# Configure git filters with keep-output (this overrides any existing config)
echo "Configuring git filters to keep outputs..."
git config filter.nbstripout.clean 'nbstripout --keep-output'
git config filter.nbstripout.smudge cat
git config filter.nbstripout.required true

echo "🏗️  Building Docker image..."
docker-compose build

echo "✅ Setup complete!"
echo "✅  Run: docker-compose up"